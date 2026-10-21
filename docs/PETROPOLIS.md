# Petrópolis: o que ainda é do RJ e precisa trocar

Este repositório nasceu em 21/10/2026 como cópia dos dois repositórios da CVB-RJ
(Redação @ `519242e` e página institucional @ `d8d89d3`). Tudo começou igual; a
lista abaixo é o roteiro para ir trocando conforme cada canal de Petrópolis for
criado. Marque o item quando o canal novo estiver no ar e o código apontar para ele.

> **Regra de ouro:** nenhum serviço de Petrópolis usa chave, banco, FTP ou conta do
> RJ. Cada um tem a sua. Credenciais vivem na Vercel / Hostinger / GitHub Secrets,
> nunca no código (ver `AGENTS.md`).

## 1. Infraestrutura (antes do primeiro deploy)

- [ ] **Supabase**: projeto próprio de Petrópolis. Aplicar as migrações de
      `supabase/migrations/` em ordem num banco vazio. Depois, se quiser, pôr o
      `project_ref` novo em `.mcp.json` (foi retirado o do RJ).
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

- [ ] Nome, endereço, CNPJ, telefones e e-mail (dados no `README.md`) nos
      rodapés, JSON-LD (`NGO`), páginas de privacidade/termos/reembolso e
      e-mails transacionais.
- [ ] Logotipos (`docs/identidade/`) no lugar dos do RJ, na Redação e no site.
- [ ] Equipe, história, notícias, fotos e textos institucionais da `pagina/site/`.
- [ ] Traduções (`pagina/traducoes/`, `pagina/site/en`, `pagina/site/es`).

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
