#!/usr/local/env python3
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass

import codefast as cf

SUPVISOR_CONF_TEMPLATE = '''
[program:PLACEHOLDER]
directory=/tmp/
command=COMMAND
user=root
autostart=true
autorestart=true
redirect_stderr=true
stopasgroup=true
killasgroup=true'''


class Symbols:
    smiley = '😀'
    sad = '😞'
    question = '❓'
    info = 'ℹ️'
    warning = '⚠️'
    error = '🚫'
    success = '✅'
    fail = '❌'
    ok = '✅'
    turtule = '🐢'
    mokey = '🐵'


class Apps:
    core_apps = [
        'tree', 'p7zip-full', 'python3-pip', 'emacs', 'ufw', 'curl', 'wget',
        'unzip', 'aria2', 'shadowsocks-libev', 'ncdu', 'git', 'supervisor',
        'graphviz'
    ]
    stat_apps = [
        'vnstat', 'iftop', 'bmon', 'tcptrack', 'slurm', 'sysstat', 'bc', 'pv',
        'neofetch', 'jq', 'htop', 'vnstat', 'ffmpeg', 'nload', 'ncdu'
    ]


@dataclass
class Cmd:
    pre_msg: str = ''
    command: str = ''
    post_msg: str = ''


class BashRunner:
    @staticmethod
    def get_output(command: str) -> str:
        return subprocess.check_output(command, shell=True).decode('utf-8')

    @staticmethod
    def call(command: str) -> int:
        return subprocess.call(command, shell=True)

    @staticmethod
    def call_with_msg(cmd_obj: Cmd) -> None:
        cf.info(cmd_obj.pre_msg)
        resp = BashRunner.call(cmd_obj.command)
        if resp == 0:
            cf.info(cmd_obj.post_msg + ' ' + Symbols.success)
        else:
            raise Exception(f'{cmd_obj.post_msg} failed')


class Installer:
    @abstractmethod
    def install(self):
        pass


class CoreAppInstaller(Installer):
    def install(self):
        for app in Apps.core_apps:
            cmd = Cmd(pre_msg=f'Installing {app}',
                      command=f'apt install {app}',
                      post_msg=f'{app} installed')
            BashRunner.call_with_msg(cmd)


class StatAppInstaller(Installer):
    def install(self):
        for app in Apps.stat_apps:
            cmd = Cmd(pre_msg=f'Installing {app}',
                      command=f'apt install {app}',
                      post_msg=f'{app} installed')
            BashRunner.call_with_msg(cmd)


class Config(ABC):
    @abstractmethod
    def run(self):
        pass


class EndlessConfig(Config):
    def __init__(self):
        self.supervisor_name = 'endlessh'
        self.command = '/usr/local/bin/endlessh -p 22'
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.supervisor_name)
        self.conf = self.conf.replace('COMMAND', self.command)

    def run(self):
        cmd = Cmd(pre_msg=f'Installing {self.supervisor_name}',
                  command=f'pip3 install endlessh==0.0.4.dev3 joblib',
                  post_msg=f'{self.supervisor_name} installed')
        BashRunner.call_with_msg(cmd)
        cf.info('update supervisor config file')
        cf.io.write(self.conf, '/etc/supervisor/conf.d/endlessh.conf')
        BashRunner.call(f'supervisorctl reread')
        BashRunner.call(f'supervisorctl update')
        BashRunner.call(f'supervisorctl start {self.supervisor_name}')


class Executor:
    def __init__(self):
        pass

    @classmethod
    def run(cls):
        CoreAppInstaller().install()
        StatAppInstaller().install()
        EndlessConfig().run()


def main():
    Executor.run()


if __name__ == '__main__':
    main()
