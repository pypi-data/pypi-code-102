"""Xdotool 命令包装器

xdoctl 通过包装 xdotool 提供的各种操作和命令，提供一种使用 Python 操作 xdotool 工具的方式。

常用操作示例：

>>> import xdoctl
# 鼠标操作
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
# 键盘操作
# 通过 keyboard.key_press() 模拟按下指定字符的行为
>>> xdoctl.keyboard.key_press('A')  # 输入单个字符
>>> xdoctl.keyboard.key_press('E', 'x', 'a', 'm', 'p', 'l', 'e')  # 输入一个单词
>>> xdoctl.keyboard.key_press(*list('Example'))  # 等效于 `keyboard.key_press('E', 'x', 'a', 'm', 'p', 'l', 'e')`
>>> xdoctl.keyboard.key_press(*list('This'), 'space', *list('is'), 'space', 'a', 'n', *list('example'))  # 输入一个句子
# 通过 keyboard.type_() 输入特定内容（比 keyboard.key_press() 更高效和易用）
>>> xdoctl.keyboard.type_('This is an example')
# 窗口操作
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
from . import keyboard, misc, mouse, window
