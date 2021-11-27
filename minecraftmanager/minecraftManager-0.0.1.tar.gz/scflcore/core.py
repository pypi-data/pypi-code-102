import mctools
from mctools import RCONClient

class MinecraftRconManager():
  def __init__(self, host: str=None, port: int=25565, password: str=None):
    self.password = password
    self.host = host
    self.rcon = RCONClient(host, port=port)

  def runCommand(self, command: str=None):
    if self.host is None:
      print("Host is invalid")
    else:
      if self.password is None:
        print("Password is invalid")
      else:
        try:
          if self.rcon.login(self.password):
            resp = self.rcon.command("{}".format(command))
            self.rcon.stop()
        except Exception as e:
          print(e)