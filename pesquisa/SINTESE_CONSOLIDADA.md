# Síntese consolidada — o que já foi feito e o que pode melhorar

*Skill `academic-research-skills` (deep-research, modo review/síntese) sobre o corpus **completo** do
repositório: 3 versões do artigo, 23 scripts, 14 documentos de pesquisa, auditorias, pareceres e o
`.tex` local mais recente enviado pelo autor. Data: 2026-07-09. Objetivo (pedido do autor): "olhar
tudo, condensar, entender o que já foi feito e o que pode melhorar" — porque partes detalhadas
(fórmulas, resultados) foram se perdendo entre as reescritas.*

---

## 0. TL;DR

O projeto já tem **um artigo maduro e aprovável** (`es_estrutura_produtiva.tex`, versão local de
julho: 4 frentes empíricas + parecer Minor→Accept + integridade PASS). O problema não é falta de
material — é o **oposto**: o material está espalhado em 3 artigos e 14 documentos, e a cada
reescrita a versão corrente **perdeu camadas** que as anteriores tinham (equações numeradas do
método, modelo nulo com escores-z, extração hipotética, discussão de regionalização). Além disso, a
versão local do `.tex` cita **2 scripts e 2 CSVs que não estão no repositório** — a reprodutibilidade,
que é a marca do projeto, está quebrada na margem. Este documento é o índice-mestre: mapeia tudo o
que existe (§1–§3), lista o que se perdeu e onde recuperar (§4–§5), e propõe o plano de fechamento
priorizado (§6–§7).

---

## 1. A linha do tempo do projeto (3 ciclos, 1 pivô)

| Ciclo | Artigo | Tese | Status |
|---|---|---|---|
| **v1** | `paper/es_insumo_produto.tex` (9 págs, 20 refs) | *O ES como economia-plataforma*: vazamento 24,9%, spillover R$ 18,2 bi vs feedback 0,32%, destino concentrado no núcleo SP/RJ (52,5%), upstreamness 3,12 | Completo, auditado (`AUDITORIA.md`, `AUDITORIA_HARD.md`), parecer Minor→Accept (`REVIEW_FULL_MODE.md`). **Arquivado** como working paper |
| **v2** | `paper/es_plataforma_fractal.tex` (6 págs, 6 refs) | *A plataforma é fractal*: mecânica de vazamento/feedback é genérica de posição-e-porte (modelo nulo 27 UFs, z-scores; R²=0,59/0,91), a especificidade do ES é **composicional** | Completo, integridade PASS (`INTEGRITY_RQ_AB.md`). **Descartado pelo autor** ("não é essa a pegada") e parcialmente absorvido na v3 |
| **v3** | `paper/es_estrutura_produtiva.tex` | *Estrutura Produtiva do ES*: caracterização no gênero clássico brasileiro ("Estrutura Produtiva de [Estado]"), com a plataforma como **uma seção** (abertura) | **Versão viva.** Parecer Major→revisão→Minor→Accept; Stage 4.5 PASS; a versão local (julho) adiciona C4 (decomposição pela demanda final) e multiplicadores territoriais |

O pivô v2→v3 está registrado em `paper_creation_process.md` (a decisão editorial mais importante do
projeto). A regra que emergiu dele — **"conciliar > descartar"** — foi aplicada só em parte: a v3
absorveu as *conclusões* da v1/v2, mas não o seu *aparato* (ver §4).

## 2. Inventário do que existe

### 2.1 As quatro frentes empíricas da v3 (todas verificadas)

| Frente | Matriz | Scripts | Resultados-âncora |
|---|---|---|---|
| **C1 Retrato 2008** | MIP ES×RB 2008 (26 set., c/ emprego) | `17`, `19`, `22` | mult. produção 1,76 (I)/2,45 (II); emprego concentrado em trabalho-intensivos (têxtil 67,9); setores-chave = transformação; mineração enclave (p/ trás ≈0,9); ligações puras: mineração 4,4, metalurgia 3,4; benchmark 27 UFs: ES 2º em base (36,4%), 24º em mult. emprego, "genérico em tipo, extremo em grau" |
| **C2 Panorama 2010–2021** | Série nacional N68 (NEREUS) | `18`, `diag_sider` | celulose adensa (1,41→1,51); siderurgia recua em 2021 por **efeito de preço** (diagnóstico próprio); extração permanece enclave (<1) |
| **C3 Território 2015** | Sistema 10 microrregiões (35 set.) | `20`, `21` | mosaico de vocações (LQ: celulose 8,2 Rio Doce; rochas 7,7; minério 9,5; têxtil 9,6; pecuária 21,9); HHI territorial: enclaves extrativos são os mais mono-estruturais; metrópole retém 90,9% vs Litoral Sul 66,2% *(retenção: script local `24`, ver §5)* |
| **C4 Quem puxa** | MIP ES×RB 2008 | *`25` (local, não versionado)* | demanda externa induz **61,7% da produção mas só 47,5% do emprego**; refino/metalurgia/mineração >96% puxados de fora |
| **+ Abertura** (herdada v1/v2) | ES×RB + interestadual 27 UFs | `01`–`16` | vazamento 24,9%; spillover→núcleo 52,5%, feedback 0,32%; invariância de escala R² 0,59/0,91; upstreamness 3,12 (WIOD) |

### 2.2 Scripts (23 versionados + 2 ausentes)

- `01`–`13`: pipeline da v1 (base bi-regional, interestadual, cluster, upstreamness, sankey, tabela
  setorial, auditoria contrafactual).
- `14`–`16`: pipeline da v2 (benchmark nulo 27 UFs, intra-ES fractal, figura).
- `17`–`22`: pipeline da v3 (caracterização 2008, trajetória N68, microrregiões, benchmark de
  caracterização).
- `23`: carbono-plataforma — **pronto, aguardando o vetor de CO₂** (para se o dado não existir; ver
  `DEEP_RESEARCH_CARBONO.md`).
- **`24_micro_mult_chave.py` e `25_decomposicao_fd.py`: citados no `.tex` local, NÃO estão no
  repositório** (nem `outputs/micro_multiplicadores.csv` e `outputs/decomposicao_fd.csv`). Estão só
  na máquina local → **P0 do plano (§6)**.

### 2.3 Documentos de processo (o que consultar para quê)

| Preciso de… | Documento |
|---|---|
| Materiais do professor (`Material IO/`) triados e classificados | `DEEP_RESEARCH_MATERIAL_IO.md` (16 docs: 8 estritos, 3 agenda ambiental, 2 método, 2 fora) |
| O gênero "Estrutura Produtiva de [Estado]" e a bateria padrão | `DEEP_RESEARCH_CARACTERIZACAO.md` |
| Literatura de regionalização/IIOAS (22 fontes anotadas, matriz fonte×tema) | `REVISAO_LITERATURA_IIOAS.md` |
| Números da caracterização e do fractal | `RESULTADOS_CARACTERIZACAO.md`, `RESULTADOS_RQ_AB.md` |
| Auditoria numérica (todos os números de manchete regenerados do zero) | `AUDITORIA.md`, `AUDITORIA_HARD.md` |
| Pareceres e respostas (2 rodadas, v1 e v3) | `REVIEW_FULL_MODE.md`, `REVIEW_CARACTERIZACAO.md`, `RESPOSTA_AOS_PARECERISTAS.md` |
| Gates de integridade (0 alucinação; 2 erros pegos e corrigidos) | `INTEGRITY_*.md` |
| Agendas futuras (RQ-C SDA nacional, RQ-D WIOD 2000×2014, RQ-E carbono) | `DEEP_RESEARCH_PANORAMA.md`, `DEEP_RESEARCH_CARBONO.md` |
| Registro do processo e lições | `paper_creation_process.md` |

## 3. Materiais do professor: o que já entrou e o que ainda não

Da triagem de `Material IO/` (`DEEP_RESEARCH_MATERIAL_IO.md`), **já incorporados** à v3: Haddad et
al. (2017), Figueiredo et al. (2004, MT), Porsse et al. (2008, RS), Peixoto et al. (2013, RS),
Guilhoto & Sesso Filho (2005), Miller & Blair, Antràs-Chor, Carvalho & Perobelli (2009, agenda).
**Ainda não aproveitados** e relevantes para a pegada "caracterização de estados → ES":

1. **Estudos do gênero localizados mas nunca verificados/citados** — "Estrutura Produtiva do Pará"
   (MPRA), "Estrutura Produtiva de Santa Catarina", matriz inter-regional do Maranhão (apontados em
   `DEEP_RESEARCH_CARACTERIZACAO.md` §6.2 como "a verificar"). Hoje a v3 cita só MT e RS como
   precedentes do gênero; verificar e citar PA/SC/MA fecharia a moldura "trazer os melhores artigos
   de caracterização estadual para o ES".
2. **Domingues & Haddad (2002, MG/RB)** — estava na v1 e na revisão de literatura, **caiu na v3**.
   É o precedente bi-regional mais próximo (MG, economia mineral vizinha).
3. **Bloco de regionalização** (Round 1983 ficou; mas Chenery-Moses, FLQ 2016, CHARM, Riddington
   2006, Dixon & Rimmer, Hulu & Hewings — todos anotados em `REVISAO_LITERATURA_IIOAS.md`) —
   a v3 comprimiu a discussão de método não-censitário a 3 linhas.
4. **Guilhoto et al. (2010, Nordeste)** e **Ichihara & Guilhoto (2008, municípios SP)** — precedentes
   diretos do recorte multiestadual e intra-estadual; nunca citados.

## 4. O que se perdeu entre as versões (o diagnóstico central)

A migração v1→v2→v3 comprimiu o método a parágrafos de prosa. A v3 **não tem uma única equação
numerada**; a v1 tinha o particionamento de Isard exibido (eqs. 1–2, notação Miller-Blair LL/LM/ML/MM,
elogiado pelo parecerista R1 como "a forma certa"); a v2 tinha, além dele, o modelo nulo
(`m_r = α + β ln x_r`) e a extração hipotética. Inventário do que existe em versões antigas e não está
na v3 local:

### 4.1 Fórmulas e aparato de método
| Item | Onde está | Estado na v3 |
|---|---|---|
| Partição de Isard $A$/$L$ em blocos LL/LM/ML/MM + forma reduzida com feedback explícito (2 equações) | v1 §3 (eqs. 1–2) | prosa inline, sem display |
| Modelo nulo métrica ~ α + β·ln(porte) (a máquina por trás dos R²=0,59/0,91) | v2 §3 | R² citados **sem** o modelo que os gera |
| Extração hipotética (Miller-Blair) | v2 §3 | ausente |
| HHI de concentração de destino do spillover | v2 §3 | só o HHI de composição territorial ficou |
| Discussão não-censitária completa (Chenery-Moses, LQ/FLQ, CHARM, gravitacional, Riddington) | v1 §2 | reduzida a FLQ/GRAS em 3 linhas |
| Tratamento de qualidade WIOD (49/2464 setores negativos; 185 excluídos; nível+ranking) | v1 §6 + `AUDITORIA_HARD.md` E | 1 linha ("ranking, não nível") |

### 4.2 Resultados computados que sumiram do texto
| Resultado | Script/CSV | Por que importa |
|---|---|---|
| **ES não é outlier em nenhuma métrica de decomposição** (z-scores +0,45/−0,05/+0,03; feedback observado 0,32% *abaixo* do previsto 0,45% para o porte) | `14`, `benchmark_ufs.csv` | é a resposta mais forte ao "genérico vs específico" — mais forte que o benchmark composicional que ficou |
| **Extração hipotética da metrópole: −13,0%** na produção da periferia | `15` | fecha quantitativamente o desenho centro-periferia da §Território |
| Núcleo SP+RJ feedback 1,97% vs cluster 0,49% | `14` | dá escala à assimetria |
| MG (60%) e RS (55%) escoam mais ao núcleo que o ES (52,5%); ES é 14º/27 em HHI de destino | `benchmark_ufs.csv` | qualifica a concentração de destino (não é recorde capixaba) |
| Sensibilidade S23 (coluna desbalanceada: 8,4%→7,9%; R² estável) | `15` | robustez do sistema microrregional, hoje só "declarada" em Limitações |
| Vazamento de **emprego** por setor (refino 61,6% etc.) | `01`, `es_setores_resultados.csv` | está na Tabela `tab_setores` mas perdeu a leitura distributiva que a v1 fazia |

### 4.3 Referências que caíram (v1+revisão → v3)
`domingues2002matriz` · `flegg2016evaluating` · `tobben2015charm` · `riddington2006comparison` ·
`oecd2019tiva` · `tukker2013global` · `guilhoto2019exploring` · `yamano2020co2` — todas verificadas
em rodadas anteriores; as quatro primeiras sustentavam exatamente a discussão de incerteza dos fluxos
estimados que o parecerista R1 cobrou (R2 do parecer: "sensibilidade/incerteza" — hoje respondida só
com FLQ 1995/2000 e GRAS).

> **Recomendação estrutural (como condensar sem perder):** corpo enxuto como está + **Apêndice A
> (formulário metodológico)** com as equações numeradas de todas as ferramentas (Leontief, tipo II,
> Isard/feedback, RH/Ghosh, ligações puras GSH, LQ, HHI, decomposição de demanda final, modelo nulo,
> extração hipotética) + **Apêndice B (robustez)**: z-scores do modelo nulo, sensibilidade S23,
> conciliação 24,9/22,8/27,4%, tratamento WIOD. Assim a síntese não briga com o detalhe — cada um
> tem seu lugar, e nada mais se perde nas próximas reescritas.

## 5. Divergência repositório × máquina local (achado desta revisão)

O `.tex` enviado (773 linhas) está **à frente** do commitado (641 linhas). O que a versão local
adiciona: §Método "Decomposição pela demanda final"; §Retrato "Quem puxa a economia" +
Tabela `tab:decomp`; §Território "Multiplicadores e retenção territorial" + Tabela `tab:micro`;
referência Peixoto et al. (2013) reincorporada. Esta versão foi **commitada agora** nesta branch
para não se perder. Ficam faltando na origem (só existem na sua máquina):

- `pesquisa/24_micro_mult_chave.py` → `outputs/micro_multiplicadores.csv`
- `pesquisa/25_decomposicao_fd.py` → `outputs/decomposicao_fd.csv`

Sem eles, a Tabela 1 (decomposição) e a Tabela 4 (retenção territorial) **não são reproduzíveis** —
e a reprodutibilidade é o ponto forte reconhecido por todos os pareceristas. Além disso, três
artefatos do repositório estão **desatualizados** e apontam para a v1: `README.md` (descreve o
artigo-plataforma como produto principal), `CITATION.cff` (título da v1) e `Makefile` (alvo `paper`
compila `es_insumo_produto.tex`).

## 6. Plano de melhoria priorizado

| # | Ação | Esforço | Ganho |
|---|---|---|---|
| **P0** | **Commitar da máquina local** os scripts `24`/`25` + 2 CSVs (fechar a reprodutibilidade da versão atual) | minutos | crítico |
| **P1** | Atualizar `README.md`, `CITATION.cff`, `Makefile` para a v3 (hoje descrevem a v1) | 30 min | higiene/apresentação |
| **P2** | **Apêndice A (formulário metodológico)** + **Apêndice B (robustez)** restaurando o aparato perdido (§4.1–4.2), recuperando as equações da v1/v2 | ½–1 dia | responde diretamente a queixa "as fórmulas se perderam"; blinda o método |
| **P3** | Reincorporar ao texto os 3 resultados perdidos de maior valor: z-scores do modelo nulo (§benchmark), extração hipotética −13% (§território) e núcleo 1,97% vs 0,49% (§abertura) | ½ dia | fortalece exatamente o eixo "específico × genérico" que decidiu o parecer |
| **P4** | **Ancoragem teórica na economia regional**: o artigo usa "economia de base" sem citar a teoria da base de exportação (North 1955; Tiebout 1956) e identifica "polos de crescimento" via ligações puras sem citar Perroux (1955) — as duas pontes canônicas do debate regional que o professor pediu. Cano e Friedmann já estão; falta fechar o triângulo | ½ dia + verificação das refs | insere o ES no **debate** de economia regional, não só no método |
| **P5** | Verificar e citar os estudos do gênero PA/SC/MA + Domingues & Haddad (2002) + Guilhoto NE (2010) (§3 acima) | ½ dia | completa "os melhores artigos de caracterização de estados → ES" |
| **P6** | **Âncora 2019**: reestimar a bateria central (multiplicadores, RH, vazamento, destino) na matriz interestadual de Haddad et al. (2025, ano-base 2019, 68 set., com satélite de emprego) e comparar 2008×2019 — transforma "2008–2021" de retrato+pano de fundo em **duas fotografias comparadas** | 2–4 dias (dado público na RBERU) | a maior elevação de contribuição disponível; de quebra habilita P7 |
| **P7** | Carbono-plataforma: baixar o satélite de CO₂ da mesma matriz 2019 → `dados/co2_intensidade.csv` → rodar `23` | 1 dia após P6 | fecha a agenda ambiental já declarada na Discussão |
| **P8** | Consolidação documental: os 14 `.md` de `pesquisa/` ficam como trilha; este arquivo é o índice-mestre (apontado no README) | feito | navegabilidade |

**Sequência sugerida até a entrega (18/07):** P0+P1 imediatos → P2+P3 (o "recheio" perdido) →
P4+P5 (literatura) → P6/P7 se houver fôlego (senão ficam como agenda declarada, que o texto já faz).

### Status da execução (atualizado em 2026-07-13)

| # | Status | Observação |
|---|---|---|
| P0 | ✅ **fechado** (commit `9cc83ea`) | `fechar_R1.bat` executado: asserts `[OK]` nos 3 scripts; 4 CSVs commitados; paridade verificada célula a célula (APPROVE do review theorist-toolbox) |
| P1 | ✅ | README/CITATION/Makefile descrevem a v3 |
| P2 | ✅ | Apêndices A (9 subseções, 8 equações) e B (5 subseções) no `.tex` |
| P3 | ✅ | z-scores, extração hipotética (−13%), núcleo 1,97% vs cluster 0,49% reintegrados |
| P4 | ✅ | North/Tiebout/Perroux + ponte tipo II; Domingues & Haddad (2002) no benchmark |
| P5 | ✅ parcial | Pará citado (Sesso Filho & Guilhoto 2010, RBERU 4(2), verificado); SC/MA fora — metadados não confirmados (rede bloqueou as fontes primárias) |
| P6 | 🔧 infraestrutura pronta | `26_ancora_2019.py` fail-closed: para sem o dado, inspeciona layout no 1º contato, computa a bateria com LAYOUT confirmado. **Falta:** baixar os suplementos de Haddad et al. (2025) — RBERU art. 1225 ou NEREUS/USP (hosts bloqueados pela rede deste ambiente) — para `dados/MIP_2019/` |
| P7 | 🔧 pipeline pronto (`23`) | o satélite de CO₂ vem no MESMO pacote da matriz 2019 → agregar aos 26 setores em `dados/co2_intensidade.csv` |
| P8 | ✅ | este arquivo é o índice-mestre (apontado no README) |

**Pós-plano (rodada 3 de parecer, `REVIEW_FULL_MODE_V2.md`):** decisão Minor Revision (banda
superior) → Accept condicional; R2–R4 e S1–S5 aplicados (`RESPOSTA_AOS_PARECERISTAS.md`,
seção rodada 3); R1 = P0. Artigo: 19 págs, 36 refs, 0 indefinidas.

**Rodada editorial (planejada 2026-07-16, executada 2026-07-17):** plano e status em
[`PLANO_MELHORIAS.md`](PLANO_MELHORIAS.md) — resumo 422→181 palavras; 6 figuras regeneradas
no padrão editorial (PDF vetorial, vírgula decimal, sem título embutido); abstract EN;
babel/microtype/caption; nova §2 "Quadro analítico" (lentes de economia regional ↔
instrumentos de insumo-produto, com tabela-síntese); 7 refs novas verificadas (Richardson
1985; Guilhoto et al. 2010 NE; Ichihara & Guilhoto 2008; Bittencourt et al. 2023 SC;
Flegg et al. 2016; Többen & Kronenberg 2015; Riddington et al. 2006). Artigo: 21 págs.,
43 refs, 0 indefinidas.

**Rodada 4 de parecer (2026-07-17):** full-mode sobre a versão pós-editorial
(`REVIEW_FULL_MODE_V3.md`) — decisão **Minor (banda superior) → Accept condicional a F1**;
itens 1–6 do roadmap aplicados na hora (`RESPOSTA_AOS_PARECERISTAS.md`, rodada 4): conciliação
18,2/18,1 no Apêndice B.3, gramática do abstract EN, claim de raridade removido de §2,
Bittencourt 2023 reenquadrado, legendas de figura na convenção script-do-dado, alavancas
condicionadas às safras. Resta só F1 (autor).

## 7. Estado editorial (para não retrabalhar o que está fechado)

- Parecer v3: Major → 4 obrigatórios + 4 sugeridos **FULLY ADDRESSED** → re-review **Minor→Accept**
  (resíduo NEW-1 resolvido por nota). Integridade Stage 2.5 e 4.5: **PASS, zero issues**.
- Pendência de parecer **estruturalmente irresolvível** (declarada): varredura numérica do fator F
  do IIOAS — exige insumos brutos do método, não disponíveis. Mantida como limitação; não gastar
  esforço aqui.
- Convenção spillover/feedback: **fechada** (Miller-Blair V3: 51,5/18,2/0,164 bi; os 60,6/22,4/0,199
  do paper-semente não reproduzem — decisão registrada em `MAPA_DE_PESQUISA.md` B).
- Todos os números de manchete das 3 versões foram regenerados do zero a partir dos `.xlsx` crus
  (`AUDITORIA_HARD.md` §0) — nenhuma pendência numérica conhecida na versão commitada; a versão
  local depende de P0 para o mesmo status.
