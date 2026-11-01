/**
 * O portal de transparência e a página de canais oficiais no site, com
 * documentos de EXEMPLO, enquanto a Redação de Petrópolis não está no ar.
 *
 * Usa os mesmos geradores que a Redação usa ao publicar
 * (lib/transparencia/paginas.ts, com o esqueleto de lib/site/esqueleto.ts):
 * quando a equipe enviar os documentos de verdade pela tela Transparência, a
 * Redação grava por cima, nos mesmos endereços, e os exemplos saem. Até lá,
 * cada PDF e cada ficha dizem "exemplo", não há código de verificação (ele
 * nasce na trilha de auditoria da Redação) e as páginas ficam fora dos
 * buscadores (.htaccess com noindex).
 *
 *   npx tsx scripts/gerar-transparencia-de-exemplo.ts
 *
 * Grava em pagina/site/: transparencia/ (index.html, .htaccess e arquivos/*.pdf)
 * e canais-oficiais/ (index.html e .htaccess). Depois, publique só esses
 * arquivos na Hostinger (pagina/README.md).
 */
import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { PDFDocument, StandardFonts, degrees, rgb } from 'pdf-lib'
import { usarChatDoSite, usarFolhaDoSite } from '../lib/site/esqueleto'
import { DADOS_DA_FILIAL } from '../lib/site/juridico'
import { htaccessDoPortal, paginaDaTransparencia, paginaDosCanais, type DocumentoNoPortal } from '../lib/transparencia/paginas'
import type { Canal, Categoria } from '../lib/transparencia/regras'

const SITE = join(process.cwd(), 'pagina', 'site')
const ORIGEM = 'https://cruzvermelhapetropolis.org'
const AGORA = new Date()
const AVISO = 'Documento de exemplo, só para mostrar como o portal funciona. Não é documento oficial da filial.'

const versao = (arquivo: string) => createHash('sha256').update(readFileSync(join(SITE, arquivo))).digest('hex').slice(0, 10)

// As mesmas tags versionadas que o gerador do site põe nas páginas dele.
usarFolhaDoSite(`<link rel="stylesheet" href="/assets/site.css?v=${versao('assets/site.css')}">`)
usarChatDoSite(`<!-- Chat de contato por e-mail (o mesmo da home) -->
    <link rel="stylesheet" href="/chat/chat.css?v=${versao('chat/chat.css')}">
    <script src="/chat/chat.js?v=${versao('chat/chat.js')}" defer></script>`)

type Exemplo = { arquivo: string; categoria: Categoria; titulo: string; periodo: string; paragrafos: string[] }

const EXEMPLOS: Exemplo[] = [
  {
    arquivo: 'exemplo-estatuto-social.pdf', categoria: 'estatuto', titulo: 'Estatuto social (exemplo)', periodo: 'Em vigor',
    paragrafos: [
      'Aqui entra o estatuto social registrado da filial, em PDF, como foi registrado em cartório.',
      'O estatuto define a finalidade, a forma de eleição da diretoria, os conselhos e como a filial presta contas.',
    ],
  },
  {
    arquivo: 'exemplo-ata-de-eleicao-e-posse.pdf', categoria: 'atas', titulo: 'Ata de eleição e posse da diretoria (exemplo)', periodo: 'Mandato atual',
    paragrafos: [
      'Aqui entra a ata da assembleia que elegeu e deu posse à diretoria em exercício.',
      'Na versão pública, dados pessoais (CPF, endereço, assinaturas) saem tarjados, como pede a LGPD; a íntegra pode ser pedida pelo pedido de documentos.',
    ],
  },
  {
    arquivo: 'exemplo-demonstracoes-contabeis-2025.pdf', categoria: 'demonstracoes', titulo: 'Demonstrações contábeis de 2025 (exemplo)', periodo: '2025',
    paragrafos: [
      'Aqui entram o balanço patrimonial, a demonstração do resultado, o fluxo de caixa e as notas explicativas do ano.',
      'Com elas vem o parecer do conselho fiscal, na seção Pareceres.',
    ],
  },
  {
    arquivo: 'exemplo-relatorio-de-atividades-2025.pdf', categoria: 'relatorio_anual', titulo: 'Relatório de atividades de 2025 (exemplo)', periodo: '2025',
    paragrafos: [
      'Aqui entra o relatório do que a filial fez no ano: ações humanitárias, prevenção, resposta a chuvas fortes, formação e voluntariado.',
      'Números de pessoas atendidas, horas de voluntariado e campanhas, com fotos e o que mudou para a cidade.',
    ],
  },
  {
    arquivo: 'exemplo-cartao-cnpj.pdf', categoria: 'certidoes', titulo: 'Comprovante de inscrição no CNPJ (exemplo)', periodo: 'Atual',
    paragrafos: [
      `Aqui entra o comprovante de inscrição no CNPJ da filial (${DADOS_DA_FILIAL.cnpj}), emitido no site da Receita Federal.`,
      'Na mesma seção entram as certidões negativas de débitos, com a data de validade de cada uma.',
    ],
  },
]

async function pdfDeExemplo(e: Exemplo): Promise<Uint8Array> {
  const pdf = await PDFDocument.create()
  pdf.setTitle(e.titulo)
  pdf.setAuthor('Cruz Vermelha Brasileira – Filial do Município de Petrópolis')
  // Data fixa: o mesmo exemplo gera sempre o mesmo arquivo (e a mesma impressão digital).
  pdf.setCreationDate(new Date('2026-11-01T12:00:00Z'))
  pdf.setModificationDate(new Date('2026-11-01T12:00:00Z'))
  const pagina = pdf.addPage([595.28, 841.89])
  const normal = await pdf.embedFont(StandardFonts.Helvetica)
  const negrito = await pdf.embedFont(StandardFonts.HelveticaBold)
  const vermelho = rgb(0.8, 0, 0)
  pagina.drawText('EXEMPLO', { x: 120, y: 330, size: 110, font: negrito, color: rgb(0.95, 0.85, 0.85), rotate: degrees(35) })
  pagina.drawText('Cruz Vermelha Brasileira – Filial do Município de Petrópolis', { x: 56, y: 780, size: 12, font: negrito, color: vermelho })
  pagina.drawText(`CNPJ ${DADOS_DA_FILIAL.cnpj}`, { x: 56, y: 764, size: 10, font: normal })
  pagina.drawText(e.titulo, { x: 56, y: 720, size: 18, font: negrito })
  pagina.drawText('DOCUMENTO DE EXEMPLO — NÃO É DOCUMENTO OFICIAL', { x: 56, y: 692, size: 11, font: negrito, color: vermelho })
  let y = 660
  for (const p of [...e.paragrafos, AVISO]) {
    let linha = ''
    for (const palavra of p.split(' ')) {
      const tentativa = linha ? `${linha} ${palavra}` : palavra
      if (normal.widthOfTextAtSize(tentativa, 11) > 480) { pagina.drawText(linha, { x: 56, y, size: 11, font: normal }); y -= 16; linha = palavra } else linha = tentativa
    }
    if (linha) { pagina.drawText(linha, { x: 56, y, size: 11, font: normal }); y -= 16 }
    y -= 10
  }
  return pdf.save({ useObjectStreams: false })
}

async function main() {
  const pastaDosArquivos = join(SITE, 'transparencia', 'arquivos')
  mkdirSync(pastaDosArquivos, { recursive: true })
  const publicadoEm = AGORA.toISOString()

  const documentos: DocumentoNoPortal[] = []
  for (const [i, e] of EXEMPLOS.entries()) {
    const bytes = await pdfDeExemplo(e)
    writeFileSync(join(pastaDosArquivos, e.arquivo), bytes)
    const sha256 = createHash('sha256').update(bytes).digest('hex')
    documentos.push({
      id: `exemplo-${i + 1}`, categoria: e.categoria, titulo: e.titulo, descricao: AVISO, periodo: e.periodo,
      atual: { nome: e.arquivo, tamanho: bytes.length, sha256, url: `${ORIGEM}/transparencia/arquivos/${e.arquivo}`, publicadoEm, codigo: null },
      anteriores: [],
    })
    console.log(`arquivo: transparencia/arquivos/${e.arquivo} (${bytes.length} bytes, SHA-256 ${sha256.slice(0, 12)}…)`)
  }

  // Faixa de demonstração no topo: o portal de verdade (o da Redação) não tem esta faixa.
  const FAIXA = `<p style="margin:0 0 18px;padding:12px 16px;border-radius:12px;background:#fff5f5;border:1px solid #f3c7c7;color:#a30000;font-weight:700">Página de demonstração: os documentos abaixo são exemplos e serão trocados pelos documentos oficiais da filial. Eles ainda não têm código de verificação, que nasce na trilha pública de auditoria.</p>`
  const portal = paginaDaTransparencia({ documentos, parcerias: [], agora: AGORA, indexar: false })
    .replace('<p class="pt-olho">Portal da transparência</p>', `${FAIXA}\n        <p class="pt-olho">Portal da transparência</p>`)
  if (!portal.includes(FAIXA)) throw new Error('Não achei onde pôr a faixa de demonstração no portal.')
  writeFileSync(join(SITE, 'transparencia', 'index.html'), portal)
  writeFileSync(join(SITE, 'transparencia', '.htaccess'), htaccessDoPortal(false))

  const f = DADOS_DA_FILIAL
  const canais: Canal[] = [
    { tipo: 'site', rotulo: 'Site', valor: 'cruzvermelhapetropolis.org', url: `${ORIGEM}/` },
    { tipo: 'email', rotulo: 'E-mail', valor: f.email, url: `mailto:${f.email}` },
    ...f.telefones.map((t): Canal => ({ tipo: 'whatsapp', rotulo: 'Telefone e WhatsApp', valor: t, url: `https://wa.me/55${t.replace(/\D/g, '')}` })),
    { tipo: 'instagram', rotulo: 'Instagram', valor: `@${f.instagram}`, url: `https://www.instagram.com/${f.instagram}/` },
    { tipo: 'endereco', rotulo: 'Endereço', valor: 'Rua Carlos Gomes, 6 — Centro, Petrópolis/RJ, CEP 25680-120', url: null },
    { tipo: 'cnpj', rotulo: 'CNPJ', valor: f.cnpj, url: null },
  ]
  const paginaDeCanais = paginaDosCanais({
    versao: 1, canais, observacao: 'A filial não pede doações por mensagem de pessoas físicas nem em contas de terceiros: doe só pela página Doe deste site.',
    publicadoEm, codigo: null, hash: null, chaveId: null, agora: AGORA, indexar: false,
  })
  // Sem a trilha no ar, a frase de que a lista "é registrada" ainda não vale: vai no futuro.
  const FRASE = 'Esta lista é registrada na trilha pública de auditoria a cada versão: não muda sem deixar registro.'
  if (!paginaDeCanais.includes(FRASE)) throw new Error('Não achei a frase da trilha na página de canais.')
  mkdirSync(join(SITE, 'canais-oficiais'), { recursive: true })
  writeFileSync(join(SITE, 'canais-oficiais', 'index.html'), paginaDeCanais.replace(FRASE,
    'Quando a trilha pública de auditoria da filial entrar no ar, cada versão desta lista será registrada nela: não mudará sem deixar registro.'))
  writeFileSync(join(SITE, 'canais-oficiais', '.htaccess'), htaccessDoPortal(false))
  console.log('páginas: transparencia/index.html e canais-oficiais/index.html')
}

main().catch((e) => { console.error(e); process.exit(1) })
