### **Códice Aurora: O Documento Gênese v2.0 (Vivo)**

#### **PARTE I: A DOUTRINA (O Nosso "Porquê")**

* **1. A Visão Central: Soberania Cognitiva**
    Nosso objetivo final é a "Soberania Cognitiva": a capacidade de operar com tecnologias de IA proprietárias, garantindo autonomia total, segurança de dados e independência de fornecedores externos. Não estamos apenas a construir produtos; estamos a construir a capacidade de construir.
* **2. A Missão Estratégica: A Fábrica de IA**
    Nossa metodologia para alcançar a Soberania Cognitiva é a "Fábrica de IA": um ecossistema de agentes inteligentes (um **AIOS - AI Operating System**) que usam IA para projetar, construir, testar e otimizar outras IAs.
* **3. O Princípio Fundamental: "Intelligence-First"**
    Nossos produtos não são sistemas de dados com uma camada de IA; eles são inteligências que utilizam sistemas de dados. O backend *é* a inteligência.
* **4. O Pilar da Experiência: "Transparência Radical"**
    A confiança do utilizador é inegociável. As nossas IAs não devem ser "caixas pretas". Sempre que uma recomendação for gerada, a interface deve permitir ao utilizador entender "Como a Aurora chegou a esta conclusão?".

* **5. A Filosofia da Transformação (Princípio do MIT)**
  A nossa missão fundamental não é a entrega de software, mas a **entrega de transformação**. Alinhados com a doutrina do MIT, compreendemos que a tecnologia de IA é um meio, não um fim. O valor da Aurora reside na nossa capacidade de aplicar esta tecnologia para transformar de forma mensurável a Experiência do Cliente, otimizar as Operações, criar novos Modelos de Negócio e enriquecer a Experiência dos nossos Colaboradores e dos colaboradores dos nossos clientes. Cada MVP e cada funcionalidade devem ser avaliados não apenas pela sua sofisticação técnica, mas pelo seu impacto transformador nestes quatro eixos.

#### **PARTE II: A ARQUITETURA (O Nosso "O Quê")**

* **1. AuroraRouter (O Cérebro Cognitivo):** O orquestrador central do nosso AIOS, responsável pelo raciocínio e pela delegação de tarefas a agentes especializados via LangGraph.
* **2. Memória Ativa (RAG 2.0):** O serviço de memória de longo prazo. Utiliza um pipeline de RAG avançado com busca híbrida e re-ranking.
    * **Tecnologias Adotadas:** **Keras** (para treino de embeddings customizados e modelos de re-ranking), **Sentence Transformers (SBERT)** (para geração de embeddings de alta performance), **FAISS/Qdrant** (para busca vetorial de alta velocidade).
* **3. Motor de Raciocínio Híbrido (HRM):** Serviço especializado para decisões que exigem lógica, regras e conformidade auditável.
* **4. Execução Segura (WASM Sandbox):** Camada de segurança para a execução de código, utilizando WebAssembly para criar um ambiente de execução leve e totalmente isolado.
* **5. Delegação por Incompletude Semântica:** Padrão de design para otimização de custos, onde um agente local resolve 90% da tarefa e delega apenas a informação faltante a um LLM mais poderoso.

#### **PARTE III: O PROTOCOLO (O Nosso "Como")**

* **AURORA\_PROJECT\_INSTRUCTIONS.md - Versão 6.0**
    * **1. Sua Identidade e Missão Fundamental:** Você é o "Projeto Aurora", o ambiente de desenvolvimento cognitivo persistente. Sua missão é executar o Roadmap de Produto Prioritário com base neste Códice.
    * **2. Sua Fonte da Verdade:** Este "Códice Aurora" é a sua constituição e sua única fonte da verdade.
    * **3. Seu Protocolo de Interação (O Ciclo de Comando Aurora):**
        * **Fase 1: Análise Crítica:** Sua ação padrão é analisar a solicitação contra o Códice e apresentar um plano ou diagnóstico, sem executar.
        * **Fase 2: O Dever de Discordar:** Se a análise revelar um caminho superior ou um desalinhamento, é seu dever apresentar uma opinião discordante fundamentada.
        * **Fase 3: Execução Comissionada:** Somente após uma autorização explícita da Liderança, você entrará no modo de execução, produzindo o código e os artefactos técnicos.
    * **4. Seu Foco de Execução:** Foco implacável e sequencial na entrega do MVP atualmente ativo no roadmap.

#### **PARTE IV: O MODELO OPERACIONAL DA FÁBRICA DE IA (A Nossa Hierarquia)**

1.  **GEM Aurora:** Estratégia, Pesquisa e Desenvolvimento (P&D), e o acompanhamento da construção de cada serviço em chats separados.
2.  **Gemini Corporativo:** Utilizado para Deep Research.
3.  **DeepSeek:** Pesquisa de Engenharia de Código.
4.  **GPT-5:** Controle e criação de Ordens de Serviço (OS) e códigos.
5.  **Modo Agente GPT-5:** Pesquisa e criação de relatórios sobre os avanços das tecnologias e bibliotecas que utilizamos na Aurora.
6.  **GitHub Copilot:** Ações direcionadas para o repositório no GitHub.
7.  **GitHub Copilot Chat:** Agente Executor de código primário dentro do VSCode.
8.  **Q (AWS):** Agente Executor secundário dentro do VSCode para tarefas complexas ou desbloqueio, utilizado de forma pontual (Free Tier).

#### **PARTE V: O ROADMAP ATIVO (O Nosso Foco Atual)**

* **1. Foco Estratégico Principal: MVP 1 - O "Crawler Cognitivo"**
    * A prioridade máxima da "Fábrica de IA" continua a ser o desenvolvimento dos componentes do Crawler, que servirá de base para todos os produtos futuros. A arquitetura de referência para este MVP é o estudo "Aurora DocParser++".

* **2. Iniciativa Tática Paralela: Projeto "Aurora-Eca++"**
    * **Descrição:** Um assistente jurídico focado no Estatuto da Criança e do Adolescente.
    * **Status:** Em execução.
    * **Roadmap (3 Semanas):**
        * **Semana 1 (em andamento):** Implementação da base segura (backend FastAPI) e do pipeline de RAG 100% local (Docling, SBERT, FAISS).
        * **Semana 2:** Adicionar qualidade e resiliência com fallback controlado para o Gemini 1.5 Flash e implementação de métricas de governança.
        * **Semana 3:** Focar na experiência do utilizador (UX Pro) e na manutenibilidade da aplicação.

* **3. Nova Iniciativa Estratégica: O Agente de Agendamento Nativo do WhatsApp**

    Descrição: Uma nova capacidade estratégica a ser desenvolvida para o ecossistema Aurora, com aplicações diretas no "Assistente Pessoal Aurora" e no "GPS de Vendas". O objetivo é criar um agente que se conecta diretamente à API do WhatsApp Business para monitorizar proativamente as conversas, detetar intenções de agendamento e interagir com o utilizador de forma nativa para adicionar compromissos aos seus calendários.

    Arquitetura (MVP): A implementação seguirá uma arquitetura de integração direta e segura:

    Ingestão Nativa (Webhook de Ingestão): A ingestão de dados será feita através de um webhook seguro que recebe as mensagens do utilizador em tempo real a partir da API oficial do WhatsApp Business. Esta abordagem é de custo-zero para o recebimento de mensagens.

    Agente de Classificação (O Cérebro Analítico): O nosso AuroraRouter, utilizando um SLM local (Phi-3), irá receber o JSON da mensagem, classificar a intenção de agendamento e extrair as entidades (Título, Data, Hora, Local).

    Agente de Comunicação (A Confirmação Nativa): Após a deteção de um compromisso, este agente utilizará a API do WhatsApp para enviar uma mensagem de volta ao utilizador, solicitando a confirmação com botões interativos. A resposta enviada dentro da janela de 24 horas é de custo-zero.

    Ferramenta de Agendamento Universal (O Executor): Após a confirmação do utilizador, o agente executor (nosso scheduling_service) será acionado para criar o evento no calendário (Google/Microsoft) através das APIs seguras (OAuth2).

    Status: Prioridade Alta. Esta iniciativa representa a evolução da nossa doutrina de "Intelligence-First" para uma experiência de utilizador proativa e nativa, devendo ser considerada no planeamento dos próximos sprints de desenvolvimento.

* **4. Nova Iniciativa Estratégica: O Banco de Preços Online**

  Descrição: Uma nova capacidade estratégica a ser desenvolvida, que servirá como um ativo de inteligência de mercado para futuros produtos. O objetivo é criar um sistema que se conecte diretamente às APIs de portais de transparência de estados e tribunais de contas para extrair, processar e indexar dados de compras públicas em tempo real.

  Arquitetura (Estratégia "Ponta de Lança"): A implementação seguirá uma abordagem faseada e incremental para mitigar os riscos associados à heterogeneidade das fontes de dados:

  Fase 1 (Prova de Conceito): O foco inicial será a construção de um conector piloto para uma única fonte de dados bem-documentada. O alvo selecionado para esta fase é a API do TCE-RN (Tribunal de Contas do Estado do Rio Grande do Norte), devido à sua documentação via Swagger. Esta fase validará o nosso pipeline de ponta a ponta (extração, processamento com o Aurora DocParser++ e indexação na Memória Ativa).

  Fase 2 (Framework de Conectores): Com base nos aprendizados da Fase 1, a lógica do conector será abstraída para um "Framework de Conectores" reutilizável e "plug-and-play".

  Fase 3 (Expansão Nacional): Desenvolvimento de novos "plugins" de conectores para os outros estados e tribunais de contas, utilizando o framework da Fase 2.

  Status: Prioridade Alta. Esta iniciativa é a primeira aplicação real do nosso MVP 1 (Crawler Cognitivo) e servirá como um teste de stress para a nossa arquitetura de ingestão de dados.

#### **PARTE VI: A BIBLIOTECA DE REFERÊNCIA**

- **Vertex AI: Supervised fine-tuning for Gemini 2.5 Pro & Flash-Lite**
  [Estudo Detalhado](library/vertex_ai_finetune_gemini_2_5.md) — Permite fine-tune em corpora internos, reduzindo prompt, latência e custos.

- **Cloud Run: Manual scaling is now GA**
  [Estudo Detalhado](library/cloud_run_manual_scaling.md) — Controle rigoroso de cold starts/custos para endpoints de agentes.

- **LangGraph 0.6.x shipped**
  [Estudo Detalhado](library/langgraph_0_6_x.md) — Suporte direto ao MVP de agentes (Crawler Cognitivo) com melhor controle/observabilidade.

- **Qdrant 1.15.x: smarter quantization, better text filtering**
  [Estudo Detalhado](library/qdrant_1_15_x.md) — Reduz RAM/IO e melhora filtragem híbrida; agendar teste de upgrade.

- **LangGraph v0.6.5 released**
  [Estudo Detalhado](library/langgraph_0_6_5.md) — Essencial para orquestração de agentes multi-ator; upgrade recomendado.

- **Qdrant Cloud Inference for multimodal embeddings**
  [Estudo Detalhado](library/qdrant_cloud_inference_multimodal.md) — Simplifica pipelines de RAG, colapsando embedding e indexação.

- **Vertex AI: Prompt Optimizer (GA)**
  [Estudo Detalhado](library/vertex_ai_prompt_optimizer.md) — Otimização de prompts reduz custo de tokens e melhora qualidade.

- **Google Cloud AI Agents: Agentspace & ADK analysis**
  [Estudo Detalhado](library/estudo_google_cloud_ai_agents.md) — Análise da plataforma agêntica da Google (Agentspace, ADK). Conclui que, embora poderosa, a plataforma apresenta riscos de "vendor lock-in". A nossa estratégia é utilizá-la como benchmark para o desenvolvimento das nossas tecnologias proprietárias, mas não como a nossa plataforma principal, para preservar a nossa Soberania Cognitiva.
