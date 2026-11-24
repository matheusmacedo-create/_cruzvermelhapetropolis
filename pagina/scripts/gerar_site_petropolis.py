"""Gera o site da Cruz Vermelha Brasileira – Filial de Petrópolis em pagina/site/.

Site enxuto e só de Petrópolis (27/10/2026): nenhuma foto, pessoa, história ou dado
da filial de Petrópolis. As fotos são turísticas da cidade, de licença livre, com o
crédito em /creditos/ (lista em pagina/site/assets/fotos/creditos.json).

Uso: python3 pagina/scripts/gerar_site_petropolis.py
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SITE = RAIZ / "site"
ORIGEM = "https://cruzvermelhapetropolis.org"

FILIAL = {
    "nome": "Cruz Vermelha Brasileira – Filial do Município de Petrópolis",
    "curto": "Cruz Vermelha Petrópolis",
    "cnpj": "09.198.238/0001-48",
    "rua": "Rua Carlos Gomes, 6",
    "bairro": "Centro",
    "cidade": "Petrópolis",
    "uf": "RJ",
    "cep": "25680-120",
    "email": "contato@cruzvermelhapetropolis.org",
    "telefones": ["(21) 99605-6454", "(21) 97465-0301"],
    "instagram": "_cruzvermelhapetropolis",
}
INSTAGRAM = f"https://www.instagram.com/{FILIAL['instagram']}/"
TEL = {t: "+55" + "".join(c for c in t if c.isdigit()) for t in FILIAL["telefones"]}


def zap(telefone: str, mensagem: str = "Olá! Vim pelo site da Cruz Vermelha Petrópolis.") -> str:
    """Link do WhatsApp (os dois telefones da filial são WhatsApp), com a mensagem já escrita."""
    from urllib.parse import quote
    return f"https://wa.me/{TEL[telefone].lstrip('+')}?text={quote(mensagem)}"


def links_zap(separador: str = " · ", mensagem: str | None = None) -> str:
    return separador.join(
        f'<a href="{esc(zap(t, mensagem) if mensagem else zap(t))}" rel="noopener" target="_blank">{t}</a>' for t in FILIAL["telefones"]
    )
ENDERECO = f'{FILIAL["rua"]} · {FILIAL["bairro"]} · {FILIAL["cidade"]}/{FILIAL["uf"]} · CEP {FILIAL["cep"]}'
MAPA = "https://www.google.com/maps/search/?api=1&query=" + "Rua+Carlos+Gomes%2C+6%2C+Centro%2C+Petr%C3%B3polis+-+RJ%2C+25680-120"

FOTOS = json.loads((SITE / "assets" / "fotos" / "creditos.json").read_text(encoding="utf-8"))

# Guia das chuvas (/guia-das-chuvas/): a página é gerada sempre, mas fica fora do menu e
# dos buscadores (noindex) até sair a versão final do Plano de Contingência 2026/2027 da
# Prefeitura. Antes de virar para True, reconferir o texto na versão final do plano.
GUIA_CHUVAS_NO_AR = False

MENU = [
    ("/quem-somos/", "Quem somos"),
    ("/voluntariado/", "Voluntariado"),
    ("/prevencao/", "Prevenção"),
    *([("/guia-das-chuvas/", "Chuvas")] if GUIA_CHUVAS_NO_AR else []),
    ("/principios-fundamentais/", "Princípios"),
    ("/transparencia/", "Transparência"),
    ("/contato/", "Contato"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def foto(chave: str, classe: str = "", carregar: str = "lazy") -> str:
    f = FOTOS[chave]
    return (
        f'<img class="{classe}" src="/assets/fotos/{f["arquivo"]}" width="{f["largura"]}" height="{f["altura"]}" '
        f'alt="{esc(f["alt"])}" loading="{carregar}" decoding="async">'
    )


def legenda(chave: str) -> str:
    f = FOTOS[chave]
    return f'<figcaption>{esc(f["legenda"])} <a href="/creditos/">Foto: {esc(f["autor"])}, {esc(f["licenca"])}</a></figcaption>'


ICONES = {
    "mao": '<path d="M12 21s-7-4.4-9.3-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.3 6c-2.3 4.6-9.3 9-9.3 9z"/>',
    "pessoas": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.6"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>',
    "predio": '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6"/><path d="M4 21h16"/>',
    "chuva": '<path d="M7 15a5 5 0 1 1 1.6-9.7A6 6 0 0 1 20 9a4 4 0 0 1-1 7.9"/><path d="M9 18l-1 3M13 18l-1 3M17 18l-1 3"/>',
    "telefone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "local": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "mochila": '<rect x="5" y="7" width="14" height="14" rx="3"/><path d="M9 7V5a3 3 0 0 1 6 0v2M9 13h6"/>',
    "whatsapp": '<path d="M4 20l1.3-3.9A8 8 0 1 1 8 18.8z"/><path d="M9.5 9.5c.3 1.6 1.4 3.3 3 4.2l1.2-.9 1.8.8-.3 1.6c-3 .3-6.6-3.2-6.4-6.3l1.5-.4.9 1.7z"/>',
    "sms": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/>',
}


def icone(nome: str) -> str:
    return (
        '<svg class="icone" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONES[nome]}</svg>'
    )


def cabecalho(atual: str) -> str:
    itens = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == atual else ""}>{rotulo}</a>' for href, rotulo in MENU
    )
    return f"""<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="wrap topo-linha">
    <a class="marca" href="/" aria-label="{esc(FILIAL['curto'])}: início">
      <img src="/assets/otim/logo-cvb-petropolis-520.webp" width="520" height="156" alt="Cruz Vermelha Brasileira – Petrópolis">
    </a>
    <button class="menu-botao" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav id="menu" class="menu" aria-label="Menu principal">{itens}<a class="botao botao-vermelho" href="/doe/">Doe</a></nav>
  </div>
</header>"""


def rodape() -> str:
    tels = " · ".join(f'<a href="tel:{TEL[t]}">{t}</a>' for t in FILIAL["telefones"])
    links = "".join(f'<li><a href="{h}">{r}</a></li>' for h, r in MENU + [("/doe/", "Doe"), ("/privacidade/", "Privacidade"), ("/creditos/", "Créditos das fotos")])
    return f"""<footer class="rodape">
  <div class="wrap rodape-grade">
    <div>
      <img class="rodape-logo" src="/assets/otim/logo-cvb-petropolis-520.webp" width="520" height="156" alt="Cruz Vermelha Brasileira – Petrópolis" loading="lazy">
      <p>{esc(FILIAL['nome'])}<br>CNPJ {FILIAL['cnpj']}</p>
    </div>
    <div>
      <h2>Fale com a filial</h2>
      <p>{icone('local')} <a href="{MAPA}" rel="noopener" target="_blank">{esc(ENDERECO)}</a></p>
      <p>{icone('telefone')} {tels}</p>
      <p>{icone('whatsapp')} WhatsApp: {links_zap()}</p>
      <p>{icone('email')} <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a></p>
      <p>{icone('instagram')} Instagram: <a href="{INSTAGRAM}" rel="noopener" target="_blank">@{FILIAL['instagram']}</a></p>
    </div>
    <div>
      <h2>Navegue</h2>
      <ul>{links}</ul>
    </div>
  </div>
  <div class="wrap rodape-fim">
    <p>Em emergência: Defesa Civil <a href="tel:199">199</a> · Bombeiros <a href="tel:193">193</a> · SAMU <a href="tel:192">192</a>. A filial não faz atendimento de urgência.</p>
    <p>&copy; 2026 {esc(FILIAL['nome'])}. Parte do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho.</p>
  </div>
</footer>"""


ORGANIZACAO = {
    "@context": "https://schema.org",
    "@type": "NGO",
    "@id": ORIGEM + "/#organizacao",
    "name": FILIAL["nome"],
    "alternateName": FILIAL["curto"],
    "url": ORIGEM + "/",
    "logo": ORIGEM + "/assets/logo-cvb-petropolis.png",
    "email": FILIAL["email"],
    "telephone": [TEL[t] for t in FILIAL["telefones"]],
    "taxID": FILIAL["cnpj"],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": FILIAL["rua"],
        "addressLocality": FILIAL["cidade"],
        "addressRegion": FILIAL["uf"],
        "postalCode": FILIAL["cep"],
        "addressCountry": "BR",
    },
    "sameAs": [INSTAGRAM],
    "parentOrganization": {"@type": "NGO", "name": "Cruz Vermelha Brasileira"},
}


# Google Analytics 4 da filial (o identificador sai impresso em toda página; não é segredo).
ID_DO_ANALYTICS = "G-MJ0DGJHLVW"
# Google Tag Manager da filial (também público). O trecho é o oficial do GTM: o
# evento gtm.start é o que dispara os gatilhos de "visualização de página".
ID_DO_GTM = "GTM-PDLBB439"


def pagina(caminho: str, titulo: str, descricao: str, corpo: str, foto_social: str = "hero", extra_head: str = "", extra_fim: str = "", contato_flutuante: bool = True, classe_body: str = "") -> None:
    """contato_flutuante=False tira o botão do WhatsApp e o balão do chat (páginas de emergência:
    quem precisa de socorro liga 199/193, não escreve para a filial)."""
    url = ORIGEM + caminho
    if '/doe/' in caminho:
        classe_body = (classe_body + " pagina-doe").strip()
    chat_css = f'\n  <link rel="stylesheet" href="/chat/chat.css?v={VERSAO_CHAT_CSS}">' if contato_flutuante else ""
    chat_js = f'\n<script src="/chat/chat.js?v={VERSAO_CHAT_JS}" defer></script>' if contato_flutuante else ""
    zap_flutuante = (
        f'\n<a class="zap-flutuante" href="{esc(zap(FILIAL["telefones"][0]))}" rel="noopener" target="_blank" aria-label="Falar com a filial pelo WhatsApp">{icone("whatsapp")}<span>WhatsApp</span></a>'
        if contato_flutuante else ""
    )
    og = ORIGEM + "/assets/fotos/" + FOTOS[foto_social]["arquivo"]
    ld = json.dumps(ORGANIZACAO, ensure_ascii=False, separators=(",", ":"))
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ID_DO_ANALYTICS}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{ID_DO_ANALYTICS}');
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{ID_DO_GTM}');</script>
  <!-- End Google Tag Manager -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(titulo)}</title>
  <meta name="description" content="{esc(descricao)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="{esc(FILIAL['curto'])}">
  <meta property="og:title" content="{esc(titulo)}">
  <meta property="og:description" content="{esc(descricao)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta name="theme-color" content="#cc0000">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
  <link rel="stylesheet" href="/assets/site.css?v={VERSAO_CSS}">{chat_css}{extra_head}
  <script type="application/ld+json">{ld}</script>
</head>
<body{f' class="{classe_body}"' if classe_body else ''}>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={ID_DO_GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
{cabecalho(caminho)}
<main id="conteudo">
{corpo}
</main>
{rodape()}{zap_flutuante}
<script src="/assets/site.js?v={VERSAO_JS}" defer></script>{chat_js}{extra_fim}
</body>
</html>
"""
    destino = SITE / caminho.strip("/") / "index.html" if caminho != "/404.html" else SITE / "404.html"
    if caminho == "/":
        destino = SITE / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    print("gravado", destino.relative_to(RAIZ))


def topo_de_pagina(eyebrow: str, titulo: str, texto: str, chave_foto: str) -> str:
    return f"""<section class="faixa-foto">
  {foto(chave_foto, "faixa-foto-img", "eager")}
  <div class="wrap faixa-foto-texto">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{esc(titulo)}</h1>
    <p>{texto}</p>
  </div>
</section>"""


PRINCIPIOS = [
    ("Humanidade", "Prevenir e aliviar o sofrimento humano em todas as circunstâncias, proteger a vida e a saúde e fazer respeitar a pessoa humana, favorecendo a compreensão mútua, a amizade, a cooperação e uma paz duradoura entre os povos."),
    ("Imparcialidade", "Não fazer distinção de nacionalidade, raça, religião, condição social ou opinião política. Atender as pessoas apenas na medida das suas necessidades, dando prioridade aos casos mais urgentes."),
    ("Neutralidade", "Para manter a confiança de todos, não tomar partido nas hostilidades nem nas controvérsias de ordem política, racial, religiosa ou ideológica."),
    ("Independência", "Auxiliar os poderes públicos nas atividades humanitárias, sujeita às leis do país, mas conservando sempre a autonomia que permite agir de acordo com os Princípios."),
    ("Voluntariado", "Ser uma instituição de socorro voluntária e desinteressada, sem qualquer busca de lucro."),
    ("Unidade", "Só pode existir uma Sociedade da Cruz Vermelha ou do Crescente Vermelho em cada país, aberta a todos e com ação humanitária em todo o território."),
    ("Universalidade", "O Movimento é universal: todas as Sociedades Nacionais têm os mesmos direitos e o dever de se ajudar mutuamente."),
]


def home() -> str:
    cartoes = [
        ("pessoas", "Seja voluntário", "Dedique parte do seu tempo à ação humanitária na cidade. A filial recebe quem quer ajudar e explica como funciona.", "/voluntariado/", "Quero ser voluntário"),
        ("mao", "Doe", "Doações sustentam o trabalho da filial. Combine com a gente a melhor forma de ajudar, sempre em nome do CNPJ da filial.", "/doe/", "Como doar"),
        ("predio", "Seja parceiro", "Empresas, escolas, igrejas e associações de moradores podem somar forças em campanhas e ações de prevenção.", "/contato/", "Fale com a filial"),
    ]
    html_cartoes = "".join(
        f'<article class="cartao">{icone(i)}<h3>{t}</h3><p>{x}</p><a class="seta" href="{h}">{b}</a></article>'
        for i, t, x, h, b in cartoes
    )
    chips = "".join(f'<li><a href="/principios-fundamentais/#{p[0].lower()}">{p[0]}</a></li>' for p in PRINCIPIOS)
    tels = " · ".join(f'<a href="tel:{TEL[t]}">{t}</a>' for t in FILIAL["telefones"])
    return f"""<section class="hero">
  {foto("hero", "hero-img", "eager")}
  <div class="wrap hero-texto">
    <p class="eyebrow">Filial do Município de Petrópolis</p>
    <h1>Na serra, perto de quem precisa.</h1>
    <p>Somos a Cruz Vermelha Brasileira em Petrópolis: uma associação sem fins lucrativos, parte do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho. Nossa missão é prevenir e aliviar o sofrimento humano, com imparcialidade.</p>
    <div class="acoes">
      <a class="botao botao-vermelho" href="/voluntariado/">Seja voluntário</a>
      <a class="botao botao-branco" href="/doe/">Como doar</a>
    </div>
  </div>
  <p class="credito-hero"><a href="/creditos/">Foto: {esc(FOTOS['hero']['legenda'])}</a></p>
</section>

<section class="faixa-info" aria-label="A filial em números">
  <div class="wrap faixa-info-grade">
    <div><b>Centro</b><span>{esc(FILIAL['rua'])}, Petrópolis</span></div>
    <div><b>7</b><span>Princípios Fundamentais</span></div>
    <div><b>191</b><span>Sociedades Nacionais no mundo</span></div>
    <div><b>2007</b><span>Inscrição da filial no CNPJ</span></div>
  </div>
</section>

<section class="secao">
  <div class="wrap">
    <p class="eyebrow">Como ajudar</p>
    <h2>Petrópolis pode contar com você</h2>
    <div class="grade-3">{html_cartoes}</div>
  </div>
</section>

<section class="secao secao-suave">
  <div class="wrap duas-colunas">
    <figure class="foto-moldura">{foto("serra")}{legenda("serra")}</figure>
    <div>
      <p class="eyebrow">Prevenção</p>
      <h2>Cidade de serra, cidade preparada</h2>
      <p>Petrópolis convive com chuvas fortes no verão e com encostas que exigem atenção. Informação e preparo salvam vidas: saber para onde ir, a quem ligar e o que levar faz diferença antes, durante e depois de uma emergência.</p>
      <ul class="lista-icones">
        <li>{icone('sms')} <span>Receba alertas da Defesa Civil: envie o seu <b>CEP</b> por SMS para <b>40199</b>.</span></li>
        <li>{icone('mochila')} <span>Deixe pronta uma mochila com documentos, remédios, lanterna, água e carregador.</span></li>
        <li>{icone('telefone')} <span>Emergência: Defesa Civil <a href="tel:199">199</a>, Bombeiros <a href="tel:193">193</a>, SAMU <a href="tel:192">192</a>.</span></li>
      </ul>
      <a class="seta" href="/prevencao/">Mais orientações de prevenção</a>
    </div>
  </div>
</section>

<section class="secao">
  <div class="wrap duas-colunas invertido">
    <div>
      <p class="eyebrow">Quem somos</p>
      <h2>Parte de um movimento presente em quase todos os países</h2>
      <p>A filial de Petrópolis integra a Cruz Vermelha Brasileira, a Sociedade Nacional do Brasil no Movimento Internacional da Cruz Vermelha e do Crescente Vermelho. É uma associação privada, sem fins lucrativos, com sede no Centro da cidade.</p>
      <p>Trabalhamos com voluntários, parceiros e a comunidade, guiados pelos sete Princípios Fundamentais do Movimento.</p>
      <a class="seta" href="/quem-somos/">Conheça a filial</a>
    </div>
    <figure class="foto-moldura">{foto("imperial")}{legenda("imperial")}</figure>
  </div>
</section>

<section class="secao secao-escura">
  <div class="wrap">
    <p class="eyebrow">O que nos guia</p>
    <h2>Os sete Princípios Fundamentais</h2>
    <ul class="chips">{chips}</ul>
  </div>
</section>

<section class="secao" id="contato">
  <div class="wrap duas-colunas">
    <div>
      <p class="eyebrow">Contato</p>
      <h2>Venha nos conhecer</h2>
      <ul class="lista-icones">
        <li>{icone('local')} <span><a href="{MAPA}" rel="noopener" target="_blank">{esc(ENDERECO)}</a></span></li>
        <li>{icone('telefone')} <span>{tels}</span></li>
        <li>{icone('whatsapp')} <span>WhatsApp: {links_zap()}</span></li>
        <li>{icone('email')} <span><a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a></span></li>
      </ul>
      <a class="botao botao-vermelho" href="{MAPA}" rel="noopener" target="_blank">Ver no mapa</a>
    </div>
    <figure class="foto-moldura">{foto("cristal")}{legenda("cristal")}</figure>
  </div>
</section>"""


def quem_somos() -> str:
    return topo_de_pagina("Quem somos", "A Cruz Vermelha em Petrópolis",
        "A filial do Município de Petrópolis da Cruz Vermelha Brasileira.", "rionegro") + f"""
<section class="secao">
  <div class="wrap texto">
    <h2>A filial</h2>
    <p>A <b>{esc(FILIAL['nome'])}</b> é uma associação privada sem fins lucrativos, inscrita no CNPJ sob o nº {FILIAL['cnpj']} desde 14 de novembro de 2007, com sede na {esc(FILIAL['rua'])}, no Centro de Petrópolis.</p>
    <p>Faz parte da Cruz Vermelha Brasileira, a Sociedade Nacional do Brasil, e com ela do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho, presente em 191 países.</p>
    <h2>Nossa missão</h2>
    <blockquote>Prevenir e aliviar, com absoluta imparcialidade, os sofrimentos humanos, contribuindo para a defesa da vida, da saúde e da dignidade humana.</blockquote>
    <h2>O que fazemos</h2>
    <ul>
      <li><b>Voluntariado:</b> acolhemos e organizamos pessoas que querem dedicar tempo à ação humanitária.</li>
      <li><b>Prevenção:</b> levamos informação sobre preparo para emergências e primeiros cuidados à comunidade.</li>
      <li><b>Apoio comunitário:</b> participamos de campanhas e ações de assistência social, em parceria com a comunidade e com o poder público.</li>
    </ul>
    <h2 id="como-nos-financiamos">Como nos financiamos</h2>
    <p>A filial é uma associação sem fins lucrativos e se mantém com doações de pessoas e empresas, campanhas e parcerias. Os documentos que mostram como o dinheiro entra e é usado (estatuto, atas, demonstrações contábeis e relatórios de atividades) ficam no <a href="/transparencia/">portal da transparência</a>; o que não estiver lá pode ser pedido pelo <a href="/pedido-de-documentos/">pedido de documentos</a>.</p>
    <h2>O Movimento Internacional</h2>
    <p>O Movimento reúne três partes: o <b>Comitê Internacional da Cruz Vermelha</b> (CICV), que protege e assiste as vítimas de conflitos armados; a <b>Federação Internacional das Sociedades da Cruz Vermelha e do Crescente Vermelho</b> (FICV), que coordena a ajuda em desastres e o desenvolvimento das Sociedades Nacionais; e as <b>Sociedades Nacionais</b>, como a Cruz Vermelha Brasileira, que atuam em cada país.</p>
    <h2>O emblema</h2>
    <p>A cruz vermelha sobre fundo branco é um símbolo de proteção reconhecido internacionalmente. O seu uso é restrito por lei; quem vir o emblema usado de forma indevida pode avisar a filial pelo e-mail <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
    <p><a class="seta" href="/principios-fundamentais/">Conheça os Princípios Fundamentais</a></p>
  </div>
</section>"""


def voluntariado() -> str:
    assunto = "Quero ser voluntário da Cruz Vermelha Petrópolis"
    corpo = "Nome completo:%0D%0ATelefone ou WhatsApp:%0D%0ABairro:%0D%0ADias e horários disponíveis:%0D%0AO que gostaria de fazer:%0D%0A"
    return topo_de_pagina("Voluntariado", "Seja voluntário em Petrópolis",
        "Ajudar perto de casa, com formação e com uma equipe.", "serra") + f"""
<section class="secao">
  <div class="wrap duas-colunas">
    <div class="texto">
      <h2>Como funciona</h2>
      <p>O voluntariado da Cruz Vermelha é um trabalho não remunerado, feito por escolha própria, nos termos da Lei do Voluntariado (Lei nº 9.608/1998). Quem entra assina um termo de adesão e passa a agir de acordo com os Princípios Fundamentais do Movimento.</p>
      <ol class="passos">
        <li><b>Mande seus dados</b> pelo e-mail ou ligue para a filial.</li>
        <li><b>Converse com a equipe</b> sobre o que você gosta de fazer e quando pode ajudar.</li>
        <li><b>Receba a orientação inicial</b> sobre o Movimento, os Princípios e o trabalho da filial.</li>
        <li><b>Participe das ações</b> de acordo com a sua disponibilidade.</li>
      </ol>
    </div>
    <aside class="caixa">
      <h2>Quero participar</h2>
      <p>Envie um e-mail com nome, telefone, bairro, disponibilidade e o que gostaria de fazer.</p>
      <a class="botao botao-vermelho" href="mailto:{FILIAL['email']}?subject={assunto.replace(' ', '%20')}&amp;body={corpo}">Enviar e-mail</a>
      <a class="botao botao-zap" href="{esc(zap(FILIAL['telefones'][0], 'Olá! Quero ser voluntário da Cruz Vermelha Petrópolis.'))}" rel="noopener" target="_blank">{icone('whatsapp')} Chamar no WhatsApp</a>
      <p class="pequeno">WhatsApp ou telefone: {links_zap(mensagem='Olá! Quero ser voluntário da Cruz Vermelha Petrópolis.')}</p>
    </aside>
  </div>
</section>"""


def doe() -> str:
    valores = "".join(
        f'<button class="doe-op doe-valor" type="button" data-valor="{v}">R$ {v // 100}</button>'
        for v in (3000, 6000, 10000, 15000, 25000, 50000)
    )
    tels = " ou ".join(f'<a href="tel:{TEL[t]}">{t}</a>' for t in FILIAL["telefones"])
    return f"""<div class="doe">
<section class="doe-hero">
  <div class="wrap doe-grid doe-grid-chamada">
    <div class="doe-intro">
      <p class="eyebrow">Doe agora</p>
      <h1>Quando a emergência chega, a ajuda precisa já estar pronta.</h1>
      <p class="lead">Petrópolis conhece de perto a força das chuvas na serra. Sua doação é o que permite à Cruz Vermelha estar preparada: fomentar as ações sociais e humanitárias, investir em prevenção, socorrer a população em desastres naturais e calamidades públicas e ampliar e fortalecer o voluntariado da nossa instituição.</p>
      <p class="lead"><b>Doe hoje. Em menos de um minuto, por PIX ou cartão, e o recurso fica em Petrópolis.</b></p>
    </div>
    <div class="doe-extras">
      <ul class="doe-confianca">
        <li>{icone('predio')}<span><b>CNPJ {FILIAL['cnpj']}</b>, {esc(FILIAL['nome'])}. É o CNPJ que aparece no comprovante.</span></li>
        <li>{icone('mao')}<span><b>Pagamento em ambiente seguro</b>, processado pela Unicopag. Os dados do cartão não ficam guardados no site.</span></li>
        <li>{icone('email')}<span><b>Comprovante por e-mail</b> assim que o pagamento é confirmado.</span></li>
      </ul>
      {foto("cristal", "doe-foto")}
    </div>
    <aside class="doe-card" id="doe-card">
      <p class="doe-teste" id="doe-teste" hidden>Modo de teste: o valor cobrado não é o valor escolhido.</p>
      <div class="doe-passos" aria-hidden="true">
        <span class="doe-passo ativo"><i>1</i> Valor</span>
        <span class="doe-traco"></span>
        <span class="doe-passo"><i>2</i> Dados</span>
        <span class="doe-traco"></span>
        <span class="doe-passo"><i>3</i> Pagamento</span>
      </div>
      <form id="doe-form" novalidate>
        <div id="doe-valor">
          <div class="doe-bloco" id="doe-frequencia" hidden>
            <span class="doe-rotulo">Frequência</span>
            <div class="doe-opcoes">
              <button class="doe-op doe-freq ativo" type="button" data-freq="unica">Doação única<small>Contribua uma vez</small></button>
              <button class="doe-op doe-freq" type="button" data-freq="mensal">Mensal<small>Apoie todo mês</small></button>
            </div>
          </div>
          <div class="doe-bloco">
            <span class="doe-rotulo">Valor da doação</span>
            <div class="doe-valores">{valores}</div>
            <label class="doe-outro">
              <span>R$</span>
              <input id="doe-outro" type="text" inputmode="numeric" autocomplete="off" placeholder="Outro valor" aria-label="Outro valor em reais">
            </label>
          </div>
          <button class="btn btn-red doe-acao" type="button" id="doe-continuar" style="margin-top:20px">Continuar</button>
          <p class="doe-aviso">Conexão segura. O comprovante chega no seu e-mail assim que o pagamento é confirmado.</p>
        </div>

        <div id="doe-dados" hidden>
          <div class="doe-bloco">
            <span class="doe-rotulo">Seus dados</span>
            <label class="doe-campo"><span>Nome completo</span><input id="doe-nome" type="text" autocomplete="name" enterkeyhint="next"></label>
            <label class="doe-campo"><span>E-mail</span><input id="doe-email" type="email" autocomplete="email" inputmode="email" enterkeyhint="next"></label>
            <div class="doe-dupla">
              <label class="doe-campo"><span>CPF</span><input id="doe-cpf" type="text" inputmode="numeric" autocomplete="off" placeholder="000.000.000-00"></label>
              <label class="doe-campo"><span>Telefone</span><input id="doe-telefone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(24) 99999-9999"></label>
            </div>
          </div>
          <div class="doe-bloco">
            <span class="doe-rotulo">Forma de pagamento</span>
            <div class="doe-opcoes">
              <button class="doe-op doe-metodo ativo" type="button" data-metodo="pix">PIX<small>Confirmação na hora</small></button>
              <button class="doe-op doe-metodo" type="button" data-metodo="cartao">Cartão<small>Crédito, à vista</small></button>
            </div>
            <div class="doe-cartao-grid" id="doe-cartao" hidden style="margin-top:14px">
              <label class="doe-campo largo"><span>Número do cartão</span><input id="doe-cartao_numero" type="text" inputmode="numeric" autocomplete="cc-number" placeholder="0000 0000 0000 0000" disabled></label>
              <label class="doe-campo largo"><span>Nome como está no cartão</span><input id="doe-cartao_nome" type="text" autocomplete="cc-name" disabled></label>
              <label class="doe-campo"><span>Validade</span><input id="doe-cartao_validade" type="text" inputmode="numeric" autocomplete="cc-exp" placeholder="MM/AA" disabled></label>
              <label class="doe-campo"><span>Código de segurança</span><input id="doe-cartao_cvv" type="text" inputmode="numeric" autocomplete="cc-csc" placeholder="000" disabled></label>
            </div>
            <label class="doe-caixa" id="doe-cobre-caixa">
              <input type="checkbox" id="doe-cobre">
              <span>Quero cobrir os <b>custos de processamento</b> (<span id="doe-taxa-valor">R$ 0,00</span>) para a filial receber o valor cheio.</span>
            </label>
            <label class="doe-caixa" id="doe-anonimo-caixa">
              <input type="checkbox" id="doe-anonimo">
              <span>Quero <b>doar anonimamente</b>: meu nome não aparece em agradecimentos públicos.</span>
            </label>
            <label class="doe-caixa" id="doe-aceite-caixa">
              <input type="checkbox" id="doe-aceite">
              <span>Li e concordo com a <a href="/privacidade/" target="_blank" rel="noopener">Política de Privacidade</a> e autorizo o uso dos meus dados para processar a doação.</span>
            </label>
          </div>
          <div class="doe-resumo"><span>Total da doação</span><b class="doe-total">R$ 0,00</b></div>
          <div class="doe-armadilha" aria-hidden="true"><label>Não preencha<input id="doe-site" type="text" tabindex="-1" autocomplete="off"></label></div>
          <button class="btn btn-red doe-acao" type="submit" id="doe-enviar">Doar</button>
          <button class="doe-voltar" type="button">Voltar e mudar o valor</button>
          <p class="doe-erro" id="doe-erro" role="alert"></p>
        </div>
      </form>
      <div id="doe-pix" hidden></div>
      <div id="doe-obrigado" hidden></div>
      <noscript><p class="doe-aviso">Esta página precisa de JavaScript para gerar o pagamento. Ative o JavaScript ou escreva para {FILIAL['email']}.</p></noscript>
    </aside>
  </div>
</section>
</div>
<section class="secao">
  <div class="wrap">
    <p class="eyebrow">Para onde vai a sua doação</p>
    <h2>Cada contribuição mantém a ajuda de pé antes, durante e depois da crise</h2>
    <div class="grade-4">
      <article class="cartao">{icone('mao')}<h3>Ações sociais e humanitárias</h3><p>Apoio a famílias e comunidades em situação de vulnerabilidade, com imparcialidade e sem distinção de quem precisa.</p></article>
      <article class="cartao">{icone('sms')}<h3>Prevenção</h3><p>Informação e preparo para que cada morador saiba o que fazer, para onde ir e a quem chamar quando o risco aparece.</p></article>
      <article class="cartao">{icone('chuva')}<h3>Desastres e calamidades</h3><p>Resposta e auxílio à população atingida por chuvas, deslizamentos, enchentes e outras calamidades públicas.</p></article>
      <article class="cartao">{icone('pessoas')}<h3>Voluntariado</h3><p>Mais gente preparada para agir: acolhimento, formação e estrutura para ampliar e fortalecer o voluntariado da filial.</p></article>
    </div>
    <p class="acoes"><a class="botao botao-vermelho" href="#doe-card">Quero doar agora</a></p>
  </div>
</section>
<section class="secao secao-suave">
  <div class="wrap grade-3">
    <article class="cartao">{icone('mochila')}<h3>Doação de itens</h3><p>Antes de levar, fale com a gente: assim os itens chegam a quem precisa no momento certo e nada se perde.</p><a class="seta" href="/contato/">Fale com a filial</a></article>
    <article class="cartao">{icone('predio')}<h3>Empresas e parceiros</h3><p>Campanhas, ações de prevenção e apoio institucional. Conte o que a sua organização gostaria de fazer.</p><a class="seta" href="mailto:{FILIAL['email']}">Escrever para a filial</a></article>
    <article class="cartao">{icone('telefone')}<h3>Atenção a golpes</h3><p>A filial não pede doações por mensagem de pessoas físicas nem em contas de terceiros. Doe só por esta página ou confirme pelos telefones {tels}.</p></article>
  </div>
</section>"""


def doe_obrigado() -> str:
    return f"""<div class="doe">
<section class="doe-hero">
  <div class="wrap" style="max-width:640px">
    <aside class="doe-card" style="position:static">
      <div id="doe-valor" hidden></div>
      <div id="doe-dados" hidden></div>
      <div id="doe-pix"><p class="doe-aviso">Carregando sua doação…</p></div>
      <div id="doe-obrigado" hidden></div>
      <noscript><p class="doe-aviso">Esta página precisa de JavaScript para mostrar sua doação. Confira seu e-mail: o comprovante e o código PIX foram enviados para lá.</p></noscript>
    </aside>
    <p class="doe-aviso" style="margin-top:20px">Dúvidas sobre sua doação? Escreva para <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
  </div>
</section>
</div>"""


def prevencao() -> str:
    return topo_de_pagina("Prevenção", "Preparados para a chuva na serra",
        "Orientações simples para antes, durante e depois de uma emergência.", "serra") + """
<section class="secao">
  <div class="wrap grade-3">
    <article class="cartao"><h3>Antes</h3><ul>
      <li>Cadastre o seu CEP para alertas: envie por SMS para <b>40199</b>.</li>
      <li>Conheça o ponto de apoio mais próximo de casa e o caminho até ele.</li>
      <li>Combine com a família um ponto de encontro e um contato fora da cidade.</li>
      <li>Prepare uma mochila: documentos em saco plástico, remédios, água, lanterna, pilhas e carregador.</li>
    </ul></article>
    <article class="cartao"><h3>Durante</h3><ul>
      <li>Com alerta ou sirene, siga as orientações da Defesa Civil e saia de áreas de risco.</li>
      <li>Fique atento a rachaduras, portas emperrando, árvores inclinadas e água barrenta descendo a encosta.</li>
      <li>Não atravesse ruas ou rios alagados, a pé ou de carro.</li>
      <li>Desligue a energia e o gás se for sair de casa.</li>
    </ul></article>
    <article class="cartao"><h3>Depois</h3><ul>
      <li>Só volte para casa quando a Defesa Civil liberar.</li>
      <li>Evite contato com a água da enchente e lave bem as mãos.</li>
      <li>Cuide da sua saúde emocional e da de quem está perto: conversar ajuda.</li>
      <li>Procure informações oficiais e desconfie de boatos.</li>
    </ul></article>
  </div>
  <div class="wrap aviso">
    <p><b>Em emergência, ligue:</b> Defesa Civil <a href="tel:199">199</a> · Bombeiros <a href="tel:193">193</a> · SAMU <a href="tel:192">192</a> · Polícia Militar <a href="tel:190">190</a>.</p>
  </div>
</section>"""


# Guia das chuvas: texto fiel ao "Guia de orientação para as chuvas de verão em Petrópolis"
# (pacote "Chuvas de verão" da Comunicação Social, 06/11/2026, ajustes de 24/11/2026). As
# fontes de cada trecho ficam no original; aqui só sai o texto público. Nenhum número além
# de 199, 193, 192, 190 e do SMS 40199.
def tel(numero: str) -> str:
    return f'<a class="guia-tel" href="tel:{numero}">{numero}</a>'


GUIA_SECOES = [
    ("por-que", "1. Por que se preparar"),
    ("alertas", "2. Como receber os alertas"),
    ("risco", "3. O que muda quando o risco aumenta"),
    ("sirenes", "4. As sirenes"),
    ("nao-esperar", "5. Quando não esperar a sirene"),
    ("deslizamento", "6. Deslizamento: sinais e o que fazer"),
    ("rios", "7. Rios e ruas alagadas"),
    ("ponto-de-apoio", "8. Ponto de apoio e abrigo"),
    ("plano-da-familia", "9. O plano da família"),
    ("em-casa", "10. Em casa durante a chuva"),
    ("depois", "11. Depois da chuva"),
    ("golpes", "12. Golpes e informação falsa"),
    ("telefones", "13. Telefones e onde se informar"),
    ("cruz-vermelha", "A Cruz Vermelha e as chuvas"),
    ("fontes", "14. Fontes"),
]


def guia_chuvas() -> str:
    t199, t193, t192, t190 = tel("199"), tel("193"), tel("192"), tel("190")
    indice = "".join(f'<li><a href="#{a}">{esc(r)}</a></li>' for a, r in GUIA_SECOES)
    voltar = '<p class="guia-voltar"><a href="#indice">Voltar ao índice</a></p>'

    def secao(ancora: str, conteudo: str) -> str:
        rotulo = dict(GUIA_SECOES)[ancora]
        return f'<section class="guia-secao" id="{ancora}" aria-labelledby="{ancora}-t">\n<h2 id="{ancora}-t">{esc(rotulo)}</h2>\n{conteudo}\n{voltar}\n</section>'

    def fonte(texto: str, url: str) -> str:
        return f'<a href="{esc(url)}" rel="noopener" target="_blank">{texto}</a>'

    secoes = [
        secao("por-que", """<p>Petrópolis fica na serra, com encostas íngremes e vales estreitos. Muitas casas foram construídas nas encostas ao longo das últimas décadas. Quando chove muito, a água desce rápido, e o solo pode ceder.</p>
<p>Dezembro e janeiro costumam trazer chuva forte em toda a cidade.</p>
<p>Para este verão, o Instituto Nacional de Meteorologia (INMET) indica maior chance de chuva acima da normal em partes do Sudeste, por causa do El Niño. Isso é um motivo para se preparar, não para ter pânico.</p>
<p><b>Preparar-se é simples e funciona.</b> Este guia reúne o que a Defesa Civil e o governo federal orientam. Leia agora, com calma, e compartilhe com sua família e seus vizinhos.</p>"""),
        secao("alertas", f"""<p>Use mais de um canal. Nenhum deles substitui o olhar para o que acontece ao seu redor.</p>
<ul>
  <li><b>SMS 40199.</b> Envie o seu CEP e passe a receber os avisos da Defesa Civil de Petrópolis.</li>
  <li><b>Alerta no celular (Defesa Civil Alerta).</b> Aparece como uma janela na tela e só fecha quando você a fecha. <b>Não precisa de cadastro.</b> Funciona em celulares 4G e 5G da área do risco. Não há cobrança para receber o alerta.</li>
  <li><b>Alerta "extremo":</b> toca alto, mesmo com o celular no silencioso, e pede <b>ação imediata</b>. <b>Leia o texto do alerta e siga o que ele manda.</b></li>
  <li><b>Canais oficiais:</b> perfis da Prefeitura e da Defesa Civil, canal de WhatsApp da Defesa Civil, carros de som, rádio e apitos comunitários.</li>
  <li><b>{t199}.</b> Telefone da Defesa Civil.</li>
</ul>
<p class="guia-destaque"><b>Se o alerta manda sair, ou se você vê sinais no terreno ou o rio subindo, saia primeiro.</b> Conferir nos canais oficiais fica para depois.</p>"""),
        secao("risco", f"""<p>A Defesa Civil trabalha com avisos que ficam mais fortes conforme a chuva e o risco aumentam. Para você, isso significa:</p>
<ul>
  <li><b>Chuva forte prevista:</b> fique atento aos canais oficiais. Sirenes podem tocar o aviso de chuva forte.</li>
  <li><b>Risco de deslizamento:</b> as sirenes tocam o aviso de mobilização e a mensagem manda ir para local seguro ou ponto de apoio.</li>
  <li><b>Risco alto de alagamento ou de cheia dos rios:</b> em casa, faça o seguinte:
    <ul>
      <li><b>se a sua casa está em área de risco, saia antes de a rua alagar</b>: vá para a casa de um parente, um local seguro ou o ponto de apoio, e siga as orientações da Defesa Civil;</li>
      <li>se a Defesa Civil mandar sair, vá ao ponto de apoio, associação, igreja ou escola indicada, levando documentos, remédios e roupas;</li>
      <li>se a rua já está alagada, <b>não entre na água</b>: espere escoar ou procure outro caminho;</li>
      <li>em casa, mantenha <b>alguém da família acordado e atento</b> ao nível da água, <b>inclusive à noite</b>;</li>
      <li><b>tire os aparelhos elétricos das tomadas</b>, <b>feche os registros de gás e de água</b> e <b>recolha os animais</b>.</li>
    </ul>
  </li>
  <li><b>Emergência:</b> o atendimento é feito pelo <b>{t199}</b>.</li>
</ul>
<p>Em qualquer situação: <b>siga as orientações da Defesa Civil e mantenha a calma.</b></p>"""),
        secao("sirenes", """<p>Petrópolis tem <b>22 sirenes</b>, instaladas em áreas de risco. As sirenes são um <b>reforço</b>, e não o único aviso.</p>
<h3>Os dois toques</h3>
<ul>
  <li><b>1º toque:</b> <i>"Atenção! A Defesa Civil informa a probabilidade de chuvas moderadas a fortes nas próximas horas."</i></li>
  <li><b>2º toque:</b> <i>"A Defesa Civil de Petrópolis informa: há risco de deslizamentos nesta área. Atenção, moradores! Dirijam-se para locais seguros e pontos de apoio."</i></li>
</ul>
<p class="guia-destaque"><b>Ouviu o 2º toque? Saia agora</b> para o local seguro ou o ponto de apoio combinado, ajude quem precisa e só volte quando a Defesa Civil liberar.</p>
<p><b>A sirene pode tocar mesmo com chuva fraca ou sem chuva na sua rua.</b> Ela leva em conta a chuva dos últimos dias, que deixa o solo encharcado. <b>Vá assim mesmo.</b></p>
<p><b>Teste mensal.</b> Todo dia <b>10, às 10h</b>, as sirenes são testadas. Se estiver chovendo, o teste não é feito. <b>Se a sirene tocar no dia 10 às 10h com chuva ou com alerta, não é teste: aja como se fosse de verdade.</b></p>
<p><b>Sirene e rio.</b> No Centro, a sirene também toca quando o rio pode transbordar. <b>Se você está na rua ou num ônibus perto do rio</b>, não atravesse a água: vá para a ilha de segurança mais próxima ou para um lugar alto (<a href="#rios">seção 7</a>). <b>Se você está em casa em área de risco</b>, siga para o local seguro ou o ponto de apoio pela rota combinada, sem passar por rua alagada.</p>
<p><b>Onde não há sirene.</b> Em algumas comunidades o aviso é feito por apitos, tocados por voluntários dos Núcleos Comunitários de Defesa Civil: um sinal para sair (mobilização) e outro quando o risco passa (desmobilização). Onde não há sirene nem apito, o aviso vem pelo celular, pelo SMS 40199, por carros de som e pelos canais oficiais. A localização das sirenes está no Anexo 1 do plano de contingência.</p>"""),
        secao("nao-esperar", """<p class="guia-destaque guia-destaque-forte"><b>Os sinais no terreno e o alerta no celular podem chegar antes da sirene. Não espere por ela.</b></p>
<p><b>Saia mesmo sem sirene, sem alerta e sem ordem de ninguém se:</b></p>
<ul>
  <li>você vê <b>sinais de deslizamento</b> (<a href="#deslizamento">seção 6</a>);</li>
  <li>o <b>rio sobe depressa</b> ou a rua começa a alagar (<a href="#rios">seção 7</a>);</li>
  <li>um <b>alerta no celular manda sair</b>;</li>
  <li>a Defesa Civil, os Bombeiros ou os vizinhos mandam sair.</li>
</ul>
<p><b>Saia primeiro. Avise depois.</b></p>"""),
        secao("deslizamento", f"""<h3>Sinais de que o terreno está se movendo:</h3>
<ul>
  <li>rachaduras no chão, no piso ou nas paredes;</li>
  <li>árvores, postes ou cercas inclinados;</li>
  <li>degraus, desníveis ou fendas no terreno;</li>
  <li>o piso da casa levantando;</li>
  <li>barulhos vindos do chão, como pequenos tremores.</li>
</ul>
<h3>Se perceber qualquer um deles:</h3>
<ol>
  <li><b>Saia imediatamente de casa.</b></li>
  <li><b>Depois,</b> avise a Defesa Civil ({t199}), os Bombeiros ({t193}) e os moradores da região.</li>
  <li><b>Ajude</b> crianças, idosos e quem tem dificuldade de locomoção que estiverem perto de você.</li>
  <li>Siga as orientações da Defesa Civil.</li>
</ol>
<h3>Antes da época de chuva, na sua casa e no seu terreno:</h3>
<ul>
  <li>não jogue lixo ou entulho na encosta, nem em bueiros e córregos;</li>
  <li>não plante bananeiras na encosta, não desmate e não construa em área de risco ou sem acompanhamento técnico;</li>
  <li>evite jogar água ou esgoto no terreno;</li>
  <li>limpe as calhas e revise o telhado.</li>
</ul>
<p><b>Depois de um deslizamento:</b> não entre no local sem autorização e não volte para casa até a Defesa Civil liberar.</p>"""),
        secao("rios", """<p>Em Petrópolis, os rios podem subir <b>muito rápido</b>. No Centro, o Rio Quitandinha pode transbordar em poucos minutos depois de uma chuva forte.</p>
<h3>Quando o rio sobe ou a rua alaga:</h3>
<ul>
  <li><b>Afaste-se do rio.</b></li>
  <li><b>Nunca atravesse rua, ponte ou avenida alagada</b>, nem de carro, moto ou bicicleta. A força da água arrasta.</li>
  <li><b>Vá para um lugar alto</b> e espere a água baixar. Não pare perto de árvores e postes.</li>
  <li><b>Evite o contato com a água do alagamento.</b> Ela pode estar contaminada.</li>
  <li><b>Ajude</b> crianças, idosos e quem tem dificuldade de locomoção. <b>Garanta a segurança dos animais.</b></li>
</ul>
<p><b>Ilhas de segurança (no Centro).</b> São faixas demarcadas em ruas que cortam as vias interditadas pela cheia do Rio Quitandinha, como a Rua Dr. Nelson de Sá Earp. Ali quem está na rua pode desviar e esperar, em segurança, até o rio voltar ao leito. O mapa está no plano de contingência. Fora do Centro, procure um lugar alto.</p>
<p><b>O que você pode ver no Centro quando o rio sobe:</b> sinalizadores luminosos e cancelas que fecham as vias. Respeite. Os avisos também chegam por SMS, sirenes e pelo aplicativo Waze.</p>
<p><b>Dentro de um ônibus, se a água entrar:</b> o motorista desliga o veículo e abre as portas. Todos seguem <b>a pé para a ilha de segurança mais próxima</b>, <b>pela calçada oposta ao rio</b>, levando só o essencial (documentos e celular).</p>"""),
        secao("ponto-de-apoio", """<p>São coisas diferentes.</p>
<ul>
  <li><b>Ponto de apoio:</b> local mapeado pela Defesa Civil (escolas, creches, salões e quadras) onde a comunidade é <b>acolhida temporariamente enquanto durar o risco</b>. Quando a Defesa Civil encerra o ponto, as pessoas voltam para casa.</li>
  <li><b>Abrigo temporário:</b> espaço para quem <b>ficou desabrigado</b>, definido pela Secretaria de Assistência Social.</li>
</ul>
<p><b>Como saber qual está aberto.</b> Nem todos os pontos abrem a cada chuva. <b>Confirme pelos canais oficiais</b> da Defesa Civil. A relação dos pontos está no plano de contingência, no site da Prefeitura (Defesa Civil, Planos de Contingência). <b>Descubra o ponto mais próximo de você antes da chuva, e combine com a família o caminho e o ponto de encontro.</b></p>
<h3>O que levar (e o que fazer ao sair):</h3>
<ul>
  <li><b>documentos e objetos de valor, em saco plástico bem fechado</b>;</li>
  <li><b>remédios</b>;</li>
  <li><b>água potável</b> e <b>roupas</b>;</li>
  <li><b>lanterna e pilhas</b>. Não use vela nem lamparina: há risco de incêndio;</li>
  <li><b>animais de estimação</b>.</li>
</ul>
<p><b>Antes de sair de casa, se houver tempo</b> (no deslizamento, saia sem pegar nada): desligue os aparelhos elétricos e o quadro geral de energia, e feche os registros de água e de gás.</p>"""),
        secao("plano-da-familia", f"""<p>Monte o plano <b>hoje</b>, com todos da casa:</p>
<ul>
  <li><b>Onde vamos?</b> Casa de parentes ou amigos em lugar seguro, ou o ponto de apoio mais próximo.</li>
  <li><b>Por onde vamos?</b> Combine o caminho e um ponto de encontro.</li>
  <li><b>Quem leva o quê?</b> Deixe os documentos e os remédios juntos, em saco plástico, num lugar de fácil acesso.</li>
  <li><b>Quem ajuda quem?</b> Combine com vizinhos e familiares quem ajuda cada pessoa que precisa de apoio.</li>
</ul>
<p><b>Crianças e escola.</b> Acompanhe os canais oficiais da Prefeitura para saber se há aula. Combine com a família <b>quem busca a criança</b>, sempre sem atravessar rua alagada nem passar por encosta em risco.</p>
<p><b>Idosos e pessoas com dificuldade de locomoção.</b> Combine antes quem ajuda cada pessoa a sair e <b>saia ao primeiro aviso</b>, sem esperar o último momento. Deixe os remédios de uso contínuo separados com os documentos.</p>
<p><b>Pessoas acamadas, gestantes e pessoas com deficiência.</b> Em caso de dúvida sobre como sair ou como pedir ajuda, <b>ligue {t199} (Defesa Civil)</b>.</p>
<p><b>Animais.</b> Recolha-os e leve-os com você. Garanta a segurança deles.</p>"""),
        secao("em-casa", f"""<ul>
  <li><b>Energia.</b> Em risco de alagamento, desligue os aparelhos e o <b>quadro geral</b> (a chave geral da luz), <b>antes de a água entrar</b>. Se a água já chegou ao quadro, não toque nele. Não use equipamento elétrico que tenha molhado.</li>
  <li><b>Gás e água.</b> Feche os registros de gás e de água quando precisar sair ou quando o risco estiver alto.</li>
  <li><b>Luz.</b> Tenha lanterna e pilhas. <b>Não use vela nem lamparina.</b></li>
  <li><b>Fio caído na rua. Não se aproxime e não toque.</b> Mantenha pessoas e animais longe. Não jogue água sobre o fio e não tente movê-lo. Avise a concessionária de energia (Enel). Se alguém se machucar, ligue <b>{t193}</b> ou <b>{t192}</b>.</li>
  <li><b>Atenção ao nível da água, mesmo à noite.</b> Fique de olho em quanto a água sobe.</li>
  <li><b>Mantenha calhas e ralos limpos</b> antes da época de chuva, e avise a Prefeitura se houver bueiro entupido ou destampado.</li>
</ul>"""),
        secao("depois", f"""<h3>Voltar para casa</h3>
<ul>
  <li><b>Só volte com a liberação da Defesa Civil.</b></li>
  <li><b>Volte de dia.</b></li>
  <li>Não entre em área de deslizamento sem autorização.</li>
  <li>Procure trincas e estufamentos nas paredes. Em dúvida, ligue {t199}.</li>
</ul>
<h3>Limpeza e saúde</h3>
<ul>
  <li><b>Evite o contato com água e lama.</b> Use luvas e botas de borracha. Sem elas, use sacos plásticos duplos amarrados nas mãos e nos pés.</li>
  <li><b>Lama e lixo:</b> raspe a lama e retire o lixo.</li>
  <li><b>Alimentos:</b> jogue fora <b>todo alimento que teve contato com a água ou a lama</b>, e também os de embalagem que não é à prova d'água ou lacrada (potes, garrafas, vidros, caixas), <b>mesmo que pareçam secos</b>. Em dúvida, jogue fora. Nunca prove para testar.</li>
  <li><b>Água para beber:</b> não use água de poços ou fontes naturais depois da enchente. Se a água da torneira estiver em dúvida, <b>filtre ou coe</b> e <b>ferva por 5 minutos</b>, contados a partir do início da fervura. Deixe esfriar e guarde em recipiente limpo e tampado.</li>
  <li><b>Cuidado com entulhos:</b> podem esconder animais peçonhentos.</li>
</ul>
<p><b>Leptospirose.</b> É uma doença causada por contato com água ou lama contaminada pela urina de ratos. Procure um serviço de saúde se, nos dias seguintes ao contato com a água ou a lama da enchente, aparecerem <b>febre, dor de cabeça, dor muscular (principalmente na panturrilha), falta de apetite, náuseas ou vômitos</b>. <b>Conte ao médico que você teve contato com a água ou a lama.</b> <b>Não tome remédio por conta própria.</b></p>
<p><b>Diarreia.</b> Se tiver <b>três ou mais episódios em 24 horas</b>, procure atendimento médico.</p>
<p><b>Cuidado emocional.</b> Depois de uma enchente é comum sentir medo, tristeza e cansaço. Fale com família e amigos. Se os sinais persistirem, procure ajuda profissional.</p>"""),
        secao("golpes", f"""<ul>
  <li><b>Desconfie de mensagens não oficiais</b> nas redes sociais. Elas podem ser falsas e causar pânico, com risco de ferimentos e de morte. <b>Não repasse.</b></li>
  <li><b>Confira nos canais oficiais</b> da Defesa Civil e da Prefeitura: perfis oficiais, site, carros de som, rádio, SMS.</li>
  <li><b>O alerta oficial no celular não exige cadastro nem cobrança.</b> Cobrança em nome de operadora ou de instituição pode ser golpe.</li>
  <li><b>Doações e cadastro de atendimento:</b> o cadastro oficial de quem foi atingido é feito pela Secretaria de Assistência Social da Prefeitura. Para doar, prefira instituições conhecidas e desconfie de pedidos que chegam por mensagem. Em dúvida, ligue {t199}.</li>
</ul>"""),
        secao("telefones", """<ul class="guia-telefones">
  <li><a href="tel:199"><b>199</b><span>Defesa Civil: risco na casa, na encosta ou no rio</span></a></li>
  <li><a href="tel:193"><b>193</b><span>Corpo de Bombeiros: pessoa presa, soterrada ou ilhada</span></a></li>
  <li><a href="tel:192"><b>192</b><span>SAMU: pessoa ferida ou passando mal</span></a></li>
  <li><a href="tel:190"><b>190</b><span>Polícia Militar</span></a></li>
</ul>
<p><b>Onde se informar:</b> perfis oficiais da Prefeitura de Petrópolis e da Defesa Civil, SMS 40199 (com o seu CEP), alerta no celular (Defesa Civil Alerta), carros de som e rádio.<br>
<b>O plano de contingência</b> está no site da Prefeitura (Defesa Civil, Planos de Contingência).</p>"""),
        secao("cruz-vermelha", f"""<p>Humanidade é o primeiro princípio do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho: proteger a vida e a saúde, com atenção a quem está mais perto do perigo. Este guia existe para ajudar você, sua família e seus vizinhos a se prepararem. Em emergência, <b>o aviso e a orientação vêm da Defesa Civil: ligue {t199}.</b></p>"""),
        secao("fontes", f"""<ul class="guia-fontes">
  <li>Prefeitura de Petrópolis. <b>Plano de Contingência para Chuvas Intensas, Verão 2026/2027, versão 1</b> (aberta a contribuições). {fonte("PDF", "https://www.petropolis.rj.gov.br/pmp/index.php/downloads/105-downloads/67-defesa-civil/102-planos-de-contingencia/218-2026?download=971:plano-de-contingencia-para-chuvas-intensas-verao-2026-2027")} · {fonte("Página de planos da Defesa Civil", "https://www.petropolis.rj.gov.br/pmp/index.php/defesa-civil/planos-de-contingencia")}</li>
  <li>Ministério da Integração e do Desenvolvimento Regional (MDR). {fonte("Como agir? Deslizamento", "https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/deslizamento.pdf")}</li>
  <li>MDR. {fonte("Como agir? Alagamentos", "https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/copy2_of_ComoagirAlagamentosMDR.pdf")}</li>
  <li>MDR. {fonte("Chuvas intensas", "https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/chuvas_intensas.pdf")}</li>
  <li>MDR. {fonte("Defesa Civil Alerta", "https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/defesa-civil-alerta")}</li>
  <li>Ministério da Saúde. {fonte("Leptospirose", "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/l/leptospirose")} · {fonte("Enchentes", "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/e/enchentes")} · {fonte("Cuidados com a água", "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/e/enchentes/cuidados-com-a-agua")} · {fonte("Cuidados com os alimentos", "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/e/enchentes/cuidados-com-os-alimentos")}</li>
  <li>Enel (orientação geral da empresa). {fonte("Fios caídos após tempestades: como agir com segurança", "https://www.enel.com.br/pt-saopaulo/midia/news/d2026-2/fios-caidos-apos-tempestades-como-agir-com-seguranca.html")}</li>
  <li>INMET. {fonte("Painel El Niño, boletim de outubro", "https://portal.inmet.gov.br/noticias/painel-el-nino-boletim-de-outubro-e-divulgado")}</li>
  <li>Ministério dos Direitos Humanos e da Cidadania. {fonte("Orientação para a Pessoa Idosa em situação de riscos e desastres", "https://www.gov.br/mdh/pt-br/navegue-por-temas/pessoa-idosa/publicacoes/guia-de-orientacao-para-pessoa-idosa-em-situacao-de-riscos-e-desastres-1/GUIA.pdf")} (2024)</li>
</ul>
<p class="pequeno"><i>Este guia reúne orientações de órgãos oficiais e não substitui as instruções da Defesa Civil em uma emergência. Confira sempre os canais oficiais.</i></p>"""),
    ]

    return f"""<div class="guia">
<section class="guia-topo">
  <div class="wrap guia-largura">
    <h1>Guia de orientação para as chuvas de verão em Petrópolis</h1>
    <p class="guia-subtitulo"><b>Como se preparar, como receber os alertas e o que fazer quando a chuva é forte. Verão 2026/2027.</b></p>
    <p class="pequeno"><i>Atualizado em 06/11/2026 · base: Plano de Contingência para Chuvas Intensas 2026/2027 da Prefeitura de Petrópolis (versão 1)</i></p>
  </div>
</section>
<div class="wrap guia-largura">
<section class="guia-perigo" id="em-perigo" aria-labelledby="em-perigo-t">
  <h2 id="em-perigo-t">Em perigo, faça isto</h2>
  <ol>
    <li><b>Viu sinal de deslizamento? Saia de casa na hora. Avise depois.</b> Chame a Defesa Civil ({t199}) e os Bombeiros ({t193}) já a salvo, e avise os vizinhos.</li>
    <li><b>Não espere a sirene.</b> Os sinais no terreno e o alerta no celular podem chegar antes dela, e valem tanto quanto ela.</li>
    <li><b>Rio subindo ou rua alagada? Afaste-se do rio. Não atravesse a água.</b> Vá para um lugar alto (no Centro, para uma ilha de segurança; veja a <a href="#rios">seção 7</a>).</li>
    <li><b>Sinal de deslizamento: saia sem pegar nada.</b> Se o perigo é alagamento e ainda há tempo, leve documentos, remédios e água, desligue a chave geral da luz e feche gás e água.</li>
    <li><b>Pessoa presa, ferida ou ilhada: {t193} (Bombeiros) ou {t192} (SAMU). Risco na casa ou na encosta: {t199} (Defesa Civil).</b> Polícia: {t190}.</li>
  </ol>
</section>
<details class="guia-indice" id="indice" open>
  <summary>Índice</summary>
  <ul>{indice}</ul>
</details>
{chr(10).join(secoes)}
</div>
</div>
<aside class="guia-emergencia" aria-label="Telefones de emergência">
  <span>Emergência:</span>
  <a href="tel:199"><b>199</b> Defesa Civil</a>
  <a href="tel:193"><b>193</b> Bombeiros</a>
</aside>
<script>
  // No celular o índice começa fechado (no computador, aberto). Sem JS, fica aberto.
  if (window.matchMedia('(max-width: 760px)').matches) document.getElementById('indice').removeAttribute('open');
</script>"""


def principios() -> str:
    itens = "".join(
        f'<article class="principio" id="{n.lower()}"><span class="numero">{i}</span><div><h2>{n}</h2><p>{t}</p></div></article>'
        for i, (n, t) in enumerate(PRINCIPIOS, 1)
    )
    return topo_de_pagina("O que nos guia", "Os sete Princípios Fundamentais",
        "Proclamados em 1965, em Viena, valem para todo o Movimento Internacional da Cruz Vermelha e do Crescente Vermelho.", "rionegro") + f"""
<section class="secao">
  <div class="wrap lista-principios">{itens}</div>
</section>"""


def contato() -> str:
    tels = "<br>".join(f'<a href="tel:{TEL[t]}">{t}</a>' for t in FILIAL["telefones"])
    return topo_de_pagina("Contato", "Fale com a filial",
        "Estamos no Centro de Petrópolis.", "imperial") + f"""
<section class="secao">
  <div class="wrap grade-3">
    <article class="cartao">{icone('local')}<h3>Endereço</h3><p>{esc(FILIAL['rua'])}<br>{FILIAL['bairro']} · {FILIAL['cidade']}/{FILIAL['uf']}<br>CEP {FILIAL['cep']}</p><a class="seta" href="{MAPA}" rel="noopener" target="_blank">Abrir no mapa</a></article>
    <article class="cartao">{icone('whatsapp')}<h3>WhatsApp e telefone</h3><p>{tels}</p><p>{"".join(f'<a class="botao botao-zap botao-pequeno" href="{esc(zap(t))}" rel="noopener" target="_blank">WhatsApp {t}</a>' for t in FILIAL["telefones"])}</p></article>
    <article class="cartao">{icone('email')}<h3>E-mail, chat e Instagram</h3><p><a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a><br>Instagram: <a href="{INSTAGRAM}" rel="noopener" target="_blank">@{FILIAL['instagram']}</a></p><p><button class="botao botao-vermelho botao-pequeno" type="button" data-abrir-chat>Escrever pelo chat</button></p></article>
  </div>
  <div class="wrap aviso"><p>A filial não faz atendimento de urgência. Em emergência: Defesa Civil <a href="tel:199">199</a> · Bombeiros <a href="tel:193">193</a> · SAMU <a href="tel:192">192</a>.</p></div>
</section>"""


def privacidade() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Privacidade</p>
<h1>Política de privacidade</h1>
<p>Este site é mantido pela {esc(FILIAL['nome'])}, CNPJ {FILIAL['cnpj']}, {esc(ENDERECO)}.</p>
<h2>O que coletamos</h2>
<p>Usamos o Google Analytics, pelo Google Tag Manager, para saber quantas pessoas visitam o site e quais páginas leem. Ele grava cookies no seu navegador e recebe dados do acesso (páginas vistas, aparelho, navegador e região aproximada), sem nome nem contato; os números servem só para melhorar o site. Você pode bloquear esses cookies nas configurações do navegador. O site não usa cookies de publicidade. Os contatos são feitos por e-mail ou telefone, por iniciativa de quem nos procura. As fontes de texto vêm do Google Fonts, que recebe o endereço IP do seu acesso para entregar os arquivos.</p>
<h2>Doações</h2>
<p>Para doar em <a href="/doe/">/doe/</a>, pedimos nome, e-mail, CPF e telefone, que o meio de pagamento exige, e guardamos o registro da doação (valor, forma de pagamento, situação e o endereço IP de onde ela foi feita) para emitir o comprovante, prestar contas e evitar fraudes. O pagamento é processado pela Unicopag: os dados do cartão vão direto para ela e não ficam guardados no site, que só recebe a bandeira e os quatro últimos dígitos. A base legal é a execução da doação e o cumprimento de obrigações legais (LGPD, art. 7º, II e V).</p>
<h2>Quando você nos escreve</h2>
<p>Os dados que você mandar por e-mail ou telefone (nome, contato e o que contar na mensagem) são usados só para responder e, se for o caso, para organizar o voluntariado ou a doação, com base no seu consentimento e no interesse legítimo da filial (Lei Geral de Proteção de Dados, Lei nº 13.709/2018). Não vendemos nem compartilhamos esses dados para fins comerciais.</p>
<h2>Seus direitos</h2>
<p>Você pode pedir acesso, correção ou exclusão dos seus dados pelo e-mail <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
<p class="pequeno">Atualizada em 1º de novembro de 2026.</p>
</div></section>"""


def creditos() -> str:
    linhas = "".join(
        f'<li><b>{esc(f["legenda"])}</b> — {esc(f["autor"])}, <a href="{esc(f["licenca_url"])}" rel="noopener" target="_blank">{esc(f["licenca"])}</a>, via <a href="{esc(f["origem"])}" rel="noopener" target="_blank">Wikimedia Commons</a>{", recortada e reduzida" if f.get("editada") else ""}.</li>'
        for f in FOTOS.values()
    )
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Créditos</p>
<h1>Créditos das fotos</h1>
<p>As fotos deste site mostram pontos turísticos de Petrópolis e são de licença livre. Elas não retratam ações da filial.</p>
<ul>{linhas}</ul>
</div></section>"""


def pedido_de_documentos() -> str:
    assunto = "Pedido de documentos – Cruz Vermelha Petrópolis"
    corpo = "Nome completo:%0D%0AE-mail ou telefone:%0D%0ADocumento que procuro:%0D%0APara que vou usar (opcional):%0D%0A"
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Transparência</p>
<h1>Pedido de documentos</h1>
<p>Procura um documento da filial que não está no <a href="/transparencia/">portal da transparência</a>, ou a íntegra de um que saiu com dados tarjados? Peça aqui. A resposta vem por e-mail.</p>
<h2>Como pedir</h2>
<ol class="passos">
  <li><b>Diga qual documento</b> você procura (por exemplo: ata de uma assembleia, demonstrações de um ano, certidão).</li>
  <li><b>Deixe um contato</b> para a resposta: e-mail ou telefone.</li>
  <li><b>Se for a íntegra</b> de um documento com dados pessoais, conte para que vai usar: a filial avalia o pedido de acordo com a LGPD (Lei nº 13.709/2018).</li>
</ol>
<p class="acoes"><button class="botao botao-vermelho" type="button" data-abrir-chat data-assunto="documentos">Pedir pelo chat</button>
<a class="botao botao-contorno" href="mailto:{FILIAL['email']}?subject={assunto}&amp;body={corpo}">Pedir por e-mail</a></p>
<p class="pequeno">Pedidos que não dependem de documento da filial (certidões de cartório, por exemplo) podem ser feitos direto ao órgão que emite.</p>
</div></section>"""


def gestao() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Transparência</p>
<h1>Como funciona a nossa gestão</h1>
<p>A filial publica os documentos que mostram quem a dirige, como decide e como usa o dinheiro que recebe. Três regras valem para tudo o que sai como oficial:</p>
<h2>1. Cada documento tem uma impressão digital</h2>
<p>Todo PDF do <a href="/transparencia/">portal da transparência</a> sai com a sua impressão digital (SHA-256): um código calculado a partir do próprio arquivo. Se uma vírgula mudar, o código muda. Qualquer pessoa confere em <a href="/verificar/">Verificar um documento</a> ou no próprio computador.</p>
<h2>2. Nada é trocado em silêncio</h2>
<p>Quando um documento ganha versão nova, a anterior continua listada. Com a trilha pública de auditoria da filial, cada registro ganha também um código de verificação, um carimbo de tempo e um selo diário, que mostram quando o documento foi publicado e se continua valendo. A trilha entra no ar junto com o sistema interno da filial.</p>
<h2>3. Só os canais oficiais falam pela filial</h2>
<p>Os endereços, telefones e perfis da filial estão em <a href="/canais-oficiais/">Canais oficiais</a>. A filial não pede doações por mensagem de pessoas físicas nem em contas de terceiros: doe só pela página <a href="/doe/">Doe</a>.</p>
<h2>Dados pessoais</h2>
<p>Documentos com dados de pessoas (CPF, endereço, assinaturas) saem com esses dados tarjados. A íntegra pode ser pedida pelo <a href="/pedido-de-documentos/">pedido de documentos</a>. Veja também a <a href="/privacidade/">política de privacidade</a>.</p>
</div></section>"""


def verificar() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Transparência</p>
<h1>Verificar um documento</h1>
<p>Confira se um PDF é o mesmo que a filial publicou no <a href="/transparencia/">portal da transparência</a>. O arquivo não sai do seu computador: a impressão digital (SHA-256) é calculada aqui mesmo, no navegador, e comparada com as que estão publicadas no portal.</p>
<div class="verificar-caixa">
  <label for="verificar-arquivo"><b>Escolha o PDF</b></label>
  <input id="verificar-arquivo" type="file" accept="application/pdf,.pdf">
  <p id="verificar-resultado" class="verificar-resultado" role="status" aria-live="polite"></p>
</div>
<h2>Pelo computador</h2>
<p>No Windows: <code>certutil -hashfile arquivo.pdf SHA256</code>. No Mac ou Linux: <code>shasum -a 256 arquivo.pdf</code>. O resultado tem de ser igual à impressão digital publicada no portal.</p>
<h2>Pelo código de verificação</h2>
<p>A consulta pelo código de verificação (o que traz a data do registro, o carimbo de tempo e o selo diário) abre quando a trilha pública de auditoria da filial entrar no ar. Até lá, confira pela impressão digital. <a href="/gestao/">Entenda como funciona</a>.</p>
</div></section>
<script>
(function () {{
  var campo = document.getElementById('verificar-arquivo');
  var saida = document.getElementById('verificar-resultado');
  if (!campo || !window.crypto || !crypto.subtle) {{ if (saida) saida.textContent = 'Este navegador não calcula a impressão digital. Use o comando abaixo.'; return; }}
  function hex(buf) {{ return Array.prototype.map.call(new Uint8Array(buf), function (b) {{ return ('0' + b.toString(16)).slice(-2); }}).join(''); }}
  campo.addEventListener('change', function () {{
    var arquivo = campo.files && campo.files[0];
    if (!arquivo) return;
    saida.className = 'verificar-resultado';
    saida.textContent = 'Calculando…';
    Promise.all([
      arquivo.arrayBuffer().then(function (b) {{ return crypto.subtle.digest('SHA-256', b); }}).then(hex),
      fetch('/transparencia/', {{ cache: 'no-store' }}).then(function (r) {{ return r.ok ? r.text() : ''; }})
    ]).then(function (r) {{
      var hash = r[0];
      var publicados = (r[1].match(/[0-9a-f]{{64}}/g) || []);
      var achou = publicados.indexOf(hash) >= 0;
      saida.className = 'verificar-resultado ' + (achou ? 'verificar-ok' : 'verificar-nao');
      saida.textContent = (achou ? 'Confere: este arquivo é igual a um documento publicado no portal. ' : 'Não confere: nenhum documento publicado no portal tem esta impressão digital. ') + 'SHA-256: ' + hash;
    }}).catch(function () {{ saida.textContent = 'Não foi possível conferir agora. Tente de novo ou use o comando abaixo.'; }});
  }});
}})();
</script>"""


def nao_encontrada() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Página não encontrada</p>
<h1>Não achamos esta página</h1>
<p>O endereço pode ter mudado. Comece pelo <a href="/">início</a> ou fale com a filial pelo e-mail <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
</div></section>"""


def hash_curto(caminho: Path) -> str:
    """Versão do arquivo para o ?v= (cache). Ignora CRLF: no Windows o git entrega os arquivos
    com CRLF e o hash mudaria sem o arquivo ter mudado (o servidor recebe LF)."""
    return hashlib.sha256(caminho.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:10]


def versao(arquivo: str) -> str:
    return hash_curto(SITE / "assets" / arquivo)


VERSAO_CSS = versao("site.css")
VERSAO_JS = versao("site.js")
# Chat "Fale com a gente" (o mesmo do RJ): manda a mensagem por e-mail pela API em chat/api/contato.php.
VERSAO_CHAT_CSS = hash_curto(SITE / "chat/chat.css")
VERSAO_CHAT_JS = hash_curto(SITE / "chat/chat.js")
DOE_HEAD = f'\n  <link rel="stylesheet" href="/doe/static/doe.css?v={hash_curto(SITE / "doe/static/doe.css")}">'
DOE_FIM = f'\n<script src="/doe/static/doe.js?v={hash_curto(SITE / "doe/static/doe.js")}" defer></script>'

if __name__ == "__main__":
    pagina("/", "Cruz Vermelha Brasileira – Petrópolis", "Filial do Município de Petrópolis da Cruz Vermelha Brasileira: voluntariado, doações, prevenção e contato.", home())
    pagina("/quem-somos/", "Quem somos – Cruz Vermelha Petrópolis", "A filial de Petrópolis da Cruz Vermelha Brasileira: missão, o que fazemos e o Movimento Internacional.", quem_somos(), "rionegro")
    pagina("/voluntariado/", "Voluntariado – Cruz Vermelha Petrópolis", "Como ser voluntário da Cruz Vermelha Brasileira em Petrópolis.", voluntariado(), "serra")
    pagina("/doe/", "Doe agora – Cruz Vermelha Petrópolis", "Quando a emergência chega, a ajuda precisa já estar pronta. Doe por PIX ou cartão para as ações humanitárias, a prevenção, o socorro em desastres e o voluntariado da Cruz Vermelha em Petrópolis.", doe(), "cristal", DOE_HEAD, DOE_FIM)
    pagina("/doe/obrigado/", "Sua doação – Cruz Vermelha Petrópolis", "Acompanhe a sua doação para a Cruz Vermelha Petrópolis.", doe_obrigado(), "cristal", DOE_HEAD + '\n  <meta name="robots" content="noindex">', DOE_FIM)
    pagina("/prevencao/", "Prevenção – Cruz Vermelha Petrópolis", "Orientações para antes, durante e depois de chuvas fortes e emergências em Petrópolis.", prevencao(), "serra")
    pagina("/guia-das-chuvas/", "Guia das chuvas de verão – Cruz Vermelha Petrópolis",
           "Como se preparar, como receber os alertas e o que fazer quando a chuva é forte em Petrópolis. Verão 2026/2027.",
           guia_chuvas(), "serra",
           "" if GUIA_CHUVAS_NO_AR else '\n  <meta name="robots" content="noindex, nofollow">',
           contato_flutuante=False, classe_body="pagina-guia")
    pagina("/principios-fundamentais/", "Princípios Fundamentais – Cruz Vermelha Petrópolis", "Os sete Princípios Fundamentais do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho.", principios(), "rionegro")
    pagina("/contato/", "Contato – Cruz Vermelha Petrópolis", "Endereço, telefones e e-mail da Cruz Vermelha Brasileira em Petrópolis.", contato(), "imperial")
    pagina("/pedido-de-documentos/", "Pedido de documentos – Cruz Vermelha Petrópolis", "Peça um documento da Cruz Vermelha Petrópolis que não está no portal da transparência.", pedido_de_documentos())
    pagina("/gestao/", "Como funciona a nossa gestão – Cruz Vermelha Petrópolis", "Impressão digital dos documentos, versões, canais oficiais e dados pessoais: como a Cruz Vermelha Petrópolis presta contas.", gestao())
    pagina("/verificar/", "Verificar um documento – Cruz Vermelha Petrópolis", "Confira se um PDF é o mesmo que a Cruz Vermelha Petrópolis publicou no portal da transparência.", verificar())
    pagina("/privacidade/", "Privacidade – Cruz Vermelha Petrópolis", "Como o site da Cruz Vermelha Petrópolis trata dados pessoais.", privacidade())
    pagina("/creditos/", "Créditos das fotos – Cruz Vermelha Petrópolis", "Autoria e licença das fotos de Petrópolis usadas no site.", creditos())
    pagina("/404.html", "Página não encontrada – Cruz Vermelha Petrópolis", "Página não encontrada.", nao_encontrada())
