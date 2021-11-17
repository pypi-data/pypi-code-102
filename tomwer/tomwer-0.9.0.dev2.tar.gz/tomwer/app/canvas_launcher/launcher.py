import os
import sys
from orangecanvas.application.canvasmain import DockWidget
import pkg_resources

from silx.gui import qt
from Orange.canvas.config import Config as _Config

# from orangecanvas import config
from Orange.canvas import __main__ as _Main
from .splash import splash_screen, getIcon
import tomwer.version
from tomwer.gui import icons
from urllib.request import urlopen
import logging
import argparse
from tomwer.core.log.logger import TomwerLogger
import shutil
from orangecanvas.application.outputview import (
    TextStream,
    ExceptHook,
    TerminalTextDocument as _TerminalTextDocument,
)
from contextlib import closing
from orangewidget.workflow.widgetsscheme import WidgetsScheme as _WidgetsScheme
from processview.gui.processmanager import ProcessManagerWindow
from Orange.canvas.mainwindow import MainWindow as _MainWindow
from Orange import canvas
from orangecanvas.main import Main

_logger = logging.getLogger(__name__)


MAX_LOG_FILE = 10
"""Maximal log file kepts for orange"""

LOG_FILE_NAME = "orange.log"

LOG_FOLDER = "/var/log/orange"


def version():
    return tomwer.version.version


class MainWindow(_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_supervisor_dock = DockWidget(
            self.tr("scan supervisor"),
            self,
            objectName="processes-dock",
            allowedAreas=qt.Qt.BottomDockWidgetArea,
            visible=self.show_processes_manager_action.isChecked(),
        )

        self.process_supervisor_dock.setWidget(ProcessManagerWindow(parent=None))
        self.process_supervisor_dock.visibilityChanged[bool].connect(
            self.show_processes_manager_action.setChecked
        )
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.process_supervisor_dock)

    def setup_actions(self):
        super().setup_actions()
        # create the action to connect with it
        self.show_processes_manager_action = qt.QAction(
            self.tr("&Scan supervisor"),
            self,
            toolTip=self.tr("Show scan states relative to processes."),
            checkable=True,
            triggered=lambda checked: self.process_supervisor_dock.setVisible(checked),
        )

    def setup_menu(self):
        super().setup_menu()
        self.view_menu.addAction(self.show_processes_manager_action)


class WidgetsScheme(_WidgetsScheme):
    """Simple redefinition of the WidgetsScheme to allow loops"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_loop_flags(self.AllowLoops)


class TomwerConfig(_Config):
    """Configuration defined for tomwer"""

    ApplicationName = "tomwer"
    ApplicationVersion = version()

    @staticmethod
    def splash_screen():
        return splash_screen()

    @staticmethod
    def core_packages():
        return super().core_packages() + ["tomwer-add-on"]

    @staticmethod
    def application_icon():
        return getIcon()

    @staticmethod
    def workflow_constructor(*args, **kwargs):
        return WidgetsScheme(*args, **kwargs)

    @staticmethod
    def widgets_entry_points():
        """
        Return an `EntryPoint` iterator for all 'orange.widget' entry
        points.
        """
        # Ensure the 'this' distribution's ep is the first. iter_entry_points
        # yields them in unspecified order.
        WIDGETS_ENTRY = "orange.widgets"

        def is_tomwer_extension(entry):
            return "tomwer" in entry.name.lower()

        all_eps = filter(
            is_tomwer_extension, pkg_resources.iter_entry_points(WIDGETS_ENTRY)
        )

        all_eps = sorted(
            all_eps,
            key=lambda ep: 0 if ep.dist.project_name.lower() == "orange3" else 1,
        )
        return iter(all_eps)

    @staticmethod
    def addon_entry_points():
        return TomwerConfig.widgets_entry_points()


class TomwerSplashScreen(qt.QSplashScreen):
    def __init__(
        self,
        parent=None,
        pixmap=None,
        textRect=None,
        textFormat=qt.Qt.PlainText,
        **kwargs
    ):
        super(TomwerSplashScreen, self).__init__(pixmap=icons.getQPixmap("tomwer"))

    def showMessage(self, message, alignment=qt.Qt.AlignLeft, color=qt.Qt.black):
        version = "tomwer version {}".format(tomwer.version.version)
        super().showMessage(version, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.white)


class TerminalTextDocument(_TerminalTextDocument):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)

    @staticmethod
    def get_log_level(my_str):
        if "DEBUG" in my_str:
            return qt.Qt.darkBlue
        elif "ERROR" in my_str:
            return qt.Qt.red
        elif "WARNING" in my_str:
            return qt.Qt.magenta
        elif "CRITICAL" in my_str:
            return qt.Qt.red
        elif "Info" in my_str:
            return qt.Qt.black
        elif "CRITICAL" in my_str:
            return qt.Qt.darkYellow
        elif "PROCESS_STARTED" in my_str:
            return qt.Qt.black
        elif "PROCESS_SUCCEED" in my_str:
            return qt.Qt.darkGreen
        elif "PROCESS_FAILED" in my_str:
            return qt.Qt.red
        elif "PROCESS_ENDED" in my_str:
            return qt.Qt.black
        elif "PROCESS_SKIPPED" in my_str:
            return qt.Qt.magenta
        else:
            return None

    def writeWithFormat(self, string: str, charformat) -> None:
        assert qt.QThread.currentThread() is self.thread()
        # remove linux reset sequence
        string = string.replace("\033[0m", "")
        # remove linux reset sequence
        string = string.replace("\033[1;%dm", "")
        # remove linux reset sequence
        string = string.replace("[1m", "")
        string = string.replace("[1;30m", "")
        string = string.replace("[1;31m", "")
        string = string.replace("[1;32m", "")
        string = string.replace("[1;33m", "")
        string = string.replace("[1;34m", "")
        string = string.replace("[1;35m", "")

        color = self.get_log_level(string) or qt.Qt.red
        charformat.setForeground(color)

        # super().writelinesWithFormat(string, charformat)
        cursor = self.textCursor()
        cursor.setCharFormat(charformat)
        cursor.insertText(string)


if hasattr(_Main, "OMain"):
    _OMain = _Main.OMain
    
else:
    from orangecanvas.main import Main as ocMain
    import signal
    import pyqtgraph
    from Orange.widgets.settings import widget_settings_dir
    from logging.handlers import RotatingFileHandler
    from orangecanvas.utils.overlay import Notification, NotificationServer
    from orangewidget.workflow.errorreporting import handle_exception
    from Orange.canvas import config
    from Orange.version import release as is_release
    from orangecanvas.document.usagestatistics import UsageStatistics
    
    log = logging.getLogger(__name__)


    def check_for_updates():
        pass
    

    def send_usage_statistics():
        pass


    def pull_notifications():
        pass

        
    def make_sql_logger(level=logging.INFO):
        sql_log = logging.getLogger('sql_log')
        sql_log.setLevel(level)
        handler = RotatingFileHandler(os.path.join(config.log_dir(), 'sql.log'),
                                    maxBytes=1e7, backupCount=2)
        sql_log.addHandler(handler)


    class _OMain(ocMain):
        DefaultConfig = "Orange.canvas.config.Config"

        def run(self, argv):
            # Allow termination with CTRL + C
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            # Disable pyqtgraph's atexit and QApplication.aboutToQuit cleanup handlers.
            pyqtgraph.setConfigOption("exitCleanup", False)
            super().run(argv)

        def argument_parser(self) -> argparse.ArgumentParser:
            parser = super().argument_parser()
            parser.add_argument(
                "--clear-widget-settings", action="store_true",
                help="Clear stored widget setting/defaults",
            )
            return parser

        def setup_logging(self):
            super().setup_logging()
            make_sql_logger(self.options.log_level)

        def setup_application(self):
            super().setup_application()
            clear_settings_flag = os.path.join(widget_settings_dir(),
                                            "DELETE_ON_START")
            # NOTE: No OWWidgetBase subclass should be imported before this
            options = self.options
            if options.clear_widget_settings or \
                    os.path.isfile(clear_settings_flag):
                shutil.rmtree(widget_settings_dir(), ignore_errors=True)

            notif_server = NotificationServer()
            canvas.notification_server_instance = notif_server

            self._update_check = check_for_updates()
            self._send_stat = send_usage_statistics()
            self._pull_notifs = pull_notifications()

            settings = qt.QSettings()
            settings.setValue('startup/launch-count',
                            settings.value('startup/launch-count', 0, int) + 1)

            if settings.value("reporting/send-statistics", False, type=bool) \
                    and is_release:
                UsageStatistics.set_enabled(True)

            app = self.application

            # set pyqtgraph colors
            def onPaletteChange():
                p = app.palette()
                bg = p.base().color().name()
                fg = p.windowText().color().name()

                log.info('Setting pyqtgraph background to %s', bg)
                pyqtgraph.setConfigOption('background', bg)
                log.info('Setting pyqtgraph foreground to %s', fg)
                pyqtgraph.setConfigOption('foreground', fg)
                app.setProperty('darkMode', p.color(qt.QPalette.Base).value() < 127)

            app.paletteChanged.connect(onPaletteChange)
            onPaletteChange()

        def show_splash_message(self, message: str, color=qt.QColor("#FFD39F")):
            super().show_splash_message(message, color)

        def create_main_window(self):
            window = MainWindow()
            window.set_notification_server(canvas.notification_server_instance)
            return window

        def setup_sys_redirections(self):
            super().setup_sys_redirections()
            if isinstance(sys.excepthook, ExceptHook):
                sys.excepthook.handledException.connect(handle_exception)

        def tear_down_sys_redirections(self):
            if isinstance(sys.excepthook, ExceptHook):
                sys.excepthook.handledException.disconnect(handle_exception)
            super().tear_down_sys_redirections()



class OMain(_OMain):
    config: TomwerConfig
    DefaultConfig = "tomwer.app.canvas_launcher.launcher.TomwerConfig"

    def run(self, argv):
        dealWithLogFile()
        super().run(argv)

    def setup_application(self):
        qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
        return super().setup_application()

    def setup_logging(self):
        super().setup_logging()
        rootlogger = logging.getLogger()
        rootlogger = TomwerLogger(rootlogger)
        logging.setLoggerClass(TomwerLogger)

    def setup_sys_redirections(self):
        # TODO: try to connect with the TomwerLogger
        self._tomwLogger = TomwerLogger("tomwer")
        try:
            self.output = doc = TerminalTextDocument()

            stdout = TextStream(objectName="-stdout")
            stderr = TextStream(objectName="-stderr")
            doc.connectStream(stdout)
            doc.connectStream(stderr, color=qt.Qt.red)

            if sys.stdout is not None:
                stdout.stream.connect(sys.stdout.write, qt.Qt.DirectConnection)

            self.__stdout__ = sys.stdout
            sys.stdout = stdout

            if sys.stderr is not None:
                stderr.stream.connect(sys.stderr.write, qt.Qt.DirectConnection)

            self.__stderr__ = sys.stderr
            sys.stderr = stderr
            self.__excepthook__ = sys.excepthook
            sys.excepthook = ExceptHook(stream=stderr)

            self.stack.push(closing(stdout))
            self.stack.push(closing(stderr))
        except Exception as e:
            super().setup_sys_redirections()

    def argument_parser(self) -> argparse.ArgumentParser:
        parser = super().argument_parser()
        parser.add_argument(
            "--no-color-stdout-logs",
            "--no-colored-logs",
            action="store_true",
            help="instead of having logs in the log view, color logs of the stdout",
            default=False,
        )
        return parser

    def create_main_window(self):
        window = MainWindow()
        window.set_notification_server(canvas.notification_server_instance)
        return window


class Launcher:
    """Proxy to orange-canvas"""

    def launch(self, argv):
        return OMain().run(argv)


def check_is_latest_release() -> bool:
    """Check if the current version is the latest release."""
    url = "https://gitlab.esrf.fr/tomotools/tomwer/-/raw/master/tomwer/version.py"
    current_version = tomwer.version.version
    try:
        version_file_html = urlopen(url, data=None, timeout=10)
    except Exception as e:
        _logger.warning(
            "Fail to load version of the latest release." " Reason is {}".format(e)
        )
        return True
    else:
        latest_release_version = None
        for line in version_file_html.readlines():
            t_line = line.decode("utf-8")
            t_line = t_line.replace(" ", "")
            if t_line.startswith("latest_release_version_info="):
                latest_release_version = t_line.replace(
                    "latest_release_version_info=", ""
                )
                break
        if latest_release_version is None:
            _logger.warning("Unable to find the version of the latest " "release.")

        elif current_version < latest_release_version:
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Question)
            types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
            message = (
                "The version you want to use ({}) is not the latest "
                "version ({}). Do you want to continue ?"
            )
            msg.setStandardButtons(types)
            msg.setWindowTitle("No the latest version")
            msg.setText(message)
            return msg.exec_() == qt.QMessageBox.Ok
        return True


def dealWithLogFile():
    """Move log file history across log file hierarchy and create the new log file"""

    # move log file if exists
    for i in range(MAX_LOG_FILE):
        logFile = LOG_FILE_NAME
        if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
            logFile = os.path.join(LOG_FOLDER, logFile)
        defLogName = logFile

        iLog = MAX_LOG_FILE - i
        maxLogNameN1 = logFile + "." + str(iLog)
        if iLog - 1 == 0:
            maxLogNameN2 = defLogName
        else:
            maxLogNameN2 = logFile + "." + str(iLog - 1)
        if os.path.exists(maxLogNameN2):
            try:
                stat = os.stat(maxLogNameN2)
                shutil.copy(maxLogNameN2, maxLogNameN1)
                os.utime(maxLogNameN1, (stat.st_atime, stat.st_mtime))
            except Exception:
                pass
    # create a new log file
    if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
        logFile = os.path.join(LOG_FOLDER, logFile)
        logging.basicConfig(
            filename=logFile,
            filemode="w",
            level=logging.WARNING,
            format="%(asctime)s %(message)s",
        )
