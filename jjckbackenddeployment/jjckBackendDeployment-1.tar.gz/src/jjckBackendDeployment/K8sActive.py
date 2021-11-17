import logging
# from kubernetes import client, config
from os import path
import kubernetes.config as config
import kubernetes.client as client
import yaml
import requests


class K8sTool(object):

    def __init__(self):
        config.load_kube_config(config_file="kubeconfig.yaml")
        # config.load_kube_config()
        self.DEPLOYMENT_NAME = "nginx-deployment"
        self.api = client.AppsV1Api()

    # def config(self):
    #     config.load_kube_config(config_file="kubeconfig.yaml")
    def getPod(self):
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            if i.metadata.namespace == "realses" or i.metadata.namespace == "default":
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def deployment_object(self):
        # Configured Pod template container
        container = client.V1Container(
            name="nginx",
            image="nginx:1.15.4",
            ports=[client.V1ContainerPort(container_port=80)],
            # resources=client.V1ResourceRequirements(
            #     requests={"cpu": "100m", "memory": "200Mi"},
            #     limits={"cpu": "500m", "memory": "500Mi"},
            # ),
        )

        # Create and configure a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
            spec=client.V1PodSpec(containers=[container]),
        )

        # Create the specification of deployment
        spec = client.V1DeploymentSpec(
            replicas=3, template=template, selector={
                "matchLabels":
                    {"app": "nginx"}})

        # Instantiate the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=self.DEPLOYMENT_NAME,
                                         labels={"k8s.kuboard.cn/layer": "web", "k8s.kuboard.cn/name": "website"}),
            spec=spec,
        )

        return deployment

    def create_deployment(self):
        with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.AppsV1Api()
            resp = k8s_apps_v1.create_namespaced_deployment(
                body=dep, namespace="default")
            print(client.V1Container)
            print("Deployment created. status='%s'" % resp.metadata.name)

    def create_deployment(self, api, deployment):
        # Create deployement
        resp = api.create_namespaced_deployment(
            body=deployment, namespace="default"
        )

        print("\n[INFO] deployment `nginx-deployment` created.\n")
        print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
        print(
            "%s\t\t%s\t%s\t\t%s\n"
            % (
                resp.metadata.namespace,
                resp.metadata.name,
                resp.metadata.generation,
                resp.spec.template.spec.containers[0].image,
            )
        )

    def update_deployment(self, api, deployment):
        # Update container image
        deployment.spec.template.spec.containers[0].image = "nginx:1.16.0"

        # patch the deployment
        resp = api.patch_namespaced_deployment(
            name=self.DEPLOYMENT_NAME, namespace="default", body=deployment
        )

        print("\n[INFO] deployment's container image updated.\n")
        print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
        print(
            "%s\t\t%s\t%s\t\t%s\n"
            % (
                resp.metadata.namespace,
                resp.metadata.name,
                resp.metadata.generation,
                resp.spec.template.spec.containers[0].image,
            )
        )

    def update_deployment(self, *upArgs):
        """
        更新K8S上的部署
        :param upArgs:  name=upArgs[0][0],namespace=upArgs[0][1],update_image=upArgs[0][2];
        update_image格式示例：docker.muniuma.cn/dotnetbackend:%tag
        :return:
        """
        name=upArgs[0][0]
        namespace=upArgs[0][1]
        update_image=upArgs[0][2]
        args=name + namespace + update_image
        print("传入的参数为：" + args)
        body = self.api.read_namespaced_deployment(name, namespace)
        body.spec.template.spec.containers[0].image = update_image
        try:
            self.api.replace_namespaced_deployment(name,namespace,body)
            print("更新完成"+args)
            # print("更新完成"+apiResponse.format(namespace, name, update_image))
        except Exception as e:
            print("Exception when calling AppsV1Api->replace_namespaced_deployment: %s\n" % e)
            logging.exception(e)

# class K8sCiCdTool:
#     """
#     CICD专用
#     """
#     def cicdUpdateActive(self, *update):
#         tourl=update[0][0]
#         todate=update[0][3]
#         tocookie=update[0][2]
#         toheaders=update[0][1]
#         req=requests.put(url=tourl,data=todate,headers=toheaders,cookies=tocookie)
#         print(req.content)
