from PySide2 import QtGui


def get_screen_height(qobject):
    if hasattr(qobject, "screen"):
        return qobject.screen().size().height()
    else:
        print("unable to detect screen height falling back to default value of 1080")
        return 1080


def get_icon(icon_name):
    fallback = QtGui.QIcon(f":/icons/{icon_name}").pixmap(256, 256)
    return QtGui.QIcon.fromTheme(icon_name, fallback)
