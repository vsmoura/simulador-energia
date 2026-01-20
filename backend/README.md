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

Crie um arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

## Banco de dados e migrations

Para criar as tabelas via Alembic:

```bash
alembic upgrade head
```

## Rodando localmente

```bash
uvicorn app.main:app --reload --port 8000
```

## Rodando com Docker

```bash
docker compose up --build
```

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
