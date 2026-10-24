from fastapi import APIRouter

from app.schemas.operation import OperationRequest
from app.services.wallet_service import wallet_service

router = APIRouter(prefix="/operations", tags=["operations"])


@router.post("/income")
def add_income(operation: OperationRequest) -> dict[str, str | float | None]:
    return wallet_service.add_income(operation)


@router.post("/expense")
def add_expense(operation: OperationRequest) -> dict[str, str | float | None]:
    return wallet_service.add_expense(operation)
