#!/usr/bin/env bash
# testes/rodar.sh — valida o kit IA de Elite sem rede e sem API.
# Uso: bash kit/testes/rodar.sh   (de qualquer pasta)
set -uo pipefail
KIT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
OK=0; FALHA=0
ok(){ echo "ok    $1"; OK=$((OK+1)); }
nok(){ echo "FALHA $1"; FALHA=$((FALHA+1)); }
checa(){ local nome="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$nome"; else nok "$nome"; fi; }

# sem rede nem chave: nada abaixo pode depender disso
unset ANTHROPIC_API_KEY OPENAI_API_KEY GROQ_API_KEY OPENROUTER_API_KEY

# 1. prompts: 7 arquivos, não vazios, com bloco de prompt
n=$(ls "$KIT"/prompts/0[1-7]-*.md 2>/dev/null | wc -l)
[ "$n" -eq 7 ] && ok "7 prompts" || nok "7 prompts (achei $n)"
for f in "$KIT"/prompts/*.md; do
  if [ "$(wc -w < "$f")" -ge 40 ] && grep -q '^```text' "$f"; then ok "prompt $(basename "$f")"; else nok "prompt $(basename "$f") vazio ou sem bloco"; fi
done

# 2. skills: 4, com frontmatter name = pasta e description
for s in entrevista-me fure-minha-ideia mostra-nao-conta testa-agora; do
  f="$KIT/skills/$s/SKILL.md"
  if [ -f "$f" ] && [ "$(head -1 "$f")" = "---" ] \
     && sed -n '2,6p' "$f" | grep -qx "name: $s" \
     && sed -n '2,6p' "$f" | grep -qE '^description: .{40,}' \
     && [ "$(awk '/^---$/{c++} END{print c}' "$f")" -ge 2 ]; then ok "skill $s"; else nok "skill $s (frontmatter)"; fi
done

# 3. scripts: sintaxe e --help
checa "reuniao.py compila" python3 -m py_compile "$KIT/scripts/reuniao.py"
checa "reuniao.py --help" python3 "$KIT/scripts/reuniao.py" --help
checa "ditado.sh sintaxe" bash -n "$KIT/scripts/ditado.sh"
checa "ditado.sh --help" bash "$KIT/scripts/ditado.sh" --help
checa "ditado.sh --checar" bash "$KIT/scripts/ditado.sh" --checar
checa "instalar.sh sintaxe" bash -n "$KIT/instalar.sh"

# 4. reuniao.py --simular: transcrição de exemplo → tarefas por regra
if python3 "$KIT/scripts/reuniao.py" --simular --saida "$TMP/sim" >/dev/null 2>&1; then
  T="$TMP/sim/tarefas.md"
  [ -s "$TMP/sim/ata.md" ] && [ -s "$TMP/sim/transcricao.txt" ] && ok "simular gera ata.md e transcricao.txt" || nok "simular: faltou ata/transcrição"
  grep -q '| Responsável | O que fazer | Prazo |' "$T" && ok "tarefas.md tem a tabela" || nok "tarefas.md sem tabela"
  grep -qE '^\| Paulo \|.*\| sexta \|' "$T" && ok "tarefa: Paulo até sexta" || nok "tarefa: Paulo até sexta"
  grep -qE '^\| Bia \|.*\| quarta \|' "$T" && ok "tarefa: Bia até quarta" || nok "tarefa: Bia até quarta"
  grep -qE '^\| Rafael \|.*\| amanhã \|' "$T" && ok "tarefa: Rafael amanhã" || nok "tarefa: Rafael amanhã"
  grep -q '30/10' "$TMP/sim/ata.md" && ok "ata registra a decisão 30/10" || nok "ata sem a decisão 30/10"
else
  nok "reuniao.py --simular rodou"
fi

# 5. reuniao.py --motor prompt com .txt: não chama nada, grava o prompt de colar
if python3 "$KIT/scripts/reuniao.py" "$KIT/exemplos/reuniao-exemplo.txt" --motor prompt --saida "$TMP/p" >/dev/null 2>&1 \
   && grep -q 'Transcrição:' "$TMP/p/prompt-para-colar.md" && grep -q 'Marina:' "$TMP/p/prompt-para-colar.md"; then
  ok "motor prompt gera prompt-para-colar.md"; else nok "motor prompt"; fi

# 6. áudio sem faster-whisper → orienta e sai com 3 (só testa se não estiver instalado)
if ! python3 -c "import faster_whisper" 2>/dev/null; then
  : > "$TMP/x.mp3"
  python3 "$KIT/scripts/reuniao.py" "$TMP/x.mp3" --saida "$TMP/a" >/dev/null 2>"$TMP/err"; rc=$?
  [ "$rc" -eq 3 ] && grep -q 'pip install faster-whisper' "$TMP/err" && ok "sem faster-whisper: orienta (rc 3)" || nok "sem faster-whisper (rc $rc)"
fi

# 7. instalar.sh em pasta temporária (nunca na ~/.claude real)
if bash "$KIT/instalar.sh" --destino "$TMP/skills" >/dev/null 2>&1 && [ "$(ls "$TMP/skills" | wc -l)" -eq 4 ]; then
  ok "instalar.sh copia 4 skills"; else nok "instalar.sh"; fi
saida_inst="$(bash "$KIT/instalar.sh" --destino "$TMP/skills" 2>&1)"
grep -q 'pulei' <<<"$saida_inst" && ok "instalar.sh não sobrescreve sem --forcar" || nok "instalar.sh sobrescreveu"

# 8. nada de API paga no código do kit
if grep -rniE 'api\.openai\.com|api\.groq\.com|openrouter\.ai|api\.anthropic\.com' "$KIT/scripts" "$KIT/instalar.sh" >/dev/null; then
  nok "kit cita endpoint de API paga"; else ok "nenhuma API paga no código"; fi

# 9. exemplo do mostra-nao-conta é um HTML único
f="$KIT/exemplos/painel-falar-vs-digitar.html"
grep -q '<style>' "$f" && grep -q '</html>' "$f" && ! grep -qE '<link[^>]+stylesheet' "$f" && ok "exemplo HTML auto-contido" || nok "exemplo HTML"

echo "----"
echo "$OK ok · $FALHA falha(s)"
[ "$FALHA" -eq 0 ]
