import sys
import os
import psutil as p
import requests
from bs4 import BeautifulSoup
from colorama import init
init()

class Super_os:

    def deleteFile(self, file):
        try:
            os.remove(file)
        except:
            print("Error on the way")

    def deleteFolder(self, folder):
        try:
            os.removedirs(folder)
        except:
            print("Error")

    def toFile(self, put):
        try:
            os.chdir(put)
        except:
            return "Path not found"

    def exit(self):
        sys.exit()

    def rename(self, one_rename, two_rename):
        try:
            os.rename(one_rename, two_rename)
        except:
            return "Error rename"

    def current(self):
        try:
            return os.getcwd()
        except:
            raise NotADirectoryError("failed to find out the current working directory")

    def command(self, command):
        try:
            return os.system(command)
        except:
            raise WindowsError("failed to execute command")

    def seeFile(self, file):
        try:
            return os.listdir()
        except:
            raise FileNotFoundError("failed to execute command")

    def system(self):
        try:
            a = os.name
            if a.lower() == "nt":
                return "Windows"
            else:
                return "Linux or MacOS or another"
        except:
            raise WindowsError("failed to find out your system")

    def user(self):
        try:
            return os.getlogin()
        except:
            raise NameError("failed to find username")

    def pyFile(self):
        try:
            return sys.executable
        except:
            raise FileNotFoundError("could not find a path through which the python lies")

    def Version(self):
        try:
            return sys.version
        except:
            raise FileNotFoundError("failed to find out python version")

    def prLoad(self):
        try:
            a = p.cpu_percent(interval=1)
            b = str(int(a)) + "%"
            return b
        except:
            raise WindowsError("failed to find out the load on the processor")

    """
    def suspendProcess(self, nameProcess):
        try:
            p.suspend(nameProcess)
        except:
            raise WindowsError("failed to freeze file")

    def unsuspendProcess(self, nameProcess):
        try:
            p.resume(nameProcess)
        except:
            raise WindowsError("failed to unfreeze the file")

    def terminateProcess(self, nameProcess):
        try:
            p.terminate(nameProcess)
        except:
            raise WindowsError("failed to superkill the process")

    def killProcess(self, nameProcess):
        try:
            p.kill(nameProcess)
        except:
            raise WindowsError("failed to kill process")
    """

    def prId(self):
        try:
            return os.getpid()
        except:
            raise WindowsError("failed to find out the id of the current process")

    def Weight(self, object):
        try:
            return os.path.getsize(object)
        except:
            raise WindowsError("failed to find out the file weight")

    def battery(self):
        try:
            return p.sensors_battery()
        except:
            raise OSError("could not find a component in the system")

    def form(self, firstname, secondname, text):
        try:
            strok = str(f"This is a text from {firstname} {secondname}.\nText: \n {text}")
        except:
            raise WindowsError("Failed to create text")

    def absolute(self, path):
        try:
            if os.path.isabs(path) == True:
                return True
            else:
                return False
        except:
            raise OSError("failed to find out the type of path")

    def randomByte(self, byte):
        try:
            return os.urandom(byte)
        except:
            raise WindowsError("failed to generate a random number of bytes")

    def help(self):
        print("to get help or read the documentation go to our telegram channel: https://t.me/LibrarySoe")

soe = Super_os()
