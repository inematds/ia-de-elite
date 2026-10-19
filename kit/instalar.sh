#!/usr/bin/env bash
# instalar.sh — copia as 4 skills do kit IA de Elite para o Claude Code.
# Só roda quando VOCÊ executar. Não instala pacotes, não usa rede.
#
# Uso:
#   bash kit/instalar.sh                 copia para ~/.claude/skills/
#   bash kit/instalar.sh --destino DIR   copia para outra pasta (ex.: .claude/skills de um projeto)
#   bash kit/instalar.sh --dry-run       só mostra o que faria
#   bash kit/instalar.sh --forcar        sobrescreve skill de mesmo nome já existente
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"; DRY=0; FORCAR=0
while [ $# -gt 0 ]; do case "$1" in
  --destino) DEST="$2"; shift 2;;
  --dry-run) DRY=1; shift;;
  --forcar) FORCAR=1; shift;;
  -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
  *) echo "opção desconhecida: $1" >&2; exit 2;;
esac; done

n=0
for d in "$AQUI"/skills/*/; do
  nome="$(basename "$d")"; alvo="$DEST/$nome"
  if [ -e "$alvo" ] && [ "$FORCAR" = 0 ]; then echo "pulei  $nome (já existe em $alvo; use --forcar)"; continue; fi
  if [ "$DRY" = 1 ]; then echo "copiaria $nome → $alvo"; n=$((n+1)); continue; fi
  mkdir -p "$DEST"; rm -rf "$alvo"; cp -r "$d" "$alvo"; echo "ok     $nome → $alvo"; n=$((n+1))
done
echo "$n skill(s). No Claude Code, peça: \"me entrevista antes de…\", \"fure minha ideia…\", \"mostra, não conta…\", \"testa agora…\"."
