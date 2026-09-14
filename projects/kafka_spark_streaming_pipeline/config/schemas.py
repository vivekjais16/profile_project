"""
Pydantic Event Schemas & Serialization Contracts
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import uuid


class TransactionType(str, Enum):
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    TRADE_EXECUTION = "TRADE_EXECUTION"


class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    SETTLED = "SETTLED"
    FLAGGED_ANOMALY = "FLAGGED_ANOMALY"
    REJECTED = "REJECTED"


class FinancialEvent(BaseModel):
    """Immutable real-time telemetry/transaction event published to Kafka."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str = Field(..., description="Unique account/wallet identifier")
    counterparty_id: Optional[str] = Field(None, description="Destination account identifier")
    transaction_type: TransactionType = Field(..., description="Financial operation category")
    amount: float = Field(..., gt=0, description="Monetary value in base currency (USD)")
    currency: str = Field(default="USD", min_length=3, max_length=3)
    merchant_category: str = Field(default="GENERAL_COMMERCE")
    ip_address: str = Field(default="127.0.0.1")
    geo_location: str = Field(default="US-EAST")
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Real-time ML anomaly/fraud risk probability")
    event_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("currency")
    def uppercase_currency(cls, v: str) -> str:
        return v.upper()

    def to_kafka_dict(self) -> Dict[str, Any]:
        """Serialize event to JSON-compatible dictionary with ISO timestamp."""
        data = self.model_dump()
        data["event_timestamp"] = self.event_timestamp.isoformat()
        return data


class WindowedMetricAggregate(BaseModel):
    """Aggregated analytical metric output by PySpark Structured Streaming."""

    window_start: datetime
    window_end: datetime
    transaction_type: str
    total_volume_usd: float
    transaction_count: int
    avg_transaction_amount: float
    max_transaction_amount: float
    avg_risk_score: float
    high_risk_flag_count: int
