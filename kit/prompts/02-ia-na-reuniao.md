# Hábito 2 — A IA ouvindo a reunião

**Por quê:** uma reunião gravada e transcrita vira, em segundos, uma ata e uma lista de tarefas com dono e prazo. É o trabalho de um assistente executivo por um custo quase zero.

**Como:** grave a reunião (com o aviso e o consentimento de todos), transcreva (o `kit/scripts/reuniao.py` faz isso no seu computador, sem enviar o áudio para ninguém) e cole a transcrição com o prompt abaixo.

## Prompt (copie e cole)

```text
Você é meu assistente executivo. Abaixo está a transcrição de uma reunião.
Entregue, em português:

## Ata
- Assunto e participantes
- Decisões tomadas (uma por linha)
- Pontos em aberto

## Tarefas
Uma tabela com as colunas: Responsável | O que fazer | Prazo | Trecho da fala que originou.
Regras:
- Só tarefas que alguém assumiu ou recebeu de verdade; não invente.
- Se o prazo não foi dito, escreva "sem prazo".
- Se o responsável não ficou claro, escreva "a definir" e liste nos pontos em aberto.

Transcrição:
[cole aqui]
```
