# Aurora Kafka (Minimal KRaft)

Stack mínima com **1 broker Kafka (KRaft)** + **Kafka UI** para desenvolvimento Aurora.

---

## 🚀 Como usar

### 1. Subir stack
```bash
make -f Makefile.kafka kafka-up
```

### 2. Criar tópico padrão

```bash
make -f Makefile.kafka kafka-topic-create
make -f Makefile.kafka kafka-topic-list
```

### 3. Rodar consumer

```bash
make -f Makefile.kafka kafka-consumer-run
```

### 4. Produzir mensagem de teste

```bash
make -f Makefile.kafka kafka-producer-test
```

### 5. UI

* [http://localhost:8080](http://localhost:8080)

---

## 🛠 Troubleshooting

* **Erro: connection refused `localhost:9092`**
  → Confirme se stack está ativa:

  ```bash
  docker ps | grep kafka
  ```

# 📊 Aurora Kafka — Guia de Uso

## 1. Subir stack mínima
```bash
make -f Makefile.kafka kafka-up
```

UI disponível em: [http://localhost:8080](http://localhost:8080)

## 2. Subir stack persistente (com métricas)

```bash
make -f Makefile.kafka kafka-persist-up
```

* Kafka em `localhost:9092`
* Prometheus em [http://localhost:9090](http://localhost:9090)
* Grafana em [http://localhost:3000](http://localhost:3000) (login: admin / admin)

## 3. Criar tópico pilares

```bash
make -f Makefile.kafka kafka-topic-create
```

## 4. Dashboards Grafana

Importe o JSON:

```
infra/grafana/dashboards/kafka-overview.json
```

### Queries úteis (PromQL)

Mensagens/s:

```promql
sum(rate(kafka_server_brokertopicmetrics_messagesin_total{topic="pilares"}[1m]))
```

Bytes trafegados:

```promql
sum(rate(kafka_server_brokertopicmetrics_bytesin_total{topic="pilares"}[1m]))
sum(rate(kafka_server_brokertopicmetrics_bytesout_total{topic="pilares"}[1m]))
```

Latência p95:

```promql
histogram_quantile(0.95, rate(kafka_network_requestmetrics_requestqueue_time_ms_bucket[5m]))
```

### JMX exporter

We include a JMX Prometheus exporter in the persistent stack. The exporter listens on `9404` and Prometheus scrapes it. If you need to customize metrics, edit `infra/docker/jmx-exporter-config.yml`.

* JMX exporter: http://localhost:9404/metrics
