import platform
import json
import multiprocessing
import yamale
import yaml
from pathlib import Path
from typing import Iterable, Union
import docker

MAX_NUM_WORKERS = int(multiprocessing.cpu_count() // 2)
WORKFLOW_SCHEMA_PATH = Path(__file__).parent / "workflow-schema.yaml"


def get_high_level_docker_api():
    return docker.from_env()


def get_low_level_docker_api():
    return docker.APIClient()


def parse_stream(out):
    data = json.loads(out)
    if "stream" in data:
        return data["stream"]
    elif "error" in data:
        return data["error"]
    else:
        return str(data)


def do_print(*args, name: str = None, quiet: bool = False) -> None:
    if not quiet:
        print(f"[parallel_docker_build{'' if name is None else f'|{name}'}]", *args)


def do_build(
    dockerfile: Path,
    full_name: str,
    context: Path = None,
    rebuild: bool = False,
    quiet: bool = False,
    name: str = None,
) -> None:
    api = get_low_level_docker_api()
    name = full_name if name is None else f"{name}|{full_name}"
    _context = str(Path.cwd()) if context is None else str(context.resolve())
    if dockerfile.is_absolute():
        if not str(dockerfile).startswith(_context):
            raise FileNotFoundError(
                f"Dockerfile ({dockerfile} is not in context: {_context}"
            )
        _dockerfile = str(dockerfile).lstrip(_context)
    else:
        _dockerfile = str(dockerfile)
    options = {
        "path": _context,
        "dockerfile": _dockerfile,
        "tag": f"{full_name}:latest",
        "nocache": rebuild,
        "quiet": False,
        "name": name,
    }
    do_print(f"Building: {options}", name=name, quiet=quiet)
    for out in api.build(**options):
        do_print(parse_stream(out).rstrip("\n"), name=name, quiet=quiet)


def do_push(full_name: str, tags: list, quiet: bool = False, name: str = None) -> None:
    api = get_high_level_docker_api()
    name = full_name if name is None else f"{name}|{full_name}"
    for tag in tags:
        do_print(f"Pushing: {full_name}:{tag}", name=name, quiet=quiet)
        api.images.push(full_name, tag=tag)


def make_image(
    dockerfile: Path,
    organization: str,
    context: Path = None,
    allow_cross_platform: bool = False,
    push: bool = False,
    rebuild: bool = False,
    quiet: bool = False,
    name: str = None,
) -> None:
    # Name for initial logging before the docker image full_name is known
    _name = (
        dockerfile.parent.stem if name is None else f"{name}|{dockerfile.parent.stem}"
    )
    # Parser full name and check platform
    extra_tags = [s.lstrip(".") for s in dockerfile.suffixes]
    for t in extra_tags:
        if t != t.lower():
            raise ValueError(
                f"Dockerfile suffix tags must all be lowercase: {dockerfile}"
            )
    image_arch = "x86_64"
    if "l4t" in extra_tags:
        do_print(f"Found Linux 4 Tegra tag in {dockerfile}", name=_name)
        image_arch = "aarch64"
    if "arm64v8" in extra_tags:
        do_print(f"Found ARM64v8 tag in {dockerfile}", name=_name)
        image_arch = "aarch64"
    if image_arch != platform.machine():
        if allow_cross_platform:
            do_print(
                "Attempting to build a cross platform image",
                f"(this={platform.machine()} vs requested={image_arch}):",
                f"{dockerfile}",
                name=_name,
            )
        else:
            do_print(
                "Cannot build across platforms without `-x` option",
                f"(this={platform.machine()} vs requested={image_arch}):",
                f"Skipping: {dockerfile}",
                name=_name,
            )
            return
    full_name = f"{organization}/{dockerfile.parent.stem}"
    if len(extra_tags):
        full_name += "_" + "_".join(extra_tags)
    # Build it
    do_build(
        dockerfile, full_name, context=context, rebuild=rebuild, quiet=quiet, name=name
    )
    # Push it
    if push:
        do_push(full_name, tags=["latest"], quiet=quiet, name=name)


def make_images(
    dockerfiles: Iterable[Path],
    organization: str,
    context: Path = None,
    multiprocess: bool = False,
    max_num_workers: int = MAX_NUM_WORKERS,
    allow_cross_platform: bool = False,
    push: bool = False,
    rebuild: bool = False,
    quiet: bool = False,
    name: str = None,
) -> None:
    if len(dockerfiles) == 1 or not multiprocess:
        for dockerfile in dockerfiles:
            make_image(
                dockerfile,
                organization,
                context=context,
                allow_cross_platform=allow_cross_platform,
                rebuild=rebuild,
                push=push,
                quiet=quiet,
                name=name,
            )
    else:
        results = []
        with multiprocessing.Pool(min(max_num_workers, len(dockerfiles))) as pool:
            for dockerfile in dockerfiles:
                do_print(f"Adding build job: {dockerfile}", name=name)
                results.append(
                    pool.apply_async(
                        make_image,
                        args=(dockerfile, organization),
                        kwds=dict(
                            context=context,
                            allow_cross_platform=allow_cross_platform,
                            rebuild=rebuild,
                            push=push,
                            quiet=quiet,
                            name=name,
                        ),
                    )
                )
            [r.wait() for r in results]


def get_dockerfiles_from_path(path: Union[str, Path] = None, name: str = None) -> list:
    path = (
        Path.cwd() if path is None else path if isinstance(path, Path) else Path(path)
    )
    dockerfiles = []
    for p in list(path.rglob("**/Dockerfile*")) + list(path.rglob("Dockerfile*")):
        if p.is_dir():
            do_print(f"Skipping directory: {p}", name=name)
        else:
            dockerfiles.append(p)
    if len(dockerfiles) == 0:
        do_print(f"No `Dockerfile*`s found: {path}", name=name)
    do_print(f"Found {len(dockerfiles)} Dockerfiles here: {path}", name=name)
    return dockerfiles


def get_dockerfiles_from_paths(
    paths: Iterable[Union[str, Path]], name: str = None
) -> list:
    dockerfiles = []
    for path in paths:
        path = path if isinstance(path, Path) else Path(path)
        if path.is_dir():
            dockerfiles.extend(get_dockerfiles_from_path(path, name=name))
        elif path.stem.startswith("Dockerfile"):
            dockerfiles.append(path)
        else:
            raise ValueError(f"Path is not a dockerfile: {path}")
    return dockerfiles


def validate_workflow_yaml(workflow: Union[Path, dict]) -> dict:
    """Validate workflow yaml file

    Parameters
    ----------
    workflow : Union[Path, dict]
        Workflow yaml path or loaded dictionary.

    Returns
    -------
    dict
        Validated workflow
    """
    # Load
    if isinstance(workflow, Path):
        data = yamale.make_data(path=workflow)
    elif isinstance(workflow, dict):
        data = yamale.make_data(content=yaml.dump(workflow))
    else:
        raise ValueError(f"The workflow is not supported: {workflow}")
    schema = yamale.make_schema(WORKFLOW_SCHEMA_PATH)
    yamale.validate(schema, data)
    return data[0][0]


def run_workflow(workflow: Path, rebuild: bool = False, quiet: bool = False) -> None:
    do_print(f"Loading: {workflow}")
    workflow = validate_workflow_yaml(workflow)
    for i, stage in enumerate(workflow["stages"]):
        name = f"{stage['name']}(Stage {i} of {len(workflow['stages'])})"
        do_print("Starting run...", name=name)
        make_images(
            workflow["paths"],
            workflow["organization"],
            context=workflow.parent,
            max_num_workers=workflow["max_num_workers"],
            allow_cross_platform=workflow["allow_cross_platform"],
            push=workflow["push"],
            rebuild=rebuild,
            quiet=quiet,
            name=name,
        )
    do_print(f"Workflow complete: {workflow}")
