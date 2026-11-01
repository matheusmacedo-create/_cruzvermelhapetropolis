# Cruz Vermelha Brasileira – Filial de Petrópolis · site institucional

A página de `cruzvermelhapetropolis.org` (Hostinger, `public_html/`) sai de
`scripts/gerar_site_petropolis.py`, que grava as páginas em `site/`:

```sh
python3 pagina/scripts/gerar_site_petropolis.py
```

- `site/` — o que vai para o servidor: páginas, `assets/`, o chat (`chat/`) e a
  doação (`doe/`, com a biblioteca do checkout em `doe/api/nucleo/`).
- As chaves da doação ficam **só no servidor**, em
  `public_html/doe/api/nucleo/config.php` (modelo em `site/doe/api/config.example.php`).
- Publique **só os arquivos alterados**: `hosting_websites_deploy-static-site-archive`
  apaga o que não está no pacote, inclusive o `config.php`.

O que ainda falta trocar e o histórico da filial estão em
[`../docs/PETROPOLIS.md`](../docs/PETROPOLIS.md).
