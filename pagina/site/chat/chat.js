/* Chat de contato por e-mail da Cruz Vermelha Brasileira Petrópolis (site inteiro, sem dependências).
   Cria o botão flutuante e um painel em estilo de conversa que pergunta assunto, curso, nome, e-mail,
   telefone (opcional) e mensagem, e envia tudo para /chat/api/contato.php, que
   grava, manda por e-mail à equipe e devolve um protocolo. Entrou em 19/09/2026 no lugar do botão do
   WhatsApp da secretaria: o contato passa a chegar por e-mail, com cópia para quem escreveu.
   Fonte: site/chat/chat.js; as páginas referenciam /chat/chat.js?v=<hash> (scripts/chat_widget.py).
   Abrir de fora: qualquer elemento com data-abrir-chat (e opcionalmente data-assunto / data-curso),
   o endereço com #chat, ou window.cvChat.abrir(). */
(function () {
  'use strict';
  if (window.cvChat) return;

  var API = '/chat/api/contato.php';
  var URL_MATRICULA = '/matricula-cursos-presenciais/';
  var URL_CHECKOUT = URL_MATRICULA + 'checkout/';
  var URL_PRIVACIDADE = '/privacidade/';
  var EMAIL_CONTATO = 'contato@cruzvermelhapetropolis.org';
  var PRAZO = '3 dias úteis';
  var INSCRICAO = 'R$ 99,00';
  var CHAVE = 'cv_chat';
  var NOME = 'Cruz Vermelha Brasileira Petrópolis';
  var LOGO = '/assets/otim/logo-petropolis-240.webp'; // logo oficial (quadrado)

  /* chat:cursos — Petrópolis não tem escola: nenhum curso no chat. */
  var CURSOS = [];
  /* /chat:cursos */

  /* chat:respostas (Petrópolis, 29/10/2026) */
  var RESPOSTAS = [
    { assuntos: ["outro"], rotulo: "O que é a Cruz Vermelha Petrópolis?", p: "O que é a Cruz Vermelha Brasileira em Petrópolis?", r: "É a Filial do Município de Petrópolis da Cruz Vermelha Brasileira: uma associação privada sem fins lucrativos, CNPJ 09.198.238/0001-48, parte do Movimento Internacional da Cruz Vermelha e do Crescente Vermelho. Trabalha com voluntários, prevenção e ações humanitárias na cidade, guiada pelos sete Princípios Fundamentais." },
    { assuntos: ["doacoes", "voluntariado"], rotulo: "Como posso ajudar?", p: "Como ajudar a Cruz Vermelha em Petrópolis?", r: "Você pode doar em dinheiro pela página Doe (cruzvermelhapetropolis.org/doe), por PIX ou cartão, com comprovante por e-mail; ser voluntário; ou propor uma parceria da sua empresa, escola ou associação. Para doar itens, fale antes com a gente, para que cheguem a quem precisa no momento certo." },
    { assuntos: ["doacoes"], rotulo: "A doação é segura?", p: "Como sei que a doação vai para a filial?", r: "A doação pelo site é processada pela Unicopag e o comprovante sai em nome da filial, CNPJ 09.198.238/0001-48. A filial não pede doações por mensagem de pessoas físicas nem em contas de terceiros: na dúvida, confirme pelos telefones (21) 99605-6454 ou (21) 97465-0301." },
    { assuntos: ["voluntariado"], rotulo: "Como ser voluntário?", p: "Como ser voluntário da Cruz Vermelha em Petrópolis?", r: "Mande nome, telefone, bairro, disponibilidade e o que gostaria de fazer por aqui, pelo e-mail contato@cruzvermelhapetropolis.org ou pelo WhatsApp (21) 99605-6454. A equipe conversa com você e explica a orientação inicial. O voluntariado não é remunerado (Lei 9.608/1998)." },
    { assuntos: ["outro"], rotulo: "Vocês atendem emergência?", p: "A Cruz Vermelha em Petrópolis atende emergências?", r: "Não. A filial não faz atendimento de urgência nem marca consultas. Em emergência, ligue para a Defesa Civil (199), os Bombeiros (193) ou o SAMU (192). Para receber alertas de chuva, envie o seu CEP por SMS para 40199." },
    { assuntos: ["outro"], rotulo: "Onde fica?", p: "Onde fica a Cruz Vermelha em Petrópolis?", r: "Na Rua Carlos Gomes, 6, Centro, Petrópolis/RJ, CEP 25680-120. Antes de ir, combine pelo WhatsApp ou telefone (21) 99605-6454 ou (21) 97465-0301." },
    { assuntos: ["outro"], rotulo: "Tem telefone ou WhatsApp?", p: "Como falar com a Cruz Vermelha em Petrópolis?", r: "Pelo WhatsApp ou telefone (21) 99605-6454 e (21) 97465-0301, pelo e-mail contato@cruzvermelhapetropolis.org ou por este chat, que manda a sua mensagem por e-mail para a equipe." }
  ];
  /* /chat:respostas */

  // A missão primeiro: voluntariado e doação antes da escola (19/10/2026, Ad Grants). As chaves são as de
  // mcp_contato_assuntos() (api/lib/email.php), com os mesmos rótulos; só a ordem muda aqui.
  var ASSUNTOS = [
    ['voluntariado', 'Voluntariado'],
    ['doacoes', 'Doações e parcerias'],
    ['outro', 'Outro assunto']
  ];
  // Assuntos com uma ação pronta no site: o botão aparece junto das respostas, antes de escrever para a equipe.
  var ACOES = {
    voluntariado: { href: '/voluntariado/cadastro/', rotulo: 'Fazer o cadastro de voluntário' },
    doacoes: { href: '/doe/?utm_source=site&utm_medium=chat', rotulo: 'Doar pelo site' }
  };
  // Petrópolis não tem escola: nenhum assunto pede curso (as respostas de curso acima ficam sem uso).
  var COM_CURSO = [];
  var ORDEM = ['assunto', 'curso', 'nome', 'email', 'telefone', 'mensagem'];
  var ROTULOS = { assunto: 'Assunto', curso: 'Curso', nome: 'Nome', email: 'E-mail', telefone: 'Telefone', mensagem: 'Mensagem' };
  var ICONES = {
    balao: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3C6.5 3 2 6.6 2 11c0 2.1 1 4 2.7 5.4L4 21l4.6-1.9c1.1.3 2.2.4 3.4.4 5.5 0 10-3.6 10-8S17.5 3 12 3zm-4 9.3a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6zm4 0a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6zm4 0a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6z"/></svg>',
    cruz: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7z"/></svg>',
    x: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M18.3 5.7a1 1 0 0 0-1.4 0L12 10.6 7.1 5.7a1 1 0 1 0-1.4 1.4l4.9 4.9-4.9 4.9a1 1 0 1 0 1.4 1.4l4.9-4.9 4.9 4.9a1 1 0 0 0 1.4-1.4L13.4 12l4.9-4.9a1 1 0 0 0 0-1.4z"/></svg>',
    enviar: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.4 20.4l17.5-7.5c.8-.4.8-1.5 0-1.8L3.4 3.6c-.7-.3-1.4.3-1.4.9v5.2c0 .5.4.9.9 1L15 12 2.9 13.3c-.5.1-.9.5-.9 1v5.2c0 .7.7 1.2 1.4.9z"/></svg>'
  };

  // ------------------------------------------------------------------ utilidades
  function el(tag, attrs, filhos) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      var v = attrs[k];
      if (k === 'html') e.innerHTML = v;
      else if (k === 'text') e.textContent = v;
      else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), v);
      else if (v === false || v == null) return;
      else e.setAttribute(k, v === true ? '' : v);
    });
    (filhos || []).forEach(function (f) { if (f) e.appendChild(typeof f === 'string' ? document.createTextNode(f) : f); });
    return e;
  }
  function digitos(v) { return String(v || '').replace(/\D+/g, ''); }
  function telefoneBonito(v) {
    var d = digitos(v).slice(0, 11), corte = d.length > 10 ? 7 : 6;
    if (d.length < 10) return v;
    return '(' + d.slice(0, 2) + ') ' + d.slice(2, corte) + '-' + d.slice(corte);
  }
  function rotuloAssunto(chave) {
    for (var i = 0; i < ASSUNTOS.length; i++) if (ASSUNTOS[i][0] === chave) return ASSUNTOS[i][1];
    return chave;
  }
  function curso(slug) {
    for (var i = 0; i < CURSOS.length; i++) if (CURSOS[i].slug === slug) return CURSOS[i];
    return null;
  }
  function nomeCurso(slug) { var c = curso(slug); return c ? c.nome : ''; }
  /* Curso em foco na página: ?curso= na URL, curso aberto na matrícula ou escolhido no checkout. */
  function cursoDaPagina() {
    var q = new URLSearchParams(location.search).get('curso');
    if (q && curso(q)) return q;
    var ativo = document.querySelector('.mr-detalhe.ativo[data-curso]');
    if (ativo && curso(ativo.getAttribute('data-curso'))) return ativo.getAttribute('data-curso');
    var sel = document.getElementById('ck-curso');
    if (sel && sel.value && curso(sel.value)) return sel.value;
    return '';
  }
  /* utm_*, fbclid e gclid: da URL atual ou os que o checkout guardou na sessão (mesma chave).
     Só com consentimento de estatística no aviso de cookies (window.cvrjMedicao); sem ele, a
     mensagem segue sem a origem da visita. */
  function origem() {
    var o = {};
    var c = null;
    try { c = window.cvrjMedicao && window.cvrjMedicao.ler(); } catch (e) { c = null; }
    if (!c || !c.estatistica) return o;
    new URLSearchParams(location.search).forEach(function (v, k) { if (/^(utm_|fbclid$|gclid$)/.test(k)) o[k] = v.slice(0, 255); });
    try {
      var salvo = JSON.parse(sessionStorage.getItem('mcp_origem') || '{}');
      Object.keys(salvo).forEach(function (k) { if (!o[k]) o[k] = salvo[k]; });
    } catch (e) { /* armazenamento bloqueado */ }
    return o;
  }
  function rastrear(eventoGa, dadosGa, eventoMeta, dadosMeta, idMeta) {
    try { if (window.gtag && eventoGa) window.gtag('event', eventoGa, dadosGa || {}); } catch (e) { /* GA4 ausente */ }
    try { if (window.fbq && eventoMeta) window.fbq('track', eventoMeta, dadosMeta || {}, idMeta ? { eventID: idMeta } : undefined); } catch (e) { /* pixel ausente */ }
  }

  // ------------------------------------------------------------------ estado (sobrevive à navegação entre páginas)
  function novoEstado() { return { aberto: false, passo: 'assunto', respostas: {}, editando: false, erro: '',
    protocolo: '', aberturaRastreada: false, duvidasVistas: false, duvidasLidas: [] }; }
  function carregar() {
    try {
      var s = JSON.parse(sessionStorage.getItem(CHAVE) || 'null');
      if (s && s.respostas && typeof s.passo === 'string') { s.enviando = false; return s; }
    } catch (e) { /* sem sessão guardada */ }
    return novoEstado();
  }
  function guardar() { try { sessionStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (e) { /* segue sem guardar */ } }
  var estado = carregar();

  function precisaCurso() { return COM_CURSO.indexOf(estado.respostas.assunto) >= 0; }
  function respondido(passo) {
    var r = estado.respostas;
    if (passo === 'curso') return !precisaCurso() || Object.prototype.hasOwnProperty.call(r, 'curso');
    if (passo === 'telefone') return Object.prototype.hasOwnProperty.call(r, 'telefone');
    return typeof r[passo] === 'string' && r[passo] !== '';
  }
  var MAX_DUVIDAS = 5;  // mais que isso vira parede de botão no celular

  /* O curso escolhido, quando há ficha ou dúvidas dele para mostrar. */
  function fichaDoCurso() {
    if (!precisaCurso() || !estado.respostas.curso) return null;
    var c = curso(estado.respostas.curso);
    return c && (c.carga || c.valor || (c.faq && c.faq.length)) ? c : null;
  }
  /* O que o chat sabe responder aqui: as dúvidas do curso escolhido ou, na falta dele, as
     respostas da FAQ marcadas para este assunto. Sempre texto escrito e revisado por gente. */
  function duvidasDoPasso() {
    var c = fichaDoCurso();
    if (c && c.faq && c.faq.length) return c.faq.slice(0, MAX_DUVIDAS);
    var assunto = estado.respostas.assunto;
    return RESPOSTAS.filter(function (x) { return x.assuntos.indexOf(assunto) >= 0; })
      .slice(0, MAX_DUVIDAS).map(function (x) { return { p: x.p, r: x.r, rotulo: x.rotulo }; });
  }
  function temOQueResponder() { return !!fichaDoCurso() || duvidasDoPasso().length > 0; }
  function proximoPasso() {
    // Antes de pedir nome e e-mail: o que a escola já respondeu sobre este curso. Muita gente
    // para por aqui, e quem para não precisou abrir chamado nem esperar três dias úteis.
    if (!estado.duvidasVistas && respondido('assunto') && respondido('curso') && temOQueResponder()) return 'duvidas';
    for (var i = 0; i < ORDEM.length; i++) if (!respondido(ORDEM[i])) return ORDEM[i];
    return 'revisar';
  }

  /* Ficha do curso e as dúvidas que a escola já respondeu, como botões.
     Botão em vez de adivinhação: a resposta é sempre a que a escola escreveu, e o chat nunca
     precisa interpretar o que a pessoa quis dizer — não tem como responder errado. */
  function fichaHtml(c) {
    var linhas = [];
    if (c.carga) linhas.push(escapar(c.carga) + ' presenciais, na sede');
    if (c.escolaridade) linhas.push('Escolaridade mínima: ' + escapar(c.escolaridade));
    if (c.valor) linhas.push('Curso: ' + escapar(c.valor) + ' · Inscrição: ' + INSCRICAO);
    var html = 'Sobre o <b>' + escapar(c.nome) + '</b>:\n· ' + linhas.join('\n· ');
    return c.descricao ? html + '\n\n' + escapar(c.descricao) : html;
  }
  function jaLida(pergunta) {
    for (var i = 0; i < estado.duvidasLidas.length; i++) if (estado.duvidasLidas[i].p === pergunta) return true;
    return false;
  }
  function telaDuvidas() {
    var c = fichaDoCurso();
    var lista = duvidasDoPasso().filter(function (q) { return !jaLida(q.p); });
    var botoes = lista.map(function (q) { return { valor: 'q' + q.p, rotulo: q.rotulo || q.p }; });
    if (c) botoes.push({ valor: 'matricula', rotulo: 'Fazer matrícula em ' + c.nome, classe: 'cheio' });
    else if (precisaCurso()) botoes.push({ href: URL_MATRICULA, rotulo: 'Ver cursos e matrícula', classe: 'cheio' });
    else if (ACOES[estado.respostas.assunto]) botoes.push({ href: ACOES[estado.respostas.assunto].href, rotulo: ACOES[estado.respostas.assunto].rotulo, classe: 'cheio' });
    botoes.push({ valor: 'seguir', rotulo: 'Escrever para a equipe', classe: 'neutro' });
    var abertura = estado.duvidasLidas.length
      ? (lista.length ? 'Ficou mais alguma?' : 'Era o que eu tinha aqui. Quer falar com a equipe?')
      : (lista.length ? 'Posso responder alguma destas agora?' : 'Quer falar com a equipe?');
    return { html: abertura, chips: botoes };
  }

  // ------------------------------------------------------------------ perguntas do robô e respostas da pessoa
  function pergunta(passo) {
    var r = estado.respostas, daPagina, chips;
    switch (passo) {
      case 'assunto':
        return { html: 'Oi! Aqui é o atendimento da <b>' + NOME + '</b>, associação sem fins lucrativos que forma voluntários, faz campanhas humanitárias e leva educação preventiva às comunidades de Petrópolis. Deixe sua mensagem e a nossa equipe responde <b>por e-mail em até ' + PRAZO + '</b>.\nSobre o que você quer falar?',
          chips: ASSUNTOS.map(function (a) { return { valor: a[0], rotulo: a[1] }; }) };
      case 'curso':
        daPagina = cursoDaPagina();
        chips = CURSOS.filter(function (c) { return c.slug === daPagina; }).concat(CURSOS.filter(function (c) { return c.slug !== daPagina; }))
          .map(function (c) { return { valor: c.slug, rotulo: c.nome + (c.slug === daPagina ? ' (este curso)' : '') }; });
        chips.push({ valor: '', rotulo: 'Ainda não sei', classe: 'neutro' });
        return { html: 'Sobre qual curso?', chips: chips };
      case 'duvidas':
        return telaDuvidas();
      case 'nome':
        return { html: 'Como você se chama?', entrada: { tipo: 'text', autocomplete: 'name', placeholder: 'Seu nome' } };
      case 'email':
        return { html: 'Qual e-mail podemos usar para responder?', entrada: { tipo: 'email', autocomplete: 'email', placeholder: 'voce@exemplo.com' } };
      case 'telefone':
        return { html: 'Se quiser um retorno também por telefone, informe com DDD. É opcional.', entrada: { tipo: 'tel', autocomplete: 'tel', placeholder: '(24) 99999-9999' },
          chips: [{ valor: '', rotulo: 'Prefiro só por e-mail', classe: 'neutro' }] };
      case 'mensagem':
        return { html: 'Pode escrever sua mensagem. Quanto mais detalhes, melhor a resposta.', entrada: { tipo: 'textarea', autocomplete: 'off', placeholder: 'Escreva aqui…' } };
      case 'revisar':
        return { html: 'Tudo certo? Confira antes de enviar.', resumo: true,
          chips: [{ valor: 'enviar', rotulo: 'Enviar mensagem', classe: 'cheio' }, { valor: 'corrigir', rotulo: 'Corrigir algo', classe: 'neutro' }] };
      case 'corrigir':
        return { html: 'O que você quer corrigir?', chips: ORDEM.filter(function (p) { return p !== 'curso' || precisaCurso(); })
          .map(function (p) { return { valor: p, rotulo: ROTULOS[p] }; }).concat([{ valor: 'voltar', rotulo: 'Voltar', classe: 'neutro' }]) };
      case 'enviado':
        chips = [];
        if (precisaCurso() && r.curso) chips.push({ href: URL_CHECKOUT + '?curso=' + encodeURIComponent(r.curso), rotulo: 'Fazer matrícula em ' + nomeCurso(r.curso) });
        else if (precisaCurso()) chips.push({ href: URL_MATRICULA, rotulo: 'Ver cursos e matrícula' });
        chips.push({ acao: copiarEmail, rotulo: 'Copiar e-mail da equipe', classe: 'neutro' });
        chips.push({ valor: 'nova', rotulo: 'Nova mensagem', classe: 'neutro' }, { valor: 'fechar', rotulo: 'Fechar', classe: 'neutro' });
        return { html: 'Recebemos sua mensagem, <b>' + escapar(primeiroNome(r.nome)) + '</b>! Protocolo <b>' + escapar(estado.protocolo) + '</b>.\n\nA resposta chega <b>por e-mail</b>, em <b>' + escapar(r.email) + '</b>, em até ' + PRAZO + ', com o protocolo no assunto. Fique de olho na caixa de entrada e no spam.\n\nDaqui em diante a conversa segue por e-mail. Para não perder a resposta, salve <b>' + EMAIL_CONTATO + '</b> nos seus contatos.', chips: chips };
      case 'falhou':
        return { html: escapar(estado.erro || 'Não consegui enviar agora.') + '\nVocê pode tentar de novo ou escrever direto para <a href="' + linkEmail() + '">' + EMAIL_CONTATO + '</a>.',
          chips: [{ valor: 'tentar', rotulo: 'Tentar de novo', classe: 'cheio' }, { href: linkEmail(), rotulo: 'Escrever por e-mail', classe: 'neutro' }] };
    }
    return null;
  }
  function resposta(passo) {
    var r = estado.respostas;
    if (passo === 'assunto') return rotuloAssunto(r.assunto);
    if (passo === 'curso') return r.curso ? nomeCurso(r.curso) : 'Ainda não sei';
    if (passo === 'telefone') return r.telefone ? r.telefone : 'Prefiro só por e-mail';
    return r[passo] || '';
  }
  function escapar(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function primeiroNome(nome) { return String(nome || '').trim().split(/\s+/)[0] || ''; }
  function copiarEmail(botao) {
    var feito = function (ok) { botao.textContent = ok ? 'E-mail copiado' : EMAIL_CONTATO; };
    if (navigator.clipboard) navigator.clipboard.writeText(EMAIL_CONTATO).then(function () { feito(true); }, function () { feito(false); });
    else feito(false);
  }
  function linkEmail() {
    var r = estado.respostas;
    var corpo = (r.mensagem || '') + '\n\nNome: ' + (r.nome || '') + (r.telefone ? '\nTelefone: ' + r.telefone : '') + (r.curso ? '\nCurso: ' + nomeCurso(r.curso) : '');
    return 'mailto:' + EMAIL_CONTATO + '?subject=' + encodeURIComponent('Contato pelo site: ' + rotuloAssunto(r.assunto || 'outro')) + '&body=' + encodeURIComponent(corpo);
  }
  function validar(passo, valor) {
    if (passo === 'nome' && valor.length < 2) return 'Digite seu nome para a gente saber com quem fala.';
    if (passo === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(valor)) return 'Esse e-mail não parece válido. Confira e envie de novo.';
    if (passo === 'telefone' && valor !== '' && (digitos(valor).length < 10 || digitos(valor).length > 11)) return 'Telefone incompleto. Use DDD + número, ou toque em "Prefiro só por e-mail".';
    if (passo === 'mensagem' && valor.length < 10) return 'Conte um pouco mais: a mensagem precisa ter pelo menos 10 caracteres.';
    if (passo === 'mensagem' && valor.length > 3000) return 'A mensagem pode ter até 3.000 caracteres.';
    return '';
  }

  // ------------------------------------------------------------------ interface
  var raiz, botao, painel, mensagens, leitor, form, campo, enviarBtn, contagem = 0;

  function balao(classe, conteudo, texto) {
    var b = el('div', { class: 'cv-chat-msg ' + classe });
    if (texto) b.textContent = conteudo; else b.innerHTML = conteudo;
    return b;
  }
  function chips(lista, passo) {
    return el('div', { class: 'cv-chat-chips' }, lista.map(function (c) {
      var classe = 'cv-chat-chip' + (c.classe ? ' ' + c.classe : '');
      if (c.href) return el('a', { class: classe, href: c.href, text: c.rotulo });
      if (c.acao) return el('button', { class: classe, type: 'button', text: c.rotulo, onclick: function () { c.acao(this); } });
      return el('button', { class: classe, type: 'button', text: c.rotulo, onclick: function () { escolher(passo, c.valor); } });
    }));
  }
  function resumo() {
    var dl = el('dl');
    ORDEM.forEach(function (p) {
      if (p === 'curso' && !precisaCurso()) return;
      dl.appendChild(el('dt', { text: ROTULOS[p] }));
      dl.appendChild(el('dd', { text: resposta(p) }));
    });
    return el('div', { class: 'cv-chat-resumo' }, [dl]);
  }
  function digitando() { return el('div', { class: 'cv-chat-digitando', 'aria-label': 'Enviando…' }, [el('i'), el('i'), el('i')]); }

  function render() {
    raiz.classList.toggle('aberto', estado.aberto);
    botao.setAttribute('aria-expanded', String(estado.aberto));
    if (estado.aberto) botao.setAttribute('aria-label', 'Fechar o chat'); else botao.removeAttribute('aria-label');
    painel.hidden = !estado.aberto;
    if (!estado.aberto) return;

    var itens = [];
    ORDEM.forEach(function (p) {
      if (p === 'curso' && !precisaCurso()) return;
      if (!respondido(p) || p === estado.passo) return;
      itens.push(balao('robo', pergunta(p).html));
      itens.push(balao('pessoa', resposta(p), true));
      // A ficha do curso e as dúvidas já respondidas ficam na conversa, logo depois do curso:
      // quem seguiu para o e-mail continua vendo o que já foi dito.
      if (p === 'curso' && (estado.duvidasLidas.length || estado.passo === 'duvidas' || estado.duvidasVistas)) {
        if (fichaDoCurso()) itens.push(balao('robo', fichaHtml(fichaDoCurso())));
        estado.duvidasLidas.forEach(function (d) {
          itens.push(balao('pessoa', d.p, true));
          itens.push(balao('robo', escapar(d.r)));
        });
      }
    });
    var q = pergunta(estado.passo);
    if (q) {
      itens.push(balao('robo', q.html));
      if (estado.erro && estado.passo !== 'falhou') itens.push(balao('robo erro', estado.erro, true));
      if (q.resumo) itens.push(resumo());
      if (estado.enviando) itens.push(digitando());
      else if (q.chips) itens.push(chips(q.chips, estado.passo));
    }
    var entrada = q && q.entrada && !estado.enviando ? q.entrada : null;
    campo.disabled = !entrada;
    enviarBtn.disabled = !entrada;
    if (entrada) {
      campo.placeholder = entrada.placeholder;
      campo.setAttribute('inputmode', entrada.tipo === 'email' ? 'email' : entrada.tipo === 'tel' ? 'tel' : 'text');
      campo.setAttribute('autocomplete', entrada.autocomplete);
      campo.setAttribute('enterkeyhint', 'send');
    } else {
      campo.placeholder = estado.passo === 'enviado' ? 'Mensagem enviada' : estado.enviando ? 'Enviando…' : 'Escolha uma opção acima';
      campo.value = '';
      ajustarAltura();
    }
    mensagens.innerHTML = '';
    itens.forEach(function (n, i) { if (i >= contagem) n.classList.add('nova'); mensagens.appendChild(n); });
    contagem = itens.length;
    mensagens.scrollTop = mensagens.scrollHeight;
    // Leitor de tela: só a fala nova do robô (a conversa inteira é redesenhada a cada passo).
    var falas = mensagens.querySelectorAll('.cv-chat-msg.robo');
    var ultima = falas.length ? falas[falas.length - 1].textContent : '';
    if (leitor.textContent !== ultima) leitor.textContent = ultima;
  }
  function focar() {
    if (!estado.aberto) return;
    if (!campo.disabled) { campo.focus({ preventScroll: true }); return; }
    var chip = mensagens.querySelector('.cv-chat-chip');
    if (chip) chip.focus({ preventScroll: true });
  }
  function ajustarAltura() {
    campo.style.height = 'auto';
    campo.style.height = Math.min(140, Math.max(44, campo.scrollHeight)) + 'px';
  }

  // ------------------------------------------------------------------ fluxo
  function responder(passo, valor) {
    estado.erro = '';
    estado.respostas[passo] = valor;
    if (estado.editando) {
      estado.editando = false;
      estado.passo = (precisaCurso() && !respondido('curso')) ? 'curso' : 'revisar';
      if (estado.passo === 'curso') estado.editando = true;
    } else {
      estado.passo = proximoPasso();
    }
    guardar(); render(); focar();
  }
  function escolher(passo, valor) {
    estado.erro = '';
    if (passo === 'revisar') {
      if (valor === 'enviar') { enviar(); return; }
      estado.passo = 'corrigir'; guardar(); render(); focar(); return;
    }
    if (passo === 'corrigir') {
      if (valor === 'voltar') { estado.passo = 'revisar'; } else { estado.passo = valor; estado.editando = true; }
      guardar(); render(); focar(); return;
    }
    if (passo === 'enviado') {
      if (valor === 'fechar') { fechar(); return; }
      var r = estado.respostas;
      estado = novoEstado();
      estado.aberto = true; estado.aberturaRastreada = true;
      estado.respostas = { nome: r.nome, email: r.email, telefone: r.telefone || '' };
      guardar(); render(); focar(); return;
    }
    if (passo === 'falhou') { if (valor === 'tentar') enviar(); return; }
    if (passo === 'duvidas') {
      if (valor === 'matricula') {
        rastrear('chat_duvida_matricula', { curso: estado.respostas.curso });
        location.href = URL_CHECKOUT + '?curso=' + encodeURIComponent(estado.respostas.curso);
        return;
      }
      if (valor === 'seguir') {
        estado.duvidasVistas = true;
        rastrear('chat_duvida_seguiu', { curso: estado.respostas.curso, respostas_abertas: estado.duvidasLidas.length });
        estado.passo = proximoPasso(); guardar(); render(); focar(); return;
      }
      var procurada = String(valor).slice(1), faq = duvidasDoPasso();
      for (var i = 0; i < faq.length; i++) if (faq[i].p === procurada && !jaLida(procurada)) {
        estado.duvidasLidas.push({ p: faq[i].p, r: faq[i].r });
        rastrear('chat_duvida_respondida', { curso: estado.respostas.curso, pergunta: faq[i].p });
      }
      guardar(); render(); focar(); return;
    }
    responder(passo, valor);
  }
  function aoEnviarTexto(e) {
    if (e) e.preventDefault();
    var q = pergunta(estado.passo);
    if (!q || !q.entrada || estado.enviando) return;
    var valor = campo.value.trim();
    var erro = validar(estado.passo, valor);
    if (erro) { estado.erro = erro; render(); campo.focus(); return; }
    if (estado.passo === 'telefone') valor = telefoneBonito(valor);
    if (estado.passo === 'email') valor = valor.toLowerCase();
    campo.value = '';
    ajustarAltura();
    responder(estado.passo, valor);
  }
  function enviar() {
    if (estado.enviando) return;
    var r = estado.respostas;
    estado.enviando = true; estado.erro = ''; estado.passo = 'revisar';
    render();
    var corpo = {
      nome: r.nome, email: r.email, telefone: r.telefone || '', assunto: r.assunto,
      curso: precisaCurso() ? (r.curso || '') : '', mensagem: r.mensagem,
      // O que o chat já respondeu antes do chamado. O servidor confere cada texto contra as
      // perguntas que existem e descarta o resto — nada daqui entra num e-mail sem conferência.
      ja_respondido: estado.duvidasLidas.map(function (d) { return d.p; }),
      pagina: location.pathname + location.search, origem: origem(), site: ''
    };
    // O id do Contact do Pixel vai junto: o servidor manda o mesmo Contact à API de Conversões (só com "sim" para marketing).
    try { if (window.cvrjMedicao && window.cvrjMedicao.novoId) corpo.evento_id = window.cvrjMedicao.novoId('ct'); } catch (e) { /* sem bloco de medição */ }
    fetch(API, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(corpo) })
      .then(function (resp) { return resp.json().catch(function () { return null; }).then(function (d) { return { http: resp.status, d: d }; }); })
      .catch(function () { return { http: 0, d: null }; })
      .then(function (x) {
        var d = x.d && typeof x.d === 'object' ? x.d : { ok: false, erro: x.http === 0 ? 'Sem conexão. Verifique a internet e tente de novo.' : 'O servidor não respondeu como esperado.' };
        estado.enviando = false;
        if (d.ok) {
          estado.protocolo = d.protocolo || '';
          estado.passo = 'enviado';
          rastrear('contato_enviado', { assunto: r.assunto, curso: corpo.curso, pagina: location.pathname },
            'Contact', { content_category: r.assunto, content_name: nomeCurso(corpo.curso) || rotuloAssunto(r.assunto) }, corpo.evento_id);
        } else if (d.campo && ORDEM.indexOf(d.campo) >= 0) {
          estado.passo = d.campo; estado.editando = true; estado.erro = d.erro || '';
        } else {
          estado.passo = 'falhou'; estado.erro = d.erro || 'Não consegui enviar agora.';
        }
        guardar(); render(); focar();
      });
  }
  function abrir(inicial) {
    if (inicial && estado.passo === 'assunto' && !estado.respostas.assunto) {
      if (inicial.assunto && rotuloAssunto(inicial.assunto) !== inicial.assunto) estado.respostas.assunto = inicial.assunto;
      if (inicial.curso && curso(inicial.curso) && precisaCurso()) estado.respostas.curso = inicial.curso;
      if (estado.respostas.assunto) estado.passo = proximoPasso();
    }
    estado.aberto = true;
    guardar(); render(); focar();
    if (!estado.aberturaRastreada) {
      estado.aberturaRastreada = true; guardar();
      rastrear('contato_aberto', { pagina: location.pathname });
    }
  }
  function fechar() { estado.aberto = false; guardar(); render(); botao.focus(); }

  // ------------------------------------------------------------------ montagem
  function montar() {
    raiz = el('div', { class: 'cv-chat', id: 'cv-chat' });
    botao = el('button', { class: 'cv-chat-abrir', type: 'button', 'aria-expanded': 'false', 'aria-controls': 'cv-chat-painel',
      html: '<span class="cv-chat-abrir-ico">' + ICONES.balao + '</span><span class="cv-chat-abrir-rotulo">Fale com a gente</span><span class="cv-chat-abrir-x">' + ICONES.x + '</span>',
      onclick: function () { if (estado.aberto) fechar(); else abrir(); } });
    var topo = el('header', { class: 'cv-chat-topo', html: '<span class="cv-chat-avatar"><img src="' + LOGO + '" width="44" height="44" alt=""></span><div><b id="cv-chat-titulo">' + NOME + '</b><small><span class="cv-chat-status">Atendimento por e-mail</span> · resposta em até ' + PRAZO + '</small></div>' });
    topo.appendChild(el('button', { class: 'cv-chat-fechar', type: 'button', 'aria-label': 'Fechar o chat', html: ICONES.x, onclick: fechar }));
    mensagens = el('div', { class: 'cv-chat-mensagens', role: 'log' });
    leitor = el('div', { class: 'cv-chat-sr', 'aria-live': 'polite', 'aria-atomic': 'true' });
    campo = el('textarea', { rows: '1', 'aria-label': 'Sua resposta', placeholder: '' });
    campo.addEventListener('input', ajustarAltura);
    campo.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); aoEnviarTexto(); } });
    enviarBtn = el('button', { class: 'cv-chat-enviar', type: 'submit', 'aria-label': 'Enviar', html: ICONES.enviar });
    form = el('form', { class: 'cv-chat-compor', novalidate: true, onsubmit: aoEnviarTexto }, [campo, enviarBtn]);
    var rodape = el('p', { class: 'cv-chat-rodape', html: 'Seus dados são usados só para responder ao contato. <a href="' + URL_PRIVACIDADE + '">Política de privacidade</a>' });
    painel = el('div', { class: 'cv-chat-painel', id: 'cv-chat-painel', role: 'dialog', 'aria-labelledby': 'cv-chat-titulo', hidden: true }, [topo, mensagens, form, rodape, leitor]);
    raiz.appendChild(painel);
    raiz.appendChild(botao);
    document.body.appendChild(raiz);

    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && estado.aberto) fechar(); });
    document.addEventListener('click', function (e) {
      var gatilho = e.target.closest ? e.target.closest('[data-abrir-chat]') : null;
      if (!gatilho) return;
      e.preventDefault();
      abrir({ assunto: gatilho.getAttribute('data-assunto') || '', curso: gatilho.getAttribute('data-curso') || '' });
    });
    function porHash() { if (location.hash === '#chat') abrir(); }
    window.addEventListener('hashchange', porHash);

    // Home no celular (data-cv-chat-depois-do-hero): o ícone só aparece depois de rolar um pouco. No topo ele cobria o
    // canto do botão "Doe agora" (360x740); o painel e o gatilho #chat/data-abrir-chat continuam funcionando.
    if (document.querySelector('[data-cv-chat-depois-do-hero]') && window.matchMedia) {
      var estreito = window.matchMedia('(max-width: 620px)');
      var atualizarRecolhimento = function () {
        raiz.classList.toggle('cv-chat-recolhido', estreito.matches && (window.pageYOffset || 0) < 240);
      };
      window.addEventListener('scroll', atualizarRecolhimento, { passive: true });
      window.addEventListener('resize', atualizarRecolhimento);
      atualizarRecolhimento();
    }

    render();
    porHash();
  }

  if (document.body) montar(); else document.addEventListener('DOMContentLoaded', montar);
  window.cvChat = { abrir: abrir, fechar: fechar };
})();
