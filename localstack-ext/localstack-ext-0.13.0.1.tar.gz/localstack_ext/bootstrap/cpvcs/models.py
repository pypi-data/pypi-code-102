from datetime import datetime
FprGs=str
FprGD=int
FprGB=super
FprGV=False
FprGC=isinstance
FprGX=hash
FprGH=True
FprGK=list
FprGM=map
FprGA=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:FprGs):
  self.hash_ref:FprGs=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:FprGs,rel_path:FprGs,file_name:FprGs,size:FprGD,service:FprGs,region:FprGs):
  FprGB(StateFileRef,self).__init__(hash_ref)
  self.rel_path:FprGs=rel_path
  self.file_name:FprGs=file_name
  self.size:FprGD=size
  self.service:FprGs=service
  self.region:FprGs=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return FprGV
  if not FprGC(other,StateFileRef):
   return FprGV
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return FprGX((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return FprGV
  if not FprGC(other,StateFileRef):
   return FprGV
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return FprGH
  return FprGV
 def metadata(self)->FprGs:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:FprGs,state_files:Set[StateFileRef],parent_ptr:FprGs):
  FprGB(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:FprGs=parent_ptr
 def state_files_info(self)->FprGs:
  return "\n".join(FprGK(FprGM(lambda state_file:FprGs(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:FprGs,head_ptr:FprGs,message:FprGs,timestamp:FprGs=FprGs(datetime.now().timestamp()),delta_log_ptr:FprGs=FprGA):
  self.tail_ptr:FprGs=tail_ptr
  self.head_ptr:FprGs=head_ptr
  self.message:FprGs=message
  self.timestamp:FprGs=timestamp
  self.delta_log_ptr:FprGs=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:FprGs,to_node:FprGs)->FprGs:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:FprGs,state_files:Set[StateFileRef],parent_ptr:FprGs,creator:FprGs,rid:FprGs,revision_number:FprGD,assoc_commit:Commit=FprGA):
  FprGB(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:FprGs=creator
  self.rid:FprGs=rid
  self.revision_number:FprGD=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(FprGM(lambda state_file:FprGs(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:FprGs,state_files:Set[StateFileRef],parent_ptr:FprGs,creator:FprGs,comment:FprGs,active_revision_ptr:FprGs,outgoing_revision_ptrs:Set[FprGs],incoming_revision_ptr:FprGs,version_number:FprGD):
  FprGB(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(FprGM(lambda stat_file:FprGs(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
