import os
import signal
import subprocess
from datetime import datetime, timedelta, time
from time import sleep

from ctpbee.date import trade_dates


class Flux(object):
    """
    Hickey任务调度机制

    主要为了完成自动拉起程序
    """
    from datetime import time
    DAY_START = time(9, 0)  # 日盘启动和停止时间
    DAY_END = time(15, 5)
    NIGHT_START = time(21, 0)  # 夜盘启动和停止时间
    NIGHT_END = time(2, 35)

    TIME_MAPPING = {
        "dy_st": "DAY_START",
        "dy_ed": "DAY_END",
        "ng_st": "NIGHT_START",
        "ng_ed": "NIGHT_END"
    }

    def __init__(self, command: str):
        self.names = []
        from datetime import time
        self.open_trading = {
            "ctp": {"DAY_START": time(9, 0), "NIGHT_START": time(21, 0)}
        }
        self.os_command = command

        self.limit_time_area = []

    def auth_time(self, current: datetime):
        current_string = str(current.date())

        last_day = str((current + timedelta(days=-1)).date())
        """
        如果前一天是交易日， 今天不是 那么交易到今晚晚上2点：30

        如果前一天不是交易日，今天是  那么早盘前 不启动 

        如果前一天不是交易日, 今天也不是交易日 那么不启动 
        """
        if (last_day in trade_dates and current_string not in trade_dates and current.time() > self.NIGHT_END) or \
                (last_day not in trade_dates and current_string in trade_dates and current.time() < self.DAY_START) or \
                (last_day not in trade_dates and current_string not in trade_dates):
            return False

        if self.DAY_END >= current.time() >= self.DAY_START:
            return True
        if current.time() >= self.NIGHT_START:
            return True
        if current.time() <= self.NIGHT_END:
            return True
        return False

    def auth_area(self, current: datetime) -> bool:
        auth = False
        for (start, end) in self.limit_time_area:
            if start <= current.time() <= end:
                auth = True
                break
        return auth

    @staticmethod
    def add_seconds(tm, seconds, direction=False):
        full_date = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        if not direction:
            full_date = full_date - timedelta(seconds=seconds)
        else:
            full_date = full_date + timedelta(seconds=seconds)
        return full_date.time()

    def start_all(self, info=True, interface="ctp", in_front=300):
        """
        开始进程管理
        * app_func: 创建app的函数
        * interface: 接口名字
        * in_front: 相较于开盘提前多少秒进行运行登陆.单位: seconds
        """
        print("Hey Julia")

        for i, v in self.open_trading[interface].items():
            setattr(self, i, self.add_seconds(getattr(self, i), in_front))
        p = None
        while True:
            current = datetime.now()
            # 当前是否为交易时间的验证
            trade_status = self.auth_time(current)
            user_auth = self.auth_area(current)
            status = trade_status and user_auth
            if info:
                print(f"{current.strftime('%Y-%m-%d %H:%M:%S')} flux running ---> ^_^ ")
            if p is None and status:
                p = subprocess.Popen(self.os_command, shell=False, close_fds=True, preexec_fn=os.setsid)
                print("===> program start successful")
            if not status and p is not None:
                print("Kill Program ", p.pid)
                os.killpg(p.pid, signal.SIGUSR1)
                p = None
            sleep(1)

    def update_time(self, timed: time, flag: str):
        """
        此函数被用来修改更新启动时间或者关闭时间

        :param timed:
        :param flag:需要修改的字段 仅仅
                  "dy_st": "白天开始",
                 "dy_ed": "白天结束",
                "ng_st": "晚上开始",
               "ng_ed": "晚上结束"
    }
        :return: None
        """
        if flag not in self.TIME_MAPPING.keys():
            raise ValueError(f"注意你的flag是不被接受的，我们仅仅支持\n "
                             f"{str(list(self.TIME_MAPPING.keys()))}四种")
        if not isinstance(timed, time):
            raise ValueError(f"timed错误的数据类型，期望 time, 当前{str(type(timed))}")

        setattr(self, self.TIME_MAPPING[flag], timed)

    def insert(self, start: time, end: time):
        """
        此函数用于插入命令启动时间以及持续时间
        """
        assert end >= start
        self.limit_time_area.append((start, end))

    def __repr__(self):
        return "7*24 manager ^_^"


if __name__ == '__main__':
    # flux = Flux(command="dir")
    # flux.insert(time(11, 11), time(11, 12))
    # flux.start_all()
    a = time(11, 12)
    b = time(11, 11)
    print(a < b)
