# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import os

from pathlib import Path
from os.path import (
    dirname, 
    realpath, 
    join, 
    split, 
    splitext
)

from elangai.utils._logging import ELANGAI_ERROR
from elangai.__about__ import __version__ as VERSION


DEFAULT_APP_NAME = 'myapp'

REPLACE_EXTENSION = {'.py-tpl' : '.py',
                     '.json-tpl' : '.json'}

REPLACE_COMPONENT = {'{{ app_name }}' : DEFAULT_APP_NAME,
                     '{{ elangai_version }}' : VERSION}


def _make_directory(cls, directory_path: str):
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=False)
    except:
        ELANGAI_ERROR(NameError, "{} is already exist".format(directory_path))


def _get_relative_dir(cls, app_name: str, root: str):
    _, relative_dir = split(root)
    return app_name if relative_dir == 'app_name' else join(app_name, relative_dir)


def _get_new_name(cls, filename: str):
    ext = splitext(filename)[1:][0]
    if ext in REPLACE_EXTENSION:
        return filename[:-len(ext)] + REPLACE_EXTENSION[ext]
    return filename


def _get_new_data(cls, app_name: str, old_path: str):
    new_data = []
    REPLACE_COMPONENT['{{ app_name }}'] = app_name
    with open(old_path, 'r') as f:
        for line in f.readlines():
            for component in REPLACE_COMPONENT:
                if component in line:
                    line = line.replace(component, REPLACE_COMPONENT[component])
            new_data.append(line)
    return new_data


def _make_copy(cls, new_data: list, new_path: str):
    with open(new_path, 'a') as f:
        for line in new_data:
            f.write(line)


def _join_utils(cls, root: str, new_path: str):
    return join(root, new_path)


def _walk_utils(cls, directory: str):
    return os.walk(directory)


class TemplateUtils:
    IMPORTANT_DIR = {'model', 'input', 'utils', 'output'}
    JOIN = _join_utils
    MKDIR = _make_directory
    RELATIVE_DIR = _get_relative_dir
    TEMPLATE_DIR = join(dirname(realpath(__file__)), 'app_name')
    NEW_NAME = _get_new_name
    NEW_DATA = _get_new_data
    CRAWL = _walk_utils
    COPY = _make_copy


UTILS = TemplateUtils()
