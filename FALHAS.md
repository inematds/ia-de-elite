# FALHAS.md — ia-de-elite

| data | o que quebrou | menor correção | tipo |
|---|---|---|---|
| 2026-10-19 | testes/rodar.sh: `instalar.sh \| grep -q` falhava com pipefail (SIGPIPE) | capturar a saída antes do grep | prompt |
