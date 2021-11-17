from localstack.utils.aws import aws_models
EgDcP=super
EgDcJ=None
EgDcy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EgDcP(LambdaLayer,self).__init__(arn)
  self.cwd=EgDcJ
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EgDcy.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(RDSDatabase,self).__init__(EgDcy,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(RDSCluster,self).__init__(EgDcy,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(AppSyncAPI,self).__init__(EgDcy,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(AmplifyApp,self).__init__(EgDcy,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(ElastiCacheCluster,self).__init__(EgDcy,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(TransferServer,self).__init__(EgDcy,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(CloudFrontDistribution,self).__init__(EgDcy,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EgDcy,env=EgDcJ):
  EgDcP(CodeCommitRepository,self).__init__(EgDcy,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
