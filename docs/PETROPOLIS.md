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
- [ ] **Branch `main`** criada em 01/11/2026; falta a proteção dela e torná-la
      o branch padrão no GitHub (todo merge na `main` publica).

## 2. Domínio, hospedagem e e-mail

- [x] **Site no ar (22/10/2026): https://cruzvermelhapetropolis.org** — Hostinger,
      mesma conta e plano do RJ (`u448697994`), HTTPS ativo. Publicado com
      `hosting_websites_deploy-static-site-archive` a partir de `pagina/site/`
      mais as fotos de `assets/` copiadas do site do RJ (não versionadas; 22
      arquivos que o RJ também não tem ficaram de fora). A pasta
      `matricula-cursos-presenciais/api/` subiu sem `config*.php`: chat,
      cadastro de voluntários e medição respondem erro até ter configuração
      própria de Petrópolis.
- [x] Domínio trocado na página (links, canônicos, JSON-LD, sitemaps,
      `.htaccess`, cookie de consentimento). Subdomínios e e-mails do RJ
      (`doar.`, `projetocores.`, `presidente@`…) continuam com o domínio do RJ.
- [x] **Fora dos buscadores** (`robots.txt` com `Disallow: /`) enquanto o
      conteúdo for do RJ (Palácio, história, equipe). Voltar o robots antigo,
      que está comentado no próprio arquivo, quando o conteúdo for trocado.

- [ ] Domínio do site de Petrópolis (no RJ: `cruzvermelhariodejaneiro.org`,
      citado em ~100 arquivos da Redação e ~200 da `pagina/`).
- [ ] Hospedagem do site estático (no RJ: Hostinger, `public_html/`) e conta FTP
      própria para a Redação publicar notícias, sitemap e robots.
- [ ] Subdomínio da Redação (no RJ: `redacao.cruzvermelhariodejaneiro.org`).
- [ ] Domínio verificado no Resend para os envios (no RJ: `@`, `noticias.`,
      `info.`, `parceria.`), SPF/DKIM/DMARC.
- [ ] Search Console da propriedade nova.

## 3. Identidade e conteúdo

> **29/10/2026 — contatos oficiais:** e-mail contato@cruzvermelhapetropolis.org e
> telefones (21) 99605-6454 e (21) 97465-0301, no site, na Redação
> (`lib/site/juridico.ts`) e na configuração da doação. O cartão CNPJ ainda traz
> o Gmail e os fixos (24); atualizar lá também, se for o caso.

> **01/11/2026 — portal da transparência no site, com documentos de exemplo.**
> `/transparencia/` e `/canais-oficiais/` saem dos mesmos geradores que a Redação
> usa ao publicar (`lib/transparencia/paginas.ts`), rodados por
> `npx tsx scripts/gerar-transparencia-de-exemplo.ts`: cinco PDFs marcados
> "EXEMPLO" (estatuto, ata, demonstrações, relatório e CNPJ), com impressão
> digital SHA-256, sem código de verificação e com uma faixa de demonstração;
> as duas pastas ficam com `noindex` (`.htaccess`) até os documentos oficiais
> entrarem. Quando a Redação estiver no ar e a equipe enviar os documentos pela
> tela Transparência, ela grava por cima, nos mesmos endereços (apague então os
> PDFs `exemplo-*` de `public_html/transparencia/arquivos/`). Novas no gerador
> do site: `/verificar/` (confere a impressão digital no navegador, contra as
> publicadas no portal; a consulta por código abre com a trilha),
> `/pedido-de-documentos/` (pelo chat, assunto "Pedido de documento", ou
> e-mail), `/gestao/` e a seção "Como nos financiamos" em Quem somos; o menu
> ganhou "Transparência". O esqueleto das páginas da Redação
> (`lib/site/esqueleto.ts`) passou a ter o cabeçalho, o rodapé, a folha
> (`/assets/site.css?v=`, lida da home) e a medição (gtag + GTM) do site de
> Petrópolis; saíram o aviso de cookies e o Pixel da Meta do RJ.

> **01/11/2026 — revisão do nome em todo o repositório.** Nenhum texto, endereço,
> CNPJ ou nome da filial do RJ ficou no código, nos textos, nos testes e na
> documentação: domínio e e-mails passaram para `cruzvermelhapetropolis.org` (a
> Redação vai morar em `palacio.cruzvermelhapetropolis.org`, `lib/dominio.ts`),
> razão social e CNPJ para os de Petrópolis, a sede para a Rua Carlos Gomes, 6, os
> ofícios e termos para "Petrópolis, <data>" (foro da Comarca de Petrópolis), os
> feriados da biblioteca PHP para os de Petrópolis, e os anúncios do Ad Grants para
> a cidade de Petrópolis (`geoTargetConstants/1001653`). O que fica com "RJ" é o
> estado (Petrópolis/RJ, Polícia Civil do RJ, São Jorge). Saíram da `pagina/` os
> geradores, a documentação e as traduções do site do RJ (só fica
> `scripts/gerar_site_petropolis.py`) e `docs/relatorios/` (relatórios do RJ).
> As migrações antigas não podem mudar: a nova
> `20261101120000_cvrj_nomes_de_petropolis.sql`, a última da fila, troca os nomes
> do RJ que elas gravam no banco (funções, padrões de coluna, empresa principal do
> financeiro, setores e mapa do ecossistema). Os identificadores internos `cvrj_*`
> (tabelas, migrações, cookies) e `selo-cvbrj/1` ficam: não aparecem para ninguém.
> Ainda falta, quando a conta existir: verificar `noticias.`, `info.` e
> `parceria.cruzvermelhapetropolis.org` no Resend, e a página do Facebook da
> filial (o link do Facebook do RJ saiu do rodapé das páginas da Redação). O
> Instagram é `@_cruzvermelhapetropolis`: está no rodapé e no contato do site, no
> JSON-LD (`sameAs`), no e-mail de agradecimento da doação e na Redação.

> **01/11/2026 — Google Tag Manager `GTM-PDLBB439`** em todas as páginas do site,
> com o trecho oficial (o do `<head>` e o `<noscript>` logo após o `<body>`), ao
> lado do gtag do GA4. Se o contêiner também tiver uma tag do GA4 com o mesmo
> `G-MJ0DGJHLVW`, as visitas contam em dobro: deixe a medição só num dos dois.

> **01/11/2026 — Redação atualizada com o RJ** até `5c87d90` (30/10/2026):
> 47 commits, 76 arquivos — Google Ads (Ad Grants), voz (ElevenLabs),
> autocadastro de colaborador pelo WhatsApp, coordenadores de setor, fichas do
> cadastro de voluntários do site, "Esqueci minha senha" pelo WhatsApp, grupos
> do Google, backup e pg_net, com 6 migrações novas (entram pelo workflow
> **Aplicar migrações** junto com as outras). Os textos para pessoas foram
> trocados para Petrópolis. Ficaram do RJ de propósito:
> - os planos do Ad Grants (`lib/google/ads-regras.ts`): cidade do Rio, guias
>   do site do RJ e títulos no limite de 30 letras. Refazer para Petrópolis
>   antes de criar qualquer campanha;
> - as fichas do site (`lib/voluntariado/fichas-do-site.ts`) já apontam para
>   cruzvermelhapetropolis.org, mas a página de Petrópolis ainda não tem o
>   formulário de cadastro nem a API: até lá a busca não traz nada;
> - os e-mails institucionais `@cruzvermelhariodejaneiro.org` (como no resto
>   da Redação, esperando o domínio de e-mail de Petrópolis).
> A conferência `scripts/conferir-google-ads.ts` tem uma falha que também
> acontece no RJ ("a volta do Ads troca o código com o mesmo cliente": o
> texto procurado mudou na rota).

> **01/11/2026 — Google Analytics 4 `G-MJ0DGJHLVW`** em todas as páginas do
> site (gerador `pagina/scripts/gerar_site_petropolis.py`) e na Redação
> (`ID_DO_ANALYTICS` em `lib/site/analytics.ts`, para as páginas que ela
> publicar). A política de privacidade passou a citar o Analytics. Ainda é do
> RJ em `lib/site/analytics.ts`: o número da propriedade (`ID_DA_PROPRIEDADE`,
> de onde Resultados lê os números) e o Pixel da Meta.

> **29/10/2026 — chat "Fale com a gente" de volta**, o mesmo balão do RJ
> (`pagina/site/chat/`), com respostas rápidas de Petrópolis e sem cursos. A
> mensagem vai por e-mail para contato@cruzvermelhapetropolis.org (com cópia para
> quem escreveu) e fica gravada no banco da doação (`chat/api/contato.php` usa a
> biblioteca de `doe/api/nucleo/`). Testado no ar: protocolo CV-261029-0001.
> Publicação arquivo a arquivo (TUS com `?override=true`), sem apagar o
> `config.php`.

> **27/10/2026 — página refeita só com Petrópolis.** `pagina/site/` agora sai de
> `pagina/scripts/gerar_site_petropolis.py` (início, quem somos, voluntariado,
> doe, prevenção, princípios, contato, privacidade, créditos e 404), com fotos
> turísticas da cidade de licença livre (créditos em `/creditos/` e em
> `pagina/site/assets/fotos/creditos.json`). Saíram todas as páginas, fotos,
> pessoas, história, campanhas, chat, formulários e a API herdados do RJ; os
> endereços antigos levam por 301 às páginas novas (`.htaccess`). O site voltou
> a aceitar buscadores (`robots.txt` com `Allow: /` e `sitemap.xml`). Os outros
> scripts de `pagina/scripts/` e `pagina/docs/` são do site do RJ e não valem
> mais para esta página. Os itens abaixo sobre a página ficam como histórico.

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
      na FAQ e no chat; `historia/` e `en/history/`; equipe e gestão
      (pessoas e e-mails do RJ); Dia das Crianças, Campanha do Agasalho,
      Projeto Cores e base legal. Ainda há menções em texto à escola do RJ
      (O-CVB Filial Rio de Janeiro Ensino Ltda) em "Quem somos", na bio, na
      formação de voluntários, na equipe, nos termos e no reembolso.
- [x] **Notícias e escola fora da página (22/10/2026):** saíram `en/news/`
      e `traducoes/en/noticias/`, a matrícula (`matricula-cursos-presenciais/`,
      menos a pasta `api/`, que também atende o formulário de voluntários, o
      chat e a medição), `cursos.html`, `en/courses/`, `es/cursos/`, o
      `sitemap-escola.xml` e o kit `pagina/escola/`. Também os links do menu e
      do rodapé, as seções de cursos e notícias da home, os grupos de cursos da
      FAQ (pt/en/es), os assuntos de curso do chat, os 301 do `.htaccess`, as
      URLs dos sitemaps e o `llms.txt`. As notícias de Petrópolis voltam pela
      Redação, em `/noticias/`; o link "Notícias" pode voltar ao menu então.
- [ ] Os geradores de `pagina/scripts/` ainda montam a escola
      (`gerar_matricula_presencial.py` e os que dependem dele) e conferem o link
      da escola no menu: `gerar_idiomas.py` para com "o menu da home não tem o
      link da escola". Ajustar os geradores antes de regerar qualquer página.
- [ ] Contatos sem equivalente ainda: WhatsApp do voluntariado
      (21) 97036-0264, Instagram `cruzvermelhabrasileirarj` e a página do
      Facebook do RJ.
- [ ] Os geradores de `pagina/scripts/` não reproduzem byte a byte as páginas
      que estão no repositório (ex.: o 404 perde o chat). Regerar uma página
      só depois de conferir o diff.

## 4. Canais e integrações de terceiros

- [x] **Google Analytics 4 (01/11/2026):** `G-MJ0DGJHLVW` no site e na Redação.
      Falta o número da propriedade em `ID_DA_PROPRIEDADE`.
- [ ] **Meta Pixel** (e o histórico do GA4 abaixo): os do RJ (`G-HDYZZ5JZHF`,
      `2224500131617302`) estão **desligados** na página (`var GTAG = ''` e
      `var PIXEL = ''`: nada é baixado nem enviado). Com os de Petrópolis,
      voltar os endereços e trocar os IDs no `gtag('config')`/`fbq('init')`.
      O aviso de cookies ainda cita GA e Meta. Na Redação, `lib/site/analytics.ts`
      ainda tem os IDs do RJ.
- [ ] Redes sociais (Upload-Post: perfil e página do Facebook).
- [ ] WhatsApp (instância e número).
- [x] **Doações pela Unicopag (29/10/2026):** `/doe/` com PIX e cartão, mesmo
      código do RJ (`pagina/site/doe/api/`, com a biblioteca comum do checkout em
      `doe/api/nucleo/`). Banco MySQL próprio na Hostinger
      (`u448697994_doacaopetro`, a tabela `mcp_doacoes` se cria sozinha). As
      chaves (Unicopag de Petrópolis, senha do banco, e-mails) ficam **só no
      servidor**, em `public_html/doe/api/nucleo/config.php` (modelo em
      `doe/api/config.example.php`). **Atenção:** publicar com
      `deploy-static-site-archive` apaga o que não está no pacote, inclusive o
      `config.php`; depois de cada publicação assim, mande o `config.php` de
      novo (ou publique só os arquivos alterados). Sem Resend, os e-mails saem
      pelo `mail()` da Hostinger. Doação mensal desligada (como no RJ).
      `config.php` enviado ao servidor em 29/10/2026 e testado com um PIX de
      R$ 5 não pago (protocolo CVD-261029-0001): a Unicopag gerou o código e a
      doação ficou gravada no banco.
- [ ] Escola (no RJ: `escola.cursoscruzvermelha.org`) — decidir se Petrópolis
      terá escola, catálogo e matrícula próprios ou se tira essas áreas.

## 5. Documentação

- [ ] `ARQUITETURA.md`, `docs/` e `pagina/README.md` descrevem o ecossistema do
      RJ (contas, IDs, histórico). Ir reescrevendo conforme os itens acima mudam.
- [ ] `docs/COLABORAR-COM-CLAUDE-CODE.md`: trocar o nome do repositório.
