try:
    from PySide6 import QtGui
except ImportError:
    from PySide2 import QtGui


def get_screen_height(qobject):
    if hasattr(qobject, "screen"):
        return qobject.screen().size().height()
    else:
        print("unable to detect screen height falling back to default value of 1080")
        return 1080


def get_icon(icon_name):
    theme_name = icon_name.replace("-light", "")  # respect system theme
    fallback = QtGui.QIcon(f":/icons/{icon_name}").pixmap(256, 256)
    return QtGui.QIcon.fromTheme(theme_name, fallback)
