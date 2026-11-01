import 'server-only'
import { usarChatDoSite, usarFolhaDoSite } from '@/lib/site/esqueleto'

/**
 * O chat "Fale com a gente" e a folha do site nas páginas que a Redação gera.
 *
 * As páginas do site carregam /assets/site.css?v=HASH, /chat/chat.css?v=HASH e
 * /chat/chat.js?v=HASH: quem muda o arquivo muda o HASH, no gerador do site
 * (pagina/scripts/gerar_site_petropolis.py). Um endereço sem versão ficaria
 * velho no navegador de quem já visitou, então as páginas daqui usam a versão
 * que a HOME usa agora, lida da própria home na hora de publicar. Se a leitura
 * falhar, a página sai sem o chat e com a folha sem versão
 * (esqueleto.ts, folhaDoSite) — nunca com uma versão adivinhada.
 */

const HOME = 'https://cruzvermelhapetropolis.org/'
const TEMPO_LIMITE_MS = 4000
const VALIDADE_MS = 10 * 60_000
const VALIDADE_DA_FALHA_MS = 60_000

// Só a forma exata que as páginas do site escrevem: caminho conhecido e versão
// em hexadecimal. O que não casar não entra na página.
const CSS = /<link\s+rel="stylesheet"\s+href="(\/chat\/chat(?:\.min)?\.css\?v=[0-9a-f]{6,40})"\s*\/?>/
const JS = /<script\s+src="(\/chat\/chat\.js\?v=[0-9a-f]{6,40})"\s+defer\s*><\/script>/
const FOLHA = /<link\s+rel="stylesheet"\s+href="(\/assets\/site\.css\?v=[0-9a-f]{6,40})"\s*\/?>/

/** As duas tags, montadas por nós a partir dos endereços versionados da home. Vazio se faltar uma. */
export function extrairTagsDoChat(html: string): string {
  const css = CSS.exec(html)?.[1]
  const js = JS.exec(html)?.[1]
  if (!css || !js) return ''
  return `<!-- Chat de contato por e-mail (o mesmo da home) -->
    <link rel="stylesheet" href="${css}">
    <script src="${js}" defer></script>`
}

/** A tag da folha do site, montada por nós a partir do endereço versionado da home. Vazio se não houver. */
export function extrairTagDaFolha(html: string): string {
  const href = FOLHA.exec(html)?.[1]
  return href ? `<link rel="stylesheet" href="${href}">` : ''
}

let guardado: { tags: string; folha: string; ate: number } | null = null

/**
 * Lê as tags do chat e a da folha do site e as deixa prontas para as páginas
 * desta rodada: devolve as do chat (quem monta a página as passa adiante) e
 * guarda as duas no esqueleto, que as usa quando a página não recebe nenhuma.
 * Nunca lança: sem a home, devolve vazio, as páginas saem sem o chat e com a
 * folha sem versão, e o resto da publicação segue.
 */
export async function prepararChatDoSite(buscar: typeof fetch = fetch): Promise<string> {
  if (guardado && guardado.ate > Date.now()) {
    usarChatDoSite(guardado.tags)
    usarFolhaDoSite(guardado.folha)
    return guardado.tags
  }
  let tags = ''
  let folha = ''
  try {
    const resposta = await buscar(HOME, { cache: 'no-store', redirect: 'follow', signal: AbortSignal.timeout(TEMPO_LIMITE_MS) })
    if (resposta.ok) {
      const home = await resposta.text()
      tags = extrairTagsDoChat(home)
      folha = extrairTagDaFolha(home)
    }
  } catch {
    tags = ''
    folha = ''
  }
  if (!tags) console.warn('[site] não encontrei a versão do chat na home: as páginas desta rodada saem sem o chat')
  if (!folha) console.warn('[site] não encontrei a versão da folha do site na home: as páginas desta rodada usam /assets/site.css sem versão')
  // A leitura só vale os 10 minutos inteiros se trouxe as duas versões.
  guardado = { tags, folha, ate: Date.now() + (tags && folha ? VALIDADE_MS : VALIDADE_DA_FALHA_MS) }
  usarChatDoSite(tags)
  usarFolhaDoSite(folha)
  return tags
}
