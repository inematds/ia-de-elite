# Ditado grátis — fale em vez de digitar

Em média, a gente digita 30 a 50 palavras por minuto e fala 150 a 200. Todos os caminhos abaixo são grátis.

| Onde | Como ativar | Observação |
|---|---|---|
| **Windows 10/11** | `Win + H` em qualquer campo de texto | Configurações › Hora e idioma › Fala para escolher o idioma. Diga "vírgula", "ponto". |
| **macOS** | Ajustes › Teclado › Ditado: ligar. Depois aperte `Fn` duas vezes (ou a tecla de microfone) | Funciona em qualquer app, inclusive no navegador. |
| **Google Docs** | Ferramentas › Digitação por voz (`Ctrl + Shift + S`) | Só no Chrome. Bom para textos longos, depois cole no chat. |
| **Celular (Android/iPhone)** | Toque no microfone do teclado | O app do ChatGPT, do Claude e do Gemini também têm modo voz. |
| **Linux** | `bash kit/scripts/ditado.sh` (faster-whisper local) | Grava, transcreve no seu computador e copia o texto. |

## Linux com `ditado.sh`

```bash
pip install faster-whisper          # uma vez só (grátis, roda local)
bash kit/scripts/ditado.sh          # grava até você apertar Enter, transcreve e copia
bash kit/scripts/ditado.sh --segundos 30 --modelo small
bash kit/scripts/ditado.sh --arquivo minha-fala.wav   # transcreve um áudio pronto
bash kit/scripts/ditado.sh --checar # mostra o que está instalado
```

Precisa de um gravador (`arecord`, que vem no `alsa-utils`, ou `ffmpeg`). Para copiar sozinho, `xclip` (X11) ou `wl-copy` (Wayland).

## Treine o vocabulário

O ditado erra nomes próprios e siglas. Três jeitos de resolver:

1. No `ditado.sh`, passe `--vocab "INEMA, Claude Code, Supabase"`: as palavras viram dica para o Whisper.
2. No chat, cole no começo: "Vocabulário que eu uso (escreva sempre assim): …".
3. Fale devagar a palavra difícil nas primeiras vezes e corrija; o prompt `prompts/01-fale-nao-digite.md` pede para a IA listar o que ela corrigiu.
