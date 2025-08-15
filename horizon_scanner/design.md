# Design e Arquitetura – Aurora Horizon Scanner

## Visão Geral
O **Aurora Horizon Scanner** está dividido em três componentes principais:

1. **Coletor**: responsável por extrair dados de fontes variadas (papers, changelogs,
   RFCs, releases, vídeos). Deve ser modular e extensível, permitindo a inclusão
   de novas fontes de forma simples.
2. **Analisador e Prioritizador**: avalia os itens coletados, determina se são
   novidades relevantes para o ecossistema Aurora e atribui prioridades (A, B ou C)
   com base em impacto potencial no roadmap.
3. **Gerador de Relatórios e OS‑Es**: consolida as descobertas em relatórios diários e
   cria Ordens de Serviço de Estudo para itens críticos, encaminhando‑as para o time de P&D.

## Fluxo de Dados
1. O **Coletor** obtém dados brutos das fontes configuradas em `config.py`.
2. Os itens brutos são passados ao **Analisador**, que os enriquece com
   informações adicionais (por exemplo, se já existem no stack) e define a prioridade.
3. O **Gerador de Relatórios** cria um relatório diário com 5–8 descobertas mais
   relevantes e, para itens de prioridade A, elabora OS‑Es contendo escopo técnico,
   impacto esperado e plano de avaliação.

## Critérios de Priorização
- **A – Ação Imediata**: tecnologias com alto potencial de impacto direto em custos,
  latência, segurança ou que habilitam novos recursos imprescindíveis.
- **B – Observar**: inovações relevantes, mas que requerem mais maturidade ou análise antes de adoção.
- **C – Curadoria**: tendências emergentes, interessantes para acompanhamento, mas sem impacto imediato.

## Considerações Futuras
- Integração com o **Crawler Cognitivo** para reaproveitar infraestrutura de coleta.
- Implementação de cache e deduplicação para evitar análise de itens repetidos.
- Geração automática de e‑mails com OS‑Es via integrações internas.
