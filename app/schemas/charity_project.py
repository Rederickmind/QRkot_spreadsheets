from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectUpdate(BaseModel):
    """Схема обновления проекта."""
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: int = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectUpdate):
    """Схема создания проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def field_cant_be_empty(cls, value: str):
        if not value or value is None:
            raise ValueError('Все поля должны быть не пустыми!')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема данных проекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True