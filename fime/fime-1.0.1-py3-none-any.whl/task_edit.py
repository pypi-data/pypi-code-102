from PySide2 import QtCore, QtGui, QtWidgets

from fime.util import get_icon


class TaskEdit(QtWidgets.QDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Edit Tasks")
        self.list = QtCore.QStringListModel()

        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.list)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().hide()
        self.tableView.verticalHeader().hide()

        new_button = QtWidgets.QPushButton()
        new_button.setText("New item")
        new_button.setIcon(get_icon("list-add"))
        new_button.pressed.connect(self.new_task)
        new_button.setAutoDefault(False)

        del_button = QtWidgets.QPushButton()
        del_button.setText("Delete item")
        del_button.setIcon(get_icon("list-remove"))
        del_button.pressed.connect(self.del_task)
        del_button.setAutoDefault(False)

        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setIcon(get_icon("dialog-ok"))
        ok_button.pressed.connect(self.accept)
        ok_button.setAutoDefault(True)

        blayout = QtWidgets.QHBoxLayout()
        blayout.addWidget(new_button)
        blayout.addWidget(del_button)
        blayout.addWidget(ok_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tableView)
        layout.addLayout(blayout)
        self.setLayout(layout)

    @QtCore.Slot()
    def new_task(self):
        l = self.list.stringList()
        l.append("")
        self.list.setStringList(l)
        i = self.list.index(len(l)-1)
        self.tableView.setCurrentIndex(i)
        self.tableView.edit(i)

    @QtCore.Slot()
    def del_task(self):
        l = self.list.stringList()
        del l[self.tableView.currentIndex().row()]
        self.list.setStringList(l)

    @property
    def tasks(self):
        ret = self.list.stringList()
        return list(filter(None, ret))  # filter empty strings

    @tasks.setter
    def tasks(self, tasks):
        self.list.setStringList(tasks)
