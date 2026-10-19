# 🧠 IA de Élite — 7 hábitos de quienes usan la IA al máximo nivel

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

IA de Élite es una guía con los 7 hábitos que separan a quien usa la IA de verdad de quien solo hace preguntas sueltas en el chat: hablar en lugar de escribir, dejar que la IA escuche la reunión, pedir visuales en lugar de texto, ser entrevistado por la IA, pedir fallas, probar con tus propias manos y mantener la mente abierta. Sirve para cualquier persona que ya use ChatGPT, Claude o Gemini. Junto con la guía viene un kit abierto y gratuito con 7 prompts para copiar, 4 skills para Claude Code y scripts que corren en tu computadora. Para los prompts basta un chat; para los scripts, Python.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/ia-de-elite/guia/es/**

## Los 7 hábitos

| # | Hábito | En el kit |
|---|---|---|
| 1 | **Habla, no escribas** — en promedio 30–50 palabras/min escribiendo × 150–200 hablando | `prompts/01`, `scripts/ditado.md`, `scripts/ditado.sh` |
| 2 | **La IA escuchando la reunión** — la transcripción se convierte en acta y tareas (quién, qué, plazo) | `scripts/reuniao.py`, `prompts/02` |
| 3 | **Muestra, no cuentes** — HTML, gráficos, 3D en lugar de texto | `prompts/03`, skill `mostra-nao-conta` |
| 4 | **La IA te entrevista** — "hazme todas las preguntas que necesites" | `prompts/04`, skill `entrevista-me` |
| 5 | **Pide fallas, no opinión** — la IA tiende a estar de acuerdo; pide lo que está mal | `prompts/05`, skill `fure-minha-ideia` |
| 6 | **Pruébalo tú mismo** — pide que lo haga en lugar de preguntar si puede | `prompts/06`, skill `testa-agora` |
| 7 | **Mente abierta** — probar es barato, no probar sale caro | `prompts/07` |

## El kit

```
kit/
├── prompts/        7 prompts listos (uno por hábito)
├── skills/         entrevista-me · fure-minha-ideia · mostra-nao-conta · testa-agora
├── scripts/        reuniao.py · ditado.sh · ditado.md
├── exemplos/       reuniao-exemplo.txt · painel-falar-vs-digitar.html
├── testes/rodar.sh valida el kit sin red y sin API
└── instalar.sh     copia las skills a ~/.claude/skills/
```

## Inicio rápido

```bash
git clone https://github.com/inematds/ia-de-elite.git && cd ia-de-elite
bash kit/testes/rodar.sh                          # 30 ok · 0 falha(s)
python3 kit/scripts/reuniao.py --simular --saida teste-reuniao
bash kit/instalar.sh --dry-run                    # después sin --dry-run
```

- **reuniao.py**: audio/video (o .txt/.srt) → `transcricao.txt`, `ata.md`, `tarefas.md`. Transcribe **en tu computadora** con faster-whisper (`pip install faster-whisper`). El acta sale por `claude -p` (suscripción de Claude Code), por Ollama local o como prompt para pegar en cualquier chat (`--motor prompt`). Nunca llama a una API de pago.
- **ditado.sh** (Linux): graba, transcribe en local y copia el texto. Windows: `Win + H`. macOS: `Fn` dos veces.

Abierto y gratuito · licencia MIT · [INEMA.CLUB](https://inema.club)
