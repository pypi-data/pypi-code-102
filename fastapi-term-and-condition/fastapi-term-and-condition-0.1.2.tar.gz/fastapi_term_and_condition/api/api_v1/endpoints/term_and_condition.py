from fastapi_pagination import PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from starlette import status
from starlette.datastructures import QueryParams

from ....crud import crud
from ....exceptions import ItemNotFound
from ....schemas.term_and_condition import TermAndConditionIn


# admin

class TermAndConditionWrapper(object):

    def get_term_and_condition(self, db: Session, term_and_condition_id: int):
        term_and_condition = crud.term_and_condition.get(db, id=term_and_condition_id)
        if not term_and_condition:
            raise ItemNotFound(status.HTTP_404_NOT_FOUND, val="term_and_condition")
        return term_and_condition

    def list_term_and_conditions(self, db: Session, params: PaginationParams, filters: QueryParams):
        term_and_conditions = crud.term_and_condition.get_all(db, filter_query_params=filters)
        return paginate(term_and_conditions, params)

    def create_term_and_condition(self, db: Session, term_and_condition_schema: TermAndConditionIn):
        term_and_condition = crud.term_and_condition.create(db=db, obj_in=term_and_condition_schema)
        return term_and_condition

    def update_term_and_condition(self, db: Session, term_and_condition_id: int, term_and_condition_schema: TermAndConditionIn):
        term_and_condition = crud.term_and_condition.get(db, id=term_and_condition_id)
        if not term_and_condition:
            raise ItemNotFound(status.HTTP_404_NOT_FOUND, val="term_and_condition")
        term_and_condition = crud.term_and_condition.update(db, db_obj=term_and_condition, obj_in=term_and_condition_schema)
        return term_and_condition

    def delete_term_and_condition(self, db: Session, term_and_condition_id: int):
        term_and_condition = crud.term_and_condition.get(db, id=term_and_condition_id)
        if not term_and_condition:
            raise ItemNotFound(status.HTTP_404_NOT_FOUND, val="term_and_condition")
        term_and_condition = crud.term_and_condition.remove(db, id=term_and_condition_id)
        return term_and_condition


term_and_condition_wrapper = TermAndConditionWrapper()
