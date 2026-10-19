---
name: testa-agora
description: Troca a pergunta "a IA consegue fazer X?" por um teste real — faz a menor versão de X agora, mostra o resultado, avalia o que ficou bom e fraco, propõe o próximo teste e registra tudo com data em testes-ia.md. Use quando o usuário perguntar "a IA consegue...", "dá pra fazer X com IA?", "será que o Claude faz...", "testa agora" ou "testa isso".
---

# testa-agora

Hábito 6 do IA de Elite: teste você mesmo. As capacidades mudam toda semana; a resposta de memória envelhece, o teste não.

## Passo a passo

1. Reescreva a pergunta como tarefa: "a IA consegue X?" → "fazer a menor versão útil de X".
2. Diga em uma linha qual é essa menor versão e o critério de sucesso (o que tem que aparecer para contar como "conseguiu").
3. **Faça.** Gere o arquivo, rode o comando, escreva o texto. Não descreva o que faria.
4. Mostre o resultado (caminho do arquivo, saída do comando ou o próprio conteúdo).
5. Avalie em 3 linhas: o que ficou bom, o que ficou fraco, se passou no critério.
6. Proponha o próximo teste, um degrau mais difícil.
7. Acrescente uma linha em `testes-ia.md` no diretório atual (crie se não existir):

```
| AAAA-MM-DD | modelo/ferramenta | tarefa | passou? (sim/parcial/não) | observação curta |
```

## Regras

- Sem chamar API paga nem serviço externo sem o usuário pedir; prefira o que roda local ou na própria conversa.
- Se a tarefa precisar de algo que você não tem (arquivo, login, hardware), diga o que falta e faça a parte possível.
- "Não consegui" também é resultado: registre com o motivo.
