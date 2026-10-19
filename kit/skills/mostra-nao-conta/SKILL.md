---
name: mostra-nao-conta
description: Transforma um texto, relatório, tabela ou explicação numa página HTML visual auto-contida (um arquivo só, abre no navegador) com números em destaque, gráficos rotulados, fluxos e, quando fizer sentido, 3D com three.js. Use quando o usuário disser "mostra, não conta", "vira painel", "transforma em visual", "faz um HTML disso", "explica com gráfico", ou entregar um relatório denso para resumir.
---

# mostra-nao-conta

Hábito 3 do IA de Elite: em vez de mais texto, uma visualização.

## Passo a passo

1. Leia o material e escolha **no máximo 3 mensagens principais**. Escreva-as numa frase cada antes de desenhar.
2. Decida a forma de cada parte:
   - número importante → cartão com o número grande e uma legenda;
   - comparação → barras horizontais com rótulo e valor escrito;
   - evolução no tempo → linha;
   - processo → fluxo com setas ou linha do tempo;
   - objeto/espaço (casa, peça, sala) → cena 3D com three.js (CDN `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js`), com rotação pelo mouse.
3. Gere **um único arquivo** `.html`: CSS e JS inline, sem build, sem servidor, sem chave de API. Bibliotecas só por CDN público.
4. Salve no diretório atual com nome curto (`painel-<assunto>.html`) e diga ao usuário como abrir (`xdg-open`, `open` ou dois cliques).
5. Confira antes de entregar: o arquivo abre sem erro no console, cabe na tela do celular (sem rolagem horizontal), todo gráfico tem rótulo e valor.

## Regras de visual

- Fundo escuro (`#0c0c10`), texto claro, um acento só (amarelo `#FACC15`).
- Fonte do sistema ou Inter; letra de leitura nunca menor que 14px.
- Cor nunca carrega informação sozinha: sempre rótulo ou valor junto.
- Sem dado inventado: se o material não tem o número, não desenhe o número.
- Animação curta (até 1 s) e respeitando `prefers-reduced-motion`.

## Exemplo

`kit/exemplos/painel-falar-vs-digitar.html` (do kit IA de Elite) mostra o formato esperado: números grandes, barras rotuladas e um fluxo.
