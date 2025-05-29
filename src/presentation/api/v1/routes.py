from fastapi import APIRouter
from src.presentation.api.v1.endpoints import (
    auth,
    user
)
router = APIRouter()
# Include the endpoints in the router
router_list = [
    auth.router,
    user.router
]
for route in router_list:
    router.include_router(route)