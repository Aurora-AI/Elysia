# 🚀 Aurora Project Dashboard

Dashboard interativo para visualizar o progresso do projeto Aurora-Core.

## 📋 Funcionalidades

- **Métricas Gerais**: Total de tarefas, concluídas, em progresso e a fazer
- **Progresso Geral**: Barra de progresso do projeto completo
- **Visualização por Épicos**: Progresso detalhado de cada épico
- **Tabela de Tarefas**: Lista completa com status colorido
- **Atualização Automática**: Carrega dados do `project_plan.yaml`

## 🚀 Como Executar

### Método 1: Script Automático
```bash
poetry run python run_dashboard.py
```

### Método 2: Streamlit Direto
```bash
poetry run streamlit run dashboard.py
```

## 🌐 Acesso

Após executar, acesse: **http://localhost:8501**

## 📊 Dados

O dashboard lê automaticamente o arquivo `project_plan.yaml` na raiz do projeto.

## 🎨 Recursos Visuais

- **Cores por Status**:
  - 🔴 A FAZER: Vermelho
  - 🟢 EM PROGRESSO: Verde-água
  - 🔵 CONCLUÍDO: Azul

- **Métricas em Tempo Real**
- **Barras de Progresso Interativas**
- **Layout Responsivo**

## 🛠️ Tecnologias

- **Streamlit**: Framework web
- **Pandas**: Manipulação de dados
- **PyYAML**: Leitura de configuração
- **Python**: Backend