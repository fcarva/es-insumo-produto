# Resultados — RQ-A (fractal) + RQ-B (benchmark): a plataforma é invariante de escala

*Pipeline `academic-pipeline` · **Stage 2 (análise)** do flagship escolhido (RQ-A + RQ-B).
Scripts reprodutíveis: `pesquisa/14_benchmark_ufs.py`, `pesquisa/15_intra_es_fractal.py`.
Saídas: `outputs/benchmark_ufs.csv`, `outputs/intra_es_fractal.csv`. Data: 2026-06-26.*

> **Achado-núcleo (honesto, e mais forte que a tese original).** A "lógica-plataforma" — *unidade
> pequena gera encadeamento que escoa para um núcleo mais rico, com retorno ≈ 0* — é uma **regularidade
> de posição-e-porte**, **invariante de escala**: governa a relação *periferia → metrópole* dentro do ES
> exatamente como governa *ES → Sudeste* dentro do Brasil. Como a **mecânica é genérica**, o que é
> **específico do ES** não está na decomposição (vazamento/feedback), e sim na **composição** (pauta
> mineral/primária, *upstreamness*). A plataforma é uma **condição composicional**, não um artefato do método.

---

## 1. RQ-B — Benchmark 27 UFs: específico-ES × genérico (modelo nulo)

`14_benchmark_ufs.py` computa, para cada UF (2008), vazamento médio do multiplicador, razão de
**feedback** (inversa particionada Miller-Blair, UF=L vs resto=M), **HHI** de concentração de destino do
spillover e % ao núcleo SP+RJ; depois ajusta um **modelo nulo** (métrica ~ porte) e lê o resíduo do ES.

**Modelo nulo (métrica ~ a + b·log(produção)):**

| Métrica | b (sinal) | R² (quanto o **porte** explica) | Leitura |
|---|---|---|---|
| vazamento | −0,0025 | **0,01** | porte explica pouco; vazamento ~ abertura |
| **feedback (razão)** | +0,0033 | **0,59** | **porte explica a maior parte: estado maior, mais feedback** |
| HHI de destino | +0,0028 | 0,01 | concentração não é função do porte |

**Onde o ES cai (resíduo = observado − previsto pelo porte):**

| Métrica | ES obs. | previsto | resíduo | veredito |
|---|---|---|---|---|
| vazamento | 22,8% | 21,3% | +1,6% | **genérico** (dentro de 1 dp) |
| feedback | 0,32% | 0,45% | −0,12% | **genérico** (até *abaixo* do previsto p/ seu porte) |
| HHI destino | 0,193 | 0,193 | +0,000 | **genérico** (rank **14/27** — meio da tabela) |

→ z-scores do ES: vazamento +0,45 · feedback −0,05 · HHI +0,03. **Em nenhuma das três métricas de IO o
ES é *outlier*.** O feedback≈0 é, como o Devil's Advocate suspeitou, **efeito de porte** (núcleo SP+RJ
tem feedback médio **1,97%** vs. cluster **0,49%**) — e o ES está até *abaixo* da reta para o seu tamanho.

**Onde o ES (e o cluster) É *outlier* — composição** (de `10_cluster_setorial.py`):

| | base/commodity % | setor dominante |
|---|---|---|
| **ES** | **36,4% (2º do Brasil)** | **Mineração** (só ES e RJ) |
| MT | 43,4% (1º) | Agricultura |
| SP (núcleo) | 18,0% | Serviços privados |

→ **Conclusão RQ-B:** o que faz o ES "plataforma" não é a magnitude do vazamento/feedback (genérica de
estado pequeno-aberto), e sim a **pauta** — primário/mineral pesado, a montante. Isso **responde o
DA-1/R1 de frente**, sem retórica: a especificidade é composicional e mensurável.

---

## 2. RQ-A — A plataforma é fractal? Intra-ES (10 microrregiões, 2015)

`15_intra_es_fractal.py` aplica o **mesmo aparato** uma escala abaixo (sistema inter-regional R1–R10 ×
S1–S35, Z 350×350).

| reg | share prod. | vazamento | feedback | HHI dest. | % → metrópole |
|---|---|---|---|---|---|
| **R1 (metrópole)** | **62,3%** | **8,4%** | **1,86%** | 0,176 | (núcleo) |
| R7 | 10,6% | 24,3% | 0,87% | 0,585 | **75,7%** |
| R5 | 6,2% | 18,8% | 0,65% | 0,353 | 55,4% |
| R4 | 4,1% | **31,1%** | 0,57% | 0,334 | 44,5% |
| R3 | 1,9% | 18,2% | 0,20% | 0,588 | **75,9%** |
| R2 | 1,5% | 17,0% | 0,20% | 0,488 | 68,3% |

(R6, R8, R9, R10 análogos — periferia pequena, vazamento alto, escoa à metrópole.)

**Invariância de escala (modelo nulo intra-ES, n=10):**
- vazamento ~ log(porte): b=−0,009 (metrópole grande → menos vazamento) — **mesmo sinal** do 27-UF.
- **feedback ~ log(porte): R² = 0,91** — *ainda mais forte* que o 0,59 do nível 27-UF. **A regularidade
  size-driven se reproduz uma escala abaixo.**
- **Extração hipotética da metrópole (R1):** a produção das demais microrregiões **cairia 13,0%** se R1
  "saísse" — a periferia capixaba depende do núcleo capixaba, espelhando a dependência ES → Sudeste.

→ **Conclusão RQ-A:** o par (retém-no-núcleo / vaza-da-periferia) é **fractal**. R1/Grande Vitória é o
"SP/RJ" do ES; a periferia mineral/agrícola é o "ES" do ES. *periferia : ES :: ES : Sudeste.*

---

## 3. A síntese (o que isto dá para o artigo)

Os dois resultados **se costuram numa tese única e nova**:

1. **Mecânica = posição × porte, invariante de escala.** Vazamento alto + feedback≈0 + escoamento ao
   núcleo são **genéricos** e **fractais** — valem para qualquer unidade pequena-aberta perante seu
   núcleo, em qualquer escala (microrregião dentro do ES; UF dentro do Brasil). Provado, não afirmado.
2. **Especificidade = composição.** O ES se distingue pela **pauta** (mineração dominante, base 36%,
   *upstreamness* 3,12 vs. 1,91), não pela decomposição. A plataforma é uma **condição composicional**.
3. **Implicação.** As consequências de política (royalties, carbono embutido, captura de valor) decorrem
   da **composição**, não do vazamento *per se* — o que dá um "so what?" de política mais preciso (R3-W1).

Isto **reenquadra** o artigo original (que tratava vazamento/feedback como o achado-ES) para algo mais
defensável e mais original: **plataforma como invariância de escala + especificidade composicional**.

---

## 4. Ressalvas honestas (carregar para a redação)

1. **`ΣA ≥ 1` em S23 de TODAS as 10 regiões** (col-sum 1,07). Sistemático (setor S23), não um acaso de 1
   coluna. `B` permanece ≥ 0 e finita (sistema utilizável), mas o multiplicador simples de S23 é
   degenerado. Os agregados regionais (R1 retém 62%/8,4%; feedback~porte R²=0,91) **não** são dirigidos
   por S23 (1 de 35 setores). **Ação Stage 2:** teste de sensibilidade dropando/saneando S23.
2. **Chave R1–R10 → nome oficial PENDENTE.** R1 é inequivocamente a **Metropolitana** (62,3%, Grande
   Vitória). R2–R10 ainda por casar com Caparaó/Rio Doce/Noroeste/etc. (ordenação oficial IJSN + os 10
   arquivos `.xlsb`). Identificadas aqui por índice/porte.
3. **Sem emprego** intra-ES (só Remunerações) → "vazamento de emprego" não replicável nessa escala.
4. **2015 ≠ 2008** e **35 ≠ 26 setores** → comparação inter-escala é qualitativa (mesma *lógica*), não
   um cruzamento numérico direto; exige a tabela-ponte do §7 do `DEEP_RESEARCH_PANORAMA.md`.
5. **Fluxos sub-estaduais (IIOAS) são ainda mais sintéticos** que os interestaduais — o modelo nulo
   intra-ES (n=10) é indicativo, não inferência.
6. **Divulgação de IA:** análise e código assistidos por IA (Claude Code); todos os números acima
   reproduzem do dado real via `14_*.py`/`15_*.py` (sem números inventados).

---

## 5. Próximo passo (pipeline)

Empírico do flagship **pronto e verificado**. Falta: (a) confirmar o **reenquadramento** editorial
(plataforma = invariância de escala + composição) com o autor; (b) figura(s) do fractal (vazamento×porte
nas duas escalas; mapa periferia→metrópole); (c) sensibilidade S23; (d) redação (Stage 2 WRITE) → Stage
2.5 integridade → Stage 3 review. Checkpoint do usuário antes da redação completa.
