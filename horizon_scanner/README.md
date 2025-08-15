# Aurora Horizon Scanner

O **Aurora Horizon Scanner** é o agente de prospecção tecnológica do ecossistema Aurora.
Sua função é monitorar diariamente novas tecnologias, frameworks, arquiteturas e técnicas
que ainda não fazem parte do stack atual, avaliando seu impacto estratégico e gerando
relatórios e Ordens de Serviço de Estudo (OS‑Es) para o time de P&D.

Este módulo contém a estrutura básica do agente, incluindo:

- `config.py`: configurações estáticas, como canais de YouTube e categorias de interesse;
- `collector.py`: funções para coletar dados de diferentes fontes (papers, changelogs, RFCs, YouTube);
- `analyzer.py`: lógica de análise e priorização das descobertas;
- `reporter.py`: geração de relatórios diários e criação de OS‑Es.

As funcionalidades ainda não estão implementadas nesta fase; servem de
base para as próximas etapas do desenvolvimento.
