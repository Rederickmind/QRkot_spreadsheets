# app/crud/base.py
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        '''Получение объекта по id.'''
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        '''Получение объекта по переданному аттрибуту.'''
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        '''Получение всех объектов класса.'''
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        '''Создание объекта класса.'''
        obj_in_data = obj_in.dict()
        # Если пользователь был передан...
        if user is not None:
            # ...то дополнить словарь для создания модели.
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            obj_in: UpdateSchemaType,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        '''Обновление объекта класса.'''
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        '''Удаление объекта класса.'''
        await session.delete(db_obj)
        await session.commit()
        return db_obj
