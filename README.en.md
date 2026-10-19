# 🧠 Elite AI — 7 habits of people who use AI at the top

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Elite AI is a guide to the 7 habits that separate people who really use AI from people who just ask scattered questions in a chat: speak instead of typing, let the AI listen to the meeting, ask for visuals instead of text, be interviewed by the AI, ask for flaws, test with your own hands, and keep an open mind. It is for anyone who already uses ChatGPT, Claude or Gemini. It comes with an open, free kit: 7 prompts to copy, 4 skills for Claude Code, and scripts that run on your computer. For the prompts, a chat is all you need; for the scripts, Python.

## 📖 User guide

Full guide (landing page + step by step): **https://inematds.github.io/ia-de-elite/guia/en/**

## The 7 habits

| # | Habit | In the kit |
|---|---|---|
| 1 | **Speak, don't type** — on average 30–50 words/min typing vs. 150–200 speaking | `prompts/01`, `scripts/ditado.md`, `scripts/ditado.sh` |
| 2 | **AI listening to the meeting** — the transcript becomes minutes and tasks (who, what, deadline) | `scripts/reuniao.py`, `prompts/02` |
| 3 | **Show, don't tell** — HTML, charts, 3D instead of text | `prompts/03`, skill `mostra-nao-conta` |
| 4 | **The AI interviews you** — "ask me every question you need" | `prompts/04`, skill `entrevista-me` |
| 5 | **Ask for flaws, not opinions** — AI tends to agree; ask what is wrong | `prompts/05`, skill `fure-minha-ideia` |
| 6 | **Test it yourself** — ask it to do the task instead of asking whether it can | `prompts/06`, skill `testa-agora` |
| 7 | **Open mind** — testing is cheap, not testing is expensive | `prompts/07` |

## The kit

```
kit/
├── prompts/        7 ready-made prompts (one per habit)
├── skills/         entrevista-me · fure-minha-ideia · mostra-nao-conta · testa-agora
├── scripts/        reuniao.py · ditado.sh · ditado.md
├── exemplos/       reuniao-exemplo.txt · painel-falar-vs-digitar.html
├── testes/rodar.sh validates the kit with no network and no API
└── instalar.sh     copies the skills to ~/.claude/skills/
```

## Quick start

```bash
git clone https://github.com/inematds/ia-de-elite.git && cd ia-de-elite
bash kit/testes/rodar.sh                          # 30 ok · 0 falha(s)
python3 kit/scripts/reuniao.py --simular --saida teste-reuniao
bash kit/instalar.sh --dry-run                    # then without --dry-run
```

- **reuniao.py**: audio/video (or .txt/.srt) → `transcricao.txt`, `ata.md`, `tarefas.md`. It transcribes **on your computer** with faster-whisper (`pip install faster-whisper`). The minutes come out through `claude -p` (Claude Code subscription), through local Ollama, or as a prompt to paste into any chat (`--motor prompt`). It never calls a paid API.
- **ditado.sh** (Linux): records, transcribes locally and copies the text. Windows: `Win + H`. macOS: press `Fn` twice.

Open and free · MIT license · [INEMA.CLUB](https://inema.club)
