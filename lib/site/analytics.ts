/**
 * O Google Analytics (gtag) e o Google Tag Manager do site institucional.
 *
 * Os identificadores não são segredo: eles saem impressos no HTML de toda
 * página que os carrega — estão na home pública desde sempre. O que este
 * módulo garante é OUTRA coisa: que todas as páginas usem os MESMOS
 * identificadores e o MESMO bloco da home, porque duas versões do trecho é
 * como um site passa a contar metade das visitas sem ninguém perceber — ou a
 * medir quem não deixou.
 *
 * Dois usos, uma fonte:
 *  - o gerador de páginas (matéria, notícias, acervo, portal) inclui o bloco
 *    em toda página que nasce;
 *  - o enxerto por FTP (ligarAnalyticsDoSite) completa as páginas que já
 *    existem no servidor e ficaram de fora.
 */

/** O Analytics de Petrópolis, o mesmo que as páginas de pagina/site/ já usam. */
export const ID_DO_ANALYTICS = 'G-MJ0DGJHLVW'
/**
 * A propriedade do GA4 desse identificador (Administrador → Detalhes da
 * propriedade), de onde Resultados lê os números pela Data API. Também não é
 * segredo: sem a conta de serviço com acesso de Leitor, ninguém lê nada com ele.
 */
export const ID_DA_PROPRIEDADE = '544248603'
/** O Google Tag Manager de Petrópolis, o mesmo das páginas de pagina/site/. */
export const ID_DO_GTM = 'GTM-PDLBB439'

/**
 * O bloco de medição do <head>, o mesmo que o gerador do site
 * (pagina/scripts/gerar_site_petropolis.py) põe no topo de toda página: o gtag
 * do GA4 e o trecho oficial do Tag Manager. O site de Petrópolis não tem aviso
 * de cookies nem Pixel da Meta; a política de privacidade diz que ele usa o
 * Google Analytics. Mudou lá, muda aqui: página com bloco diferente é como um
 * site passa a contar metade das visitas (ou o dobro) sem ninguém perceber.
 */
export function blocoDoAnalytics(): string {
  return `<!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=${ID_DO_ANALYTICS}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', '${ID_DO_ANALYTICS}');
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','${ID_DO_GTM}');</script>
  <!-- End Google Tag Manager -->`
}

/** A parte do Tag Manager que vai logo depois do <body> (para quem navega sem JavaScript). */
export function noscriptDoAnalytics(): string {
  return `<!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${ID_DO_GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->`
}

/**
 * A página já carrega o gtag? Vale qualquer identificador e todas as formas do
 * bloco — a antiga (<script async src=".../gtag/js">), a que buscava o gtag.js
 * depois do load e a de agora, que só o busca com consentimento (o endereço
 * fica numa variável do bloco): uma página com qualquer uma delas não deve
 * ganhar uma segunda, porque página com dois gtags conta cada visita duas vezes.
 */
export function temAnalytics(html: string): boolean {
  return html.includes('googletagmanager.com/gtag/js') || /gtag\(\s*['"]config['"]\s*,\s*['"]G-/.test(html)
}

export type ResultadoDoEnxerto =
  | { estado: 'ligado'; html: string; detalhe: string }
  | { estado: 'ja-ligado'; detalhe: string }
  | { estado: 'recusado'; detalhe: string }

/**
 * Põe o bloco numa página que ainda não o tem — antes do </head>, como o
 * Google pede.
 *
 * As recusas são o contrato: página sem </head> não é uma página inteira
 * (pode ser um fragmento, um e-mail, um arquivo pela metade) e gravar nela
 * às cegas é como se corrompe um site inteiro por FTP. Na dúvida, não grava.
 */
export function ligarAnalyticsNaPagina(html: string): ResultadoDoEnxerto {
  if (temAnalytics(html)) {
    return { estado: 'ja-ligado', detalhe: 'A página já carrega o Google Analytics.' }
  }
  const fim = html.search(/<\/head\s*>/i)
  if (fim === -1) {
    return { estado: 'recusado', detalhe: 'A página não tem </head> — não parece uma página inteira.' }
  }
  const bloco = `\n${blocoDoAnalytics()}\n`
  return {
    estado: 'ligado',
    html: html.slice(0, fim) + bloco + html.slice(fim),
    detalhe: `Google Analytics (${ID_DO_ANALYTICS}) ligado na página.`,
  }
}
