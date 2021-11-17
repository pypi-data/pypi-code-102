from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session, aliased
from starlette import status

from exceptions import ItemNotFound
from models import models
from models.choice_types import ChoiceTypes
from ..models.models import TermAndCondition
from models.user import User
from ..schemas.term_and_condition import TermAndConditionOut, TermAndConditionIn
from .base import CRUDBase


class CRUDCommonQuestion(CRUDBase[TermAndCondition, TermAndConditionIn, TermAndConditionOut]):

    def create(self, db: Session, *, obj_in: TermAndConditionIn) -> TermAndCondition:
        db_obj = TermAndCondition(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session, filter_query_params: list) -> TermAndCondition:
        return db.query(self.model).filter(self.model.is_archive.is_(False)).filter(*filter_query_params).order_by(desc(self.model.created_at))


term_and_condition = CRUDCommonQuestion(TermAndCondition)

