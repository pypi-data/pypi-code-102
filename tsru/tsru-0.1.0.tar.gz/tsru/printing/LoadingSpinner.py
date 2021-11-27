import time
import threading

# Try to load colorama extension
try:
    from colorama import Fore
    cr = True
except ImportError:
    cr = False
if cr:
    green = Fore.GREEN
    red = Fore.RED
    white = Fore.WHITE
    gray = Fore.LIGHTBLACK_EX
else:
    green = ""
    red = ""
    white = ""
    gray = ""

class LoadingSpinner:
    """
    A class for creating a spinner to indicate to the user that something is running in the background.

    Example:\n
        spinner = LoadingSpinner("Doing something")\n
        sleep(1)\n
        success = True\n
        spinner.stop(success)\n
    Outputs:\n
        / Doing something\n
        \\ Doing something\n
        \- Doing something\n
        Done Doing something
    """
    def __init__(self, msg_running:str=f"{gray}{white}", msg_done:str=f"{green}Success{white}", msg_failed:str=f"{red}Failed {white}") -> None:
        """
        Initialize and start the spinner.

        Params:
            [OPTIONAL] msg_running: str - the message to be displayed after the spinner
            [OPTIONAL] msg_done:    str - the message to be displayed after finishing successfully
            [OPTIONAL] msg_failed:  str - the message to be displayed after finishing without success

        Returns:
            None
        """
        self.running = True
        self.msg_running = gray + msg_running + white
        self.msg_done = green + msg_done + white 
        self.msg_failed = red + msg_failed + white
        threading.Thread(target=self._run).start()
    def _run(self) -> None:
        current = "-"
        rotation = {
            "-": "\\",
            "\\": "/",
            "/": "-"
        }
        while self.running:
            print(current + "  " + self.msg_running, end="\r")
            current = rotation[current]
            time.sleep(0.2)
        if self.success:
            print(self.msg_done + "  " + self.msg_running)
        else:
            print(self.msg_failed + "  " + self.msg_running)

    def stop(self, success:bool=True) -> bool:
        """
        Stops the spinner. 

        Params:
            [OPTIONAL] success: bool - whether the process was successfull

        Returns: 
            bool: True - after completion
        """
        self.success = success
        self.running = False
        time.sleep(0.2)
        return True