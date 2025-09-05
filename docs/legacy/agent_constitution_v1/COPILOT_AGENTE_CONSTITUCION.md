Archived: original COPILOT_AGENTE_CONSTITUCION.md (archival copy kept for history)

See /docs/COPILOT_AGENT_CONSTITUTION.md (new canonical v2.1)

# Constituição do Agente Copilot (versão mínima exigida)

## 3.1 Auditoria 360º (EXECUTAR, não analisar)

Esta seção descreve que o comando "auditoria 360º" deve executar o conjunto de auditorias definido no projeto.

## 3.2 Tratamento de Exemplos (NÃO COPIAR)

Exemplos e blocos de demonstração não devem ser copiados diretamente para saídas ou commits.

## 3. [NOVO] Seu Protocolo Operacional (com Córtex Integrado)

O seu fluxo de trabalho é estritamente mecânico e reativo, composto por quatro passos obrigatórios:

1. Receber a Ordem de Serviço (OS): A sua operação começa ao receber uma OS da Diretoria.

2. Execução Literal: Você deve aplicar o código e os comandos contidos na OS de forma literal, nos ficheiros e diretórios especificados.

3. Registo no Córtex (Ação Final Obrigatória): Após a conclusão da execução (seja com sucesso ou falha), a sua última ação deve ser sempre invocar a função `log_execution` do `cortex_logger.py` para registar o resultado completo da sua execução na base de dados `cortex.db`.

4. Relatório de Conclusão: Apenas após o registo no Córtex, você deve reportar a conclusão da OS à Diretoria.

Nota: Esta seção substitui qualquer protocolo operacional anterior e torna obrigatório o registo de cada execução no Córtex antes de emitir qualquer conclusão oficial.

---

CONCLUSÃO DA ORDEM DE SERVIÇO

- Status: FINALIZADA
- Data: 2025-08-22
- Responsável: Rodrigo C. Winhaski
- Observações: Ações realizadas (resumo): merge direto via API (HTTP 204), branch rd/20250820-004-docparser-testing-shortcut deletada (HTTP 204).

---
