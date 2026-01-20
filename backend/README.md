# Backend - Clarke Energia

## Requisitos

- Python 3.12+
- Docker (opcional)

## Configuração local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Atalho com Makefile:

```bash
make install
```

Crie um arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

## Banco de dados e migrations

Para criar as tabelas via Alembic:

```bash
python -m app.db.cli migrate
```

Atalho com Makefile:

```bash
make migrate
```

Para popular dados de exemplo:

```bash
python -m app.db.cli seed
```

Atalho com Makefile:

```bash
make seed
```

## Rodando localmente

```bash
uvicorn app.main:app --reload --port 8000
```

Atalho com Makefile:

```bash
make run
```

## Rodando com Docker

```bash
docker compose up --build
```

## Health checks

- `GET /health`
- `GET /health/db`

## GraphQL

- Endpoint: `http://localhost:8000/graphql`

Exemplo de query:

```graphql
query {
  states {
    code
    name
    baseTariffPerKwh
  }
}
```