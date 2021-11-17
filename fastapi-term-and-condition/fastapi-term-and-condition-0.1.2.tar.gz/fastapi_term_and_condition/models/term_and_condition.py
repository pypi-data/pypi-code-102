
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSON

from db.base_class import Base


class TermAndCondition(Base):
    __tablename__ = 'moj_term_and_condition'
    updated_at = None
    key = Column(String(1024))
    value = Column(String(1024))
    category = Column(String(256), default='default')
    additional_data = Column(JSON, default=dict(), )
    is_active = Column(Boolean(), default=True)
