import click

from vessl.cli._base import VesslGroup, vessl_argument
from vessl.cli._util import format_bool, print_data, print_table, prompt_choices
from vessl.cli.kernel_cluster import cluster_option
from vessl.cli.organization import organization_name_option
from vessl.kernel_resource_spec import (
    list_kernel_resource_specs,
    read_kernel_resource_spec,
)


def resource_name_prompter(
        ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before resource (`--resource`).",
        )

    resources = list_kernel_resource_specs(cluster_id=cluster.id)
    resource = prompt_choices("Resource", [(x.name, x) for x in resources])
    ctx.obj["processor_type"] = resource.processor_type
    return resource.name


@click.command(name="resource", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@click.pass_context
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=resource_name_prompter
)
@cluster_option
@organization_name_option
def read(ctx, name: str):
    cluster = ctx.obj.get("cluster")
    resource = read_kernel_resource_spec(cluster_id=cluster.id, kernel_resource_spec_name=name)
    print_data(
        {
            "ID": resource.id,
            "Name": resource.name,
            "Description": resource.description,
            "CPU Type": resource.cpu_type,
            "CPU Limit": resource.cpu_limit,
            "GPU Type": resource.gpu_type,
            "GPU Limit": resource.gpu_limit,
            "Memory Limit": resource.memory_limit,
            "Spot": format_bool(resource.spot),
        }
    )


@cli.vessl_command()
@click.pass_context
@cluster_option
@organization_name_option
def list(ctx):
    resources = list_kernel_resource_specs(cluster_id=ctx.obj.get('cluster').id)
    print_table(
        resources,
        [
            "ID",
            "Name",
            "CPU Type",
            "CPU Limit",
            "GPU Type",
            "GPU Limit",
            "Memory Limit",
            "Spot",
        ],
        lambda x: [
            x.id,
            x.name,
            x.cpu_type,
            x.cpu_limit,
            x.gpu_type,
            x.gpu_limit,
            x.memory_limit,
            x.spot,
        ],
    )
