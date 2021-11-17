
from src.jjckBackendDeployment.K8sActive import K8sTool
from src.jjckBackendDeployment.DockerActive import DockerTool
from src.jjckBackendDeployment.ProjcetActive import DataTool

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def run():

    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # k8s = K8sCiCdTool()
    # tag="86800117"
    # jsondata={"kind":"deployments","namespace":"realses","name":"mnmreportapi","images":{"docker.muniuma.cn/dotnetbackend":"docker.muniuma.cn/dotnetbackend:%s"%tag}}
    # print(json.dumps(jsondata))
    # cicdArgs=["http://10.12.3.50:30080/kuboard-api/cluster/default/kind/CICDApi/admin/resource/updateImageTag",
    #           {"Content-Type": "application/json"},
    #           {"Cookie": "KuboardUsername=admin; KuboardAccessKey=t68znzjh5ihx.shjwjbjk3d7hh3ezmmxwj5ccw8rsf4e7"},
    #           json.dumps(jsondata)
    #           ]
    #
    #
    # k8s.cicdUpdateActive(cicdArgs)
    #dep = k8s.deployment_object()
    # k8s.config()
    #k8s.getPod()
    # k8s.create_deployment(k8s.api, dep)
    # k8s.update_deployment(k8s.api, dep)
    upargs=["mnmreportapi","realses","docker.muniuma.cn/dotnetbackend:88996434"]
    k8s=K8sTool()
    k8s.update_deployment(upargs)
def dockerrun():
    conpoolArry = ["10.12.2.51", 30092, 9, "", 5000]
    dtObj=DataTool(conpoolArry)
    dkObj=DockerTool()
    tagStr=dtObj.generatetag(8)
    resStr=dkObj.dockerfileActive(tagStr)
    tagArg=resStr.split(":",2)
    respParArry=[tagArg[0],tagArg[1],tagArg[2]]
    dkObj.dockerPushActive(respParArry)
    upargs = ["mnmreportapi", "realses", "docker.muniuma.cn/dotnetbackend:%s"%tagArg[2]]
    k8s=K8sTool()
    k8s.update_deployment(upargs)
    # pja=FileTool()
    # ph="D:\pythonEnvTest\dockerAutoPushEnv"
    # if pja.checkFile(ph):
    #     pja.copyFile(ph)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dockerrun()
    # print_hi('PyCharm')
    # run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
