-- Nomes de Petrópolis no que as migrações herdadas do RJ gravam no banco.
--
-- O banco de Petrópolis nasce das mesmas migrações do RJ, e elas não podem ser
-- editadas (só se acrescenta). Elas deixam o nome, o domínio e o CNPJ do RJ em
-- três lugares: no corpo de funções (sementes, trilha de auditoria, links das
-- parcerias e dos canais), em valores padrão de coluna e nas linhas semeadas
-- (empresa principal do financeiro, setores, mapa do ecossistema). Esta
-- migração, a última da fila, troca tudo pelo de Petrópolis. Idempotente: rodar
-- de novo não muda nada. Nomes do estado ("Petrópolis/RJ", "estado do Rio de
-- Janeiro") ficam como estão.

create function pg_temp.petropolis(t text) returns text language sql immutable as $$
  select replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
    t,
    'cruzvermelhariodejaneiro.org', 'cruzvermelhapetropolis.org'),
    'Cruz Vermelha Brasileira — Filial do Estado do Rio de Janeiro', 'Cruz Vermelha Brasileira — Filial do Município de Petrópolis'),
    'Cruz Vermelha Brasileira - Filial do Rio de Janeiro', 'Cruz Vermelha Brasileira - Filial de Petrópolis'),
    'Cruz Vermelha Brasileira – Filial do Rio de Janeiro', 'Cruz Vermelha Brasileira – Filial de Petrópolis'),
    'Cruz Vermelha Brasileira - Rio de Janeiro', 'Cruz Vermelha Brasileira - Petrópolis'),
    'Cruz Vermelha Brasileira Rio de Janeiro', 'Cruz Vermelha Brasileira Petrópolis'),
    'Filial Rio de Janeiro', 'Filial Petrópolis'),
    'Cruz Vermelha RJ', 'Cruz Vermelha Petrópolis'),
    'CVB-RJ', 'CVB Petrópolis'),
    '08560973000197', '09198238000148'),
    'Praça da Cruz Vermelha', 'Rua Carlos Gomes'),
    '"RIO DE JANEIRO"', '"PETRÓPOLIS"'),
    '"Rio de Janeiro"', '"Petrópolis"'),
    ' rio de janeiro''', ' petrópolis''')
$$;

-- 1. Funções: as que citam o RJ são recriadas com o texto trocado (mesma
--    assinatura, mesmas permissões: create or replace não mexe nos grants).
do $$
declare
  f record;
  novo text;
begin
  for f in
    select p.oid, pg_get_functiondef(p.oid) as def
    from pg_proc p
    join pg_namespace n on n.oid = p.pronamespace
    where n.nspname in ('public', 'private', 'auditoria')
      and p.prokind = 'f'
      and not exists (select 1 from pg_depend d where d.objid = p.oid and d.deptype = 'e')
      and (p.prosrc like '%cruzvermelhariodejaneiro.org%' or p.prosrc like '%Rio de Janeiro%'
           or p.prosrc like '%CVB-RJ%' or p.prosrc like '%Cruz Vermelha RJ%' or p.prosrc like '%08560973000197%')
  loop
    novo := pg_temp.petropolis(f.def);
    if novo <> f.def then
      execute novo;
    end if;
  end loop;
end $$;

-- 2. Valores padrão de coluna.
alter table public.oficios alter column local set default 'Petrópolis';
alter table public.pat_config alter column termo_padrao set default
  'Declaro que recebi o bem acima em boas condições, que ele pertence à Cruz Vermelha Brasileira – Filial de Petrópolis e que o usarei somente nas atividades da instituição. Comprometo-me a zelar por ele, a comunicar qualquer dano, perda ou furto assim que acontecer e a devolvê-lo quando pedido ou quando deixar a função.';
update public.pat_config
  set termo_padrao = replace(termo_padrao, 'Cruz Vermelha Brasileira – Filial do Rio de Janeiro', 'Cruz Vermelha Brasileira – Filial de Petrópolis')
  where termo_padrao like '%Cruz Vermelha Brasileira – Filial do Rio de Janeiro%';

-- 3. Linhas semeadas.
update public.fin_entidades
  set nome = 'Filial Petrópolis',
      razao_social = 'Cruz Vermelha Brasileira — Filial do Município de Petrópolis',
      cnpj = '09198238000148'
  where principal and cnpj = '08560973000197';

update public.setores
  set descricao = pg_temp.petropolis(descricao)
  where descricao is distinct from pg_temp.petropolis(descricao);

update public.mapa_itens
  set nome = pg_temp.petropolis(nome),
      descricao = pg_temp.petropolis(descricao),
      estado_detalhe = pg_temp.petropolis(estado_detalhe),
      url = pg_temp.petropolis(url),
      entregas = pg_temp.petropolis(entregas::text)::jsonb
  where nome is distinct from pg_temp.petropolis(nome)
     or descricao is distinct from pg_temp.petropolis(descricao)
     or estado_detalhe is distinct from pg_temp.petropolis(estado_detalhe)
     or url is distinct from pg_temp.petropolis(url)
     or entregas::text is distinct from pg_temp.petropolis(entregas::text);
