# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "11/10/2021"


from silx.gui import qt
from tomwer.core.settings import SlurmSettings


class SlurmSettingsDialog(qt.QDialog):
    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(qt.QVBoxLayout())
        self._mainWidget = SlurmSettingsWidget(parent=self)
        self.layout().addWidget(self._mainWidget)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Close
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        self._buttons.button(qt.QDialogButtonBox.Close).clicked.connect(self.close)

        # connect signal /slot
        self._mainWidget.sigConfigChanged.connect(self._configChanged)

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def isSlurmActive(self):
        return self._mainWidget.isSlurmActive()

    def getConfiguration(self) -> dict:
        return self._mainWidget.getConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self._mainWidget.setConfiguration(config=config)


class SlurmSettingsWidget(qt.QWidget):
    """Widget used to define Slurm configuration to be used"""

    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setLayout(qt.QFormLayout())

        # queues
        self._queue = qt.QLineEdit("", self)
        self.layout().addRow("queue / partition", self._queue)
        # TODO: add the result of a sinfo retrieving available queues

        # n workers
        self._nWorkers = qt.QSpinBox(self)
        self._nWorkers.setRange(1, 100)
        self.layout().addRow("number of workers", self._nWorkers)

        # ncores active
        self._nCores = qt.QSpinBox(self)
        self._nCores.setRange(1, 500)
        self.layout().addRow("number of cores per worker", self._nCores)

        # memory
        self._memory = qt.QSpinBox(self)
        self._memory.setRange(1, 10000)
        self._memory.setSuffix("GB")
        self.layout().addRow("memory per worker", self._memory)

        # gpu
        self._nGpu = qt.QSpinBox(self)
        self._nGpu.setRange(1, 10)
        self.layout().addRow("number of GPUs per worker", self._nGpu)

        # wall time
        self._wallTime = qt.QLineEdit("", self)
        self.layout().addRow("wall time", self._wallTime)

        # python exe
        self._pythonVenv = qt.QLineEdit("", self)
        self.layout().addRow("python venv", self._pythonVenv)
        self._pythonVenv.setToolTip(
            """
            python virtual environment path to be used to call nabu for reconstructing slices.
            """
        )

        # project name
        self._projectName = qt.QLineEdit("", self)
        self._projectName.setToolTip(
            """Name of the project. Can contains several keyword that will be formatted:
            - scan: will be replaced by the scan name
            - process: will be replaced by the process name (nabu slices, nabu volume...)
            - info: some extra information that can be provided by the process to `specify` the processing
            note: those key word have to be surronding by surrounded `{` and `}` in order to be formatted.
            """
        )
        self.layout().addRow("project name", self._projectName)

        # port
        # TODO: replace by a dedicated widget / validator for TCP adress
        self._port = qt.QSpinBox(self)
        self._port.setRange(0, 99999)
        self._port.setToolTip("TCP Port for the dask-distributed scheduler")
        self.layout().addRow("port", self._port)

        # dashboard port
        # TODO: replace by a dedicated widget / validator for TCP adress
        self._dashboardPort = qt.QSpinBox(self)
        self._dashboardPort.setRange(0, 99999)
        self._dashboardPort.setToolTip("TCP Port for the dashboard")
        self.layout().addRow("dashboard port", self._dashboardPort)

        # set up the gui
        self._nCores.setValue(SlurmSettings.N_CORES_PER_WORKER)
        self._nWorkers.setValue(SlurmSettings.N_WORKERS)
        self._memory.setValue(SlurmSettings.MEMORY_PER_WORKER)
        self._queue.setText(SlurmSettings.QUEUE)
        self._nGpu.setValue(SlurmSettings.N_GPUS_PER_WORKER)
        self._projectName.setText(SlurmSettings.PROJECT_NAME)
        self._wallTime.setText(SlurmSettings.DEFAULT_WALLTIME)
        self._pythonVenv.setText(SlurmSettings.PYTHON_VENV)
        self._port.setValue(SlurmSettings.PORT)
        self._dashboardPort.setValue(SlurmSettings.DASHBOARD_PORT)

        # connect signal / slot
        self._nCores.valueChanged.connect(self._configurationChanged)
        self._nWorkers.valueChanged.connect(self._configurationChanged)
        self._memory.valueChanged.connect(self._configurationChanged)
        self._queue.textEdited.connect(self._configurationChanged)
        self._nGpu.valueChanged.connect(self._configurationChanged)
        self._projectName.editingFinished.connect(self._configurationChanged)
        self._wallTime.editingFinished.connect(self._configurationChanged)
        self._pythonVenv.editingFinished.connect(self._configurationChanged)
        self._port.valueChanged.connect(self._configurationChanged)
        self._dashboardPort.valueChanged.connect(self._configurationChanged)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getNCores(self) -> int:
        return self._nCores.value()

    def setNCores(self, n: int) -> None:
        self._nCores.setValue(n)

    def getNWorkers(self) -> int:
        return self._nWorkers.value()

    def setNWorkers(self, n) -> None:
        self._nWorkers.setValue(n)

    def getMemory(self) -> int:
        return self._memory.value()

    def setMemory(self, memory: int) -> None:
        self._memory.setValue(memory)

    def getQueue(self) -> str:
        return self._queue.text()

    def setQueue(self, text: str) -> None:
        self._queue.setText(text)

    def getNGPU(self) -> int:
        return self._nGpu.value()

    def setNGPU(self, n: int) -> None:
        self._nGpu.setValue(n)

    def getProjectName(self):
        return self._projectName.text()

    def setProjectName(self, name):
        self._projectName.setText(name)

    def getWallTime(self):
        return self._wallTime.text()

    def setWallTime(self, walltime):
        self._wallTime.setText(walltime)

    def getPythonExe(self):
        return self._pythonVenv.text()

    def setPythonExe(self, python_venv):
        self._pythonVenv.setText(python_venv)

    def getPort(self):
        return self._port.value()

    def setPort(self, value: int):
        self._port.setValue(value)

    def getDashboardPort(self):
        return self._dashboardPort.value()

    def setDashboardPort(self, value):
        self._dashboardPort.setValue(value)

    def setConfiguration(self, config: dict) -> None:
        old = self.blockSignals(True)
        active_slurm = config.get("active_slurm", None)
        if active_slurm is not None:
            self._slurmCB.setChecked(active_slurm)

        n_cores = config.get("cores", None)
        if n_cores is not None:
            self.setNCores(n_cores)

        n_workers = config.get("n_workers", None)
        if n_workers is not None:
            self.setNWorkers(n_workers)

        memory = config.get("memory", None)
        if memory is not None:
            self.setMemory(memory)

        queue_ = config.get("queue", None)
        if queue_ is not None:
            self.setQueue(queue_)

        n_gpu = config.get("n_gpus", None)
        if n_gpu is not None:
            self.setNGPU(n_gpu)

        project_name = config.get("project_name")
        if project_name is not None:
            self.setProjectName(project_name)

        wall_time = config.get("walltime")
        if wall_time is not None:
            self.setWallTime(wall_time)

        python_venv = config.get("python_venv")
        if python_venv is not None:
            self.setPythonExe(python_venv)

        port = config.get("port")
        if port is not None:
            self.setPort(port)

        dashboard_port = config.get("dashboard_port")
        if dashboard_port is not None:
            self.setDashboardPort(dashboard_port)

        self.blockSignals(old)
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        return {
            "cores": self.getNCores(),
            "n_workers": self.getNWorkers(),
            "memory": self.getMemory(),
            "queue": self.getQueue(),
            "n_gpus": self.getNGPU(),
            "project_name": self.getProjectName(),
            "walltime": self.getWallTime(),
            "python_venv": self.getPythonExe(),
            "port": self.getPort(),
            "dashboard_port": self.getDashboardPort(),
        }

    def getSlurmClusterConfiguration(self):
        from tomwer.core.cluster import SlurmClusterConfiguration

        return SlurmClusterConfiguration().from_dict(self.getConfiguration())


if __name__ == "__main__":
    app = qt.QApplication([])
    widget = SlurmSettingsDialog()
    widget.show()
    app.exec_()
