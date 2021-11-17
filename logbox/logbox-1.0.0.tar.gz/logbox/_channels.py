# Copyright (C) 2021 Matthias Nadig

import os

from ._codes import _parse_font_color_from_rgb, _parse_background_color_from_rgb
from ._codes import COLOR_DEFAULT_FONT, COLOR_DEFAULT_BG
from ._codes import ORANGE


class Channel:
    def __init__(self,
                 name=None,
                 color_font=None, color_bg=None,
                 show_prefix_module=True,
                 show_prefix_level=True,
                 filename=None):

        self.name = name
        self.color_font = COLOR_DEFAULT_FONT if color_font is None else _parse_font_color_from_rgb(color_font)
        self.color_bg = COLOR_DEFAULT_BG if color_bg is None else _parse_background_color_from_rgb(color_bg)
        self.show_prefix_module = show_prefix_module
        self.show_prefix_level = show_prefix_level

        self.prefix_line_debug = ''
        self.prefix_line_info = ''
        self.prefix_line_warn = ORANGE + 'WARNING: '
        self.prefix_line_error = ''
        self.appendix_line_debug = ''
        self.appendix_line_info = ''
        self.appendix_line_warn = self.color_font
        self.appendix_line_error = ''

        if self.show_prefix_level:
            self.prefix_line_debug = 'D ' + self.prefix_line_debug
            self.prefix_line_info = 'I ' + self.prefix_line_info
            self.prefix_line_warn = 'W ' + self.prefix_line_warn
            self.prefix_line_error = 'E ' + self.prefix_line_error

        if self.show_prefix_module and self.name is not None:
            self.prefix_line_debug = '[{}] '.format(self.name) + self.prefix_line_debug
            self.prefix_line_info = '[{}] '.format(self.name) + self.prefix_line_info
            self.prefix_line_warn = '[{}] '.format(self.name) + self.prefix_line_warn
            self.prefix_line_error = '[{}] '.format(self.name) + self.prefix_line_error

        if filename is None:
            self.f = None
        else:
            filename_appendix = '.log'
            filename += filename_appendix
            (path_logfile, _) = os.path.split(filename)
            if path_logfile != '':
                os.makedirs(path_logfile, exist_ok=True)
            n_conflicts = 0
            filename_unique = filename
            while os.path.exists(filename_unique):
                n_conflicts += 1
                filename_unique = filename[:-len(filename_appendix)] + '_conflict{}'.format(n_conflicts) + filename_appendix
            filename = filename_unique
            self.f = open(filename, 'a+', encoding='utf-8')

    def __del__(self):
        if self.f is not None:
            self.f.close()

    def _on_log(self, str_log):
        if self.f is not None:
            self.f.write(str_log)

    def on_log(self, str_log, default_channel):
        self._on_log(str_log)

    def on_error(self, str_log, default_channel):
        self._on_log(str_log)


class SubChannel(Channel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_log(self, str_log, default_channel):
        self._on_log(str_log)
        default_channel._on_log(str_log)


class ParallelChannel(Channel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_log(self, str_log, default_channel):
        self._on_log(str_log)
