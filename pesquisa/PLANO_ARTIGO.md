# Plano — do working paper ao artigo completo

**Disciplina:** Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · PPGEco/UFES · 2026/1
**Pesquisa (2ª frente):** discussões com o Prof. Renato.
**Artigo:** *O Espírito Santo como economia-plataforma* (base empírica real + camada inter-regional)
**Marcos:** apresentação **sex 19/06/2026** · **artigo final até 18/07/2026** (fim do semestre UFES).
**Escopo CONGELADO:** fotografia transversal **MIP 2008 + WIOD 2014**. Intra-ES (microrregiões)
e série **2000×2014** → **agenda futura** (cada uma é trabalho à parte: harmonização ISIC,
deflação a preços constantes, quebras estruturais; e diluiriam a narrativa interestadual).

> Dados, estado da arte e limites em [`MAPA_DE_PESQUISA.md`](MAPA_DE_PESQUISA.md).
> Aqui está o **roteiro de execução** até o artigo completo, com a fase de **auditoria**.

---

## 0. Tese e mecanismo (uma frase + porquê)
O ES é uma **economia-plataforma**: gera encadeamento que **escoa para o núcleo SP/RJ**
(52,5% do spillover) com **feedback ≈ 0**. **Mecanismo:** o ES é um *hub de passagem*
exportador de intermediários pesados (minério, siderurgia, celulose); o choque vaza
rápido para insumos avançados e bens de consumo de SP/MG, mas as rodadas seguintes de
consumo do Sudeste **não recorrem de volta** às commodities brutas capixabas — daí a
assimetria. (Usar isto na **Discussão**.)

## 1. Estado atual (✓ validado e versionado)
- Base bi-regional ES×RB reproduz o artigo do **dado real** (vazamento 24,9%; emprego exato).
- Interestadual 27-UF: **destino do spillover** (Sudeste ex-ES = 65%); abertura ES = 8º/27.
- Cluster de estados dinâmicos (leitura Apex): ES→núcleo 52,5%, feedback≈0; figura pronta.
- Scripts `01–05`, tabelas e 2 figuras em `pesquisa/`.

## 2. Fase A — completar a análise  *(meta: até 27/06)*
- [x] **A1. Convenção fixada (Miller-Blair V3):** inj 51,5 · spillover 18,2 · feedback 0,164 bi
      (0,32%). Os 60,6/22,4/0,199 não reproduzem; adotados números reprodutíveis (`06_reconciliacao.py`).
- [x] **A2. CGV / *upstreamness*** (Antràs-Chor, WIOD 2014) — **validado do dado real**:
      pauta do ES **3,12** (paper 3,19) · Brasil **1,91** (paper 1,97) · Mundo 2,31; mineração
      no **percentil 97,7** (paper ~98). Concordância 26→56 documentada (viés WIOD → B3).
      Scripts `07/08/09`; figura `outputs/es_upstreamness.png`.
- [ ] **A3. Tabela setorial completa** do cluster (perfil do ES vs os 7 pares).
- [x] ~~**A4. Intra-ES** (microrregiões 2015)~~ → **agenda futura**. *Viabilidade auditada:*
      10 microrregiões × 35 setores, Z 350×350 + output OK; **o padrão-plataforma se confirma**
      (R1/metrópole retém — vazamento 8,4%, ~70% da produção do ES — vs periferia até 31%).
      **Para virar resultado publicável precisa:** (i) corrigir balanço (1 coluna com ΣA=1,07>1);
      (ii) chave R1–R10 (nomes) e S1–S35; (iii) aceitar limites: 2015≠2008, 35≠26 setores,
      **sem vetor de emprego** (só remunerações), fluxos sub-estaduais (IIOAS) ainda mais sintéticos.
- [ ] **A5. Figuras finais** padronizadas (paleta, fontes) para paper e slides.

## 3. Fase B — auditoria  *(meta: 28/06–08/07)*
- [ ] **B1. Contábil/numérica + reprodutibilidade:** oferta=demanda, x=Z1+y, ΣA<1, B≥0,
      multiplicadores≥1; ambiente `.venv` + `requirements.txt` travado; `src/io_core.py`
      encapsula a rotina matricial; `make paper` automatiza o LaTeX → **anula questionamento
      de "manipulação em planilha"**. Todos os scripts rodam do zero e batem com as tabelas.
- [ ] **B2. Metodológica (notação = padrão do *referee*):** garantir que o `.tex` use a
      **notação idêntica a Miller & Blair** no particionamento da matriz $A$ e da inversa de
      Leontief $L$ nas submatrizes $LL, LM, ML, MM$; ancorar em Haddad e Guilhoto (Brasil) e
      Miller & Blair (Isard). Conferir *upstreamness* (Antràs-Chor) e RH.
- [ ] **B3. Limites (seção que desarma o *referee* — ser frontal):**
  - **Gap temporal / quebra estrutural:** MIP base é **2008**; o ES sofreu choques desde
    então — o mais drástico, o **rompimento da barragem de Fundão (2015)**, que paralisou a
    Samarco e alterou o peso da extração/pelotização no estado.
  - **Aproximação WIOD:** o ES **não tem assento próprio** no WIOD 2014; assumir tecnologia
    nacional ou aplicar *shift-share* da pauta capixaba sobre a matriz BR introduz **viés**
    (a intensidade primária da exportação do ES não reflete a média nacional). Declarar.
  - **Defesa pela inércia estrutural:** justificar 2008 (MIP) + 2014 (WIOD) juntos — as
    relações de encadeamento físico de cadeias de base mudam **lentamente**, então a
    *fotografia estrutural* caracteriza o modelo capixaba ainda que os nominais defasem.
- [ ] **B4. Revisão de código:** `/code-review` nos scripts de `pesquisa/`.
- [ ] **B5. Checklist de *referee*:** pergunta clara, identificação, robustez, contribuição
      vs literatura, honestidade dos limites.

## 4. Fase C — redação e montagem  *(meta: 28/06–08/07, em paralelo à B)*
- [ ] **C1. Reescrever `paper/es_insumo_produto.tex`**: título/abstract atualizados; seções
      **Introdução · Dados · Método · Resultados** (vazamento → spillover/feedback → destino
      interestadual → cluster → CGV) **· Discussão** (tese-plataforma + mecanismo + leitura
      de capital) **· Limites (B3) · Agenda · Conclusão**.
- [ ] **C2. Tabelas** a partir dos CSVs de `outputs/` (substituir placeholders).
- [ ] **C3. Bibliografia** reconciliada (+ fontes novas; Brazil Journal/NeoFeed para o cluster).
- [ ] **C4. Compilar PDF** (`make paper`) e **release** `v1.0-disciplina` (tag + PDF).

## 5. Cronograma (deadline 18/07)
| Data | Entrega |
|---|---|
| **sex 19/06** | Apresentação: base + interestadual + cluster + 2 figuras (✓ pronto) |
| **até 27/06** | Fase A (CGV/upstreamness validado + tabela do cluster) |
| **28/06–08/07** | Fase B (auditoria) + Fase C (draft completo do `.tex`) |
| **09–15/07** | Revisão final de conteúdo + PDF |
| **16–18/07** | Buffer + entrega + release citável |

## 6. Decisões abertas (suas)
- **Nome do cluster** (hoje "cluster de estados dinâmicos / ex-núcleo SP/RJ").
- **Convenção exata** de spillover/feedback do artigo original (para A1) — se você souber a
  definição usada, trava na hora; senão eu reconcilio por varredura (ver `06_reconciliacao.py`).
- ~~Escopo~~ → **decidido: enxugar** (MIP 2008 + WIOD 2014; resto na agenda futura).

## 7. Divisão de trabalho
- **Eu:** análise, código, figuras, tabelas, draft do `.tex`, checklists de auditoria.
- **Você:** decisões editoriais (título, nome do cluster, escopo), convenção do spillover
  original, e a revisão final de conteúdo (+ alinhamento com Celso e Renato).
