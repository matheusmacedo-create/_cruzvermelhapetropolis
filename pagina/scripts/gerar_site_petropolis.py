"""Gera o site da Cruz Vermelha Brasileira – Filial de Petrópolis em pagina/site/.

Site enxuto e só de Petrópolis (27/10/2026): nenhuma foto, pessoa, história ou dado
da filial do Rio de Janeiro. As fotos são turísticas da cidade, de licença livre, com o
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
    "email": "cvbpetropolis@gmail.com",
    "telefones": ["(24) 2243-4758", "(24) 3113-0074"],
}
TEL = {t: "+55" + "".join(c for c in t if c.isdigit()) for t in FILIAL["telefones"]}
ENDERECO = f'{FILIAL["rua"]} · {FILIAL["bairro"]} · {FILIAL["cidade"]}/{FILIAL["uf"]} · CEP {FILIAL["cep"]}'
MAPA = "https://www.google.com/maps/search/?api=1&query=" + "Rua+Carlos+Gomes%2C+6%2C+Centro%2C+Petr%C3%B3polis+-+RJ%2C+25680-120"

FOTOS = json.loads((SITE / "assets" / "fotos" / "creditos.json").read_text(encoding="utf-8"))

MENU = [
    ("/quem-somos/", "Quem somos"),
    ("/voluntariado/", "Voluntariado"),
    ("/prevencao/", "Prevenção"),
    ("/principios-fundamentais/", "Princípios"),
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
    "sms": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
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
      <p>{icone('email')} <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a></p>
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
    "parentOrganization": {"@type": "NGO", "name": "Cruz Vermelha Brasileira"},
}


def pagina(caminho: str, titulo: str, descricao: str, corpo: str, foto_social: str = "hero", extra_head: str = "", extra_fim: str = "") -> None:
    url = ORIGEM + caminho
    og = ORIGEM + "/assets/fotos/" + FOTOS[foto_social]["arquivo"]
    ld = json.dumps(ORGANIZACAO, ensure_ascii=False, separators=(",", ":"))
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
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
  <link rel="stylesheet" href="/assets/site.css?v={VERSAO_CSS}">{extra_head}
  <script type="application/ld+json">{ld}</script>
</head>
<body>
{cabecalho(caminho)}
<main id="conteudo">
{corpo}
</main>
{rodape()}
<script src="/assets/site.js?v={VERSAO_JS}" defer></script>{extra_fim}
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
      <p class="pequeno">Ou ligue: {' · '.join(f'<a href="tel:{TEL[t]}">{t}</a>' for t in FILIAL['telefones'])}</p>
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
  <div class="wrap doe-grid">
    <div>
      <p class="eyebrow">Doação</p>
      <h1>Doe para a Cruz Vermelha em Petrópolis</h1>
      <p class="lead">Em menos de um minuto, por PIX ou cartão. Sua doação fica na cidade e sustenta o voluntariado, a prevenção e as ações humanitárias da filial.</p>
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
    <article class="cartao">{icone('telefone')}<h3>Telefones</h3><p>{tels}</p></article>
    <article class="cartao">{icone('email')}<h3>E-mail</h3><p><a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a></p></article>
  </div>
  <div class="wrap aviso"><p>A filial não faz atendimento de urgência. Em emergência: Defesa Civil <a href="tel:199">199</a> · Bombeiros <a href="tel:193">193</a> · SAMU <a href="tel:192">192</a>.</p></div>
</section>"""


def privacidade() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Privacidade</p>
<h1>Política de privacidade</h1>
<p>Este site é mantido pela {esc(FILIAL['nome'])}, CNPJ {FILIAL['cnpj']}, {esc(ENDERECO)}.</p>
<h2>O que coletamos</h2>
<p>O site não usa cookies de estatística ou de publicidade. Os contatos são feitos por e-mail ou telefone, por iniciativa de quem nos procura. As fontes de texto vêm do Google Fonts, que recebe o endereço IP do seu acesso para entregar os arquivos.</p>
<h2>Doações</h2>
<p>Para doar em <a href="/doe/">/doe/</a>, pedimos nome, e-mail, CPF e telefone, que o meio de pagamento exige, e guardamos o registro da doação (valor, forma de pagamento, situação e o endereço IP de onde ela foi feita) para emitir o comprovante, prestar contas e evitar fraudes. O pagamento é processado pela Unicopag: os dados do cartão vão direto para ela e não ficam guardados no site, que só recebe a bandeira e os quatro últimos dígitos. A base legal é a execução da doação e o cumprimento de obrigações legais (LGPD, art. 7º, II e V).</p>
<h2>Quando você nos escreve</h2>
<p>Os dados que você mandar por e-mail ou telefone (nome, contato e o que contar na mensagem) são usados só para responder e, se for o caso, para organizar o voluntariado ou a doação, com base no seu consentimento e no interesse legítimo da filial (Lei Geral de Proteção de Dados, Lei nº 13.709/2018). Não vendemos nem compartilhamos esses dados para fins comerciais.</p>
<h2>Seus direitos</h2>
<p>Você pode pedir acesso, correção ou exclusão dos seus dados pelo e-mail <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
<p class="pequeno">Atualizada em 27 de outubro de 2026.</p>
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


def nao_encontrada() -> str:
    return f"""<section class="secao"><div class="wrap texto">
<p class="eyebrow">Página não encontrada</p>
<h1>Não achamos esta página</h1>
<p>O endereço pode ter mudado. Comece pelo <a href="/">início</a> ou fale com a filial pelo e-mail <a href="mailto:{FILIAL['email']}">{FILIAL['email']}</a>.</p>
</div></section>"""


def versao(arquivo: str) -> str:
    return hashlib.sha256((SITE / "assets" / arquivo).read_bytes()).hexdigest()[:10]


VERSAO_CSS = versao("site.css")
VERSAO_JS = versao("site.js")
DOE_HEAD = f'\n  <link rel="stylesheet" href="/doe/static/doe.css?v={hashlib.sha256((SITE / "doe/static/doe.css").read_bytes()).hexdigest()[:10]}">'
DOE_FIM = f'\n<script src="/doe/static/doe.js?v={hashlib.sha256((SITE / "doe/static/doe.js").read_bytes()).hexdigest()[:10]}" defer></script>'

if __name__ == "__main__":
    pagina("/", "Cruz Vermelha Brasileira – Petrópolis", "Filial do Município de Petrópolis da Cruz Vermelha Brasileira: voluntariado, doações, prevenção e contato.", home())
    pagina("/quem-somos/", "Quem somos – Cruz Vermelha Petrópolis", "A filial de Petrópolis da Cruz Vermelha Brasileira: missão, o que fazemos e o Movimento Internacional.", quem_somos(), "rionegro")
    pagina("/voluntariado/", "Voluntariado – Cruz Vermelha Petrópolis", "Como ser voluntário da Cruz Vermelha Brasileira em Petrópolis.", voluntariado(), "serra")
    pagina("/doe/", "Doe – Cruz Vermelha Petrópolis", "Doe para a filial de Petrópolis da Cruz Vermelha Brasileira por PIX ou cartão, com comprovante por e-mail.", doe(), "cristal", DOE_HEAD, DOE_FIM)
    pagina("/doe/obrigado/", "Sua doação – Cruz Vermelha Petrópolis", "Acompanhe a sua doação para a Cruz Vermelha Petrópolis.", doe_obrigado(), "cristal", DOE_HEAD + '\n  <meta name="robots" content="noindex">', DOE_FIM)
    pagina("/prevencao/", "Prevenção – Cruz Vermelha Petrópolis", "Orientações para antes, durante e depois de chuvas fortes e emergências em Petrópolis.", prevencao(), "serra")
    pagina("/principios-fundamentais/", "Princípios Fundamentais – Cruz Vermelha Petrópolis", "Os sete Princípios Fundamentais do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho.", principios(), "rionegro")
    pagina("/contato/", "Contato – Cruz Vermelha Petrópolis", "Endereço, telefones e e-mail da Cruz Vermelha Brasileira em Petrópolis.", contato(), "imperial")
    pagina("/privacidade/", "Privacidade – Cruz Vermelha Petrópolis", "Como o site da Cruz Vermelha Petrópolis trata dados pessoais.", privacidade())
    pagina("/creditos/", "Créditos das fotos – Cruz Vermelha Petrópolis", "Autoria e licença das fotos de Petrópolis usadas no site.", creditos())
    pagina("/404.html", "Página não encontrada – Cruz Vermelha Petrópolis", "Página não encontrada.", nao_encontrada())
