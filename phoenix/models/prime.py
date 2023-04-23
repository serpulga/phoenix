from sqlalchemy import Column, BigInteger, Index
from sqlmodel import Field

from . import BaseModel


class Prime(BaseModel, table=True):
    __table_args__ = (Index("idx_number", "number", unique=True),)

    number: int = Field(sa_column=Column("number", BigInteger(), nullable=False))
