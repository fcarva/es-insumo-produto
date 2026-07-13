# Review of es_estrutura_produtiva.tex, round 1 (theorist-toolbox)

- Reviewer: paper-reviewer (theorist-toolbox, Koren 2026, arXiv:2606.22337), modo
  "paper-level review" + caminhada prover-style dos Apêndices A/B sob a disciplina
  `math-proof` (todo passo justificado/citado/sinalizado; sem hand-waving; hipóteses
  explícitas; dimensões conferidas) + checagem coder-style da cadeia número→artefato.
- Date: 2026-07-13
- Manuscrito: `paper/es_estrutura_produtiva.tex` @ `f146015` (19 págs., 36 refs., Apêndices A/B)
- **Verdict: REQUEST_CHANGES**
- Round: 1

## Findings

**F1 — BLOCKING — Tabelas 1 e 4 × `outputs/` — cadeia número→artefato não verificada.**
As Tabelas `tab:decomp` e `tab:micro` citam `decomposicao_fd.csv` e
`micro_multiplicadores.csv`, ausentes do repositório; os testes de autoverificação dos
scripts `24`/`25` existem mas **nunca foram executados sobre o dado bruto**. Pela escada
deste protocolo, teste não-rodado = teste falhando. *Fix:* rodar `fechar_R1.bat` na máquina
com o `Material IO` e commitar os CSVs (item já pronto; coincide com o R1 da rodada ARS-3).
Sem isso, o veredito não pode ser APPROVE.

**F2 — MAJOR — Apêndice A.2, eq. (3) (`eq:feedback`) — hipótese omitida.**
A identidade $x^{L} = (I-A^{LL})^{-1}y^{L} + [\,B^{LL}-(I-A^{LL})^{-1}]\,y^{L}$ é
apresentada como "resolvendo para $L$" **sem declarar a hipótese $y^{M}=0$**. No caso
geral, $x^{L}=B^{LL}y^{L}+B^{LM}y^{M}$ — a forma exibida vale apenas para a injeção
restrita. O mesmo vício contamina a frase seguinte (spillover $x^{M}=(I-A^{MM})^{-1}A^{ML}x^{L}$)
e, por herança, o fecho do A.3 ($(\Delta_{LL}-I)\Delta_L y^{L}$). Pela disciplina
`math-proof`, hipótese não declarada = lacuna. *Fix (1 linha):* anteceder a equação de
"Para uma injeção com $y^{M}=0$ (o experimento de \S\ref{sec:plataforma}), ...".

**F3 — MAJOR — Apêndice A.5, eq. (6) (`eq:ghs`) — inconsistência dimensional.**
Como exibida, $\mathrm{PBL}_j=\Delta_r A_{rj}\Delta_j y_j$ é um **vetor** de dimensão
$n-1$ ($\Delta_r$ é $(n{-}1){\times}(n{-}1)$, $A_{rj}$ é $(n{-}1){\times}1$, $\Delta_j$ e
$y_j$ escalares), enquanto $\mathrm{PFL}_j=\Delta_j A_{jr}\Delta_r y_r$ é um **escalar**
($A_{jr}$ é $1{\times}(n-1)$). A soma $\mathrm{PTL}_j=\mathrm{PBL}_j+\mathrm{PFL}_j$ é,
portanto, mal-formada. A quantidade efetivamente computada e reportada
(`17_caracterizacao_es_2008.py:82`) é a soma das entradas:
$\mathrm{PBL}_j=\iota'\,\Delta_r A_{rj}\,\Delta_j\,y_j$, com $\iota$ o vetor-soma.
*Fix:* inserir $\iota'$ na definição de PBL (e, por clareza de paralelismo, notar que
PFL já é escalar).

**F4 — MAJOR — §5/Apêndice A.9 — o −13,0% não tem artefato persistido.**
A extração hipotética da Metropolitana (−13,0%) rastreia-se a um *print* de console de
`15_intra_es_fractal.py` (documentado em `RESULTADOS_RQ_AB.md`), mas **nenhum CSV
versionado** carrega o número — a cadeia paper → outputs termina num stdout. Determinístico
e re-rodável, porém não persistido. *Fix:* acrescentar o resultado ao
`intra_es_fractal.csv` (coluna ou linha-resumo) na próxima execução do `15`.

**F5 — MINOR — Apêndice A.1 — fechamento tipo II sem fórmula.**
"Entram como linha e coluna adicionais de $A$" não define os coeficientes de borda. A
implementação usa $h_i = c_i/\sum_{k\in L}\mathrm{rem}_k$ (consumo das famílias do ES por
unidade de renda) na coluna e $v_i$ (com $v_i=0$ para $i\in M$) na linha. *Fix:* exibir a
matriz aumentada $\bar{A}=\begin{bmatrix}A & h\\ v' & 0\end{bmatrix}$ com as duas definições.

**F6 — MINOR — Apêndice A.1 — "limite inferior" afirmado sem o argumento.**
A justificativa é a monotonicidade elementar da inversa de Leontief: fechar também para o
consumo em produtos do resto do Brasil só *acrescenta* coeficientes não-negativos a
$\bar{A}$, e $A\le A' \Rightarrow (I-A)^{-1}\le(I-A')^{-1}$ elemento a elemento (séries de
Neumann). Uma frase resolve.

**F7 — MINOR — Apêndices A.1/A.2 — hipótese de produtividade não declarada.**
O formulário usa $(I-A)^{-1}$, $(I-A^{MM})^{-1}$ etc. sem declarar a condição sob a qual
existem e são não-negativas ($A\ge 0$ produtiva / Hawkins–Simon; raio espectral $<1$). A
verificação empírica existe (scripts; Apêndice B.2 nota a coluna S23), mas a *hipótese*
deve abrir o Apêndice A. *Fix:* uma frase no preâmbulo do A.1.

**F8 — MINOR — Apêndice A.8 — caráter descritivo do modelo nulo não restabelecido.**
A regressão roda com $n=27$ (e $n=10$ intra-ES) e o texto, corretamente, não faz inferência —
mas o apêndice não diz isso. *Fix:* meia frase ("ajuste descritivo; sem pretensão inferencial,
sobretudo com $n=10$"), ecoando o que os Limites já dizem.

## What I checked

- **Frases banidas** (strict mode): grep por "claramente / é fácil ver / obviamente /
  trivial / análogo / similar / omitido / evidentemente" — **zero ocorrências**.
- **A.2/A.3 (Isard/Miyazawa):** re-derivei $B^{LL}=\Delta_{LL}\Delta_L$ e — novo nesta
  rodada — o bloco $B^{ML}=\Delta_{MM}\Delta_M A^{ML}\Delta_L$ via identidade
  *push-through* $(I-XY)^{-1}X=X(I-YX)^{-1}$ com $X=\Delta_M A^{ML}$, $Y=\Delta_L A^{LM}$:
  a eq. (5) em blocos está **correta**. O defeito de A.2 é a hipótese, não a álgebra.
- **A.5 (GHS):** dimensões conferidas termo a termo contra a implementação
  (`17_*:76–84`) — origem do F3.
- **A.4/A.6/A.7:** normalizações de Rasmussen-Hirschman (Leontief/Ghosh) e a aditividade
  exata da decomposição ($\sum_k y^{(k)}=y \Rightarrow \sum_k x^{(k)}=x$, por linearidade)
  conferem; LQ/HHI padrão.
- **A.9 (HEM):** equivalência entre "zerar blocos" (texto) e "deletar linhas/colunas"
  (implementação do `15`) para o bloco mantido — confere.
- **Cadeias numéricas:** 1,97%/0,49% e escores-z re-deriváveis de `benchmark_ufs.csv`
  (recomputados); 40,4 re-derivado de `es_caracterizacao_2008.csv`; B.1 (2.464−185=2.279)
  confere; B.3 consistente. Cadeias das Tabelas 1/4 → F1; do −13,0% → F4.
- **Consistência paper-level:** introdução promete (i)–(iii) e o corpo entrega; resumo
  alinhado ao modelo nulo (pós rodada ARS-3); todas as \ref/\cite resolvem (36↔36).

## What was good

- A álgebra pesada está **certa**: a decomposição de Miyazawa em blocos (a peça mais
  fácil de errar do formulário) passa na re-derivação completa, incluindo o bloco
  off-diagonal que nenhuma rodada anterior verificou.
- Zero hand-waving textual — raro; o texto justifica ou remete cada passo.
- O padrão "script autoverificável" (asserts contra as tabelas publicadas) é exatamente a
  disciplina de golden-values que este protocolo exige — preservar nas revisões.
- A conciliação explícita das agregações (24,9/22,8; 90,9/91,6) e a declaração da escolha
  de classificação (nota do benchmark) sobreviveriam a um referee hostil.

---
*Regra do protocolo observada: o revisor NÃO editou o manuscrito — este arquivo é o único
produto da rodada. Correções são responsabilidade do autor (rodada 2 mediante re-review).*
