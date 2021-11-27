"""Xdotool 命令包装器 - 窗口控制部分

常用操作示例：

>>> import xdoctl
# 通过鼠标选择窗口，并获取其 windowid
>>> xdoctl.window.select_via_mouse()
123732042
# 通过 window.search() 和特定条件，获取一个 / 多个窗口的 windowid
>>> xdoctl.window.search('Konsole')
(138412036, 138412041, 138412039)
# 使用特定的 PID，通过 window.search()，获取一个 / 多个窗口的 windowid
>>> xdoctl.window.search(38616, pattern_is_pid=True)
(138412039,)
# 使用特定的 windowid，获取这个窗口的标题、PID、大小、位置等信息
>>> xdoctl.window.get_window_name(140509185)  # 窗口标题
'Visual Studio Code'
>>> xdoctl.window.get_window_pid(140509185)  # 窗口所属进程的 PID
43496
>>> xdoctl.window.get_window_geometry(140509185)  # 窗口的几何属性（包括位置、大小、所在屏幕等）
WindowGeometryAttributes(x=312, y=504, width=1848, height=888, screen=0)
# 移动窗口，其后获取窗口位置
>>> xdoctl.window.window_move(140509185, 100, 100)  # 移动窗口到 (100, 100)；相对于坐标原点（位于屏幕左上角）移动
>>> xdoctl.window.get_window_geometry(140509185)
WindowGeometryAttributes(x=0, y=49, width=1848, height=888, screen=0)
>>> xdoctl.window.window_move(140509185, 800, 600, relative=True)  # 移动窗口到 (900, 700)；相对于原窗口位置 (100, 100) 移动
>>> xdoctl.window.get_window_geometry(140509185)
WindowGeometryAttributes(x=312, y=504, width=1848, height=888, screen=0)
"""
from __future__ import annotations

from subprocess import PIPE, Popen
from typing import Literal, NamedTuple

from .misc import get_xdotool_executable_path, XdotoolError

SEARCH_OPTIONS_LITERALS = Literal['name', 'class', 'classname', 'role']


class WindowGeometryAttributes(NamedTuple):
    x: int
    y: int
    width: int
    height: int
    screen: int


# Equal to `xdotool search`
def search(pattern: str | int,
           *search_options: SEARCH_OPTIONS_LITERALS,
           match_all=False,
           maxdepth: int = None,
           only_visible=False,
           pattern_is_pid=False,
           screen: int = None,
           desktop: int = None,
           limit: int = None,
           sync=False
           ) -> tuple[int] | None:
    command = [get_xdotool_executable_path(), 'search', '--shell']
    if only_visible:
        command.append('--onlyvisible')
    if screen is not None:
        command.extend(['--screen', str(screen)])
    if desktop is not None:
        command.extend(['--desktop', str(desktop)])
    if limit is not None:
        command.extend(['--limit', str(limit)])
    if sync:
        command.append('--sync')
    if pattern_is_pid:
        command.extend(['--pid', str(pattern)])
    else:
        for _ in search_options:
            if _ in ('name', 'class', 'classname', 'role'):
                command.append(_)
            else:
                raise ValueError(f"unsupported search option: '{_}'")
        if match_all:
            command.append('--all')
        else:
            command.append('--any')
        if maxdepth is not None:
            command.extend(['--maxdepth', str(maxdepth)])
        command.extend(['--', str(pattern)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    
    formatted_stdout = completed.stdout.read().strip().replace(b'\n', b', ')
    scope = {}
    exec(formatted_stdout, scope)
    return scope['WINDOWS']


# Equal to `xdotool set_window`
def set_window(window: int,
               name: str = None,
               icon_name: str = None,
               role: str = None,
               window_class: str = None,
               window_classname: str = None,
               urgency: int = None,
               override_redirect: int = None
               ):
    command = [get_xdotool_executable_path(), 'set_window']
    for arg, shellcommand in [(name, '--name'),
                              (icon_name, '--icon-name'),
                              (role, '--role'),
                              (window_class, '--class'),
                              (window_classname, '--classname')]:
        if arg is not None:
            command.extend([shellcommand, str(arg)])
    for arg, shellcommand in [(urgency, '--urgency'), (override_redirect, '--overrideredirect')]:
        if arg:
            command.extend([shellcommand, str(arg)])
    command.extend(['--', str(window)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool selectwindow`
def select_via_mouse():
    command = [get_xdotool_executable_path(), 'selectwindow']
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    from_stdout = completed.stdout.read()
    if from_stdout is not None:
        return int(from_stdout)


# Equal to `xdotool behave`, waiting to implement
def behave():
    raise NotImplementedError


# Equal to `xdotool getwindowpid`
def get_window_pid(window: int):
    command = [get_xdotool_executable_path(), 'getwindowpid', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    from_stdout = completed.stdout.read()
    if from_stdout is not None:
        return int(from_stdout)


# Equal to `xdotool getwindowname`
def get_window_name(window: int):
    command = [get_xdotool_executable_path(), 'getwindowname', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    from_stdout = completed.stdout.read().strip().decode()
    if from_stdout is not None:
        return str(from_stdout)


# Equal to `xdotool getwindowgeometry`
def get_window_geometry(window: int):
    command = [get_xdotool_executable_path(), 'getwindowgeometry', '--shell', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    from_stdout = completed.stdout.read()
    if from_stdout:
        scope = {}
        exec(from_stdout, scope)
        return WindowGeometryAttributes(
            x=scope['X'],
            y=scope['Y'],
            width=scope['WIDTH'],
            height=scope['HEIGHT'],
            screen=scope['SCREEN']
        )


# Equal to `xdotool getwindowfocus`
def get_focusing_window(iterate_parents=True):
    command = [get_xdotool_executable_path(), 'getwindowfocus']
    if not iterate_parents:
        command.append('-f')
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    from_stdout = completed.stdout.read()
    if from_stdout is not None:
        return int(from_stdout)


# Equal to `xdotool windowsize`
def set_window_size(window: int, width: int, height: int, usehints=False, sync=False):
    command = [get_xdotool_executable_path(), 'windowsize']
    if usehints:
        command.append('--usehints')
    if sync:
        command.append('--sync')
    command.extend(['--', str(window), str(width), str(height)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowmove`
def window_move(window: int, x: int | Literal['x'], y: int | Literal['y'], relative=False, sync=False):
    command = [get_xdotool_executable_path(), 'windowmove']
    if relative:
        command.append('--relative')
    if sync:
        command.append('--sync')
    command.extend(['--', str(window)])
    if not isinstance(x, int) and str(x) != 'x':
        raise ValueError(f"'x' must be int or literal 'x', not {repr(x)}")
    if not isinstance(y, int) and str(y) != 'y':
        raise ValueError(f"'y' must be int or literal 'y', not {repr(y)}")
    command.extend([str(x), str(y)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowfocus`
def window_focus(window: int, sync=False):
    command = [get_xdotool_executable_path(), 'windowfocus']
    if sync:
        command.append('--sync')
    command.extend(['--', str(window)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowfocus`
def window_map(window: int, sync=False):
    command = [get_xdotool_executable_path(), 'windowmap']
    if sync:
        command.append('--sync')
    command.extend(['--', str(window)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowunmap`
def window_unmap(window: int, sync=False):
    command = [get_xdotool_executable_path(), 'windowunmap']
    if sync:
        command.append('--sync')
    command.extend(['--', str(window)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowfocus`
def window_minimize(window: int, sync=False):
    command = [get_xdotool_executable_path(), 'windowminimize']
    if sync:
        command.append('--sync')
    command.extend(['--', str(window)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowraise`
def window_raise(window: int):
    command = [get_xdotool_executable_path(), 'windowminimize', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowreparent`
def window_reparent(source_window: int, destination_window: int):
    command = [get_xdotool_executable_path(), 'windowminimize', '--', str(source_window), str(destination_window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowclose`
def window_close(window: int):
    command = [get_xdotool_executable_path(), 'windowclose', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowquit`
def window_quit(window: int):
    command = [get_xdotool_executable_path(), 'windowquit', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool windowkill`
def window_kill(window: int):
    command = [get_xdotool_executable_path(), 'windowkill', '--', str(window)]
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
