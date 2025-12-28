"""Stock model for test framework."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Stock:
    """Stock model representing a stock position."""

    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    value: Optional[float] = None
    cost_basis: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_percentage: Optional[float] = None

    def __post_init__(self):
        """Validate stock data after initialization."""
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")

    def to_dict(self) -> dict:
        """Convert stock to dictionary.

        Returns:
            Dictionary representation of stock
        """
        return {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'value': self.value,
            'cost_basis': self.cost_basis,
            'profit_loss': self.profit_loss,
            'profit_loss_percentage': self.profit_loss_percentage
        }

    def __repr__(self) -> str:
        """String representation of stock."""
        return f"Stock({self.symbol}: {self.quantity} shares @ ${self.price})"
