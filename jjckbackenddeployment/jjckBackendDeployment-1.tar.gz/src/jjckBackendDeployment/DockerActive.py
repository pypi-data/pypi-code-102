import logging
from docker import Client


class DockerTool(object):
    def __init__(self):
        self.c=Client(base_url='tcp://10.12.3.97:2375')
        self.REP_URL="10.12.3.50:30045/"

    # 调用dockerfile文件（这个文件一定要再项目路径下运行）
    def dockerfileActive(self, tagStr):
        dktag=self.REP_URL+"dotnetbackend:"+tagStr
        try:
            res = self.c.build(path="../../", tag=dktag, stream=True)
            for line in res:
                print(line)
        except Exception as e:
            print("调用dockerfileActive，Dockerfile创建镜像不成功%s"%e)
            logging.exception(e)
            dktag=""
        finally:
            return dktag
        #return dktag
    def dockerPushActive(self, *pushArg):
        """
        推送到K8s本地仓库
        :param pushArg: pushArg[0]仓库地址，pushArg[1]版本名称
        :return:
        """
        print("传入参数："+pushArg[0][0]+"\t"+pushArg[0][1])
        try:
            res = self.c.push(repository=pushArg[0][0]+":"+pushArg[0][1], tag=pushArg[0][2], stream=True)
            for line in res:
                print(line)
            print("成功推送到仓库，仓库本版为："+"docker.muniuma.cn/dotnetbackend"+":"+pushArg[0][2])
        except Exception as e:
            print("推送镜像不成功%s"%e)
            logging.exception(e)

# if __name__ == '__main__':
#     dkrun=DockerTool()
#     respParArry = ["10.12.3.50:30045", "11111"]
#     dkrun.dockerPushActive(respParArry)