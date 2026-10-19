# Hábito 3 — Mostre, não conte

**Por quê:** a gente entende uma imagem muito mais rápido que um parágrafo. Toda IA de chat boa sabe escrever HTML com gráficos, animação e até 3D (three.js). Peça a visualização em vez de mais texto.

**Exemplos de pedido:** a planta da casa em 3D para girar com o mouse; um relatório denso virando um painel com números grandes e barras; um conceito difícil virando um explicador animado em 5 passos.

## Prompt (copie e cole)

```text
Não me responda com texto corrido. Transforme o conteúdo abaixo em UMA página HTML
auto-contida (um arquivo só, CSS e JavaScript dentro, sem servidor) que eu possa abrir no navegador.
- Comece pelos 3 números ou fatos mais importantes, em destaque grande.
- Toda comparação vira gráfico (barras, linha ou pizza) com rótulo e valor escrito, não só cor.
- Se for um processo, mostre como linha do tempo ou fluxo com setas.
- Se fizer sentido em 3D (espaço, objeto, planta), use three.js de um CDN.
- Fundo escuro, letra grande, funciona no celular.
Me devolva só o código completo do arquivo.

Conteúdo:
[cole o texto, a tabela ou o relatório aqui]
```

No Claude e no ChatGPT a página aparece pronta ao lado da conversa; no Gemini, use o Canvas. Se não aparecer, salve o código como `painel.html` e abra com dois cliques.
