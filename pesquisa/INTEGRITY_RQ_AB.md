# Stage 2.5 — Verificação de integridade do manuscrito `es_plataforma_fractal.tex`

*Pipeline `academic-pipeline` · gate MANDATÓRIO (não pode ser pulado). Data: 2026-06-26.
Protocolo 5 fases + checklist de 7 modos de falha de IA.*

## Fase A — Referências (6 citadas)
Todas reais e reaproveitadas da bibliografia já revisada do artigo original
(`REVIEW_FULL_MODE.md`): `guilhoto2005estimacao`, `haddad2017iioas`, `isard1951`,
`miller1966`, `millerblair2009`, `round1983nonsurvey`. **0 alucinações.** `natbib`
resolveu todas (compilação sem `??`).

## Fase B — Contexto das citações
- `miller1966` → "feedback inter-regional pequeno para regiões pequenas": uso correto.
- `haddad2017iioas` → método IIOAS + Tab. 2 (estados na mesma faixa do ES): correto.
- `millerblair2009` → inversa particionada + **extração hipotética**: ambos no texto-base; correto.
- `isard1951`, `guilhoto2005estimacao`, `round1983nonsurvey` → partição inter-regional e
  regionalização não-censitária: correto. **Nenhuma citação fora de contexto.**

## Fase C — Dados (todo número rastreado ao script)
| Afirmação no `.tex` | Fonte reprodutível | Status |
|---|---|---|
| feedback~porte R²=0,59 (27-UF) / 0,91 (intra-ES) | `14`/`15` | ✓ |
| ES escores-z +0,45 / −0,05 / +0,03; ranks 8/8/14 | `benchmark_ufs.csv` | ✓ |
| ES feedback 0,32% obs vs 0,45% prev (resid −0,12) | `14` | ✓ |
| núcleo feedback 1,97% vs cluster 0,49% | `14` | ✓ |
| MG 60% e RS 55% ao núcleo > ES 52,5% | `benchmark_ufs.csv` | ✓ |
| base 36,4% **2ª do país** (MT 43,4%) | **verificado nas 27 UFs** (rank 2/27) | ✓ corrigido p/ "país" |
| Mineração dominante = ES, **PA e RJ** | **verificado nas 27 UFs** | ✓ **ERRO CORRIGIDO** |
| Metropolitana 62,3%, vaz 8,4%, feed 1,86% | `intra_es_fractal.csv` | ✓ |
| Litoral Sul 31,1%; Rio Doce 24,3%; →metro até 76% | `15` | ✓ |
| extração hipotética metrópole −13,0% | `15` | ✓ |
| sensibilidade S23: 8,4%→7,9%; R² 0,91→0,91 | `15` | ✓ |

**Achado da auditoria (corrigido):** o draft afirmava "um dos **dois** únicos (com o RJ)"
com Mineração dominante; a verificação nas 27 UFs mostrou **três** (PA, ES, RJ). Texto
corrigido para "um dos três únicos (com o Pará e o Rio de Janeiro)". A afirmação "base a 2ª
do país" foi **confirmada** (ES rank 2/27).

## Fase D — Originalidade
Prosa original; sem cópia. Reusa preâmbulo/notação Miller-Blair do artigo próprio (auto-derivado).

## Fase E — Afirmações
A tese (mecânica genérica/fractal + especificidade composicional) é sustentada pelos dados;
a analogia *periferia:ES::ES:Sudeste* é apresentada como interpretação, não como medida.

## Checklist de 7 modos de falha de IA
1. **Alucinação de citação** — NÃO (6 refs reais, verificadas).
2. **Bug de implementação** — baixo risco: B≥0 nos dois sistemas; convenções espelham
   `io_core.py`/`01`; resultado robusto a duas escalas. PASS.
3. **Resultados alucinados** — NÃO: todo número vem de script executado com CSV salvo.
4. **Dependência de atalho** — N/A.
5. **Bug como insight** — NÃO: o achado-núcleo (mecânica genérica) **contrariou** a hipótese
   inicial e foi reportado como tal; sensibilidade S23 confirma robustez. PASS.
6. **Fabricação de metodologia** — NÃO: métodos padrão (Isard particionado, HEM, modelo nulo
   OLS), descritos corretamente. PASS.
7. **Frame-lock de pipeline** — NÃO: o enquadramento **mudou** quando o dado exigiu (de
   "específico-ES" para "genérico + composicional"). PASS.

## Veredito
**PASS** — 1 erro factual detectado e corrigido; 0 modos de falha SUSPECTED. Manuscrito
compila (6 págs) e está apto a seguir para Stage 3 (REVIEW).
