from __future__ import annotations
import os, json, logging, hashlib
from kafka import KafkaConsumer
from aurora_platform.modules.rag.models.rag_models import DocumentMacro
from aurora_platform.modules.rag.pipeline.rag_pipeline import ingest_document

BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOP_RES = os.getenv("KAFKA_TOPIC_CRAWL_RESULT", "aurora.crawl.result")

log = logging.getLogger("rag_ingestion_consumer")
logging.basicConfig(level=logging.INFO)

def main() -> None:
    c = KafkaConsumer(TOP_RES, bootstrap_servers=BOOT, auto_offset_reset="earliest", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
    for msg in c:
        try:
            payload = msg.value
            doc_id = hashlib.md5(payload["url"].encode()).hexdigest()
            doc = DocumentMacro(doc_id=doc_id, url=payload["url"], text=payload["body_text"], meta=payload.get("meta", {}))
            ingest_document(doc)
            log.info("Ingested doc %s len=%d", doc.url, len(doc.text))
        except Exception as e:  # noqa: BLE001
            log.exception("Error ingesting message: %s", e)

if __name__ == "__main__":
    main()