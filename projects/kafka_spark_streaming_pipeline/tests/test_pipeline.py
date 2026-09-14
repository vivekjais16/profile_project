"""
Comprehensive Unit & Integration Test Suite for Kafka Spark Pipeline
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import sys
from pathlib import Path

# Add project root to sys.path for standalone or suite test execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

try:
    from config.schemas import FinancialEvent, TransactionType, TransactionStatus
    from producer.generator import generate_synthetic_event, event_stream_generator
    from producer.async_producer import ResilientKafkaProducer
    from api.server import app
except ImportError:
    from projects.kafka_spark_streaming_pipeline.config.schemas import FinancialEvent, TransactionType, TransactionStatus
    from projects.kafka_spark_streaming_pipeline.producer.generator import generate_synthetic_event, event_stream_generator
    from projects.kafka_spark_streaming_pipeline.producer.async_producer import ResilientKafkaProducer
    from projects.kafka_spark_streaming_pipeline.api.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_financial_event_schema_validation():
    """Verify strict Pydantic validation on monetary amount and currency formatting."""
    event = FinancialEvent(
        account_id="ACC-00042",
        counterparty_id="ACC-00099",
        transaction_type=TransactionType.TRANSFER,
        amount=1450.75,
        currency="usd",
    )
    assert event.currency == "USD"
    assert event.amount == 1450.75
    assert event.status == TransactionStatus.PENDING
    assert isinstance(event.event_timestamp, datetime)

    data = event.to_kafka_dict()
    assert data["currency"] == "USD"
    assert "event_timestamp" in data


def test_synthetic_event_generator():
    """Verify stochastic event generation properties."""
    events = [generate_synthetic_event() for _ in range(50)]
    assert len(events) == 50
    for ev in events:
        assert ev.account_id.startswith("ACC-")
        assert ev.amount > 0
        assert 0.0 <= ev.risk_score <= 1.0


def test_event_stream_batch_generator():
    """Verify continuous batch stream generator."""
    gen = event_stream_generator(batch_size=25)
    batch = next(gen)
    assert len(batch) == 25
    assert isinstance(batch[0], FinancialEvent)


@pytest.mark.asyncio
async def test_resilient_producer_publish_mock():
    """Verify fallback and simulated batch ingestion."""
    producer = ResilientKafkaProducer()
    event = generate_synthetic_event()
    success = await producer.publish_event(event)
    assert success is True
    assert producer.total_published == 1

    batch = [generate_synthetic_event() for _ in range(10)]
    count = await producer.publish_batch(batch)
    assert count == 10
    assert producer.total_published == 11


def test_api_health_endpoint(client):
    """Verify API liveness check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"


def test_api_realtime_metrics_endpoint(client):
    """Verify sliding-window metrics aggregation response."""
    response = client.get("/api/v1/metrics/realtime")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert len(data["metrics"]) > 0


def test_api_dashboard_html_render(client):
    """Verify live web dashboard HTML rendering."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Kafka & PySpark Streaming Analytics Dashboard" in response.text
    assert "Vivek Jaiswal" in response.text
