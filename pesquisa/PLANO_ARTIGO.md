# Plano — do working paper ao artigo completo

**Disciplina:** Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · PPGEco/UFES · 2026/1
**Artigo:** *O Espírito Santo como economia-plataforma* (base empírica real + camada inter-regional)
**Marco imediato:** apresentação **sex 19/06/2026**. **Artigo final:** prazo a confirmar.

> Detalhes de dados, estado da arte e limites estão em [`MAPA_DE_PESQUISA.md`](MAPA_DE_PESQUISA.md).
> Este documento é o **roteiro de execução** até o artigo completo, com fase de **auditoria**.

---

## 0. Tese (uma frase)
O ES é uma **economia-plataforma**: gera encadeamento produtivo que **escoa para o núcleo
SP/RJ** (52,5% do spillover) com **feedback ≈ 0** — leitura insumo-produto da sub-cobertura
de capital de um cluster de estados dinâmicos (ex-núcleo) do qual o ES faz parte.

## 1. Estado atual (✓ validado e versionado)
- Base bi-regional ES×RB reproduz o artigo do **dado real** (vazamento 24,9%; emprego exato).
- Interestadual 27-UF: **destino do spillover** (Sudeste ex-ES = 65%) e abertura ES = 8º/27.
- Cluster de estados dinâmicos (leitura Apex): ES→núcleo 52,5%, feedback≈0; figura pronta.
- Scripts `01–05`, tabelas e 2 figuras em `pesquisa/`.

## 2. Fase A — completar a análise
- [ ] **A1. Fixar a convenção de spillover/feedback** do artigo original (reconciliar
      60,6 / 22,4 / 199) e travar a definição usada (Miller-Blair) em texto + código.
- [ ] **A2. CGV / *upstreamness*** (WIOD 2014; 2000×2014): posição da pauta do ES via Brasil;
      fecha o arco **cluster → núcleo → mundo**.
- [ ] **A3. Tabela setorial completa** do cluster (perfil do ES vs os 7 pares).
- [ ] **A4. (opcional) Intra-ES** (microrregiões 2015): a plataforma se replica dentro do ES?
- [ ] **A5. Figuras finais** padronizadas (paleta, fontes) para paper e slides.

## 3. Fase B — auditoria (antes de fechar)
- [ ] **B1. Contábil/numérica:** oferta=demanda, x=Z1+y, ΣA<1, B≥0, multiplicadores≥1,
      reprodutibilidade (todos os scripts rodam do zero e batem com as tabelas).
- [ ] **B2. Metodológica:** conferir derivações (Isard/Leontief, spillover/feedback
      Miller-Blair cap.3, RH, *upstreamness* Antràs-Chor) contra a literatura fornecida
      (Haddad 2017; Guilhoto et al. 2019; Miller & Blair 2009).
- [ ] **B3. Limites explicitados:** fluxos interestaduais **estimados** (IIOAS, não observados);
      anos distintos (2008/2014/2015); ES não é país no WIOD; agregação 26 setores.
- [ ] **B4. Revisão de código:** `/code-review` nos scripts de `pesquisa/`.
- [ ] **B5. Revisão por pares (checklist de *referee*):** pergunta clara, identificação,
      robustez, contribuição vs literatura, honestidade dos limites.

## 4. Fase C — redação e montagem do paper
- [ ] **C1. Reescrever `paper/es_insumo_produto.tex`** com a base real e a camada inter-regional:
      título/abstract atualizados; seções **Introdução · Dados · Método · Resultados**
      (vazamento → spillover/feedback → destino interestadual → cluster → CGV) **· Discussão**
      (tese-plataforma + leitura de capital) **· Limites · Agenda · Conclusão**.
- [ ] **C2. Tabelas** geradas a partir dos CSVs de `outputs/` (substituir placeholders).
- [ ] **C3. Bibliografia** reconciliada (incluir as fontes novas + Brazil Journal/NeoFeed).
- [ ] **C4. Compilar PDF** (`make paper`) e **release** `v1.0-disciplina` (tag + PDF).

## 5. Marcos
| Quando | Entrega |
|---|---|
| **sex 19/06** | Apresentação: base + interestadual + cluster + 2 figuras (✓ material pronto) |
| +1 semana | Fase A completa (CGV + tabela do cluster) |
| +2 semanas | Fase B (auditoria) + Fase C (draft completo do `.tex`) |
| prazo final | PDF + release citável |

## 6. Decisões abertas (suas)
- **Prazo do artigo final** da disciplina (define o cronograma acima).
- **Nome do cluster** (hoje "cluster de estados dinâmicos / ex-núcleo SP/RJ").
- **Convenção exata** de spillover/feedback do artigo original (para A1).
- Escopo: incluir **intra-ES (A4)** e a comparação **2000×2014** de CGV, ou enxugar?

## 7. Divisão de trabalho
- **Eu:** análise, código, figuras, tabelas, draft do `.tex`, checklists de auditoria.
- **Você:** decisões editoriais (título, nome do cluster, escopo), convenção do spillover
  original, prazo, e a revisão final de conteúdo.
