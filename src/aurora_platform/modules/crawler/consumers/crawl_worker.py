from __future__ import annotations
import json, os, logging
from kafka import KafkaConsumer, KafkaProducer
from aurora_platform.modules.crawler.models.events import CrawlRequest
from aurora_platform.modules.crawler.pipeline.orchestrator import run_single_crawl

BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOP_REQ = os.getenv("KAFKA_TOPIC_CRAWL_REQUEST", "aurora.crawl.request")
TOP_RES = os.getenv("KAFKA_TOPIC_CRAWL_RESULT", "aurora.crawl.result")

log = logging.getLogger("crawl_worker")
logging.basicConfig(level=logging.INFO)

def main() -> None:
    c = KafkaConsumer(TOP_REQ, bootstrap_servers=BOOT, auto_offset_reset="earliest", enable_auto_commit=True, value_deserializer=lambda m: json.loads(m.decode("utf-8")))
    p = KafkaProducer(bootstrap_servers=BOOT, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    for msg in c:
        try:
            req = CrawlRequest.model_validate(msg.value)
            res, _html = run_single_crawl(req)
            p.send(TOP_RES, res.model_dump()); p.flush()
            log.info("Crawled %s status=%s links=%d", res.url, res.status, len(res.links))
        except Exception as e:  # noqa: BLE001
            log.exception("Error processing message: %s", e)

if __name__ == "__main__":
    main()