import logging
gQIXu=bool
gQIXw=hasattr
gQIXn=set
gQIXi=True
gQIXc=False
gQIXJ=isinstance
gQIXa=dict
gQIXK=getattr
gQIXH=None
gQIXf=str
gQIXM=Exception
gQIXP=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[gQIXu,Set]:
 if gQIXw(obj,"__dict__"):
  visited=visited or gQIXn()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return gQIXi,visited
  visited.add(wrapper)
 return gQIXc,visited
def get_object_dict(obj):
 if gQIXJ(obj,gQIXa):
  return obj
 obj_dict=gQIXK(obj,"__dict__",gQIXH)
 return obj_dict
def is_composite_type(obj):
 return gQIXJ(obj,(gQIXa,OrderedDict))or gQIXw(obj,"__dict__")
def api_states_traverse(api_states_path:gQIXf,side_effect:Callable[...,gQIXH],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except gQIXM as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with gQIXP(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except gQIXM as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with gQIXP(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
