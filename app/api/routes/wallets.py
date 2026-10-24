from fastapi import APIRouter

from app.schemas.wallet import CreateWalletRequest
from app.services.wallet_service import wallet_service

router = APIRouter(tags=["wallets"])


@router.get("/balance")
def get_balance(wallet_name: str | None = None) -> dict[str, str | float]:
    return wallet_service.get_balance(wallet_name)


@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest) -> dict[str, str | float]:
    return wallet_service.create_wallet(wallet)
