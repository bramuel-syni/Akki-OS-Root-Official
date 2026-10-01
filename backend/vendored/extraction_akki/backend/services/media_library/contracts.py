from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,model_validator


class Closed(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False,str_strip_whitespace=True)


class Upload(Closed):
    filename:str=Field(min_length=1,max_length=220)
    size_bytes:int=Field(gt=0)
    sha256:str=Field(pattern=r'^[a-f0-9]{64}$')
    storage_permission_confirmed:Literal[True]


class Metadata(Closed):
    revision:int=Field(ge=1)
    title:str=Field(min_length=1,max_length=140)
    language:str=Field(default='',max_length=80)
    event_label:Literal['unknown','speech','music','mixed']='unknown'
    label_status:Literal['unreviewed','human_reviewed']='unreviewed'
    rights_status:Literal['pending','declared','withdrawn']='pending'
    rights_basis:Literal['','own_recording','permission','licensed','public_domain']=''
    rights_reference:str=Field(default='',max_length=500)
    training_permission_confirmed:bool=False

    @model_validator(mode='after')
    def rights(self):
        if self.rights_status=='declared' and (not self.rights_basis or not self.rights_reference or not self.training_permission_confirmed):
            raise ValueError('Training rights require a basis, evidence reference and explicit confirmation')
        if self.label_status=='human_reviewed' and self.event_label=='unknown':
            raise ValueError('Choose a reviewed speech/music/mixed label or leave it unreviewed')
        return self


class Archive(Closed):
    revision:int=Field(ge=1)
    retention_acknowledged:Literal[True]


class Selection(Closed):
    file_ids:list[str]=Field(min_length=1,max_length=100)
    title:str=Field(default='Music dataset readiness',min_length=1,max_length=140)


class Envelope(BaseModel):
    model_config=ConfigDict(extra='allow')
    tenant_id:str