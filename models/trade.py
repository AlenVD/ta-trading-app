"""Trade model for test framework."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class TradeType(Enum):
    """Trade type enumeration."""
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade:
    """Trade model representing a stock trade."""

    symbol: str
    quantity: int
    trade_type: TradeType
    price: Optional[float] = None
    total_amount: Optional[float] = None
    timestamp: Optional[datetime] = None
    fees: Optional[float] = None

    def __post_init__(self):
        """Validate trade data after initialization."""
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    def to_dict(self) -> dict:
        """Convert trade to dictionary.

        Returns:
            Dictionary representation of trade
        """
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'trade_type': self.trade_type.value,
            'price': self.price,
            'total_amount': self.total_amount,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'fees': self.fees
        }

    def __repr__(self) -> str:
        """String representation of trade."""
        return f"Trade({self.trade_type.value} {self.quantity} {self.symbol} @ ${self.price})"
