/**
 * Os textos do papel timbrado da filial (Manual de Identidade Institucional
 * da CVB, p. 24), sem o desenho: o PDF (lib/pdf/timbrado.ts) e a folha do
 * ofício na tela (components/app/oficios/documento.tsx) usam os mesmos.
 *
 * Do manual vale o desenho; os contatos dele estão desatualizados. Os dados
 * da filial vêm de DADOS_DA_FILIAL (lib/site/juridico.ts).
 */
import { DADOS_DA_FILIAL } from '@/lib/site/juridico'

/** No alto, à direita, em três linhas como no manual (Franklin Book 8). */
export const LINHAS_DO_DECRETO = ['Reconhecida como Utilidade', 'Pública Internacional - Decreto', 'nº 9.620, de 13/06/1912'] as const

/** "Filial do Município de Petrópolis", tirado do nome completo. */
export const NOME_DA_FILIAL = DADOS_DA_FILIAL.nome.split(/\s+[—–-]\s+/)[1] ?? DADOS_DA_FILIAL.nome

/** O rodapé centrado (Franklin Book 8): o nome nas três línguas do manual e os contatos atuais. */
export function linhasDoRodape(): string[] {
  return [
    'Cruz Vermelha Brasileira | Brazilian Red Cross | Cruz Roja Brasileña',
    `${NOME_DA_FILIAL} | CNPJ ${DADOS_DA_FILIAL.cnpj}`,
    DADOS_DA_FILIAL.endereco,
    [`Telefone ${DADOS_DA_FILIAL.telefone}`, siteDaFilial(), `e-mail ${DADOS_DA_FILIAL.email}`].filter(Boolean).join(' | '),
  ]
}

/**
 * O site é o domínio do e-mail oficial. Enquanto o e-mail for de webmail
 * (Petrópolis usa um do Gmail até ter domínio próprio), não há site a mostrar.
 */
function siteDaFilial(): string | null {
  const dominio = DADOS_DA_FILIAL.email.split('@')[1] ?? ''
  return /^(gmail|googlemail|hotmail|outlook|yahoo)\./i.test(dominio) ? null : dominio
}
