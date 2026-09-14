"""
High-Throughput Synthetic Financial Event Generator
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import random
import uuid
from datetime import datetime, timezone
from typing import Generator
from ..config.schemas import FinancialEvent, TransactionType, TransactionStatus

ACCOUNT_POOL = [f"ACC-{i:05d}" for i in range(1, 500)]
MERCHANT_CATEGORIES = [
    "ECOMMERCE_RETAIL",
    "FINANCIAL_SECURITIES",
    "CROSS_BORDER_REMITTANCE",
    "CLOUD_SAAS_SUBSCRIPTION",
    "CRYPTO_LIQUIDITY_POOL",
    "PEER_TO_PEER_TRANSFER",
    "POINT_OF_SALE_DINING",
]
GEO_REGIONS = ["US-EAST-1", "US-WEST-2", "EU-WEST-1", "AP-SOUTH-1", "AP-SOUTHEAST-1"]


def generate_synthetic_event() -> FinancialEvent:
    """Generate a single realistic financial transaction event with stochastic fraud/anomaly injection."""
    account_id = random.choice(ACCOUNT_POOL)
    counterparty_id = random.choice([acc for acc in ACCOUNT_POOL if acc != account_id])
    tx_type = random.choice(list(TransactionType))
    
    # 5% probability of generating high-value or anomalous transaction pattern
    is_anomaly = random.random() < 0.05
    if is_anomaly:
        amount = round(random.uniform(15000.0, 250000.0), 2)
        risk_score = round(random.uniform(0.75, 0.99), 3)
        status = TransactionStatus.FLAGGED_ANOMALY
    else:
        amount = round(random.uniform(5.0, 4500.0), 2)
        risk_score = round(random.uniform(0.01, 0.25), 3)
        status = TransactionStatus.SETTLED

    return FinancialEvent(
        event_id=str(uuid.uuid4()),
        account_id=account_id,
        counterparty_id=counterparty_id,
        transaction_type=tx_type,
        amount=amount,
        currency="USD",
        merchant_category=random.choice(MERCHANT_CATEGORIES),
        ip_address=f"{random.randint(10, 220)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
        geo_location=random.choice(GEO_REGIONS),
        status=status,
        risk_score=risk_score,
        event_timestamp=datetime.now(timezone.utc),
        metadata={
            "channel": random.choice(["MOBILE_APP", "REST_API_V2", "WEB_PORTAL", "AUTOMATED_CRON"]),
            "client_version": "v4.12.0",
        },
    )


def event_stream_generator(batch_size: int = 100) -> Generator[list[FinancialEvent], None, None]:
    """Continuous stream generator yielding batches of synthetic events."""
    while True:
        yield [generate_synthetic_event() for _ in range(batch_size)]
