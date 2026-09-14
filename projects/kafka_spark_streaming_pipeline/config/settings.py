"""
Streaming Pipeline Global Configuration
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    """Production runtime configuration for Kafka, Spark, Redis, and Database."""

    # Project Information
    PROJECT_NAME: str = "Enterprise Kafka & PySpark Real-Time Streaming Platform"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Kafka Cluster Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_EVENTS: str = "telemetry_financial_events"
    KAFKA_TOPIC_DLQ: str = "telemetry_events_dlq"
    KAFKA_CONSUMER_GROUP: str = "pyspark_streaming_analytics_group"
    KAFKA_AUTO_OFFSET_RESET: str = "latest"
    KAFKA_BATCH_SIZE: int = 16384  # 16KB
    KAFKA_LINGER_MS: int = 20  # 20ms batch accumulation window
    KAFKA_COMPRESSION_TYPE: str = "snappy"

    # PySpark Streaming Configuration
    SPARK_APP_NAME: str = "RealTimeFinancialStreamAnalytics"
    SPARK_MASTER: str = "local[*]"
    SPARK_STREAM_TRIGGER_INTERVAL: str = "5 seconds"
    SPARK_WATERMARK_DELAY: str = "10 minutes"
    SPARK_WINDOW_DURATION: str = "5 minutes"
    SPARK_SLIDE_DURATION: str = "1 minute"
    SPARK_CHECKPOINT_DIR: str = "/tmp/spark_checkpoints/financial_stream"

    # PostgreSQL OLTP / Timescale Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "streaming_analytics"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres_secure_pass"

    @property
    def postgres_jdbc_url(self) -> str:
        return f"jdbc:postgresql://{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis Hot-Cache Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL_SECONDS: int = 86400  # 24 Hours

    # FastAPI Serving Gateway
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        case_sensitive=True,
    )


settings = PipelineSettings()
