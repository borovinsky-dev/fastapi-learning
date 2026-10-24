from pydantic import BaseModel, Field, field_validator


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator("wallet_name")
    @classmethod
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Wallet name cannot be empty")
        return value

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value
