# Frontend - Clarke Energia

## Requisitos

- Node.js 20+
- Docker (opcional)

## Configuração local

```bash
npm install
```

Crie um arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

## Rodar localmente

```bash
npm run dev
```

## Testes

```bash
npm run test
```

## Rodar com Docker

```bash
docker build -t clark-energia-frontend .
docker run -p 5173:80 clark-energia-frontend
```
