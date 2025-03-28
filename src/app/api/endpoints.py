from fastapi import APIRouter, status

import app.domain.tron.views
from app.api import schemas

tron = APIRouter(prefix="/tron")
tron.include_router(app.domain.tron.views.router, prefix="/v1", tags=["Tron"])

router = APIRouter(
    responses={
        status.HTTP_403_FORBIDDEN: {"model": schemas.SimpleApiError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.SimpleApiError},
    }
)

router.include_router(tron)
