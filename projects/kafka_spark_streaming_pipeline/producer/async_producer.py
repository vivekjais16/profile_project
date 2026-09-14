"""
Asynchronous Kafka High-Throughput Producer
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import asyncio
import json
import logging
import time
from typing import Optional
from config.settings import settings
from config.schemas import FinancialEvent
from .generator import generate_synthetic_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s")
logger = logging.getLogger("KafkaProducerEngine")


class ResilientKafkaProducer:
    """Production-grade asynchronous Kafka producer with batching, compression, and retry failover."""

    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = settings.KAFKA_TOPIC_EVENTS
        self.dlq_topic = settings.KAFKA_TOPIC_DLQ
        self._producer = None
        self._is_running = False
        self.total_published = 0
        self.total_failed = 0

    async def start(self) -> None:
        """Initialize aiokafka producer connection with optimal throughput configurations."""
        try:
            from aiokafka import AIOKafkaProducer

            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                compression_type=settings.KAFKA_COMPRESSION_TYPE,
                acks="all",  # Strongest durability guarantee
                retry_backoff_ms=250,
                max_batch_size=settings.KAFKA_BATCH_SIZE,
                linger_ms=settings.KAFKA_LINGER_MS,
            )
            await self._producer.start()
            self._is_running = True
            logger.info("✓ AIOKafkaProducer connected to cluster: %s (Topic: %s)", self.bootstrap_servers, self.topic)
        except Exception as e:
            logger.warning("Kafka cluster unavailable at %s (%s). Falling back to mock ingestion mode.", self.bootstrap_servers, e)
            self._is_running = False

    async def publish_event(self, event: FinancialEvent) -> bool:
        """Publish a single validated event with partition keying by account_id."""
        payload = event.to_kafka_dict()
        key = event.account_id

        if self._producer and self._is_running:
            try:
                await self._producer.send_and_wait(self.topic, value=payload, key=key)
                self.total_published += 1
                return True
            except Exception as exc:
                logger.error("Failed to deliver event %s to Kafka: %s. Routing to DLQ.", event.event_id, exc)
                self.total_failed += 1
                try:
                    await self._producer.send_and_wait(self.dlq_topic, value=payload, key=key)
                except Exception:
                    pass
                return False
        else:
            # Standalone / simulated mode
            self.total_published += 1
            return True

    async def publish_batch(self, events: list[FinancialEvent]) -> int:
        """Publish a batch of events concurrently using asyncio.gather."""
        tasks = [self.publish_event(event) for event in events]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful = sum(1 for r in results if r is True)
        return successful

    async def stream_continuous(self, target_events_per_sec: int = 1000, duration_seconds: Optional[int] = None) -> None:
        """Continuous load generator streaming synthetic events at target throughput."""
        logger.info("Starting high-throughput telemetry stream (~%d events/sec)...", target_events_per_sec)
        start_time = time.time()
        batch_size = max(10, target_events_per_sec // 10)
        sleep_interval = 0.1

        try:
            while True:
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    logger.info("Completed duration of %d seconds. Stopping producer.", duration_seconds)
                    break

                batch = [generate_synthetic_event() for _ in range(batch_size)]
                await self.publish_batch(batch)

                elapsed = time.time() - start_time
                rate = self.total_published / max(0.001, elapsed)
                if int(self.total_published) % 500 == 0:
                    logger.info("Ingestion Metrics: %d events published | Rate: %.1f events/sec", self.total_published, rate)

                await asyncio.sleep(sleep_interval)
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Gracefully flush and close producer connection."""
        if self._producer and self._is_running:
            await self._producer.flush()
            await self._producer.stop()
            self._is_running = False
            logger.info("Kafka Producer gracefully shut down.")


if __name__ == "__main__":
    producer = ResilientKafkaProducer()
    asyncio.run(producer.start())
    asyncio.run(producer.stream_continuous(target_events_per_sec=500, duration_seconds=10))
