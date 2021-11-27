"""Xdotool 命令包装器 - 鼠标控制部分

常用操作示例：

>>> import xdoctl
# 获取鼠标位置
>>> xdoctl.mouse.get_location()
MouseLocation(x=481, y=1088, screen=0, window=123732042)
# 改变鼠标位置，其后再次获取鼠标位置
>>> xdoctl.mouse.move(1920, 1080)
>>> xdoctl.mouse.get_location()
MouseLocation(x=1920, y=1080, screen=0, window=123732042)
# 模拟：按下鼠标左键、右键和中键
>>> xdoctl.mouse.click(1)  # 鼠标左键
>>> xdoctl.mouse.click(3)  # 鼠标右键
>>> xdoctl.mouse.click(2)  # 鼠标中键
"""
from __future__ import annotations

from subprocess import PIPE, Popen, run as procrun
from typing import NamedTuple

from .misc import get_xdotool_executable_path, XdotoolError


class MouseLocation(NamedTuple):
    x: int
    y: int
    screen: int
    window: int


# Equal to `xdotool getmouselocation`
def get_location():
    completed = procrun([get_xdotool_executable_path(), 'getmouselocation', '--shell'],
                        stdout=PIPE
                        )
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
    scope = {}
    exec(completed.stdout, scope)
    return MouseLocation(x=scope['X'],
                         y=scope['Y'],
                         screen=scope['SCREEN'],
                         window=scope['WINDOW']
                         )


# Equal to `xdotool mousemove`
def move(x: int, y: int, screen: int = None, sync=False, clear_modifiers=False):
    command = [get_xdotool_executable_path(), 'mousemove']
    if screen is not None:
        command.extend(['--screen', str(screen)])
    if sync:
        command.append('--sync')
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.extend(['--', str(x), str(y)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool mousemove_relative`
def move_relative(dx: int, dy: int, polar=False, sync=False, clear_modifiers=False):
    command = [get_xdotool_executable_path(), 'mousemove_relative']
    if polar:
        command.append('--polar')
    if sync:
        command.append('--sync')
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.extend(['--', str(dx), str(dy)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool click`
def click(button: int, window: int = None, repeat: int = None, delay: int = None, clear_modifiers=False):
    command = [get_xdotool_executable_path(), 'click']
    if window is not None:
        command.extend(['--window', str(window)])
    if repeat is not None:
        command.extend(['--repeat', str(repeat)])
    if delay is not None:
        command.extend(['--delay', str(delay)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.extend(['--', str(button)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool mousedown`
def click_hold(button: int, window: int = None, clear_modifiers=False):
    command = [get_xdotool_executable_path(), 'mousedown']
    if window is not None:
        command.extend(['--window', str(window)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.extend(['--', str(button)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool mouseup`
def click_release(button: int, window: int = None, clear_modifiers=False):
    command = [get_xdotool_executable_path(), 'mouseup']
    if window is not None:
        command.extend(['--window', str(window)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.extend(['--', str(button)])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool behave_screen_edge`, waiting to implement
def behave_screen_edge():
    raise NotImplementedError
