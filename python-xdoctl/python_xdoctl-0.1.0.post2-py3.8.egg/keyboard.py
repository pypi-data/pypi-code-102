"""Xdotool 命令包装器 - 键盘控制部分

常用操作示例：

>>> import xdoctl
# 通过 keyboard.key_press() 模拟按下指定字符的行为
>>> xdoctl.keyboard.key_press('A')  # 输入单个字符
>>> xdoctl.keyboard.key_press('E', 'x', 'a', 'm', 'p', 'l', 'e')  # 输入一个单词
>>> xdoctl.keyboard.key_press(*list('Example'))  # 等效于 `keyboard.key_press('E', 'x', 'a', 'm', 'p', 'l', 'e')`
>>> xdoctl.keyboard.key_press(*list('This'), 'space', *list('is'), 'space', 'a', 'n', *list('example'))  # 输入一个句子
# 通过 keyboard.type_() 输入特定内容（比 keyboard.key_press() 更高效和易用）
>>> xdoctl.keyboard.type_('This is an example')
"""
from __future__ import annotations

from subprocess import PIPE, Popen

from .misc import get_xdotool_executable_path, XdotoolError


# Equal to `xdotool key`
def key_press(*keysequence: str,
              window: int = None,
              repeat: int = None,
              repeat_delay=None,
              delay: int = None,
              clear_modifiers=False
              ):
    command = [get_xdotool_executable_path(), 'key']
    if window is not None:
        command.extend(['--window', str(window)])
    if repeat is not None:
        command.extend(['--repeat', str(repeat)])
    if repeat_delay is not None:
        command.extend(['--repeat-delay', str(repeat_delay)])
    if delay is not None:
        command.extend(['--delay', str(delay)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.append('--')
    command.extend(keysequence)
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool keydown`
def key_press_hold(*keysequence: str,
                   window: int = None,
                   repeat: int = None,
                   repeat_delay=None,
                   delay: int = None,
                   clear_modifiers=False
                   ):
    command = [get_xdotool_executable_path(), 'keydown']
    if window is not None:
        command.extend(['--window', str(window)])
    if repeat is not None:
        command.extend(['--repeat', str(repeat)])
    if repeat_delay is not None:
        command.extend(['--repeat-delay', str(repeat_delay)])
    if delay is not None:
        command.extend(['--delay', str(delay)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.append('--')
    command.extend(keysequence)
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Equal to `xdotool keyup`
def key_press_release(*keysequence: str,
                      window: int = None,
                      repeat: int = None,
                      repeat_delay=None,
                      delay: int = None,
                      clear_modifiers=False
                      ):
    command = [get_xdotool_executable_path(), 'keyup']
    if window is not None:
        command.extend(['--window', str(window)])
    if repeat is not None:
        command.extend(['--repeat', str(repeat)])
    if repeat_delay is not None:
        command.extend(['--repeat-delay', str(repeat_delay)])
    if delay is not None:
        command.extend(['--delay', str(delay)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    command.append('--')
    command.extend(keysequence)
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')


# Almost equal to `xdotool type`
def type_(sequence_or_file: str,
          is_from_file=False,
          window: int = None,
          delay: int = None,
          clear_modifiers=False
          ):
    # Lack of '--args' flag: how many arguments to expect in the exec command.
    # This is useful for ending an exec and continuing with more xdotool commands
    command = [get_xdotool_executable_path(), 'type']
    if window is not None:
        command.extend(['--window', str(window)])
    if delay is not None:
        command.extend(['--delay', str(delay)])
    if clear_modifiers:
        command.append('--clearmodifiers')
    if is_from_file:
        command.extend(['--file', sequence_or_file])
    else:
        command.extend(['--', sequence_or_file])
    
    completed = Popen(command, stdout=PIPE)
    completed.wait()
    if completed.returncode != 0:
        raise XdotoolError(f'xdotool returned code {completed.returncode} (should be 0)')
