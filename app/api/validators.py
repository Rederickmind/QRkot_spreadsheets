from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject
from app.services.constants import (NAME_DUPLICATE, PROJECT_CLOSE,
                                    PROJECT_NOT_FOUND, PROJECT_RAISING_MONEY,
                                    SUMM_LOWER)


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    """Проверка уникальности имени проекта."""
    project = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )
    if project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_DUPLICATE
        )


async def check_project_existence(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта в базе данных."""
    project = await charityproject_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND + f'{project_id}'
        )
    return project


def check_if_project_closed(obj):
    """Проверка - если проект закрыт, редактирование запрещено."""
    if obj.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_CLOSE
        )


def check_if_new_full_amount_less_than_invested_amount(obj, new_amount=None):
    """Проверка что новая цель сбора не может быть меньше уже вложенных средств."""
    obj.invested_amount
    if new_amount:
        if new_amount < obj.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=SUMM_LOWER + f'{obj.invested_amount}'
            )
    return obj


def check_if_project_invested(obj):
    """Проверка вложены ли в проект средства перед удалением."""
    if obj.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_RAISING_MONEY
        )
    return obj