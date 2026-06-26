# Auditoria HARD — *O Espírito Santo como economia-plataforma*

Escrutínio total e independente do manuscrito `paper/es_insumo_produto.tex`, do pipeline
`pesquisa/01–13` e do substrato de dados (`Material IO/`), guiado pela referência-âncora
**Haddad et al. (2017)** e estruturado pela rubrica de avaliação do *Auto-Empirical-Research-Skills*
(categorias: *causal-identification, reproducibility, citation-hygiene, runtime-safety,
research-integrity, writing*). Substrato da skill validado localmente (`make check`):
engine de grading e benchmark numérico **verdes** (17 cenários válidos; benchmarks
bad-control/IV-Card/DiD/LaLonde/RDD recuperam o efeito verdadeiro; eval-smoke reprova
corretamente a resposta IV-fraca plantada). As 5 "falhas" do `make check` são cosméticas
(catálogo JSON desatualizado + 3 testes negativos sensíveis a separador de caminho no Windows).

> **Veredito:** o artigo é **numericamente reprodutível e metodologicamente correto** — todos
> os ~25 números de manchete foram regenerados do zero a partir das planilhas e batem.
> Os problemas encontrados são de **higiene de citação, reprodutibilidade de console e
> consistência do material de apoio** — não corrompem nenhum resultado publicado. Lista de
> correções priorizada no fim.

---

## 0. O que foi reproduzido (do zero, a partir do `.xlsx` cru)

Interpretador `.venv` (numpy 2.4.6 / pandas 3.0.3 / openpyxl). Execução: `01,02,04,07,08,10,13`.

| Afirmação no paper | Origem | Reproduzido | OK |
|---|---|---|---|
| Vazamento médio **24,9%** (simples) | `01` | 24.90% | ✅ |
| Vazamento **22,8/22,9%** (ponderado) | `01`/`02`/`10` | 22.87 / 22.8 | ✅ |
| Imobiliários 5,3% · Alimentos 37,4% | `01` | 5.3 / 37.4 | ✅ |
| Emprego: refino 61,6 · alim 56,5 · mad-papel 50,3 · metal 49,3 | `01` | idênticos | ✅ |
| Injeção **R$ 51,5 bi** | `01`/`02` | 51.483,4 mi (idêntico nos dois recortes) | ✅ |
| Spillover **R$ 18,2 bi** | `01` (bi) / `02` (inter) | 18.162,8 / 18.122,9 mi | ✅ |
| Feedback **R$ 164 mi (0,32%)** | `01`/`13` | 163,6 mi / 0,318% | ✅ |
| 78% retido / 22% escoa | `02` | 77.9% / 22.1% | ✅ |
| **Sudeste (excl. ES) 65,4%** · SP 37,8 · RJ 14,7 · MG 12,9 | `02` | idênticos | ✅ |
| Núcleo SP+RJ 52,5% · demais pares 31,5% · cluster PIB 33,9% | `04` | idênticos | ✅ |
| Tabela 3 (`tab:cluster`) — 10 estados × 4 colunas | `10` | linha-a-linha | ✅ |
| Upstreamness **3,12** · BR 1,91 · Mundo 2,31 · mineração U=3,82 | `07`/`08` | idênticos | ✅ |
| Mineração+metalurgia+celulose = 71% das exportações | `08` | 71.4% | ✅ |
| Identidade contábil VBP = soma de linha | `01` | **erro máx 0,00%** | ✅ |
| ΣA<1 e B≥0 (bi-regional e interestadual) | `01`/`02` | 0,748 / 0,895 ; B≥0 | ✅ |

**Cross-validação estrutural confirmada:** a injeção `f^ES` é numericamente *idêntica*
(R$ 51.483,4 mi) entre a matriz bi-regional (`01`) e a interestadual (`02`); o spillover
fecha em 18,16 vs 18,12 bi — é a mesma economia em dois recortes. Sólido.

---

## 1. Referência-âncora Haddad et al. (2017) — verificada contra o PDF

Li o artigo completo (RBERU 11(4):424–446). Resultado:

- ✅ **O "27,4%" do paper é correto e bem usado.** Haddad, **Tabela 2 (p. 440)**, linha ES:
  parcela **inter-regional do multiplicador de produção total = 27,4%**. É exatamente o
  conceito do paper (`O^M_j/O_j`). O paper compara sua média simples (24,9%) a esse valor
  e o rotula corretamente como convergente *"em safra e agregação distintas"* (Haddad é
  **2011, 68 setores**; o paper é **2008, 26 setores**).
- ✅ **Corroboração independente da tese.** O *abstract* de Haddad destaca, sem prompting,
  que *"Amazonas, **Espírito Santo** e Mato Grosso foram os estados em que a demanda final de
  outras UFs e do exterior mais influencia a produção local"* — o núcleo empírico da leitura
  "economia-plataforma".
- ✅ Método IIOAS (gravitacional; F=0,5 setores 1–36 e F=0,95 setores 37–68; impedância via
  PNLT) confere com a Limitação (ii) declarada no §6.
- ❌ **Entrada bibliográfica factualmente errada** (ver Defeito A).

---

## 2. Defeitos encontrados (priorizados)

### 🔴 A — Citação Haddad et al. (2017): título/escopo/tipo errados — *citation-hygiene*
`paper/es_insumo_produto.tex:369-372` registra:
> *"Matriz **inter-regional** de insumo-produto para o **Espírito Santo**: método IIOAS. **Working paper**."*

O documento real (em `Material IO/Haddad et al (2017).pdf` e `Artigos/`) é:
> *"Matriz **INTERESTADUAL** de insumo-produto para o **BRASIL**: uma aplicação do método IIOAS",
> **Revista Brasileira de Estudos Regionais e Urbanos (RBERU)**, v. 11, n. 4, pp. 424–446, 2017.*

O **uso no texto** (método + 27,4%) está correto; o que está errado é a **metadata da
referência** — título, escopo (Brasil/27 UFs, não ES) e tipo (artigo publicado, não *working
paper*). Um leitor não encontraria a fonte sob o título citado.
**Correção:** substituir a entrada pelo título/veículo/páginas reais.

### 🟠 B — WIOD (Timmer et al. 2015) na bibliografia mas **nunca citado** — *citation-hygiene*
`timmer2015wiod` é definido (`:383`) porém não há nenhum `\cite*` no corpo (verificado por
varredura). A WIOD é a **fonte de dados de toda a camada de upstreamness** (§2, §4.5, 3 figuras).
**Correção:** inserir `\citep{timmer2015wiod}` onde a WIOD 2014 é introduzida no §2 e no §4.5.

### 🟠 C — `src/io_core.py` é "implementação de referência" mas é **código morto e incorreto** — *reproducibility/integrity*
- **Não é importado por nada** no repositório (varredura confirma); os números do paper saem de
  `pesquisa/01–13`, não dele.
- Sua função `spillover_feedback()` é **degenerada**: calcula `x_L_total = (B@y)[L]` e
  `x_L_intra = B_LL @ y_L`; como `y_M=0`, `(B@y)[L] ≡ B_LL @ y_L`, logo **`feedback ≡ 0` por
  construção, sempre**. (O feedback correto compara `B_LL` *com loop* a `(I−A^LL)^{-1}`
  *fechado* — é o que `01_es_br_base.py` faz, certo.)
- Sua `rasmussen_hirschman()` calcula a ligação **para-frente pela inversa de Leontief** — exatamente
  o bug que a `AUDITORIA.md` (B4) diz ter corrigido para **Ghosh** no pipeline real.
- `dados/README.md:9` afirma que os outputs são *"gerados por src/io_core.py"* — **falso**.

**Impacto:** zero sobre números publicados; **alto** sobre um replicador que confie no README/módulo
"de referência". **Correção:** ou corrigir `io_core.py` (feedback via partição; forward via Ghosh) ou
rebaixá-lo a "esboço não usado" e apontar o README para `pesquisa/01_es_br_base.py` como referência.

### 🟠 D — `02_interestadual.py` **não roda do zero** em console Windows padrão — *runtime-safety/reproducibility*
Em console cp1252 (o default do alvo do repo — caminhos são `C:/Users/DELL/...`), o script
**aborta com `UnicodeEncodeError`** no caractere `Σ` (`02_interestadual.py:84`), **antes** de
gravar `es_spillover_destino.csv` / `estados_abertura.csv`. A guarda
`sys.stdout.reconfigure("utf-8")` existe **apenas em `13_audit_contrafactual.py`** — não foi
propagada. (`01` sobrevive por acaso: seus não-ASCII são todos cp1252-encodáveis.) Contradiz o
cabeçalho do paper *"Números reproduzíveis ... 01–11 rodam do zero"*.
**Correção:** mover a guarda de reconfigure para um módulo comum / topo de cada script, ou trocar
`Σ` por `Sigma`/ASCII nos prints.

### 🟡 E — Upstreamness WIOD: distribuição global contaminada — *reproducibility/integrity (parcialmente declarado)*
`07` reporta `U` global com **máximo 15.055,87** e **49/2464 setores (2%) com demanda final
implícita < 0**. A mineração ("percentil 98" no paper) tem U=3,82 e cai em **p97,7** *medido
contra essa distribuição contaminada* — a cauda patológica desloca o ranking. O §6 declara a
aproximação WIOD/concordância em geral, mas **não** sinaliza que o número de percentil específico
herda o ruído dos setores degenerados. A concordância **26→56 é 1:1 ("setor representativo")**,
feita à mão (`08:24-26`) — o 3,12 é sensível a esse mapeamento.
**Correção:** (i) winsorizar/excluir os 49 setores degenerados antes do percentil e reportar o
percentil robusto; (ii) acrescentar uma frase no §6 sobre a contaminação da cauda; (iii) opcional:
checagem de sensibilidade do 3,12 a mapeamentos alternativos.

### 🟡 F — `13_audit_contrafactual.py`: vereditos `✓` hard-coded e linguagem superlativa — *research-integrity*
O bloco "RESUMO DA AUDITORIA" (`13:138-143`) imprime `✓ ...` como **strings literais,
incondicionais** aos números computados. Confronto com a execução real:
- Cenário 3 — *"adensamento ... eleva feedback, logo há margem de integração"*: feedback
  163,6 → **164,7 mi (+0,7%)**. Movimento desprezível; conclusão sobredimensionada.
- Cenário 4 — *"RB exibe feedback **muito maior** ... confirmando a assimetria"*: razões reais
  **0,65% (RB) vs 0,32% (ES)** — ambas < 1%; "muito maior" exagera um contraste de ~2×.

Nada disso entra no paper (é exploração interna de robustez), portanto **não há número publicado
afetado** — mas é o padrão "conclusão não atada à evidência" que a rubrica *research-integrity*
penaliza. **Correção:** tornar os `✓` condicionais ao resultado (`assert`/`if`) e moderar a redação.

### 🟢 G — Arredondamentos e rótulos menores — *writing (baixo)*
- "Mineração no **percentil 98**" = arredondamento de **97,7** (a `AUDITORIA.md` usa "p97,7").
  Sugestão: "percentil 98 (97,7)".
- Spillover **18,1** (Sankey/interestadual) vs **18,2** (corpo/bi-regional) — recortes distintos,
  já caveatado na legenda; manter, mas explicitar.
- "Sudeste absorve **65%**" (abstract) vs **65,4%** (§4.3) — arredondamento, ok.
- `08:46` carrega comentário-alvo obsoleto *"(alvo paper: 3,19)"* enquanto computa e publica 3,12 —
  limpar o comentário para não confundir.

### 🟢 H — Escolhas de definição/proveniência (declaradas) — *baixo*
- "Base/commodity" (`10:25`) inclui **Alimentos** entre os setores de base — defensável, mas é uma
  escolha de rótulo que infla a parcela; transparente no código.
- Coluna "PIB (%)" usa corretamente **valor adicionado** (linha 728), não VBP — sem mislabel. ✅
- Cluster vem de leitura de mercado da "Apex Partners" — proveniência não-acadêmica, mas o paper já
  o trata explicitamente como *grupo de comparação*, sem status de regionalização oficial. Ok.

---

## 3. Solidez metodológica (confirmada — *causal-identification/method*)
- Partição de Isard e **feedback pela inversa particionada** corretos no pipeline real:
  `inv_feed = (I − A^LL − A^LM (I−A^MM)^{-1} A^ML)^{-1}`, feedback = `xL_full − xL_closed`
  (`01:99-107`, `13:49-57`). Bate com a Eq. (2) do paper.
- Spillover = `(I−A^MM)^{-1} A^ML x^L` (`01:103`) — idêntico ao enunciado.
- Rasmussen-Hirschman: para-trás por Leontief, **para-frente por Ghosh** (`01:83-86`) — correção
  metodologicamente preferível, aplicada onde importa.
- Antràs-Chor `U=(I−G)^{-1}1`, `G` normalizada por linha — implementado em `07`; BR 1,91 e Mundo 2,31
  são plausíveis e estáveis.
- Convenção de feedback "V3 Miller-Blair": a assimetria (feedback ≈ 0) é **robusta à convenção**
  (0,15–0,32%) — a tese não depende da escolha.

---

## 4. Checklist de *referee* (atualizado)

| Critério | Status |
|---|---|
| Reprodutibilidade numérica (do `.xlsx` cru) | ✅ 100% dos números de manchete |
| Identidade contábil / não-negatividade | ✅ verificadas independentemente |
| Método (Isard/MB/Ghosh/Antràs) | ✅ correto no pipeline executado |
| Citação — uso no texto | ✅ todas as 6 entradas usadas, exceto Timmer (Defeito B) |
| Citação — metadata das referências | ❌ Haddad (A) errada; Timmer (B) não citada |
| Reprodução "do zero" em Windows | ⚠️ `02` quebra em cp1252 (D) |
| Material de apoio coerente | ⚠️ `io_core.py`/README enganosos (C) |
| Robustez declarada | ✅ assimetria invariante à convenção; cross-validação 2 recortes |
| Honestidade dos limites (§6) | ✅ franca; reforçar percentil WIOD (E) |

---

## 5. Plano de correção (ordem de esforço × impacto)
1. ✅ **APLICADO (A)** Entrada Haddad corrigida → "Matriz interestadual… para o Brasil",
   RBERU 11(4):424–446, 2017; autor "Gonçalves Júnior". Paper recompila sem citação indefinida.
2. ✅ **APLICADO (B)** `\citep{timmer2015wiod}` inserido no §2 (Dados) e `\citealp{timmer2015wiod}`
   no §3 (Método/upstreamness). Timmer agora citado no corpo.
3. ✅ **APLICADO (D)** Guarda `sys.stdout.reconfigure("utf-8")` propagada a `01,02,04,07,08,10`.
   Verificado: `02` agora roda do zero sob console cp1252 (exit 0) sem alterar nenhum número.
4. ✅ **APLICADO (C)** `io_core.py` corrigido para casar com o pipeline real: `spillover_feedback`
   passou à inversa particionada (feedback real, antes ≡ 0) e `rasmussen_hirschman` à inversa de
   Ghosh no para-frente; adicionado `ghosh_inversa`. Verificado contra o dado real: feedback **163,6 mi**,
   spillover 18.162,8, vazamento 24,90% — idênticos a `01`. `dados/README.md` corrigido (outputs vêm de
   `pesquisa/01–13`, não de `io_core`).
5. ✅ **APLICADO (E)** Tratamento WIOD fundamentado na literatura (subagente leu `Artigos/`): excluem-se
   setores com demanda final implícita ≤ 0 e a cauda não-econômica (U>10) → 185/2.464 removidos, 2.279
   válidos. Mineração reportada por **nível + ranking** (U=3,82; **33ª de 2.279**, percentil **98,6→99**)
   em vez do percentil sobre a distribuição bruta, em linha com Araújo Júnior (2018, p.21); base em OECD
   (2019, Tab. 2.1) e Tukker & Dietzenbacher (2013, p.10,14). Médias Brasil 1,91 / mundo 2,31 e pauta ES
   3,12 **inalteradas** (robustas). Frase + 3 referências adicionadas ao paper (§6 e bibliografia).
6. ✅ **APLICADO (F)** Vereditos do `13` agora **condicionais** aos números (`[OK]/[X]`), com referências
   por cenário (Miller 1966; Miller-Blair 2009 cap.3/6; Haddad 2017 Tab.2) e redação moderada
   ("+0,7%, efeito de nível pequeno"; "RB 2,0× o ES, ambos < 1%").
7. ✅ **APLICADO (G)** Comentário-alvo obsoleto "3,19" em `08` corrigido para "3,12". (Itens de
   arredondamento de prosa — "18,1 vs 18,2" — deixados intactos por serem editoriais.)

> **Verificação pós-correção (todos os 7 itens aplicados):** paper recompila limpo (8 págs, **sem
> citação/referência indefinida**); `io_core` reproduz o feedback 163,6 mi (antes ≡ 0); `01`/`08`
> reproduzem números idênticos; `07` robusto mantém Brasil 1,91 / mundo 2,31 / ES 3,12; `02` e `13`
> rodam do zero em console cp1252. **Nenhum número de substância do artigo mudou** — apenas o percentil
> da mineração foi reexpresso como nível+ranking (U=3,82; 33ª/2.279; ~p99) sob tratamento de dados
> fundamentado na literatura.

*Nenhum item acima altera um número publicado.* O risco residual é de forma/proveniência, não de
substância: a economia-plataforma capixaba — vazamento ~25%, spillover R$ 18,2 bi contra feedback
0,32%, Sudeste absorvendo 65%, upstreamness 3,12 — está **empiricamente sustentada e reprodutível**.
