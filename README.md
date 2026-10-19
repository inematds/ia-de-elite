# 🧠 IA de Elite — 7 hábitos de quem usa IA no topo

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![IA de Elite](capa/capa.png)](https://inematds.github.io/ia-de-elite/guia/)

## O que é

IA de Elite é um guia com os 7 hábitos que separam quem usa a IA de verdade de quem só faz perguntas soltas no chat: falar em vez de digitar, deixar a IA ouvir a reunião, pedir visual em vez de texto, ser entrevistado pela IA, pedir falhas, testar com as próprias mãos e manter a mente aberta. Serve para qualquer pessoa que já usa ChatGPT, Claude ou Gemini. Junto vem um kit aberto e grátis com 7 prompts para copiar, 4 skills para o Claude Code e scripts que rodam no seu computador. Para os prompts basta um chat; para os scripts, Python.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/ia-de-elite/guia/**

## Os 7 hábitos

| # | Hábito | No kit |
|---|---|---|
| 1 | **Fale, não digite** — em média 30–50 palavras/min digitando × 150–200 falando | `prompts/01`, `scripts/ditado.md`, `scripts/ditado.sh` |
| 2 | **A IA ouvindo a reunião** — transcrição vira ata e tarefas (quem, o quê, prazo) | `scripts/reuniao.py`, `prompts/02` |
| 3 | **Mostre, não conte** — HTML, gráficos, 3D em vez de texto | `prompts/03`, skill `mostra-nao-conta` |
| 4 | **A IA te entrevista** — "me faça todas as perguntas que precisa" | `prompts/04`, skill `entrevista-me` |
| 5 | **Peça falhas, não opinião** — a IA tende a concordar; peça o que está errado | `prompts/05`, skill `fure-minha-ideia` |
| 6 | **Teste você mesmo** — peça para fazer em vez de perguntar se consegue | `prompts/06`, skill `testa-agora` |
| 7 | **Mente aberta** — testar é barato, não testar custa caro | `prompts/07` |

## O kit

```
kit/
├── prompts/        7 prompts prontos (um por hábito)
├── skills/         entrevista-me · fure-minha-ideia · mostra-nao-conta · testa-agora
├── scripts/        reuniao.py · ditado.sh · ditado.md
├── exemplos/       reuniao-exemplo.txt · painel-falar-vs-digitar.html
├── testes/rodar.sh valida o kit sem rede e sem API
└── instalar.sh     copia as skills para ~/.claude/skills/
```

## Começo rápido

```bash
git clone https://github.com/inematds/ia-de-elite.git && cd ia-de-elite
bash kit/testes/rodar.sh                          # 30 ok · 0 falha(s)
python3 kit/scripts/reuniao.py --simular --saida teste-reuniao
bash kit/instalar.sh --dry-run                    # depois sem --dry-run
```

- **reuniao.py**: áudio/vídeo (ou .txt/.srt) → `transcricao.txt`, `ata.md`, `tarefas.md`. Transcreve **no seu computador** com faster-whisper (`pip install faster-whisper`). A ata sai pelo `claude -p` (assinatura do Claude Code), pelo Ollama local ou como prompt para colar em qualquer chat (`--motor prompt`). Nunca chama API paga.
- **ditado.sh** (Linux): grava, transcreve local e copia o texto. Windows: `Win + H`. macOS: `Fn` duas vezes.

Aberto e grátis · licença MIT · [INEMA.CLUB](https://inema.club)
