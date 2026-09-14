"""
PySpark Structured Streaming Pipeline Job
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import logging
from ..config.settings import settings
from .sinks import write_batch_multi_sink

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s")
logger = logging.getLogger("SparkStructuredStreamJob")


def get_financial_event_spark_schema():
    """Define explicit PySpark StructType schema for zero-overhead JSON parsing."""
    from pyspark.sql.types import (
        StructType, StructField, StringType, DoubleType, TimestampType, MapType
    )

    return StructType([
        StructField("event_id", StringType(), False),
        StructField("account_id", StringType(), False),
        StructField("counterparty_id", StringType(), True),
        StructField("transaction_type", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("currency", StringType(), False),
        StructField("merchant_category", StringType(), True),
        StructField("ip_address", StringType(), True),
        StructField("geo_location", StringType(), True),
        StructField("status", StringType(), True),
        StructField("risk_score", DoubleType(), True),
        StructField("event_timestamp", TimestampType(), False),
        StructField("metadata", MapType(StringType(), StringType()), True),
    ])


def create_spark_session():
    """Build tuned SparkSession with Kafka integration packages and memory optimizations."""
    from pyspark.sql import SparkSession

    return SparkSession.builder \
        .appName(settings.SPARK_APP_NAME) \
        .master(settings.SPARK_MASTER) \
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2") \
        .getOrCreate()


def process_stream():
    """
    Main PySpark Structured Streaming Execution Graph:
    1. Read binary messages from Kafka topic.
    2. Deserialize JSON into strongly-typed columnar schema.
    3. Apply 10-minute watermarking to handle out-of-order/delayed network packets.
    4. Execute 5-minute sliding window aggregations partitioned by transaction_type.
    5. Dispatch micro-batches to dual persistent sinks (PostgreSQL & Redis).
    """
    from pyspark.sql import functions as F

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    logger.info("✓ Initialized SparkSession: %s", settings.SPARK_APP_NAME)

    schema = get_financial_event_spark_schema()

    # 1. Ingest raw Kafka Stream
    raw_kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", settings.KAFKA_TOPIC_EVENTS) \
        .option("startingOffsets", settings.KAFKA_AUTO_OFFSET_RESET) \
        .option("failOnDataLoss", "false") \
        .load()

    # 2. Parse JSON payload and cast types
    parsed_events = raw_kafka_df \
        .selectExpr("CAST(value AS STRING) as json_payload", "timestamp as kafka_arrival_time") \
        .select(F.from_json(F.col("json_payload"), schema).alias("data"), "kafka_arrival_time") \
        .select("data.*", "kafka_arrival_time")

    # 3. Watermarking & Event-Time Window Aggregation
    windowed_aggregates = parsed_events \
        .withWatermark("event_timestamp", settings.SPARK_WATERMARK_DELAY) \
        .groupBy(
            F.window("event_timestamp", settings.SPARK_WINDOW_DURATION, settings.SPARK_SLIDE_DURATION),
            F.col("transaction_type")
        ) \
        .agg(
            F.sum("amount").alias("total_volume_usd"),
            F.count("event_id").alias("transaction_count"),
            F.avg("amount").alias("avg_transaction_amount"),
            F.max("amount").alias("max_transaction_amount"),
            F.avg("risk_score").alias("avg_risk_score"),
            F.sum(F.when(F.col("risk_score") >= 0.75, 1).otherwise(0)).alias("high_risk_flag_count")
        )

    logger.info("Starting Structured Streaming Query -> Trigger: %s", settings.SPARK_STREAM_TRIGGER_INTERVAL)

    query = windowed_aggregates.writeStream \
        .foreachBatch(write_batch_multi_sink) \
        .outputMode("update") \
        .trigger(processingTime=settings.SPARK_STREAM_TRIGGER_INTERVAL) \
        .option("checkpointLocation", settings.SPARK_CHECKPOINT_DIR) \
        .start()

    return query


if __name__ == "__main__":
    try:
        streaming_query = process_stream()
        streaming_query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Gracefully stopping streaming query...")
    except Exception as e:
        logger.error("Streaming pipeline terminated with error: %s", e)
