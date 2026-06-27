# Stage 2.5 — Verificação de integridade: `es_estrutura_produtiva.tex`

*Pipeline `academic-pipeline` · gate MANDATÓRIO. Data: 2026-06-26. Protocolo 5 fases + 7 modos de falha.*

## Fase A — Referências (8 citadas)
`figueiredo2004agriculture` (lida), `porsse2008matriz` (lida), `guilhoto2005estimacao`,
`haddad2017iioas`, `hirschman1958`, `millerblair2009`, `rasmussen1956`, `round1983nonsurvey`.
Todas reais; clássicos de ligação (Rasmussen 1956, Hirschman 1958) e o substrato brasileiro já
verificado. `natbib` resolveu todas (sem `??`). **0 alucinações.**

## Fase B — Contexto das citações
MT/RS (figueiredo/porsse) → "gênero aplicado a estados" ✓ · guilhoto2005/round1983 → regionalização
não-censitária ✓ · haddad2017 → IIOAS ✓ · millerblair2009 → bateria IO + ligações puras + Ghosh ✓ ·
rasmussen1956/hirschman1958 → índices de ligação ✓. Nenhuma fora de contexto.

## Fase C — Dados (todo número rastreado)
| Afirmação | Fonte | Status |
|---|---|---|
| mult. produção 1,76 (I) / 2,45 (II); emprego 27,9/R$mi | `17` | ✓ |
| têxtil 67,9 · pecuária 57 · alojam. 50,2 (top emprego) | `17` | ✓ |
| setores-chave RH (refino…eletricidade) | `17` | ✓ |
| mineração p/ frente ~1,2, p/ trás ~0,9 (enclave) | `17` | ✓ |
| ligações puras: mineração 4,4 · metalurgia 3,4 | `17` | ✓ |
| CV 0,16 (trás) / 0,28 (frente) | `17` | ✓ |
| celulose 1,41→1,51; mult 2,85→3,05; siderurgia cai 2021 | `18` | ✓ |
| petróleo/minério ligação p/ trás <1; minério pica 2015 | `18` | ✓ |
| Metropolitana 62%; LQ celulose 8,2 / minério 9,5 / têxtil 9,6 / pecuária 21,9 | `20` | ✓ |
| ES ~2% do produto nacional (2008); petróleo ~¼ do PIB estadual | benchmark (1,97%) / Gov ES-ANP | ✓ |

**Geografia econômica conferida:** Tubarão (siderurgia, Serra/Metropolitana), Cachoeiro (rochas, Central
Sul), Anchieta (pelotização, Litoral Sul), Colatina (têxtil, Centro-Oeste), Santa Maria de Jetibá
(avicultura, Central Serrana), Linhares/Aracruz (celulose, Rio Doce) — **todas batem com os LQ do dado**.

## Fase D — Originalidade
Prosa original; preâmbulo/notação reaproveitados do próprio projeto.

## Fase E — Afirmações
Caracterização descritiva sustentada pelos dados; o pico do minério em 2015 é fraseado como coincidência
temporal ("em torno de Fundão"), sem alegar causação; caveat de *proxy* nacional declarado em §Limites.

## Checklist de 7 modos de falha de IA
1. Alucinação de citação — NÃO. 2. Bug de implementação — baixo risco (B≥0; tipo II>tipo I corrigido;
ligações puras padronizadas pela média ES; unidades de emprego corrigidas) — PASS. 3. Resultados
alucinados — NÃO. 4. Atalho — N/A. 5. Bug-como-insight — NÃO (dualidade enclave/chave consistente em C1
transversal e C2 temporal). 6. Fabricação de metodologia — NÃO (métodos padrão, descritos corretamente).
7. Frame-lock — N/A (caracterização descritiva).

## Veredito (Stage 2.5)
**PASS** — 0 erro factual; 0 modo de falha SUSPECTED. Manuscrito compila (6 págs, 3 figuras) e está apto
a seguir para Stage 3 (REVIEW).

---

# Stage 4.5 — Integridade FINAL (pós-revisão, verificação independente do zero)

*Reverificação completa do manuscrito revisado (8 págs). Não apenas dos itens conhecidos.*

## Referências (10 — todas reais)
As 8 anteriores + **2 novas verificadas com DOI**: `ribeiro2024dinamica` (RBERU 18(4):596–622, 2024,
DOI 10.54766/rberu.v18i4.1111) e `sessa2017ubu` (Economia e Desenvolvimento 28(2), 2017, DOI
10.5902/1414650921397). `natbib` resolve todas; 0 `??`. **0 alucinações.**

## Dados — reverificação dos números NOVOS (revisão)
| Afirmação nova | Fonte | Status |
|---|---|---|
| benchmark: base 36,4% (2º) · prod 1,66 (14º) · emprego 25,4 (24º) · ligação 0,92 (14º) · líder/média 0,39 (2º); medianas 21,0/1,66/42,5/0,92/0,65 | `22` | ✓ |
| nota NEW-1: §4 simples/bi-regional 1,76 & 27,9 vs Tab. ponderado/interestadual 1,66 & 25,4 | `17` × `22` | ✓ reconciliado em nota de rodapé |
| celulose 1,41→1,51 (alavanca de política) | `18` | ✓ |
| Ribeiro et al. usa a mesma matriz 2015 (contraste §6) | verificado | ✓ |
| petróleo ~¼ do PIB (royalties §7) | Gov ES/ANP | ✓ |

Todos os números de C1/C2/C3 reverificados contra `17`/`18`/`20` (inalterados). **0 discrepância.**

## Checklist de 7 modos (reaplicado)
1. Citação — NÃO. 2. Bug — benchmark ponderado correto; B≥0 — PASS. 3. Resultados alucinados — NÃO.
4. Atalho — N/A. 5. Bug-como-insight — NÃO (benchmark **contrariou** "ES é especial" e devolveu "genérico
em tipo, extremo em grau" — sem raciocínio motivado). 6. Metodologia — padrão. 7. Frame-lock — NÃO (a
revisão reposicionou o objeto temporal honestamente).

## Veredito (Stage 4.5)
**PASS (zero issues)** — apto para finalização (Stage 5). Compila em 8 págs, 3 figuras, 2 tabelas, 10
refs; R&R sem concern silenciado; re-review rodada 2 = Minor→Accept (NEW-1 resolvido).
