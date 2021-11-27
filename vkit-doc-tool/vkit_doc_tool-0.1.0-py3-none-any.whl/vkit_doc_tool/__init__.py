from typing import List, Union
import pathlib
import re
import tempfile
import subprocess

import toml
import attr
import iolite as io
import fire


def read_text(path):
    with open(path) as fin:
        return fin.read()


def write_text(path, text):
    with open(path, 'w') as fout:
        fout.write(text)


def parse_doc(text):
    pattern = r'```\s*vkit-doc\s*(.+?)```'
    return re.finditer(pattern, text, re.UNICODE | re.IGNORECASE | re.DOTALL)


@attr.define
class Ref:
    path: pathlib.Path


@attr.define
class Match:
    begin: int
    end: int
    refs: List[Ref]


def parse_match(match, cwd):
    text = match.group(1)
    data = toml.loads(text)

    refs: List[Ref] = []
    for ref_raw in data.get('ref', ()):
        refs.append(Ref(path=cwd / ref_raw['path']))

    begin, end = match.span()
    return Match(
        begin=begin,
        end=end,
        refs=refs,
    )


def render_doc(path: Union[str, pathlib.Path]):
    path = io.file(path, exists=True)
    text = read_text(path)

    matches = [parse_match(match, path.parent) for match in parse_doc(text)]
    matches = sorted(matches, key=lambda match: match.begin)

    repl_texts = []
    for match in matches:
        sub_texts = []
        for ref in match.refs:
            sub_texts.append(render_doc(ref.path))
        repl_texts.append('\n'.join(sub_texts))
    assert len(repl_texts) == len(matches)

    doc = []
    pre_end = 0
    for match, repl_text in zip(matches, repl_texts):
        if match.begin > pre_end:
            doc.append(text[pre_end:match.begin])
        doc.append(repl_text)
        pre_end = match.end
    if pre_end < len(text):
        doc.append(text[pre_end:])

    doc = '\n'.join(doc)

    if '[TOC]' in doc:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md') as temp_file:
            temp_file.write(doc)
            temp_file.flush()

            result = subprocess.run(
                [
                    'markdown-toc',
                    '-t',
                    'github',
                    '--no-write',
                    temp_file.name,
                ],
                capture_output=True,
            )
            result.check_returncode()
            toc = result.stdout.decode().strip()

            doc = doc.replace('[TOC]', f'\n{toc}\n')

    return doc


def entrypoint(input_md, output_md):
    doc = render_doc(input_md)
    with open(output_md, 'w') as fout:
        fout.write(doc)


entrypoint_cli = lambda: fire.Fire(entrypoint)


def debug():
    import os
    folder = os.path.expandvars('$VKIT_DOC_TOOL_DATA')
    print(render_doc(f'{folder}/a.md'))
