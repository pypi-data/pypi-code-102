from K8sActive import K8sTool
from DockerActive import DockerTool
from ProjcetActive import DataTool

conpoolArry = ["10.12.2.51", 30092, 9, "", 5000]
dtObj = DataTool(conpoolArry)
dkObj = DockerTool()
tagStr = dtObj.generatetag(8)
resStr = dkObj.dockerfileActive(tagStr)
tagArg = resStr.split(":", 2)
respParArry = [tagArg[0], tagArg[1], tagArg[2]]
dkObj.dockerPushActive(respParArry)
upargs = ["mnmreportapi", "realses", "docker.muniuma.cn/dotnetbackend:%s" % tagArg[2]]
k8s = K8sTool()
k8s.update_deployment(upargs)