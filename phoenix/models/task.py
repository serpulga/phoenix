from datetime import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime, BigInteger
from sqlmodel import Field, SQLModel

from . import BaseModel


class TaskStatus(enum.Enum):
    New = "new"
    Processing = "processing"
    Finished = "finished"
    Failed = "failed"


class Task(BaseModel, table=True):
    number: int = Field(
        index=True, sa_column=Column("number", BigInteger(), nullable=False)
    )
    status: TaskStatus = TaskStatus.New
    finished_at: datetime | None = Field(
        sa_column=Column("finished_at", DateTime(True), nullable=True)
    )
    is_prime: bool | None = None


class TaskRead(SQLModel):
    id: uuid.UUID
    number: int
    status: TaskStatus


class TaskResult(TaskRead):
    is_prime: bool | None
    created_at: datetime
    finished_at: datetime | None
