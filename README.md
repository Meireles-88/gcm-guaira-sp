# Controle Geral da GCM-Guaíra-SP

## Estrutura do Projeto

### Backend (Django)
- Apps principais:
  - `ocorrencias`: Registro de ocorrências policiais
  - `pessoal`: Gestão de agentes
  - `armamento`: Controle de armamento e viaturas

### API (FastAPI)
- Módulos:
  - `emergencia`: Botão de pânico e alertas
  - `inteligencia`: Análise preditiva

## Configuração Inicial

1. Crie/atualize o arquivo `.env` na raiz com as variáveis necessárias
2. Execute `docker-compose up -d` para iniciar os containers
3. Acesse a API em http://localhost:8000

## Documentação Técnica
Consulte os ADRs em `docs/ADRs` para decisões arquiteturais.
