from __future__ import annotations

import json
import os

from aurora_platform.modules.crawler.models.events import CrawlRequest
from kafka import KafkaProducer

BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC_CRAWL_REQUEST", "aurora.crawl.request")


def enqueue_crawl(url: str, source: str = "api") -> None:
    p = KafkaProducer(
        bootstrap_servers=BOOT, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    evt = CrawlRequest(url=url, source=source).model_dump()
    p.send(TOPIC, evt)
    p.flush()
