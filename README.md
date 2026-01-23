# Clarke Energia - Desafio Tecnico

SPA de escolha de fornecedor. O usuario seleciona o estado (UF), informa o consumo mensal (kWh) e visualiza as solucoes disponiveis (GD e/ou Mercado Livre), fornecedores e economia estimada.

## O que foi implementado
- Frontend em React com formulario de cotacao e tela de resultados.
- Backend em Python com GraphQL para consultas de estados e cotacao.
- Calculo de economia por solucao e por fornecedor.
- Seed com dados de estados, tarifas base e fornecedores (incluindo logo).
- Testes automatizados no frontend (Jest) e backend (pytest).
- Docker configurado para rodar o stack localmente.

## Requisitos atendidos
**Produto**
- Selecionar UF.
- Informar consumo mensal (kWh > 0).
- Mostrar solucoes disponiveis por estado (GD e/ou Mercado Livre).
- Mostrar fornecedores por solucao, com economia estimada.
- Informacoes do fornecedor: nome, logo, estado de origem, solucao, custo/kWh, total de clientes, avaliacao media.
- Economia por solucao e por fornecedor, com ordenacao por melhor economia.

**Tecnicos**
- Frontend em React.
- Backend em Python.
- Integracao via GraphQL.
- Testes automatizados (frontend e backend).
- Docker para execucao local.

## Regras de negocio (cotacao)
- `consumption_kwh` deve ser maior que zero.
- `custo_base = consumo_kwh * tarifa_base_kwh(estado)`.
- `custo_fornecedor = consumo_kwh * custo_kwh_fornecedor(solucao)`.
- `economia = custo_base - custo_fornecedor`.
- Resultado apresenta economia por solucao e ranking por fornecedor.

## Links de documentacao
- Backend: [`backend/README.md`](https://github.com/vsmoura/clark-energia/blob/main/backend/README.md)
- Frontend: [`frontend/README.md`](https://github.com/vsmoura/clark-energia/blob/main/frontend/README.md)

## Como rodar localmente
```bash
docker compose up --build
```

## Deploy
- Frontend: deploy automatico via Vercel.
- Backend: deploy via Render.

## Diferenciais implementados
- GraphQL
- Testes automatizados
- Docker

## Estrutura do repo
- `backend/` API + GraphQL + DB
- `frontend/` SPA React
