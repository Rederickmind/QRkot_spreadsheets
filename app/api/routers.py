from fastapi import APIRouter

from app.api.endpoints import (charityproject_router_v1, donation_router_v1,
                               user_router_v1)

main_router_v1 = APIRouter()
main_router_v1.include_router(
    charityproject_router_v1,
    prefix='/charity_project',
    tags=['Charity Project']
)
main_router_v1.include_router(
    donation_router_v1,
    prefix='/donation',
    tags=['Donations']
)
main_router_v1.include_router(user_router_v1)