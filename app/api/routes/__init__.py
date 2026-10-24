from fastapi import APIRouter

from app.api.routes.operations import router as operations_router
from app.api.routes.wallets import router as wallets_router

router = APIRouter()
router.include_router(wallets_router)
router.include_router(operations_router)
