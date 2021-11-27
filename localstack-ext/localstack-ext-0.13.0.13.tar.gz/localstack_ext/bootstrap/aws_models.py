from localstack.utils.aws import aws_models
GkpTX=super
GkpTV=None
GkpTW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GkpTX(LambdaLayer,self).__init__(arn)
  self.cwd=GkpTV
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GkpTW.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(RDSDatabase,self).__init__(GkpTW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(RDSCluster,self).__init__(GkpTW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(AppSyncAPI,self).__init__(GkpTW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(AmplifyApp,self).__init__(GkpTW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(ElastiCacheCluster,self).__init__(GkpTW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(TransferServer,self).__init__(GkpTW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(CloudFrontDistribution,self).__init__(GkpTW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GkpTW,env=GkpTV):
  GkpTX(CodeCommitRepository,self).__init__(GkpTW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
