from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(
        sa_column=Column(
            "id",
            UUID(as_uuid=True),
            nullable=False,
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            onupdate=datetime.utcnow,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
