from __future__ import annotations

import os

CUSTOM_XDOTOOL_EXECUTABLE_PATH: str | None = None


def get_xdotool_executable_path():
    bindirpaths = []
    if CUSTOM_XDOTOOL_EXECUTABLE_PATH:
        bindirpaths.append(CUSTOM_XDOTOOL_EXECUTABLE_PATH)
    bindirpaths.extend(os.get_exec_path())
    for path in bindirpaths:
        path = os.path.join(path, 'xdotool')
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path


class XdotoolError(RuntimeError):
    pass
