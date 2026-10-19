#!/usr/bin/env python3
"""reuniao.py — áudio/vídeo de reunião → transcricao.txt + ata.md + tarefas.md (kit IA de Elite).

Tudo local por padrão:
  1. Transcrição no seu computador com faster-whisper (se instalado).
     Também aceita uma transcrição pronta (.txt, .srt, .vtt, .md).
  2. Ata e tarefas por um destes motores (--motor):
       auto    → claude (CLI do Claude Code, pela sua assinatura) se existir; senão ollama; senão prompt
       claude  → `claude -p` (assinatura; a variável ANTHROPIC_API_KEY é removida do ambiente)
       ollama  → modelo local do Ollama (`ollama run <modelo>`)
       prompt  → não chama nada: grava prompt-para-colar.md para você colar em qualquer chat
       regra   → extração simples por regras (sem IA, sem rede) — é o que o --simular usa
Nunca chama API paga (OpenAI, Groq, OpenRouter, Anthropic API).

Exemplos:
  python3 reuniao.py reuniao.mp3
  python3 reuniao.py reuniao.mp4 --modelo-whisper medium --saida ata-2026-10-19
  python3 reuniao.py transcricao.txt --motor ollama --ollama-modelo qwen2.5:7b
  python3 reuniao.py --simular            # usa a transcrição de exemplo do kit, sem rede

Formato que ajuda a regra simples: uma fala por linha, "Nome: o que disse".
"""
import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EXEMPLO = AQUI.parent / "exemplos" / "reuniao-exemplo.txt"
TEXTO_EXT = {".txt", ".srt", ".vtt", ".md"}
EXIT_SEM_WHISPER = 3

PROMPT = """Você é meu assistente executivo. Abaixo está a transcrição de uma reunião.
Responda em português, exatamente neste formato, sem nada antes ou depois:

=== ATA ===
# Ata da reunião
- Assunto e participantes
- Decisões tomadas (uma por linha)
- Pontos em aberto

=== TAREFAS ===
# Tarefas
| Responsável | O que fazer | Prazo | Trecho da fala |
|---|---|---|---|
(uma linha por tarefa)

Regras: só tarefas que alguém assumiu ou recebeu de verdade, não invente.
Prazo não dito = "sem prazo". Responsável não claro = "a definir".

Transcrição:
"""

DIAS = r"(?:segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo)(?:-feira)?"
PRAZO_RE = re.compile(
    r"\b(?:até|ate|para|pra)\s+(?:a\s+|o\s+)?("
    + DIAS
    + r"|amanhã|amanha|hoje|semana que vem|próxima semana|proxima semana|fim do mês|fim do mes"
    r"|dia\s+\d{1,2}(?:/\d{1,2})?|\d{1,2}/\d{1,2})",
    re.IGNORECASE,
)
SOLTO_RE = re.compile(r"\b(amanhã|amanha|hoje|semana que vem)\b", re.IGNORECASE)
ASSUME_RE =re.compile(r"\b(?:eu\s+)?(?:vou|fico com|deixa comigo|me encarrego|eu faço|eu faco)\b", re.IGNORECASE)
PEDE_RE = re.compile(r"^\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+)\s*,\s*(?:você|voce|vc)\s+(?:pode|consegue|fica|vai)\b(.*)", re.IGNORECASE)
FICA_RE = re.compile(r"\bfica com (?:o |a )?([A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+)\b")
DECIDE_RE = re.compile(r"\b(?:decidido|decidimos|fechado|combinado|vamos com|ficou decidido)\b", re.IGNORECASE)
FALA_RE = re.compile(r"^\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+(?: [A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+)?)\s*:\s*(.+)$")


def ler_texto(caminho: Path) -> str:
    bruto = caminho.read_text(encoding="utf-8", errors="replace")
    if caminho.suffix.lower() in {".srt", ".vtt"}:
        linhas = []
        for ln in bruto.splitlines():
            s = ln.strip()
            if not s or s.isdigit() or "-->" in s or s.upper() == "WEBVTT":
                continue
            linhas.append(s)
        return "\n".join(linhas)
    return bruto.strip()


def transcrever(caminho: Path, modelo: str, idioma: str) -> str:
    try:
        from faster_whisper import WhisperModel  # noqa: import local
    except ImportError:
        print(
            "faster-whisper não está instalado, então não dá para transcrever o áudio aqui.\n"
            "Opções:\n"
            "  1) Instale (roda no seu computador, grátis):  pip install faster-whisper\n"
            "  2) Transcreva em outro lugar e passe o .txt/.srt:  python3 reuniao.py transcricao.txt\n"
            "  3) Teste o fluxo sem áudio:  python3 reuniao.py --simular",
            file=sys.stderr,
        )
        sys.exit(EXIT_SEM_WHISPER)
    print(f"[reuniao] transcrevendo {caminho.name} com faster-whisper ({modelo}) — local, pode levar alguns minutos…", file=sys.stderr)
    dispositivo = "cuda" if shutil.which("nvidia-smi") else "cpu"
    tipo = "float16" if dispositivo == "cuda" else "int8"
    try:
        wm = WhisperModel(modelo, device=dispositivo, compute_type=tipo)
    except Exception:
        wm = WhisperModel(modelo, device="cpu", compute_type="int8")
    segmentos, _info = wm.transcribe(str(caminho), language=idioma or None, vad_filter=True)
    return "\n".join(s.text.strip() for s in segmentos if s.text.strip())


def extrair_por_regra(texto: str):
    """Extração simples, sem IA: falas 'Nome: texto' com verbo de compromisso viram tarefa."""
    tarefas, decisoes, participantes = [], [], []
    for ln in texto.splitlines():
        m = FALA_RE.match(ln)
        if not m:
            continue
        quem, fala = m.group(1).strip(), m.group(2).strip()
        if quem not in participantes:
            participantes.append(quem)
        if DECIDE_RE.search(fala):
            decisoes.append(fala)
        dono = None
        p = PEDE_RE.match(fala)
        f = FICA_RE.search(fala)
        if p:
            dono = p.group(1)
        elif f:
            dono = f.group(1)
        elif ASSUME_RE.search(fala):
            dono = quem
        if not dono:
            continue
        pz = PRAZO_RE.search(fala) or SOLTO_RE.search(fala)
        prazo = pz.group(1) if pz else "sem prazo"
        oque = re.sub(r"\s+", " ", fala).strip().rstrip(".")
        tarefas.append({"dono": dono, "oque": oque, "prazo": prazo, "trecho": f"{quem}: {fala}"})
    return participantes, decisoes, tarefas


def montar_md_regra(texto: str, origem: str):
    participantes, decisoes, tarefas = extrair_por_regra(texto)
    hoje = dt.date.today().isoformat()
    ata = [f"# Ata da reunião ({hoje})", "", f"- Origem: {origem}", f"- Participantes: {', '.join(participantes) or 'não identificados'}", "", "## Decisões"]
    ata += [f"- {d}" for d in decisoes] or ["- nenhuma decisão explícita encontrada"]
    ata += ["", "## Observação", "- Gerado pela regra simples (sem IA). Para uma ata melhor, rode com --motor claude ou ollama."]
    tab = ["# Tarefas", "", "| Responsável | O que fazer | Prazo | Trecho da fala |", "|---|---|---|---|"]
    for t in tarefas:
        cel = lambda s: s.replace("|", "/")
        tab.append(f"| {cel(t['dono'])} | {cel(t['oque'])} | {cel(t['prazo'])} | {cel(t['trecho'])} |")
    if not tarefas:
        tab.append("| a definir | nenhuma tarefa encontrada pela regra simples | sem prazo | — |")
    return "\n".join(ata) + "\n", "\n".join(tab) + "\n", len(tarefas)


def rodar_claude(prompt: str) -> str:
    amb = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    r = subprocess.run(["claude", "-p"], input=prompt, text=True, capture_output=True, env=amb, timeout=900)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"claude -p falhou (rc={r.returncode}): {r.stderr.strip()[:300]}")
    return r.stdout


def rodar_ollama(prompt: str, modelo: str) -> str:
    r = subprocess.run(["ollama", "run", modelo], input=prompt, text=True, capture_output=True, timeout=1800)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"ollama falhou (rc={r.returncode}): {r.stderr.strip()[:300]}")
    return r.stdout


def separar(resposta: str):
    if "=== TAREFAS ===" in resposta:
        a, t = resposta.split("=== TAREFAS ===", 1)
        a = a.replace("=== ATA ===", "").strip()
        return a + "\n", t.strip() + "\n"
    return resposta.strip() + "\n", "# Tarefas\n\n(o modelo não separou as tarefas; veja ata.md)\n"


def escolher_motor(pedido: str) -> str:
    if pedido != "auto":
        return pedido
    if shutil.which("claude"):
        return "claude"
    if shutil.which("ollama"):
        return "ollama"
    return "prompt"


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="reuniao.py",
        description="Reunião (áudio/vídeo ou transcrição) → ata.md + tarefas.md. Local, sem API paga.",
    )
    ap.add_argument("entrada", nargs="?", help="áudio/vídeo (mp3, wav, m4a, mp4…) ou transcrição (.txt, .srt, .vtt, .md)")
    ap.add_argument("--saida", default=None, help="pasta de saída (padrão: reuniao-AAAA-MM-DD ao lado da entrada)")
    ap.add_argument("--motor", default="auto", choices=["auto", "claude", "ollama", "prompt", "regra"])
    ap.add_argument("--ollama-modelo", default="qwen2.5:7b", help="modelo do Ollama (padrão: qwen2.5:7b)")
    ap.add_argument("--modelo-whisper", default="small", help="tiny, base, small, medium, large-v3 (padrão: small)")
    ap.add_argument("--idioma", default="pt", help="idioma do áudio (padrão: pt; vazio = detectar)")
    ap.add_argument("--simular", action="store_true", help="sem rede e sem IA: usa a transcrição de exemplo (ou a entrada .txt) e a regra simples")
    a = ap.parse_args(argv)

    if a.simular:
        fonte = Path(a.entrada) if a.entrada else EXEMPLO
        if not fonte.exists():
            ap.error(f"transcrição não encontrada: {fonte}")
        texto = ler_texto(fonte)
        motor = "regra"
    else:
        if not a.entrada:
            ap.error("informe o arquivo da reunião (ou use --simular)")
        fonte = Path(a.entrada)
        if not fonte.exists():
            ap.error(f"arquivo não encontrado: {fonte}")
        texto = ler_texto(fonte) if fonte.suffix.lower() in TEXTO_EXT else transcrever(fonte, a.modelo_whisper, a.idioma)
        motor = escolher_motor(a.motor)

    saida = Path(a.saida) if a.saida else fonte.resolve().parent / f"reuniao-{dt.date.today().isoformat()}"
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "transcricao.txt").write_text(texto + "\n", encoding="utf-8")

    if motor == "regra":
        ata, tarefas, n = montar_md_regra(texto, fonte.name)
        (saida / "ata.md").write_text(ata, encoding="utf-8")
        (saida / "tarefas.md").write_text(tarefas, encoding="utf-8")
        print(f"[reuniao] motor=regra · {n} tarefa(s) · {saida}/ata.md e tarefas.md")
        return 0

    prompt = PROMPT + texto
    if motor == "prompt":
        (saida / "prompt-para-colar.md").write_text(prompt + "\n", encoding="utf-8")
        print(f"[reuniao] sem claude/ollama: cole {saida}/prompt-para-colar.md no ChatGPT, Claude ou Gemini.")
        return 0

    try:
        resposta = rodar_claude(prompt) if motor == "claude" else rodar_ollama(prompt, a.ollama_modelo)
    except Exception as e:  # cai para o prompt de colar, sem perder a transcrição
        (saida / "prompt-para-colar.md").write_text(prompt + "\n", encoding="utf-8")
        print(f"[reuniao] {e}\n[reuniao] transcrição salva; cole {saida}/prompt-para-colar.md em qualquer chat.", file=sys.stderr)
        return 1
    ata, tarefas = separar(resposta)
    (saida / "ata.md").write_text(ata, encoding="utf-8")
    (saida / "tarefas.md").write_text(tarefas, encoding="utf-8")
    print(f"[reuniao] motor={motor} · {saida}/ata.md e tarefas.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
