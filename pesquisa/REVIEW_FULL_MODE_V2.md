# Peer Review (full mode) — Rodada 3: "Estrutura Produtiva do Espírito Santo" (versão com apêndices)

*Skill `academic-paper-reviewer` v1.10.0, modo **full** (EIC + R1/R2/R3 + Devil's Advocate →
síntese editorial). Manuscrito: `paper/es_estrutura_produtiva.tex` @ commit `3ffd875`
(19 págs, 35 refs, Apêndices A/B). Rodadas anteriores: `REVIEW_FULL_MODE.md` (v1, Minor→Accept)
e `REVIEW_CARACTERIZACAO.md` (v3 inicial, Major→Minor→Accept). Idioma do parecer: PT.
Regra de ferro observada: os revisores NÃO editam o manuscrito — este documento é o único produto.*

---

## Fase 0 — Análise de campo e configuração dos pareceristas

| Item | Diagnóstico |
|---|---|
| Disciplina primária | Economia regional / análise de insumo-produto |
| Disciplina secundária | Teoria do desenvolvimento regional (base de exportação, polos) |
| Paradigma | Positivista, estrutural-descritivo (caracterização, não inferência causal) |
| Método | Bateria IO completa (mult. I/II, RH/Ghosh, ligações puras GHS, LQ/HHI, Isard/Miyazawa, decomposição da demanda final, modelo nulo, HEM) |
| Tier de periódico-alvo | Regional brasileiro (RBERU, Nova Economia, EconomiA) — Qualis A4–B1 |
| Maturidade | Pós-2 rodadas de parecer; apêndices metodológicos novos; **quase todo** reprodutível |

**Pareceristas:** EIC (editor de ciência regional brasileira, perfil Haddad/Guilhoto) ·
R1 Metodologia (economista de IO; álgebra, reprodutibilidade, consistência numérica) ·
R2 Domínio (economista regional; literatura e ancoragem teórica) ·
R3 Perspectiva (geografia econômica/política pública) ·
Devil's Advocate (desafia a coexistência das molduras "economia de base" e "plataforma").

---

## Fase 1 — Pareceres independentes

### EIC — Editorial

**Recomendação:** Minor Revision (banda superior) · **Confiança:** 4/5

**Síntese.** A terceira versão fecha as duas lacunas que as rodadas anteriores apontaram
informalmente: o aparato matemático voltou (Apêndice A, 8 equações numeradas, notação
Miller-Blair) e o artigo agora dialoga com a teoria clássica do desenvolvimento regional
(North/Tiebout na decomposição da demanda final; Perroux nas ligações puras; Cano/Friedmann
no centro-periferia). A estrutura corpo-enxuto + apêndices é a certa para o gênero e para o
tier. O que separa esta versão do Accept é acabamento, não substância.

**Strengths.**
- **S1 — Arquitetura editorial madura.** Corpo de leitura fluida com o formulário completo em
  apêndice; cada parágrafo do §Método remete à equação correspondente (\ref{ap:*}). É o
  equilíbrio que o gênero "Estrutura Produtiva de [Estado]" raramente alcança.
- **S2 — O modelo nulo mudou o patamar da contribuição.** A frase "o ES não é outlier em
  nenhuma métrica de decomposição; a especificidade é composicional" (§7 + Tabela B.5) é a
  resposta definitiva à objeção de tautologia — e é honesta contra o próprio interesse
  retórico do artigo.

**Weaknesses.**
- **W1 — O resumo não reflete o achado mais forte.** *Problema:* o abstract ainda diz que a
  base é "hiperaberta" e menciona o vazamento/spillover, mas não diz que o modelo nulo mostra
  o ES **dentro do previsto pelo porte** em todas as métricas de decomposição — o resultado
  que imuniza o artigo contra a crítica mais séria fica invisível para quem só lê o resumo.
  *Sugestão:* 1 frase no abstract (e moderar "hiperaberta", que o próprio dado relativiza:
  8º/27 em vazamento, escore-z +0,45). *Severidade:* Major (de enquadramento, não de cálculo).
- **W2 — Extensão.** 19 páginas com 2 apêndices; adequado a RBERU, mas verificar limite do
  veículo-alvo antes da submissão. *Severidade:* Minor.

**Dimension Scores:** Originality 70 · Methodological Rigor 76 · Evidence 74 · Coherence 78 ·
Writing 79 · **Weighted ≈ 75,5**.

---

### R1 — Peer Reviewer (Metodologia)

**Recomendação:** Minor Revision · **Confiança:** 5/5

**Síntese.** Verifiquei o Apêndice A equação a equação contra as implementações versionadas:
a identidade de Miyazawa $B^{LL}=\Delta_{LL}\Delta_L$ fecha algebricamente (derivei
$(I-A^{LL}-A^{LM}\Delta_M A^{ML})^{-1} = (I-\Delta_L A^{LM}\Delta_M A^{ML})^{-1}\Delta_L$);
as ligações puras (eq. A.5) correspondem linha a linha ao que `17_caracterizacao_es_2008.py`
computa; RH para frente usa Ghosh, correto. A paridade numérica do corpo contra
`benchmark_ufs.csv`/`intra_es_fractal.csv` confere (núcleo 1,97% = média SP 2,91/RJ 1,03;
cluster 0,49%; MG 60,0/RS 55,2; z +0,45/−0,05/+0,03). Restam três pendências de consistência
e uma de reprodutibilidade — nenhuma de cálculo.

**Strengths.**
- **S1 — Formalização correta e completa** (Isard aditivo + Miyazawa multiplicativo + GHS +
  modelo nulo + HEM), com as definições que faltavam na literatura de apoio (Δ_LL explícito).
- **S2 — Padrão "script autoverificável"** nos novos `24`/`25`: os asserts contra as tabelas
  publicadas transformam a replicação em teste automatizado. Prática exemplar.

**Weaknesses.**
- **W1 — Duas tabelas ainda fora do pipeline versionado.** *Problema:* a Tabela 1
  (`tab:decomp`) e a Tabela 4 (`tab:micro`) citam `outputs/decomposicao_fd.csv` e
  `outputs/micro_multiplicadores.csv`, que **não estão no repositório**; os scripts `24`/`25`
  commitados são reconstruções ainda não executadas sobre o dado bruto (os originais estão na
  máquina do autor). *Por que importa:* a reprodutibilidade é a marca registrada do artigo —
  essas duas tabelas são hoje a exceção. *Sugestão:* rodar os scripts sobre o `Material IO`,
  conferir os asserts e commitar os 2 CSVs (ou os scripts originais, se divergirem).
  *Severidade:* **Major** (processo; bloqueia o selo "100% reprodutível", não a validade).
- **W2 — 8,4% vs 9,1% sem conciliação.** *Problema:* para a Metropolitana, o §7 e o Apêndice
  B.2 reportam **vazamento de 8,4%** (média das razões setoriais ponderada pelo VBP, de
  `15_intra_es_fractal.py`), enquanto o resumo, o §5 e a Tabela 4 reportam **retenção de
  90,9%** (razão das somas ponderadas, de `24_*`) — que implica vazamento de 9,1%. Ambas
  legítimas, mas o leitor atento verá dois números para a mesma coisa, como no episódio
  1,76/1,66 da rodada anterior (NEW-1). *Sugestão:* nota de rodapé de conciliação na Tabela 4
  (mesma solução do 24,9/22,8). *Severidade:* Major→Minor (com a nota).
- **W3 — HEM: escopo da injeção não declarado.** O Apêndice A.9 descreve a extração, mas não
  diz que o experimento usa apenas a **demanda final intra-estadual** (é o que `15_*` faz);
  o −13,0% deve ser lido sob essa injeção. 1 frase resolve. *Severidade:* Minor.
- **W4 — Miyazawa apresentado, não explorado.** O Apêndice A.3 formaliza multiplicadores
  internos/externos, mas nenhum resultado os reporta separadamente (o feedback vem da forma
  aditiva). Ou reportar um número (ex.: norma de $\Delta_{LL}-I$), ou reduzir a subseção à
  identidade e à ligação com a eq. do feedback. *Severidade:* Minor.

**Dimension Scores:** Methodological Rigor 75 (→80 com W1 fechado) · Evidence 74 ·
Reproducibility: Strong (Exceptional após W1) · **Minor Revision**.

---

### R2 — Peer Reviewer (Domínio)

**Recomendação:** Minor Revision (banda superior) · **Confiança:** 4/5

**Síntese.** A ancoragem teórica pedida está feita e feita com sobriedade: North e Tiebout
entram exatamente onde o dado os evoca (61,7% da produção vs 47,5% do emprego — a divisão de
trabalho perfeita entre base exportadora e atividades residentes), Perroux entra pelas
ligações puras, e o benchmark ganhou a linhagem mineira (Domingues & Haddad 2002). As 8
referências novas conferem (verifiquei metadados: North JPE 63(3); Tiebout JPE 64(2) — o
artigo correto de 1956, não o "Pure Theory"; Perroux Économie Appliquée 8; Miyazawa
Hitotsubashi 7(1); Cella OBES 46(1); GHS AJRS 11(1); Dietzenbacher et al. ESR 5(2)).

**Strengths.**
- **S1 — O triângulo teórico certo, sem inflação.** Base de exportação + polos + centro-
  periferia como "três descrições do mesmo dado" (§Discussão) é a síntese que o gênero pedia.
- **S2 — Linhagem metodológica completa** (Cella → GHS; Isard → Miyazawa; Rasmussen/Hirschman
  → ligações puras), agora citável e rastreável.

**Weaknesses.**
- **W1 — Precedentes estaduais do gênero ainda ausentes.** O §1 cita MT e RS; os estudos
  análogos para Pará, Santa Catarina e Maranhão (localizados em
  `DEEP_RESEARCH_CARACTERIZACAO.md` §6.2, nunca verificados) completariam a moldura "o gênero
  aplicado aos estados" e reforçariam a lacuna capixaba. *Severidade:* Minor.
- **W2 — Tiebout em uma oração.** A réplica de Tiebout (1956) é mais rica do que a menção:
  a resiliência das atividades residentes conecta-se diretamente ao fechamento tipo II do
  próprio artigo (o induzido é o canal tieboutiano). 2–3 frases fariam a ponte. *Severidade:*
  Minor.

**Dimension Scores:** Literature Integration 82 (Strong) · Originality 70 · Coherence 78 ·
**Minor Revision** (banda superior).

---

### R3 — Peer Reviewer (Perspectiva: geografia econômica / política)

**Recomendação:** Minor Revision (banda superior) · **Confiança:** 3/5

**Síntese.** Para o leitor de política regional, a versão ganhou os dois números que faltavam:
a extração hipotética (−13,0% na periferia sem a metrópole) dá materialidade ao desenho
centro-periferia, e o contraste núcleo 1,97% vs 0,49% dimensiona o "privilégio de retorno" na
federação. As três alavancas de política continuam boas; podem agora ser amarradas aos números
novos.

**Strengths.**
- **S1 — O −13,0% é o número de política territorial.** Nenhum plano de desenvolvimento
  sub-estadual capixaba dispõe hoje de uma medida de dependência sistêmica da RMGV; o artigo
  a entrega.
- **S2 — Leitura distributiva explícita** (North puxa a produção, Tiebout carrega o emprego)
  — tradução direta para o debate de emprego local.

**Weaknesses.**
- **W1 — As alavancas de política não usam os resultados novos.** A alavanca (iii)
  "diversificar com endereço territorial" ganharia força citando o −13,0% (risco da
  mono-dependência metropolitana) e a retenção de 66,2% do Litoral Sul. *Severidade:* Minor.
- **W2 — Royalties sem ponte com o modelo nulo.** Se o retorno via encadeamento é
  estruturalmente baixo para o porte (z −0,05), a captura fiscal é o canal *substituto* — o
  argumento fica mais forte com essa amarração. *Severidade:* Minor.

**Dimension Scores:** Significance & Impact 77 · Coherence 76 · **Minor Revision** (banda superior).

---

### Devil's Advocate

**Afirmação prévia (justiça):** o artigo fez o que pouquíssimos fazem — computou o teste que
poderia derrubar sua própria retórica (modelo nulo) e publicou o resultado desconfortável.

#### Strongest Counter-Argument (≈230 palavras)

O artigo agora **prova que sua "face plataforma" é um fenômeno genérico** — e mesmo assim a
mantém como marco retórico. Os escores-z mostram que o ES não é outlier em vazamento (+0,45),
feedback (−0,05) nem concentração de destino (+0,03); seu feedback está *abaixo* da reta do
porte; MG e RS escoam *mais* ao núcleo. Após esse resultado, chamar a base capixaba de
"hiperaberta" (resumo, §1) e dedicar uma seção inteira à "face plataforma" é manter o figurino
de uma tese que o próprio dado aposentou: o que resta de específico é a *composição* — e isso
o §4 (benchmark) já demonstrava. Um cético dirá: o §7 deveria encolher para um parágrafo de
contexto, e o título da seção deveria perder o rótulo-plataforma. Segundo: a especificidade
composicional — "2º estado mais intensivo em base (36,4%)" — depende de uma **escolha de
classificação** que inclui Alimentos entre os setores de base (documentada em
`AUDITORIA_HARD.md` item H como escolha que "infla a parcela"); a sensibilidade do ranking a
essa escolha nunca foi testada. Se com Alimentos fora o ES cair para 4º–5º, o "caso-limite"
vira "caso-alto". Terceiro: as duas tabelas novas (demanda final; retenção territorial) são,
neste commit, as únicas cujo rastro reprodutível ainda não fecha no repositório — justamente
as que sustentam o achado-manchete (61,7/47,5) e o desenho territorial.

#### Issue List

**MAJOR**
| # | Dimensão | Descrição | Local |
|---|---|---|---|
| DA-1 | Frame residual | Retórica "hiperaberta"/seção-plataforma sobrevive ao próprio modelo nulo que a relativiza; risco de o leitor levar a tese antiga | Resumo, §1, §7 |
| DA-2 | Robustez de classificação | "2º em base (36,4%)" sensível à inclusão de Alimentos no rótulo base/commodity; sem teste de sensibilidade | §4, Tab. 2–3 |
| DA-3 | Rastro reprodutível | Tabelas 1 e 4 dependem de CSVs ausentes do repo (scripts reconstruídos, asserts ainda não rodados no dado bruto) | §4, §5 |

**MINOR**
| # | Dimensão | Descrição | Local |
|---|---|---|---|
| DA-4 | Consistência | 8,4% (vazamento) vs 90,9% (retenção ⇒ 9,1%) para a mesma Metropolitana, agregações distintas sem nota | §5 × §7/Ap. B.2 |
| DA-5 | Precisão | HEM computado sob demanda final intra-ES apenas; não declarado | Ap. A.9 |

**CRITICAL:** nenhum.

#### Explicações alternativas ignoradas
1. **Classificação setorial** como driver do ranking composicional (DA-2) — alternativa: o ES
   é extremo *em mineração especificamente*, não "em base" — formulação aliás mais forte e
   testável (setor dominante Mineração: só ES, PA, RJ).
2. **Efeito-2008**: a composição pré-Fundão e pré-consolidação do pré-sal pode superestimar o
   peso relativo do minério na fotografia — já declarado nos Limites, mas interage com DA-2.

#### Perspectivas de stakeholder ausentes
- Municípios da periferia metropolitana (o −13,0% é agregado; a incidência municipal não).

#### Observações (não-defeitos)
- A tríade final da Discussão (North/Perroux/Cano-Friedmann como "três descrições do mesmo
  dado") é o parágrafo mais forte do artigo.
- O reporte honesto dos z-scores contra o interesse retórico pesa **contra** DA-1 ser lido
  como viés — é inconsistência de revisão, não de intenção.

---

## Fase 2 — Síntese editorial

### DECISÃO: **Minor Revision (banda superior) — Accept condicional aos itens R1–R3**

| Parecerista | Recomendação | Confiança |
|---|---|---|
| EIC | Minor Revision (superior) | 4 |
| R1 Metodologia | Minor Revision | 5 |
| R2 Domínio | Minor Revision (superior) | 4 |
| R3 Perspectiva | Minor Revision (superior) | 3 |
| DA | 3 MAJOR, 0 CRITICAL | — |

### Consenso
**[CONSENSO-4]** Fechar o rastro reprodutível das Tabelas 1 e 4 — rodar `24`/`25` no dado
bruto, conferir asserts, commitar os CSVs (R1-W1, DA-3).
**[CONSENSO-3]** Conciliar 8,4% × 9,1% por nota de rodapé na Tabela 4 (R1-W2, DA-4) — mesma
solução do precedente 24,9/22,8.
**[CONSENSO-3]** O resumo deve absorver o modelo nulo e moderar "hiperaberta" (EIC-W1, DA-1).

### Divergência principal
**DA-1 (encolher a seção-plataforma) × EIC/R2 (mantê-la).** *Arbitragem:* manter a seção —
ela agora cumpre função distinta (documentar que a mecânica é genérica e que a especificidade
é composicional), e o texto já diz isso; o que falta é o *resumo* dizer o mesmo. DA-1
resolve-se pela via do EIC-W1, sem cirurgia estrutural. **DA-2 (sensibilidade da
classificação):** acolhido como obrigatório *leve* — uma nota reportando o ranking sem
Alimentos no rótulo base (computável de `cluster_setorial.csv`/`22_*`) ou a reformulação
"extremo em mineração" blindaria o claim.

### Revisões obrigatórias (Required)
| # | Item | Fonte | Esforço |
|---|---|---|---|
| R1 | Rodar `24`/`25` sobre o Material IO (máquina local), validar asserts, commitar `decomposicao_fd.csv` + `micro_multiplicadores.csv` | R1-W1, DA-3 | 10 min (autor) |
| R2 | Nota de conciliação 8,4% (média ponderada das razões) × 9,1% (razão das somas) na Tabela 4 | R1-W2, DA-4 | 15 min |
| R3 | Resumo: +1 frase com o resultado do modelo nulo; moderar "hiperaberta" | EIC-W1, DA-1 | 20 min |
| R4 | Sensibilidade da classificação de base: nota com ranking ex-Alimentos OU reformular para "extremo em mineração" | DA-2 | 1–2 h |

### Revisões sugeridas (Suggested)
| # | Item | Fonte | Prioridade |
|---|---|---|---|
| S1 | Declarar no Ap. A.9 que a extração usa demanda final intra-estadual | R1-W3, DA-5 | P2 |
| S2 | Miyazawa: reportar 1 número interno/externo ou enxugar A.3 | R1-W4 | P3 |
| S3 | Expandir Tiebout (2–3 frases, ponte com o tipo II) | R2-W2 | P2 |
| S4 | Verificar e citar os estudos do gênero PA/SC/MA | R2-W1 | P3 |
| S5 | Amarrar as alavancas de política ao −13,0% e ao z −0,05 (royalties como canal substituto) | R3-W1/W2 | P2 |

### Racional da decisão (≈150 palavras)
A pontuação ponderada sobe de ≈73 (rodada 2) para ≈**76** (Originalidade 70 · Rigor 75 ·
Evidência 74 · Coerência 78 · Escrita 79): os apêndices fecharam o flanco metodológico, a
teoria fechou o flanco de enquadramento, e o modelo nulo elevou a honestidade epistêmica a
diferencial. Não há achado CRITICAL; os três MAJORs do DA são endereçáveis com o dado já
existente e sem nova análise (R1 é uma execução de 10 minutos na máquina do autor; R2/R3 são
notas; R4 é uma checagem sobre CSV versionado). O único item estrutural em disputa (encolher
a seção-plataforma) foi arbitrado a favor da manutenção com ajuste de resumo. Decisão: Minor
Revision de banda superior, com recomendação de Accept no re-review mediante R1–R4.

### Encerramento
O manuscrito está a quatro retoques do Accept — e três deles são notas. O eixo desta rodada
não é mais "provar que é sobre o ES" (resolvido pelo benchmark + modelo nulo), e sim **fechar
o próprio padrão de reprodutibilidade que o artigo estabeleceu** e alinhar o resumo ao que o
dado passou a dizer.

---

*Divulgação de IA: pareceres simulados pela skill `academic-paper-reviewer` (Claude Code),
com verificação direta de números contra os CSVs versionados e do aparato algébrico dos
apêndices. Nenhuma edição foi feita no manuscrito nesta rodada (regra read-only da skill).*
