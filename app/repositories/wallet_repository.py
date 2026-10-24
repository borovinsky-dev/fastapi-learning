class WalletRepository:
    """Temporary in-memory storage; can later be replaced with a database."""

    def __init__(self) -> None:
        self._balances: dict[str, float] = {}

    def get_balance(self, wallet_name: str) -> float | None:
        return self._balances.get(wallet_name)

    def get_total_balance(self) -> float:
        return sum(self._balances.values())

    def create(self, wallet_name: str, initial_balance: float) -> None:
        self._balances[wallet_name] = initial_balance

    def change_balance(self, wallet_name: str, delta: float) -> float:
        self._balances[wallet_name] += delta
        return self._balances[wallet_name]
