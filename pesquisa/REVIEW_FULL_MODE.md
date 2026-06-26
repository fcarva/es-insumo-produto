# Peer Review (full mode) — "O Espírito Santo como economia-plataforma"

*Skill `academic-paper-reviewer` v1.4, modo **full** (EIC + R1/R2/R3 + Devil's Advocate → síntese
editorial). Manuscrito: `paper/es_insumo_produto.tex` (9 págs, 20 refs). Idioma do parecer: PT.*

---

## Fase 0 — Análise de campo e configuração dos pareceristas

| Item | Diagnóstico |
|---|---|
| Disciplina primária | Economia regional / análise de insumo-produto |
| Disciplina secundária | Geografia econômica / cadeias globais de valor |
| Paradigma | Positivista, **estrutural-descritivo** (não é inferência causal) |
| Método | Multiplicadores e ligações de IO; decomposição Isard *spillover/feedback*; *upstreamness* Antràs-Chor; substrato IIOAS + WIOD |
| Tier de periódico-alvo | Regional brasileiro (RBERU, EconomiA, Nova Economia, Ensaios FEE) — Qualis A4–B1 / Scopus Q3–Q4 |
| Maturidade | Rascunho maduro; **totalmente reprodutível** (pipeline `01–13` + CSVs) |

**Pareceristas configurados:**
- **EIC** — Editor de periódico de ciência regional brasileira (perfil Haddad/Guilhoto); foco em aderência, originalidade e contribuição ao leitor regional.
- **R1 (Metodologia)** — Economista de IO; foco em construção da matriz, decomposições, reprodutibilidade e **quantificação de incerteza**.
- **R2 (Domínio)** — Economista regional brasileiro; foco em cobertura da literatura inter-regional e posicionamento teórico.
- **R3 (Perspectiva)** — Geografia econômica/desenvolvimento; foco em implicações de política e atores (royalties, Fundão, carbono).
- **Devil's Advocate** — desafia a tese-núcleo "economia-plataforma".

---

## Fase 1 — Pareceres independentes

### EIC — Editorial

**Recomendação:** Minor Revision · **Confiança:** 4/5

**Síntese.** O artigo caracteriza o Espírito Santo como "economia-plataforma" combinando quatro
leituras de IO (vazamento do multiplicador, assimetria *spillover/feedback*, destino interestadual
e *upstreamness*) sobre matrizes bi-regional/interestadual de 2008 e WIOD 2014. A execução é
sólida e — incomum — **integralmente reprodutível**. A contribuição é clara para o leitor de
economia regional brasileira e bem situada na tradição IIOAS. O principal risco editorial não é de
correção (os números conferem), mas de **interpretação**: distinguir o que é específico do ES do
que é propriedade genérica de uma região pequena e aberta. Aderência boa a RBERU/EconomiA;
recomendo Minor Revision.

**Strengths.**
- **S1 — Reprodutibilidade exemplar.** Pipeline `01–13` + CSVs versionados; todos os números do
  corpo reproduzem do dado real. Raro no campo e merece destaque editorial.
- **S2 — Síntese com identidade.** O conceito de "economia-plataforma" amarra quatro indicadores
  dispersos numa narrativa única e testável (Tab. `tab:setores`, `tab:cluster`, Fig. `fig:upstream`).
- **S3 — Contribuição incremental real.** A desagregação do destino do *spillover* para as 27 UFs
  (§4.3: SP 37,8%, Sudeste 65,4%) vai além do tratamento bi-regional agregado da tradição.

**Weaknesses.**
- **W1 — Específico vs. genérico.** *Problema:* a tese trata o baixo *feedback* (0,32%) como achado
  do ES, mas é parcialmente mecânico para regiões pequenas e abertas. *Por que importa:* sem um
  contraste explícito, o leitor não sabe quanto é "ES" e quanto é "região pequena qualquer".
  *Sugestão:* explicitar o *benchmark* (já há Haddad 27,4% e o cluster; falta formalizar o argumento).
  *Severidade:* Major.
- **W2 — Janela 2008 × Fundão.** *Problema:* o objeto central (mineração/Samarco) foi alterado por
  Fundão (2015), posterior à matriz. *Sugestão:* qualificar o alcance temporal já no resumo/§1, não
  só no §6. *Severidade:* Major.

**Dimension Scores:** Originality 66 (Adequate) · Methodological Rigor 70 (Adequate→Strong) ·
Evidence 68 (Adequate) · Coherence 75 (Strong) · Writing 78 (Strong) · **Weighted 70,7 → Minor Revision**.

---

### R1 — Peer Reviewer (Metodologia)

**Recomendação:** Major Revision · **Confiança:** 5/5

**Síntese.** Reproduzi mentalmente o aparato: coeficientes técnicos, inversa de Leontief, partição
de Isard com inversa particionada para o *feedback*, ligações de Rasmussen-Hirschman (para frente
pela inversa de **Ghosh**, correta) e *upstreamness* de Antràs-Chor sobre a WIOD. A execução está
**correta** e a transparência é alta. Minha ressalva é de **desenho**, não de cálculo: um
único *cross-section* de fluxos **estimados** (IIOAS gravitacional), reportado em estimativas
pontuais sem qualquer banda de incerteza.

**Strengths.**
- **S1 — Convenção de *feedback* correta.** A partição $(I-A^{LL}-A^{LM}(I-A^{MM})^{-1}A^{ML})^{-1}$
  é a forma certa (Miller-Blair, cap. 3), e o artigo reporta a robustez 0,15–0,32% à convenção.
- **S2 — Para-frente pela inversa de Ghosh** (e não soma de linha de Leontief) — detalhe técnico
  correto que muitos artigos erram.

**Weaknesses.**
- **W1 — Sem quantificação de incerteza.** *Problema:* os fluxos inter-regionais são estimados por
  modelo gravitacional; os destinos (SP 37,8%, RJ 14,7%…) e o vazamento (24,9%) são pontuais.
  *Por que importa:* a precisão aparente excede a precisão do dado. *Sugestão:* análise de
  sensibilidade (variar o fator $F$ do IIOAS / a impedância; reportar faixas) ou ao menos um
  parágrafo sobre propagação de erro. *Severidade:* **Major**.
- **W2 — *Baseline* mecânico ausente.** *Problema:* não há um modelo nulo ("o que um estado pequeno
  e aberto típico mostraria?"). *Sugestão:* simular a decomposição para um estado sintético de mesmo
  porte/abertura, ou citar a regularidade de *feedback* pequeno (Miller, 1966). *Severidade:* Major.
- **W3 — Mistura de safras/agregações.** *Problema:* MIP 2008 (26 setores) + WIOD 2014 (56) +
  comparação com Haddad 2011 (68). *Sugestão:* tabela de concordância e nota explícita sobre o que
  é comparável. *Severidade:* Minor.

**Dimension Scores:** Methodological Rigor 64 (Adequate) · Evidence 66 (Adequate) · Reproducibility
(nota qualitativa: Exceptional) · **inclinação: Major Revision** (pela incerteza + baseline).

---

### R2 — Peer Reviewer (Domínio)

**Recomendação:** Minor Revision · **Confiança:** 4/5

**Síntese.** Após as últimas revisões, a cobertura da literatura inter-regional brasileira está
**boa**: Haddad (2017), Porsse et al. (2008), Domingues & Haddad (2002), Peixoto et al. (2013),
Figueiredo et al. (2004), além de Guilhoto-OECD (2019) e Antràs-Chor para a camada CGV. O
posicionamento na "tradição IIOAS" é preciso. Restam dois ajustes de enquadramento.

**Strengths.**
- **S1 — Ancoragem na tradição.** O §5 conecta a assimetria capixaba aos precedentes RS/MG, e o
  §4.4/§4.5 trazem MT (Figueiredo 2004) e o agronegócio gaúcho montante/jusante (Peixoto 2013).
- **S2 — Enquadramento não-censitário** (Round 1983; LQ/FLQ; CHARM) no §2 justifica a escolha do método.

**Weaknesses.**
- **W1 — Construção do cluster.** *Problema:* o "cluster de estados dinâmicos" (SC, PR, ES, MG, RS,
  GO, MT, MS) vem de leitura de mercado (Apex), não de um critério estatístico (§4.4, nota de rodapé).
  *Por que importa:* a seleção sustenta números (33,9% do PIB, 52,5% ao núcleo). *Sugestão:*
  justificar por um critério replicável (ex.: vazamento médio + share de base acima da mediana) ou
  reposicionar como "ilustração" e não "cluster". *Severidade:* Major.
- **W2 — Literatura de economia pequena e aberta.** *Problema:* falta diálogo com o ramo de IO que
  trata regiões pequenas/abertas e a pequenez genérica do *feedback*. *Sugestão:* incorporar
  Miller (1966) e a discussão de Miller-Blair sobre efeitos de transbordamento. *Severidade:* Minor.

**Dimension Scores:** Originality 68 · Literature Integration 78 (Strong) · Coherence 75 ·
**Minor Revision**.

---

### R3 — Peer Reviewer (Perspectiva)

**Recomendação:** Minor Revision · **Confiança:** 3/5

**Síntese.** Do ângulo de geografia econômica/desenvolvimento, o trabalho é relevante: nomeia um
mecanismo (valor que transita sem se fixar) com implicação direta de política (captura de valor,
royalties, adensamento de cadeia). A nova **dimensão ambiental** (carbono-plataforma) amplia o
alcance. Falta converter o diagnóstico em recomendações de política mais concretas.

**Strengths.**
- **S1 — Ponte estrutura→política.** O "mapa de vazamento como mapa de oportunidade" (§5) é uma
  leitura acionável para a SEDES/BANDES e para o debate de royalties.
- **S2 — Extensão de carbono com substância.** O §7 (iv) ancora a extensão ambiental em dados de IO
  (siderurgia ~22 mil t CO₂/R\$ bi; metalurgia ~80% intermediária; Carvalho & Perobelli 2009;
  Yamano & Guilhoto 2020) — abre uma agenda concreta.

**Weaknesses.**
- **W1 — "So what?" de política subdesenvolvido.** *Problema:* o diagnóstico é forte, mas as
  implicações ("adensar cadeia") ficam genéricas. *Sugestão:* identificar 2–3 setores-alvo do
  próprio dado (maior vazamento × maior peso) e a alavanca de política correspondente. *Severidade:* Major.
- **W2 — Atores ausentes.** *Problema:* royalties/compensação (a contrapartida fiscal do valor que
  vaza) não entram no quadro. *Sugestão:* um parágrafo conectando vazamento real a transferências
  fiscais. *Severidade:* Minor.

**Dimension Scores:** Significance & Impact 74 (Adequate→Strong) · Coherence 74 · **Minor Revision**.

---

### Devil's Advocate

**Afirmação prévia (justiça):** o artigo é tecnicamente correto e reprodutível, e a desagregação do
destino interestadual é uma contribuição genuína.

#### Strongest Counter-Argument (≈250 palavras)
A tese "economia-plataforma" corre o risco de **renomear uma mecânica genérica como descoberta**.
Em modelos inter-regionais, uma região pequena, aberta e especializada em *commodities* primárias
**necessariamente** exibe (i) alto vazamento do multiplicador, (ii) *feedback* inter-regional
próximo de zero e (iii) posição a montante na cadeia — não porque o ES seja singular, mas porque
essas três propriedades decorrem do **porte e da abertura**, não de uma "vocação plataforma". O
próprio Miller-Blair observa que efeitos de *feedback* inter-regional são, em geral, pequenos; e a
Tabela 2 de Haddad mostra **vários** estados com parcela inter-regional do multiplicador semelhante
(MT 27,4%, AM 25,2%, MS 29,7%…). Ou seja, o que o artigo chama de "plataforma" pode ser, em boa
parte, "estado pequeno-aberto-primário qualquer". Um cético diria: o resultado é **verdadeiro mas
quase tautológico** — a metodologia praticamente garante o sinal antes de ver o dado. Soma-se a
isso que a fotografia é de **2008**, anterior ao choque de Fundão (2015) que reorganizou justamente
a mineração capixaba, e que o **cluster** comparativo é um agrupamento de mercado (Apex), não
estatístico — escolhido, talvez, porque produz o contraste desejado com SP/RJ. Sem um modelo nulo
explícito (quanto do 0,32% é "ES" e quanto é "porte"?), a contribuição empírica fica difícil de
separar do artefato metodológico. O artigo não está errado; ele precisa **provar que é sobre o ES**.

#### Issue List

**MAJOR**
| # | Dimensão | Descrição | Local |
|---|---|---|---|
| DA-1 | Logic chain / Overgeneralization | *Feedback*≈0 e alto vazamento podem ser propriedade genérica de região pequena-aberta, não específica do ES; falta modelo nulo/benchmark formal | §4.1–4.2, §5 |
| DA-2 | Confirmation bias | Cluster definido por leitura de mercado (Apex), não por critério estatístico; pode ter sido escolhido por gerar o contraste desejado | §4.4 (nota) |
| DA-3 | Overgeneralization (temporal) | Conclusões estruturais sobre a mineração do ES a partir de matriz **2008**, anterior a Fundão (2015) | §6 (deveria subir ao resumo) |

**MINOR**
| # | Dimensão | Descrição | Local |
|---|---|---|---|
| DA-4 | Evidence gap | Camada de carbono é externa (SP/RB e global), sem dado de emissão do ES — corretamente "agenda", mas a redação beira a antecipação de resultado | §7 (iv) |
| DA-5 | Logic | "71% das exportações em 3 setores" sustenta a tese, mas o numerador/denominador (pauta vs. produção) poderia ser explicitado | §4.5 |

#### Explicações alternativas ignoradas
1. **Porte e abertura** explicam (i)–(iii) melhor que "vocação plataforma" — modelo nulo necessário.
2. **Geografia de transporte/impedância** (proximidade a SP) pode dirigir o destino do *spillover*
   tanto quanto a estrutura produtiva — o IIOAS embute a impedância, então parte do "65,4% ao
   Sudeste" pode ser distância, não economia-plataforma.

#### Perspectivas de *stakeholder* ausentes
- Tesouro estadual / royalties (a contrapartida fiscal do valor que vaza).
- Trabalhadores: o vazamento de **emprego** (já calculado, §4.1) merece leitura distributiva.

#### Observações (não-defeitos)
- A honestidade do §6 (limitações declaradas) e a robustez 0,15–0,32% à convenção são pontos a favor
  que **enfraquecem** parcialmente DA-1 — o artigo já está a meio caminho de responder.

---

## Fase 2 — Síntese editorial

### DECISÃO: **Minor Revision**

| Parecerista | Papel | Recomendação | Confiança |
|---|---|---|---|
| EIC | Editor regional | Minor Revision | 4 |
| R1 | Metodologia (IO) | **Major Revision** | 5 |
| R2 | Domínio (regional) | Minor Revision | 4 |
| R3 | Perspectiva (geo/dev) | Minor Revision | 3 |
| DA | Advogado do diabo | (sem nota; 3 MAJOR, 0 CRITICAL) | — |

### Consenso

**[CONSENSO-4+]** — Reprodutibilidade/transparência é força distintiva (EIC-S1, R1-S1/S2, R2-S1).
**[CONSENSO-4+]** — É preciso **separar o específico-ES do genérico-região-pequena** (EIC-W1, R1-W2,
R2-W2, DA-1) → este é o eixo da revisão.
**[CONSENSO-3]** — Janela 2008 × Fundão deve ser elevada ao resumo/§1 (EIC-W2, DA-3).
**[CONSENSO-3]** — Construção do cluster precisa de critério replicável (R2-W1, DA-2).

### Divergência principal
- **R1 (Major) × demais (Minor).** *Tipo:* severidade. *Arbitragem do editor:* **Minor Revision**.
  *Razão:* as três objeções centrais (benchmark/null, incerteza, cluster) são endereçáveis **com o
  dado já existente** — um modelo nulo/benchmark, uma análise de sensibilidade do fator $F$/impedância
  e um critério de cluster não exigem nova coleta. Combinado à execução verificadamente correta e à
  ausência de achado DA-CRITICAL, o caso é de revisão menor exigente, não maior. (Se a sensibilidade
  revelar que os destinos são instáveis, a decisão de re-review migraria para Major.)

### Decisão — racional (≈220 palavras)
O manuscrito está acima da linha de corte (média ponderada ≈ 70/100; faixa Minor 65–79) e não há
falha fatal: os números reproduzem, as convenções de IO estão corretas (inclusive Ghosh e a inversa
particionada) e a literatura está bem coberta após as últimas revisões. O que separa o artigo de um
"Accept" não é correção, e sim **interpretação e robustez**: (1) demonstrar que o padrão é do ES e
não um artefato do porte/abertura (modelo nulo + leitura de Haddad Tab. 2 e Miller 1966); (2) reportar
**incerteza** sobre fluxos estimados; (3) dar ao cluster um critério replicável; (4) elevar a ressalva
2008×Fundão ao resumo. Nenhum item requer dado novo, o que justifica Minor (e não Major) apesar da
posição de R1. O Devil's Advocate não encontrou CRITICAL — sua objeção mais forte (quase-tautologia)
é séria mas **respondível** e, em parte, já antecipada pela robustez declarada no §6. Recomenda-se
aceitar mediante revisão menor exigente, com re-review focado nos itens R1–R4 abaixo.

### Revisões obrigatórias (Required)
| # | Item | Fonte | Severidade | Seção | Esforço |
|---|---|---|---|---|---|
| R1 | **Modelo nulo / benchmark do "plataforma".** Mostrar quanto do vazamento/feedback é genérico de região pequena-aberta (estado sintético OU leitura formal de Haddad Tab. 2 + Miller 1966). | DA-1, R1-W2, EIC-W1 | Major | §4.2/§5 | 4–6 d |
| R2 | **Incerteza dos fluxos estimados.** Sensibilidade ao fator $F$/impedância do IIOAS; reportar faixas para destinos e vazamento. | R1-W1 | Major | §3/§4.3 | 3–5 d |
| R3 | **Critério replicável do cluster** (ou rebaixar a "ilustração"). | R2-W1, DA-2 | Major | §4.4 | 1–2 d |
| R4 | **Elevar a ressalva 2008×Fundão** ao resumo e à §1. | EIC-W2, DA-3 | Minor→Major | Resumo/§1 | 0,5 d |

### Revisões sugeridas (Suggested)
| # | Item | Fonte | Prioridade |
|---|---|---|---|
| S1 | 2–3 setores-alvo de política do próprio dado (vazamento × peso) + alavanca | R3-W1 | P2 |
| S2 | Tabela de concordância de safras/agregações (2008/26 × 2014/56 × Haddad 2011/68) | R1-W3 | P2 |
| S3 | Parágrafo royalties/Tesouro como contrapartida fiscal do vazamento | R3-W2 | P3 |
| S4 | Explicitar numerador/denominador do "71% da pauta" | DA-5 | P3 |

### Roadmap de revisão
- **P1 (estrutural, ~1–1,5 sem):** R1 (benchmark/null) · R2 (sensibilidade) · R3 (cluster).
- **P2 (conteúdo, ~2–3 d):** R4 (resumo/Fundão) · S1 (política) · S2 (concordância).
- **P3 (texto, ~1 d):** S3 · S4 · polimento de prosa essayística (§5).
- **Total estimado:** Minor Revision exigente — **2–3 semanas**.

### Encerramento
Convidamos os autores a submeter versão revista atendendo aos pontos R1–R4; o eixo é **provar que o
resultado é sobre o Espírito Santo**, não sobre "uma região pequena qualquer". A base empírica e a
reprodutibilidade são uma força incomum; consolidá-la com um benchmark e bandas de incerteza deve
levar o trabalho ao patamar de aceitação.

---

# Verification Review (re-review mode) — Rodada 2

*Após correções fundamentadas na literatura. Agentes: field_analyst + EIC + editorial_synthesizer.*

## DECISÃO: **Minor Revision (banda superior) → recomendação de Accept** condicional ao item R2.

A primeira rodada foi Minor Revision com 4 itens obrigatórios. Verificação item a item:

| # | Comentário original | Status | Local | Avaliação |
|---|---|---|---|---|
| **R1** | Modelo nulo / benchmark "específico vs. genérico" | **FULLY_ADDRESSED** | §5 (novo §) | Parágrafo distingue o genérico (pequenez do *feedback*, ancorada em Miller 1966 + Haddad Tab. 2 com MT 28,5%, MS 29,7%, AM 25,2%) do específico-ES (concentração do destino 65,4/52,5% + *upstreamness* da pauta). Responde diretamente ao DA-1. |
| **R2** | Incerteza dos fluxos estimados (sensibilidade ao fator $F$/impedância) | **PARTIALLY_ADDRESSED** | §6 | Adicionado tratamento textual fundamentado (Riddington 2006; Flegg 2016) + leitura "ordens de grandeza" + robustez de convenção 0,15–0,32%. **Residual:** falta a *varredura numérica* de $F$ — que exige os insumos brutos do IIOAS, não disponíveis nas matrizes já finalizadas. Aceitável como limitação declarada neste tier; idealmente, rodar o *sweep* se os insumos forem obtidos. |
| **R3** | Critério replicável do cluster | **FULLY_ADDRESSED** | §4.4 (novo trecho) | Assinatura estrutural replicável computada do dado: 6/8 acima das duas medianas (abertura 21,8%, base 21,0%), todos os 8 acima da mediana de base, núcleo abaixo. Honesto: não afirma que o IO *deriva* o grupo, mas que o grupo *compartilha* assinatura mensurável. |
| **R4** | Ressalva 2008×Fundão no resumo/§1 | **FULLY_ADDRESSED** | Resumo + §1 | Caveat inserido no resumo ("safra anterior ao rompimento de Fundão em 2015") e no §1 ("circunscreve seu alcance temporal"). |

## Novos problemas (varredura da revisão)
| # | Tipo | Local | Descrição | Severidade |
|---|---|---|---|---|
| NEW-1 | Consistência | §5 vs Tab. 3 | Os números do §5 (MT 28,5%) são da **Tab. 2 de Haddad** (parcela inter do multiplicador total), distintos do vazamento da **Tab. 3 do próprio artigo** (MT 27,4%). Estão **atribuídos corretamente** ("a Tabela 2 de Haddad et al."), mas convém uma nota para o leitor não conflar as duas métricas. | Minor |

## Racional da nova decisão
Três dos quatro itens obrigatórios estão **FULLY_ADDRESSED** e o quarto (R2) está endereçado no nível de
redação/literatura — o único resíduo é a varredura numérica de $F$, que depende de dado não disponível e
é razoavelmente coberta pela robustez de convenção já reportada. O eixo de consenso da rodada 1 ("provar
que é sobre o ES") foi atacado de frente em §5 (R1), que neutraliza a objeção mais forte do Devil's
Advocate. A pontuação ponderada sobe de ≈70,7 para ≈**73** (Originality 68 · Methodology 74 · Evidence 70
· Coherence 78 · Writing 78), ainda em banda Minor mas próxima do corte de Accept. **Recomendação:**
aceitar mediante (a) a varredura de $F$ **ou** a manutenção explícita do resíduo como limitação declarada
(já feita), e (b) a nota NEW-1. Nenhum novo problema CRITICAL/MAJOR introduzido pela revisão.
