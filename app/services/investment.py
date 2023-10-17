from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_fully_invested_objects(
        session: AsyncSession
):
    not_invested_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        ).order_by('create_date')
    )
    project = not_invested_projects.scalars().first()
    not_invested_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        ).order_by('create_date')
    )
    donation = not_invested_donations.scalars().first()
    return project, donation


async def investment(
        session: AsyncSession,
        obj
):
    project, donation = await get_not_fully_invested_objects(session)
    if (project is None) or (donation is None):
        await session.commit()
        await session.refresh(obj)
        return obj
    project_funds = project.full_amount - project.invested_amount
    donation_funds = donation.full_amount - donation.invested_amount
    if project_funds > donation_funds:
        project.invested_amount += donation_funds
        donation.invested_amount += donation_funds
        donation.fully_invested = True
        donation.close_date = datetime.now()
    elif project_funds == donation_funds:
        project.invested_amount += donation_funds
        donation.invested_amount += donation_funds
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = datetime.now()
        donation.close_date = datetime.now()
    else:
        project.invested_amount += project_funds
        donation.invested_amount += project_funds
        project.fully_invested = True
        project.close_date = datetime.now()
    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    return await investment(session, obj)
