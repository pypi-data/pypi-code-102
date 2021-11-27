from datetime import datetime
toVJB=str
toVJk=int
toVJz=super
toVJu=False
toVJs=isinstance
toVJL=hash
toVJQ=bool
toVJK=True
toVJH=list
toVJc=map
toVJW=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:toVJB):
  self.hash_ref:toVJB=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:toVJB,rel_path:toVJB,file_name:toVJB,size:toVJk,service:toVJB,region:toVJB):
  toVJz(StateFileRef,self).__init__(hash_ref)
  self.rel_path:toVJB=rel_path
  self.file_name:toVJB=file_name
  self.size:toVJk=size
  self.service:toVJB=service
  self.region:toVJB=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return toVJu
  if not toVJs(other,StateFileRef):
   return toVJu
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return toVJL((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->toVJQ:
  if not other:
   return toVJu
  if not toVJs(other,StateFileRef):
   return toVJu
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->toVJQ:
  for other in others:
   if self.congruent(other):
    return toVJK
  return toVJu
 def metadata(self)->toVJB:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:toVJB,state_files:Set[StateFileRef],parent_ptr:toVJB):
  toVJz(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:toVJB=parent_ptr
 def state_files_info(self)->toVJB:
  return "\n".join(toVJH(toVJc(lambda state_file:toVJB(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:toVJB,head_ptr:toVJB,message:toVJB,timestamp:toVJB=toVJB(datetime.now().timestamp()),delta_log_ptr:toVJB=toVJW):
  self.tail_ptr:toVJB=tail_ptr
  self.head_ptr:toVJB=head_ptr
  self.message:toVJB=message
  self.timestamp:toVJB=timestamp
  self.delta_log_ptr:toVJB=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:toVJB,to_node:toVJB)->toVJB:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:toVJB,state_files:Set[StateFileRef],parent_ptr:toVJB,creator:toVJB,rid:toVJB,revision_number:toVJk,assoc_commit:Commit=toVJW):
  toVJz(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:toVJB=creator
  self.rid:toVJB=rid
  self.revision_number:toVJk=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(toVJc(lambda state_file:toVJB(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:toVJB,state_files:Set[StateFileRef],parent_ptr:toVJB,creator:toVJB,comment:toVJB,active_revision_ptr:toVJB,outgoing_revision_ptrs:Set[toVJB],incoming_revision_ptr:toVJB,version_number:toVJk):
  toVJz(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(toVJc(lambda stat_file:toVJB(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
