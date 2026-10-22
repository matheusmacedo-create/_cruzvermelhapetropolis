# Petrópolis: o que ainda é do RJ e precisa trocar

Este repositório nasceu em 21/10/2026 como cópia dos dois repositórios da CVB-RJ
(Redação @ `519242e` e página institucional @ `d8d89d3`). Tudo começou igual; a
lista abaixo é o roteiro para ir trocando conforme cada canal de Petrópolis for
criado. Marque o item quando o canal novo estiver no ar e o código apontar para ele.

> **Regra de ouro:** nenhum serviço de Petrópolis usa chave, banco, FTP ou conta do
> RJ. Cada um tem a sua. Credenciais vivem na Vercel / Hostinger / GitHub Secrets,
> nunca no código (ver `AGENTS.md`).

## 1. Infraestrutura (antes do primeiro deploy)

- [x] **Supabase**: projeto próprio `RedacaoCruzVermelha-Petropolis`
      (ref `eukirzqargewyarrbxht`, região São Paulo `sa-east-1`), criado em
      21/10/2026. As 5 primeiras migrações foram pelo conector do Supabase; as
      demais entram pelo workflow **Aplicar migrações** (Actions → Run
      workflow), que usa o Secret `SUPABASE_DB_URL` (Session pooler do banco
      de Petrópolis) e roda `scripts/aplicar-migracoes.sh`. Já está em `.mcp.json`. Para abrir vaga no plano
      gratuito, o projeto `puncaovenosa-fullautomatic` foi **pausado** (dá para
      reativar no painel do Supabase quando precisar).
      As sementes das migrações vieram iguais às do RJ e precisam de ajuste
      pela própria Redação: entidade financeira "Filial Rio de Janeiro" (CNPJ
      do RJ), cursos da escola e o mapa do ecossistema.
- [ ] **Vercel**: projeto novo ligado a este repositório (raiz = Redação; a
      `pagina/` já fica fora pelo `.vercelignore`). Variáveis — só os nomes, valores
      novos: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`,
      `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `FTP_HOST`, `FTP_USER`,
      `FTP_PASSWORD`, `FTP_BASE_DIR`, `SITE_PUBLIC_BASE_URL`, `RESEND_API_KEY`,
      `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `UPLOAD_POST_*`, `HUNTER_API_KEY`,
      `AUDITORIA_*`, `R2_*` (lista completa em `.env.example`).
      Os crons de `vercel.json` passam a rodar assim que o projeto existir.
- [ ] **Vercel Blob**: store próprio.
- [ ] **GitHub Actions**: o backup diário (`.github/workflows/backup-banco.yml`)
      só faz algo com os Secrets configurados neste repositório (bucket próprio).
- [ ] **Branch `main`** e proteção dela (todo merge na `main` publica).

## 2. Domínio, hospedagem e e-mail

- [ ] Domínio do site de Petrópolis (no RJ: `cruzvermelhariodejaneiro.org`,
      citado em ~100 arquivos da Redação e ~200 da `pagina/`).
- [ ] Hospedagem do site estático (no RJ: Hostinger, `public_html/`) e conta FTP
      própria para a Redação publicar notícias, sitemap e robots.
- [ ] Subdomínio da Redação (no RJ: `redacao.cruzvermelhariodejaneiro.org`).
- [ ] Domínio verificado no Resend para os envios (no RJ: `@`, `noticias.`,
      `info.`, `parceria.`), SPF/DKIM/DMARC.
- [ ] Search Console da propriedade nova.

## 3. Identidade e conteúdo

- [x] **Redação (22/10/2026):** nome da filial, CNPJ, endereço, telefone e
      e-mail (`lib/site/juridico.ts`, dados do cartão CNPJ), logo
      (`public/images/logo-cvb-petropolis.png`, encaixada na mesma grade da do
      RJ, e a cópia embutida em `lib/oficios/logo.ts`), textos de telas,
      e-mails, WhatsApp, PDFs (ofício, crachá, certificado, diploma), cartazes,
      prompts da IA e ajuda; feriados municipais de Petrópolis (16/3 e 29/6) e
      previsão do tempo na sede. O produto continua se chamando **Palácio
      Virtual**, com o selo do palácio do RJ — decidir se muda.
- [ ] Domínios e endereços: `lib/dominio.ts`, links de e-mail e do site ainda
      usam `cruzvermelhariodejaneiro.org` (esperando o domínio de Petrópolis).
- [ ] O que ainda é do RJ de propósito, até o canal existir: o Cérebro/Radar
      lê "contas oficiais do Rio"; a assinatura legal das caixas de e-mail
      (`lib/correio/mensagem.ts`) procura a linha do RJ; identificadores
      internos (`cvrj_*`, `@usuarios.cvrj.local`) ficam como estão.
- [ ] Modelos de WhatsApp: os textos mudaram ("Cruz Vermelha Petrópolis") e
      precisam ser cadastrados assim na conta da Meta de Petrópolis.
- [x] **Página (22/10/2026), identidade:** logo de Petrópolis em
      `pagina/site/assets/` (mesmos tamanhos das do RJ, versionadas até irem
      para o servidor), nome da filial em pt/en/es, endereço da sede, CEP,
      CNPJ, telefone, e-mail de contato e dados estruturados (JSON-LD) — nas
      páginas e nos geradores (`pagina/scripts/`), para não voltar ao regerar.
- [ ] **Página, conteúdo que ainda é do RJ** (precisa de texto de Petrópolis):
      o Palácio da Cruz Vermelha (1908/1919–1923) na home, em "Quem somos",
      na FAQ e no chat; `historia/` e `en/history/`; as notícias em inglês
      (`en/news/`, autoria do RJ, ficaram intactas — tirar do site);
      equipe e gestão (pessoas e e-mails do RJ); a escola e a matrícula
      (O-CVB Filial Rio de Janeiro Ensino Ltda, cursos, horários);
      Dia das Crianças, Campanha do Agasalho, Projeto Cores e base legal.
- [ ] Contatos sem equivalente ainda: WhatsApp do voluntariado
      (21) 97036-0264, Instagram `cruzvermelhabrasileirarj` e a página do
      Facebook do RJ.
- [ ] Os geradores de `pagina/scripts/` não reproduzem byte a byte as páginas
      que estão no repositório (ex.: o 404 perde o chat). Regerar uma página
      só depois de conferir o diff.

## 4. Canais e integrações de terceiros

- [ ] **Google Analytics 4**: IDs do RJ no código (`G-HDYZZ5JZHF` em ~250 lugares
      da página, `G-Z5NWV4RBTT`, `G-3JVMYP3BBS`).
- [ ] **Meta Pixel / API de Conversões**: pixel do RJ `2224500131617302` em ~84
      páginas.
- [ ] Redes sociais (Upload-Post: perfil e página do Facebook).
- [ ] WhatsApp (instância e número).
- [ ] Doações / checkout / Unicopag.
- [ ] Escola (no RJ: `escola.cursoscruzvermelha.org`) — decidir se Petrópolis
      terá escola, catálogo e matrícula próprios ou se tira essas áreas.

## 5. Documentação

- [ ] `ARQUITETURA.md`, `docs/` e `pagina/README.md` descrevem o ecossistema do
      RJ (contas, IDs, histórico). Ir reescrevendo conforme os itens acima mudam.
- [ ] `docs/COLABORAR-COM-CLAUDE-CODE.md`: trocar o nome do repositório.
