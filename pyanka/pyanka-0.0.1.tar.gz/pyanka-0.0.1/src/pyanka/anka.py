"""
Anka wrapper library
"""
from typing import List
import subprocess
import json

class AnkaVm:
    """
    This class is representing an Anka Virtual machine
    on initialising it, you need to provide a VM name
    to use.
    """
    PATH = "/usr/local/bin/anka"
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def runner(cls, args: list):
        """
        A helper function to run subprocesses.
        """
        return subprocess.run(args, capture_output=True, text=True, check=True).stdout

    def start(self):
        """
        Start or resume a stopped or suspended VM
        """
        args = [self.PATH, "start", self.name]
        self.runner(args)

    def suspend(self):
        """
        Suspend a running VM
        """
        args = [self.PATH, "suspend", self.name]
        self.runner(args)

    def stop(self):
        """
        Shut down a VM
        """
        args = [self.PATH, "stop", self.name]
        self.runner(args)

    def clone(self, target: str):
        """
        Clone a suspended or stopped VM
        Takes one argument, the name for the copy, and clones a suspended or stopped VM
        """
        args = [self.PATH, "clone", self.name, target]
        cmd = self.runner(args)
        if cmd.returncode == 0:
            vm_clone = AnkaVm(target)
            return vm_clone
        return cmd.stderr

    def delete(self):
        """
        Delete a VM
        """
        args = [self.PATH, "delete", "--yes", self.name]
        self.runner(args)

    def run(self, *args: List[str]):
        """
        Run a command inside of a VM (will start VM if suspended or stopped)
        Takes a list of arguments in the form of:
        cmd *args fe.: ("ls", "-la")
        """
        return self.runner([self.PATH, "run", self.name, *args])

    def copy(self, source: str, destination: str):
        """
        Copy files in and out of the VM and host.
        Takes two arguments, the source file/folder you want to copy
        and the desired destination.
        In this implementation the copy will always be recursive.
        """
        dest = self.name + ":" + destination
        return self.runner([self.PATH, "cp", "-R", source, dest])

    def show(self):
        """
        Show a VM's runtime properties
        """
        string_data = self.runner([self.PATH, "--machine-readable", "show", self.name])
        json_data = json.loads(string_data)
        return json_data
