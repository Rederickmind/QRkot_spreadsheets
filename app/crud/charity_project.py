from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Получение id проекта по имени."""
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, str]]:
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 1)
        )
        projects = projects.scalars().all()
        sorted_list = []
        for project in projects:
            sorted_list.append(
                {
                    'name': project.name,
                    'funding_time': project.close_date - project.create_date,
                    'description': project.description
                }
            )
        project_list = sorted(sorted_list, key=lambda x: x['funding_time'])
        return project_list


charityproject_crud = CRUDCharityProject(CharityProject)