#!/usr/bin/env bash
# ditado.sh — fale, não digite (kit IA de Elite). Linux, tudo local, grátis.
# Grava o microfone, transcreve com faster-whisper no seu computador e copia o texto.
#
# Uso:
#   bash ditado.sh                         grava até você apertar Enter
#   bash ditado.sh --segundos 30           grava 30 segundos
#   bash ditado.sh --arquivo fala.wav      transcreve um áudio pronto (sem gravar)
#   bash ditado.sh --modelo small          tiny|base|small|medium|large-v3 (padrão: base)
#   bash ditado.sh --idioma pt             idioma (padrão: pt)
#   bash ditado.sh --vocab "INEMA, Claude Code"   palavras que o Whisper deve acertar
#   bash ditado.sh --checar                mostra o que está instalado e sai
#   bash ditado.sh --help
set -uo pipefail

SEG=0; ARQ=""; MODELO="base"; IDIOMA="pt"; VOCAB=""; CHECAR=0
while [ $# -gt 0 ]; do case "$1" in
  --segundos) SEG="$2"; shift 2;;
  --arquivo) ARQ="$2"; shift 2;;
  --modelo) MODELO="$2"; shift 2;;
  --idioma) IDIOMA="$2"; shift 2;;
  --vocab) VOCAB="$2"; shift 2;;
  --checar) CHECAR=1; shift;;
  -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
  *) echo "opção desconhecida: $1 (use --help)" >&2; exit 2;;
esac; done

tem(){ command -v "$1" >/dev/null 2>&1; }
tem_fw(){ python3 -c "import faster_whisper" >/dev/null 2>&1; }

if [ "$CHECAR" = 1 ]; then
  for c in python3 arecord ffmpeg xclip wl-copy; do
    if tem "$c"; then echo "ok    $c"; else echo "falta $c"; fi
  done
  if tem_fw; then echo "ok    faster-whisper"; else echo "falta faster-whisper  (pip install faster-whisper)"; fi
  exit 0
fi

if ! tem_fw; then
  echo "faster-whisper não instalado. Instale (grátis, local):  pip install faster-whisper" >&2
  echo "No Windows use Win+H; no macOS, Fn duas vezes. Veja ditado.md." >&2
  exit 3
fi

TMP=""
if [ -z "$ARQ" ]; then
  TMP="$(mktemp --suffix=.wav)"; ARQ="$TMP"
  trap '[ -n "$TMP" ] && rm -f "$TMP"' EXIT
  if tem arecord; then GRAVA=(arecord -q -f S16_LE -r 16000 -c 1); [ "$SEG" -gt 0 ] && GRAVA+=(-d "$SEG"); GRAVA+=("$ARQ")
  elif tem ffmpeg; then GRAVA=(ffmpeg -loglevel error -y -f pulse -i default -ac 1 -ar 16000); [ "$SEG" -gt 0 ] && GRAVA+=(-t "$SEG"); GRAVA+=("$ARQ")
  else echo "sem gravador: instale alsa-utils (arecord) ou ffmpeg" >&2; exit 4; fi
  if [ "$SEG" -gt 0 ]; then
    echo "🎙  gravando ${SEG}s… fale agora." >&2; "${GRAVA[@]}"
  else
    echo "🎙  gravando… fale e aperte Enter para parar." >&2
    "${GRAVA[@]}" & PID=$!; read -r _; kill -INT "$PID" 2>/dev/null; wait "$PID" 2>/dev/null
  fi
fi
[ -s "$ARQ" ] || { echo "áudio vazio: $ARQ" >&2; exit 5; }

echo "📝 transcrevendo (local, modelo $MODELO)…" >&2
TEXTO="$(ARQ="$ARQ" MODELO="$MODELO" IDIOMA="$IDIOMA" VOCAB="$VOCAB" python3 - <<'PY'
import os, shutil
from faster_whisper import WhisperModel
dev = "cuda" if shutil.which("nvidia-smi") else "cpu"
try:
    m = WhisperModel(os.environ["MODELO"], device=dev, compute_type="float16" if dev == "cuda" else "int8")
except Exception:
    m = WhisperModel(os.environ["MODELO"], device="cpu", compute_type="int8")
segs, _ = m.transcribe(os.environ["ARQ"], language=os.environ.get("IDIOMA") or None,
                       initial_prompt=os.environ.get("VOCAB") or None, vad_filter=True)
print(" ".join(s.text.strip() for s in segs).strip())
PY
)"
echo "$TEXTO"
if tem wl-copy && [ -n "${WAYLAND_DISPLAY:-}" ]; then printf '%s' "$TEXTO" | wl-copy && echo "(copiado)" >&2
elif tem xclip && [ -n "${DISPLAY:-}" ]; then printf '%s' "$TEXTO" | xclip -selection clipboard && echo "(copiado)" >&2
fi
