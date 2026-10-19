# LESSONS.md — ia-de-elite

Uma regra por linha, mais recente no topo.

- Teste com `set -o pipefail`: nunca `cmd | grep -q` (o grep fecha cedo e o SIGPIPE derruba o pipeline); capture a saída antes. (19/10/2026)
