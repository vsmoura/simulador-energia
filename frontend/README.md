# Frontend

Interface web para simular economia no Mercado Livre de Energia, consumindo a API GraphQL do backend.

## Stack e tecnologias
- React + TypeScript
- Vite
- Apollo Client (GraphQL)
- React Hook Form + Zod (validacao)
- Jest + Testing Library
- CSS vanilla

## Arquitetura (Clean Architecture)
Camadas principais:
- **Domain**: tipos puros de negocio (`src/domain`)
- **Application**: casos de uso e portas (`src/application`)
- **Infrastructure**: integracoes (GraphQL/Apollo) (`src/infrastructure`)
- **Features/UI**: paginas e componentes (`src/features`, `src/app`)

Fluxo:
UI -> Application (use-cases) -> Ports -> Infrastructure (GraphQL)

## Estrutura de pastas (resumo)
- `src/app`: composicao da aplicacao (App)
- `src/domain`: tipos de dominio
- `src/application`: services/ports
- `src/infrastructure`: GraphQL client, queries e gateway
- `src/features`: UI por feature
- `src/styles`: estilos globais
- `src/tests`: testes

## Funcionalidades
- Selecionar estado e consumo mensal (kWh)
- Buscar cotacao via GraphQL
- Exibir ranking de fornecedores por economia
- Layout responsivo (mobile e desktop)

## Variaveis de ambiente
Arquivo base: `.env.example`

- `VITE_GRAPHQL_URL` (default: `http://localhost:8000/graphql`)

## Rodando localmente
```bash
npm install
npm run dev
```

## Testes
```bash
npm test
```

## Build de producao
```bash
npm run build
npm run preview
```

## Docker (local)
```bash
docker build --build-arg VITE_GRAPHQL_URL=http://localhost:8000/graphql -t clark-energia-frontend .
docker run -p 5173:80 clark-energia-frontend
http://localhost:5173/
```

## Deploy no Vercel (automatico)
O deploy e feito automaticamente a cada push para a branch principal.

1) Configure o projeto no Vercel apontando para a pasta `frontend`.
2) Build command:
   ```bash
   npm install && npm run build
   ```
3) Output directory:
   ```
   dist
   ```
4) Defina `VITE_GRAPHQL_URL` com a URL do backend publicado.
