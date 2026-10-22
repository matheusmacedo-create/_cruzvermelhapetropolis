/**
 * Os dados oficiais da filial (os mesmos do rodapé do site), usados nos
 * ofícios, nas compras, no termo de imagem, nos canais oficiais e na
 * verificação pública.
 *
 * As páginas jurídicas não moram mais aqui: a Política de Privacidade, os
 * Termos de Uso, a Política de Cookies e a de Cancelamento e reembolso, em
 * português, inglês e espanhol, são do repositório do site, que as gera e
 * publica (scripts/gerar_politicas.py, com o texto dos três idiomas em
 * site/politicas.json). O Palácio Virtual não grava mais /privacidade/ nem
 * /termos/. Mudou o que ele coleta de quem visita o site (newsletter, bloco de
 * medição), o texto muda lá.
 */
export const DADOS_DA_FILIAL = {
  nome: 'Cruz Vermelha Brasileira — Filial do Município de Petrópolis',
  cnpj: '09.198.238/0001-48',
  endereco: 'Rua Carlos Gomes, 6 — Centro, Petrópolis/RJ, CEP 25680-120',
  email: 'cvbpetropolis@gmail.com',
  telefone: '(24) 2243-4758',
} as const
