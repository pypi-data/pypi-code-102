import pickle
import random
from pathlib import Path
import os
import redis


class FileTool:
    """
    文件操作
    """

    def checkFile(self, pathStr):
        """
        检查文件是否存在
        :param pathStr: 文件夹路径
        :return: 返回布尔值
        """
        filepath = Path(pathStr)
        if filepath.exists():
            return True

    def copyFile(self, pathStr):
        """
        拷贝文件，将特定文件夹下的所有文件拷贝到项目中
        :param pathStr: 文件夹路径
        :return: 无
        """
        for files in os.listdir(pathStr):
            print("file:" + files)
            cppathStr = pathStr + "/" + files
            with open(cppathStr, "r", encoding="utf-8") as f:
                fcon = f.read()
            # print("文件内容" + fcon)
            tocpStr = "./" + files
            with open(tocpStr, "w", encoding="utf-8") as f:
                f.write(fcon)


class DataTool:
    """
    生成数据，写入redis,读取redis
    """

    def __init__(self, *conPool):
        pool = redis.ConnectionPool(
            host=conPool[0][0],
            port=conPool[0][1],
            db=conPool[0][2],
            password=conPool[0][3],
            max_connections=conPool[0][4]
        )
        self.redisAc = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.redisAc.connection_pool.disconnect()

    def generatetag(self, length):
        """
        生成随机数字字符串
        :param length: 字符串长度
        :return: 返回生成的字符串
        """
        num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
        return num_str

    def setActive(self, name, value, do_pickle=True, expire=60 * 60 * 24 * 7):
        """
        添加set类型，使用pickle进行持久化存储
        :param name:
        :param value:
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :param expire: 单位second，默认7天
        :return:
        """
        if do_pickle:
            self.redisAc.set(name=name, value=pickle.dumps(value), ex=expire)
        else:
            self.redisAc.set(name=name, value=value, ex=expire)

    def getActive(self, name, do_pickle=True):
        getvalue = self.redisAc.get(name=name)
        if getvalue:
            if do_pickle:
                return pickle.loads(getvalue)
            else:
                return getvalue

    def checkActive(self, keyValue):
        return self.redisAc.exists(keyValue)

# if __name__=="__main__":
#     # redis连接字符串参数
#     conpoolArry=["10.12.2.51",30092,9,"",5000]
#
#     dt_str=DataTool(conpoolArry)
#     tag=dt_str.generatetag(8)
#     print(tag)