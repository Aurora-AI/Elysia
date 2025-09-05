#!/usr/bin/env python3
"""
Teste de performance batch KG - validação ordenação e throughput
"""

import time

from aurora_platform.services.kafka_producer import send_entity_upsert


def test_batch_ordering():
    """Testa ordenação local por entity_id"""
    entity_id = f"test-entity-{int(time.time())}"

    # Envia 100 eventos com mesmo entity_id
    for i in range(100):
        payload = {
            "entity_id": entity_id,
            "entity_type": "TestEntity",
            "labels": ["Test"],
            "properties": {"counter": i, "timestamp": time.time()},
        }
        send_entity_upsert(payload)

    # TODO: Verificar no Neo4j que counter = 99 (último evento)
    print(f"✅ Enviados 100 eventos para {entity_id}")


def test_batch_throughput():
    """Testa throughput em lote"""
    start_time = time.time()
    batch_size = 1000

    for i in range(batch_size):
        payload = {
            "entity_id": f"perf-test-{i}",
            "entity_type": "PerfTest",
            "labels": ["Performance"],
            "properties": {"batch_id": int(start_time), "seq": i},
        }
        send_entity_upsert(payload)

    elapsed = time.time() - start_time
    throughput = batch_size / elapsed

    print(f"✅ Throughput: {throughput:.1f} msgs/s ({batch_size} msgs em {elapsed:.2f}s)")
    assert throughput > 100  # Mínimo 100 msgs/s


if __name__ == "__main__":
    test_batch_ordering()
    test_batch_throughput()
