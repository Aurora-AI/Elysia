PY := python

.PHONY: help
help:
	@echo "Targets:"
	@echo "  datajud-help                - Mostrar ajuda do conector"
	@echo "  datajud-query-sample        - Consulta por numeroProcesso (TRF1)"
	@echo "  datajud-paginate-sample     - Consulta paginada (TJDFT) via DSL"
	@echo "  datajud-normalize           - Normaliza JSON bruto -> JSONL normalizado"
	@echo "  datajud-chunk               - Gera chunks prontos para RAG (JSONL)"
	@echo "  datajud-all                 - Executa tudo: query -> normalize -> chunk"

datajud-help:
	$(PY) aurora-poc/datajud/datajud_connector_poc.py --help

datajud-query-sample:
	$(PY) aurora-poc/datajud/datajud_connector_poc.py \
	  --tribunal api_publica_trf1 \
	  --numero 00008323520184013202 \
	  --size 10 \
	  --save artifacts/trf1_00008323520184013202.json

# Cria DSL de exemplo (TJDFT) se não existir
dsl-file:
	@if [ ! -f dsl_tjdft_exec_fiscal.json ]; then \
	  echo '{ "size": 100, "query": {"bool":{"must":[{"match":{"classe.codigo":1116}},{"match":{"orgaoJulgador.codigo":13597}}]}}, "sort":[{"@timestamp":{"order":"asc"}}] }' > dsl_tjdft_exec_fiscal.json; \
	  echo "[OK] dsl_tjdft_exec_fiscal.json criado."; \
	fi

datajud-paginate-sample: dsl-file
	$(PY) aurora-poc/datajud/datajud_connector_poc.py \
	  --tribunal api_publica_tjdft \
	  --dsl-file dsl_tjdft_exec_fiscal.json \
	  --pages 2 \
	  --save artifacts/tjdft_exec_fiscal_p1p2.json

datajud-normalize:
	$(PY) aurora-poc/datajud/normalizer.py \
	  --input artifacts/trf1_00008323520184013202.json \
	  --output artifacts/normalized_trf1_00008323520184013202.jsonl
	@if [ -f artifacts/tjdft_exec_fiscal_p1p2.json ]; then \
	  $(PY) aurora-poc/datajud/normalizer.py \
	    --input artifacts/tjdft_exec_fiscal_p1p2.json \
	    --output artifacts/normalized_tjdft_exec_fiscal.jsonl; \
	fi

datajud-chunk:
	$(PY) aurora-poc/datajud/chunker.py \
	  --input artifacts/normalized_trf1_00008323520184013202.jsonl \
	  --output artifacts/chunks_trf1_00008323520184013202.jsonl \
	  --max-chars 1200 --overlap 120
	@if [ -f artifacts/normalized_tjdft_exec_fiscal.jsonl ]; then \
	  $(PY) aurora-poc/datajud/chunker.py \
	    --input artifacts/normalized_tjdft_exec_fiscal.jsonl \
	    --output artifacts/chunks_tjdft_exec_fiscal.jsonl \
	    --max-chars 1200 --overlap 120; \
	fi

datajud-all: datajud-query-sample datajud-paginate-sample datajud-normalize datajud-chunk

datajud-probe-trt9:
	$(PY) aurora-poc/datajud/datajud_connector_poc.py \
	  --tribunal api_publica_trt9 \
	  --numero 0000993-58.2022.5.09.0014 \
	  --size 1 \
	  --save artifacts/trt9_0000993-58.2022.5.09.0014.json \
	  --no-stdout
	head -n 40 artifacts/trt9_0000993-58.2022.5.09.0014.json

datajud-probe-trf1:
	$(PY) aurora-poc/datajud/datajud_connector_poc.py \
	  --tribunal api_publica_trf1 \
	  --numero 00008323520184013202 \
	  --size 1 \
	  --save artifacts/trf1_probe.json \
	  --no-stdout
	head -n 40 artifacts/trf1_probe.json
