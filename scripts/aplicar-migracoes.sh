#!/usr/bin/env bash
# Aplica, em ordem, as migrações de supabase/migrations/ que o banco ainda não tem.
# Feito para montar o banco de Petrópolis do zero (o conector do Supabase trava em
# migração que apaga dados) e serve para as próximas: roda pelo GitHub Actions
# (.github/workflows/aplicar-migracoes.yml) com o Secret SUPABASE_DB_URL.
#
# Cada arquivo roda numa transação só, junto com o registro em
# supabase_migrations.schema_migrations: ou entra inteiro e anotado, ou nada muda.
# Já aplicada = mesmo nome (as primeiras foram pelo conector, que anota a hora da
# aplicação como versão). Há arquivos com o mesmo timestamp: o segundo é anotado
# com versão "<timestamp>_<nome>".
#
# Variáveis:
#   SUPABASE_DB_URL   conexão do Session pooler, com a senha (nunca no código)
#   PROJETO_ESPERADO  ref do projeto; a URL precisa conter este texto, para não
#                     aplicar no banco errado (ex.: o do RJ)
#   SO_LISTAR=1       mostra o que seria aplicado e para
set -euo pipefail

RAIZ=$(cd "$(dirname "$0")/.." && pwd)
PSQL=${PSQL:-psql}

for v in SUPABASE_DB_URL PROJETO_ESPERADO; do
  [ -n "${!v:-}" ] || { echo "Falta a variável $v." >&2; exit 1; }
done
case "$SUPABASE_DB_URL" in
  *"$PROJETO_ESPERADO"*) ;;
  *) echo "A conexão não é do projeto $PROJETO_ESPERADO. Nada foi feito." >&2; exit 1 ;;
esac

sql() { PGOPTIONS='-c client_min_messages=warning' "$PSQL" "$SUPABASE_DB_URL" -X -A -t -q -v ON_ERROR_STOP=1 "$@"; }

sql -c "create schema if not exists supabase_migrations;
        create table if not exists supabase_migrations.schema_migrations (
          version text primary key, statements text[], name text);" >/dev/null

aplicadas=$(sql -c "select version || '|' || coalesce(name, '') from supabase_migrations.schema_migrations")

n=0; pulou=0
for f in $(ls "$RAIZ"/supabase/migrations/*.sql | sort); do
  base=$(basename "$f" .sql)
  versao=${base%%_*}
  nome=${base#*_}
  if grep -qE "\|${nome}\$" <<<"$aplicadas"; then
    pulou=$((pulou + 1)); continue
  fi
  if [ "${SO_LISTAR:-}" = 1 ]; then echo "aplicaria: $base"; n=$((n + 1)); continue; fi
  echo "aplicando: $base"
  if ! { cat "$f"; printf '\n;\ninsert into supabase_migrations.schema_migrations (version, name)
select case when exists (select 1 from supabase_migrations.schema_migrations where version = %s)
            then %s else %s end, %s;\n' "'$versao'" "'${versao}_${nome}'" "'$versao'" "'$nome'"; } | sql --single-transaction >/dev/null; then
    echo "FALHOU: $base (nada desta migração ficou no banco; as anteriores ficaram)." >&2
    exit 1
  fi
  n=$((n + 1))
done
echo "ok: $n aplicada(s), $pulou já estavam no banco."
