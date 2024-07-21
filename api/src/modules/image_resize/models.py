from sqlmodel import SQLModel, Field
from typing import Optional


class Images(SQLModel, table=True):

    __tablename__ = "images"

    id: Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    image_name: str = Field(default=None, unique=True, index=True, nullable=False)
    resize_status: str = Field(default="not_started", index=True, nullable=False)
