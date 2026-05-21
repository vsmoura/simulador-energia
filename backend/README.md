# Backend

Esta API entrega cotacao de energia via GraphQL e segue Clean Architecture com separacao clara de camadas.

## Stack e tecnologias
- Python 3.12+
- FastAPI (servidor HTTP)
- Strawberry GraphQL
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Pydantic Settings (configuracoes)
- PostgreSQL (producao) / SQLite (padrao local)

## Arquitetura (Clean Architecture)
Camadas principais (da mais interna para a externa):
- **Domain**: regras e tipos de negocio puros (`app/domain`)
- **Application**: casos de uso e portas (`app/application`)
- **Infrastructure**: banco, ORM, repositorios e config tecnica (`app/infrastructure`)
- **Adapters**: GraphQL e integracoes de entrada (`app/adapters`)

Regras:
- Domain nao depende de infraestrutura.
- Application depende apenas de Domain (e de portas).
- Infrastructure implementa portas e acessa recursos externos.

## Estrutura de pastas (resumo)
- `app/domain`: tipos de dominio, regras e erros
- `app/application`: services e contratos (ports)
- `app/infrastructure`: db, repositorios, config, logging
- `app/adapters/graphql`: schema, tipos e tratamento de erros
- `app/tests`: testes unitarios/integracao

## Funcionalidades
- Listagem de estados com tarifa base
- Cotacao por estado e consumo (kWh)
- Ranking de fornecedores por economia
- Health checks

### Regras de negocio (cotacao)
1) `consumption_kwh` deve ser > 0
2) Estado deve existir
3) Custo base = `consumption_kwh * base_tariff_per_kwh`
4) Cada fornecedor tem solucoes (GD e Mercado Livre) com `cost_per_kwh`
5) Economia = `base_cost - cost_total`
6) Ordena fornecedores por economia (desc)
7) Calcula melhor economia por solucao

## GraphQL
Endpoint: `http://localhost:8000/graphql`

### Queries
```graphql
query States {
  states {
    code
    name
    baseTariffPerKwh
  }
}
```

```graphql
query Quote($stateCode: String!, $consumptionKwh: Float!) {
  quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
    stateCode
    stateName
    baseTariffPerKwh
    consumptionKwh
    baseCost
    solutions {
      solutionType
      bestEconomy
      bestEconomyPercent
      suppliers {
        supplierId
        supplierName
        supplierLogoUrl
        supplierOriginState
        totalCustomers
        averageRating
        solutionType
        costPerKwh
        costTotal
        economy
        economyPercent
      }
    }
  }
}
```

### Erros
- `STATE_NOT_FOUND`
- `INVALID_CONSUMPTION`
- `UNEXPECTED_ERROR`

## Health checks
- `GET /health`
- `GET /health/db`

## Configuracao (env vars)
Prefixo: `CLARKE_`

Principais:
- `CLARKE_DATABASE_URL` (default: `sqlite:///./clark.db`)
- `CLARKE_ENVIRONMENT` (default: `development`)
- `CLARKE_APP_NAME` (default: `Clarke Energia API`)
- `CLARKE_API_VERSION` (default: `v1`)
- `CLARKE_LOG_LEVEL` (default: `INFO`)
- `CLARKE_CORS_ORIGINS` (lista; exemplo: `["http://localhost:5173"]`)

Arquivo base: `.env.example`

## Banco de dados e migrations
Criar tabelas:
```bash
python -m app.infrastructure.db.cli migrate
```

Popular dados:
```bash
python -m app.infrastructure.db.cli seed
```

## Rodando localmente
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Atalhos:
```bash
make install
make migrate
make seed
make run
```

## Docker (local)
```bash
docker compose up --build
```

O `docker-compose.yml` sobe:
- backend (porta 8000)
- frontend (porta 5173)
- postgres (porta 5432)

## Deploy no Render com Docker
1) Crie um Web Service apontando para o repo.
2) Selecione **Docker**.
3) O `Dockerfile` ja executa:
   - `alembic upgrade head`
   - `python -m app.infrastructure.db.cli seed`
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4) Defina a env var `CLARKE_DATABASE_URL` (Postgres do Render).

## Testes
```bash
pytest
