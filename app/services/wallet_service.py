from fastapi import HTTPException

from app.repositories.wallet_repository import WalletRepository
from app.schemas.operation import OperationRequest
from app.schemas.wallet import CreateWalletRequest


class WalletService:
    def __init__(self, repository: WalletRepository) -> None:
        self.repository = repository

    def get_balance(self, wallet_name: str | None) -> dict[str, str | float]:
        if wallet_name is None:
            return {"total_balance": self.repository.get_total_balance()}

        balance = self.repository.get_balance(wallet_name)
        if balance is None:
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")
        return {"wallet": wallet_name, "balance": balance}

    def create_wallet(self, wallet: CreateWalletRequest) -> dict[str, str | float]:
        if self.repository.get_balance(wallet.name) is not None:
            raise HTTPException(status_code=400, detail=f"Wallet {wallet.name} already exists")

        self.repository.create(wallet.name, wallet.initial_balance)
        return {
            "message": f"Wallet {wallet.name} created",
            "wallet": wallet.name,
            "balance": wallet.initial_balance,
        }

    def add_income(self, operation: OperationRequest) -> dict[str, str | float | None]:
        self._ensure_wallet_exists(operation.wallet_name)
        new_balance = self.repository.change_balance(operation.wallet_name, operation.amount)
        return self._operation_result("Income added", operation, new_balance)

    def add_expense(self, operation: OperationRequest) -> dict[str, str | float | None]:
        balance = self._ensure_wallet_exists(operation.wallet_name)
        if balance < operation.amount:
            raise HTTPException(status_code=400, detail=f"Insufficient funds: {balance}")

        new_balance = self.repository.change_balance(operation.wallet_name, -operation.amount)
        return self._operation_result("Expense added", operation, new_balance)

    def _ensure_wallet_exists(self, wallet_name: str) -> float:
        balance = self.repository.get_balance(wallet_name)
        if balance is None:
            raise HTTPException(status_code=404, detail=f"{wallet_name} not found")
        return balance

    @staticmethod
    def _operation_result(
        message: str, operation: OperationRequest, new_balance: float
    ) -> dict[str, str | float | None]:
        return {
            "message": message,
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": new_balance,
        }


wallet_service = WalletService(WalletRepository())
