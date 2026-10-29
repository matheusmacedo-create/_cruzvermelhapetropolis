# Cruz Vermelha Brasileira – Petrópolis · Redação + página institucional

Repositório único da CVB Petrópolis. Junta, num lugar só, o que no Rio de Janeiro
vive em dois repositórios:

| Pasta | O que é | Onde vai rodar | Veio de |
| --- | --- | --- | --- |
| raiz (`app/`, `lib/`, `supabase/`…) | **Redação**: central de comunicação e gestão (Next.js 16 + Supabase), publica notícias no site | Vercel | `matheusmacedo-create/redacao-cruzvermelhariodejaneiro` @ `519242e` |
| [`pagina/`](./pagina) | **Página institucional**: HTML estático do site principal, scripts Python de geração e publicação, docs de SEO | Hostinger (FTP) | `matheusmacedo-create/cruzvermelhariodejaneiro` @ `d8d89d3` |

A Redação ficou na raiz para que Vercel, GitHub Actions, skills do Claude Code e
`pnpm` continuem funcionando sem ajuste. A `pagina/` fica fora do eslint, do
`tsc` e do deploy da Vercel (`.vercelignore`).

> **Ponto de partida = cópia do RJ.** O código, os textos, os canais e os domínios
> ainda são os do Rio de Janeiro. A troca para Petrópolis é feita aos poucos, à
> medida que cada canal for criado (lista em
> [`docs/PETROPOLIS.md`](./docs/PETROPOLIS.md)). O histórico de commits do RJ não
> foi trazido: este repositório começa limpo, com a origem anotada acima.

## A filial

Dados do Comprovante de Inscrição no CNPJ (emitido em 21/10/2026):

- **Razão social:** Cruz Vermelha Brasileira – Filial do Município de Petrópolis
- **Nome fantasia:** Cruz Vermelha Petrópolis
- **CNPJ:** 09.198.238/0001-48 (matriz) · situação **ativa** · aberto em 14/11/2007
- **Natureza jurídica:** 399-9 – Associação Privada
- **Atividades:** 94.99-5-00 (principal, atividades associativas) e 88.00-6-00
  (assistência social sem alojamento)
- **Endereço:** R. Carlos Gomes, 6 – Centro – Petrópolis/RJ – CEP 25680-120
- **Contato:** contato@cruzvermelhapetropolis.org · (21) 99605-6454 · (21) 97465-0301
  (no cartão CNPJ ainda constam cvbpetropolis@gmail.com · (24) 2243-4758 · (24) 3113-0074)

Logotipos (vertical e horizontal) em [`docs/identidade/`](./docs/identidade).

## Como o projeto funciona

[**ARQUITETURA.md**](./ARQUITETURA.md) explica o sistema inteiro: fluxos, banco,
integrações, convenções e as armadilhas que já custaram produção. É a leitura de
entrada para quem — pessoa ou agente — vai mexer no código.

## Colaborar com o Claude Code

Cada colaborador pode conectar o próprio Claude Code (navegador, VS Code,
Cursor, JetBrains, terminal ou Codespaces). O passo a passo — acessos, regras,
atalhos `/validar`, `/migracao`, `/entregar` e o fluxo de branch + PR — está em
[**docs/COLABORAR-COM-CLAUDE-CODE.md**](./docs/COLABORAR-COM-CLAUDE-CODE.md).

## Configuração

O app depende de um projeto Supabase (Postgres + Auth) e do Vercel Blob para
arquivos. Sem as variáveis abaixo o build passa, mas toda página quebra na
primeira query.

```bash
cp .env.example .env.local   # depois preencha SUPABASE_SERVICE_ROLE_KEY
pnpm install
pnpm dev
```

| Variável | Onde usar | Observação |
| --- | --- | --- |
| `NEXT_PUBLIC_SUPABASE_URL` | browser + server | pública, vai no bundle |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | browser + server | pública, vai no bundle |
| `SUPABASE_URL` | server | usada por `lib/supabase/admin.ts` |
| `SUPABASE_SERVICE_ROLE_KEY` | server | **segredo** — ignora RLS, nunca prefixe com `NEXT_PUBLIC_` |
| `BLOB_READ_WRITE_TOKEN` | server | Vercel Blob; sem ela os uploads em `/api/files` falham |

### Banco de dados

O schema vive em `supabase/migrations/` — 19 tabelas, RLS em todas elas e três
funções (`submit_pauta_for_approval`, `submit_content_for_approval`,
`vote_on_approval`) que as server actions chamam via `supabase.rpc`.

Para aplicar em um projeto novo:

```bash
supabase link --project-ref <ref>
supabase db push
```

Os status são gravados em inglês (`incoming`, `production`, `draft`, ...) e
traduzidos para a interface em `lib/status-maps.ts`. `lib/data.ts` é mock da
Fase 1 e não reflete o banco.

### Primeiro acesso

Com o banco vazio, a home detecta que não há nenhum perfil e abre a tela de
configuração inicial, que cria o primeiro administrador e o vincula aos espaços
de Demonstração e Produção (inseridos pela migration de seed).

## Deploy

Todo merge em `main` dispara deploy automático na Vercel. Antes do primeiro
deploy, cadastre as cinco variáveis acima em Project Settings → Environment
Variables — o build não falha sem elas, então a falta só aparece em runtime.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Learn More

To learn more, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [v0 Documentation](https://v0.app/docs) - learn about v0 and how to use it.
