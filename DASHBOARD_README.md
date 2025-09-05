# ğŸš€ Aurora Project Dashboard

Dashboard interativo para visualizar o progresso do projeto Aurora-Core.

## ğŸ“‹ Funcionalidades

- **MÃ©tricas Gerais**: Total de tarefas, concluÃ­das, em progresso e a fazer
- **Progresso Geral**: Barra de progresso do projeto completo
- **VisualizaÃ§Ã£o por Ã‰picos**: Progresso detalhado de cada Ã©pico
- **Tabela de Tarefas**: Lista completa com status colorido
- **AtualizaÃ§Ã£o AutomÃ¡tica**: Carrega dados do `project_plan.yaml`

## ğŸš€ Como Executar

### MÃ©todo 1: Script AutomÃ¡tico

```bash
poetry run python run_dashboard.py
```

### MÃ©todo 2: Streamlit Direto

```bash
poetry run streamlit run dashboard.py
```

## ğŸŒ� Acesso

ApÃ³s executar, acesse: **http://localhost:8501**

## ğŸ“Š Dados

O dashboard lÃª automaticamente o arquivo `project_plan.yaml` na raiz do projeto.

## ğŸ�¨ Recursos Visuais

- **Cores por Status**:

  - ğŸ”´ A FAZER: Vermelho
  - ğŸŸ¢ EM PROGRESSO: Verde-Ã¡gua
  - ğŸ”µ CONCLUÃ�DO: Azul

- **MÃ©tricas em Tempo Real**
- **Barras de Progresso Interativas**
- **Layout Responsivo**

## ğŸ› ï¸� Tecnologias

- **Streamlit**: Framework web
- **Pandas**: ManipulaÃ§Ã£o de dados
- **PyYAML**: Leitura de configuraÃ§Ã£o
- **Python**: Backend
