# Deep research — panorama das *novas questões* (multiescala e temporal)

*Pipeline `academic-pipeline` v3.13 · **Stage 1 RESEARCH** (modo full) · idioma PT-BR.
Corpus: repositório [`es-insumo-produto`](https://github.com/fcarva/es-insumo-produto) + acervo local
`C:\Users\DELL\Downloads\Material IO`. Data: 2026-06-26.*

> **Para que serve este documento.** O artigo atual ("O ES como economia-plataforma") é uma **fotografia
> transversal de 2008** — escopo deliberadamente congelado (ver [`PLANO_ARTIGO.md`](PLANO_ARTIGO.md) §0).
> Chegaram **matrizes novas** que abrem o que antes foi adiado para "agenda futura". Este é o **brief de
> pesquisa** (RQ Brief + Metodologia + Bibliografia + Síntese) que escopa as **novas questões** sob um
> olhar **panorâmico**: não mais um ponto (ES-2008), mas um **programa multiescala e temporal**.
> É a entrada da Stage 1; a escrita de artigo (Stage 2) só começa após o checkpoint do usuário.

---

## 0. TL;DR — a virada de escopo

O trabalho de 2008 respondeu *"como é a estrutura do ES num instante"*. As matrizes novas permitem
responder algo **muito maior**: *"a lógica-plataforma é uma propriedade de **escala** e de **tempo**?"*
— quatro escalas geográficas aninhadas **e** uma série temporal nacional de 12 anos.

```
ESCALA            FONTE (no acervo)                        ANO(S)        STATUS
─────────────────────────────────────────────────────────────────────────────────────
🌍 Global         MIP-Mundo 2000  +  MIP-Mundo 2014 (WIOD) 2000 / 2014   2014 usado; 2000 NOVO
🇧🇷 Nacional/temp  Nível 68 (MIP-BR, 68 setores)            2010–2021     ★ NOVO, intocado (12 anos)
🗺️ Interestadual   MIP-26x26-BR (27 UFs)                    2008          usado (destino do vazamento)
📍 Bi-regional     MIP-ES-BR                                2008          base validada do artigo
🔬 Intra-ES        ES-2015 (estado) + 10 microrregiões      2015          ★ NOVO (antes "agenda futura")
```

Duas frentes genuinamente novas: **(i) o tempo** (Nível 68, 2010–2021 — atravessa Fundão/2015, a
recessão de 2014–16 e a COVID/2020) e **(ii) a escala fina** (10 microrregiões do ES). Juntas, elas
deixam de tratar "plataforma" como um rótulo descritivo de um estado e o transformam numa **hipótese
testável de invariância de escala e de dinâmica estrutural**.

---

## 1. Onde o artigo atual parou (e o que ficou em aberto)

Estado validado e revisado (ver [`MAPA_DE_PESQUISA.md`](MAPA_DE_PESQUISA.md),
[`REVIEW_FULL_MODE.md`](REVIEW_FULL_MODE.md)):

- **Tese:** o ES é economia-plataforma — encadeamento escoa ao núcleo SP/RJ (**52,5%** do spillover),
  com **feedback ≈ 0,32%**; vazamento médio do multiplicador **24,9%**; pauta a montante
  (*upstreamness* **3,12** vs. Brasil 1,91); mineração no **percentil ~98** global.
- **Métodos já implementados** (`src/io_core.py`, `pesquisa/01–13`): decomposição de Isard
  spillover/feedback (inversa **particionada**, Miller-Blair cap. 3), multiplicadores de produção e
  **emprego** com partição retido/vazado, ligações Rasmussen-Hirschman (para-trás por Leontief,
  para-frente por **Ghosh**), *upstreamness* de Antràs-Chor sobre WIOD.
- **Parecer (full-mode):** Minor Revision → Accept condicional. **Quatro resíduos abertos** que as
  matrizes novas atacam de frente:

| Resíduo do parecer | O que falta | Qual matriz nova resolve |
|---|---|---|
| **R1 — modelo nulo / específico-ES × genérico** | provar que feedback≈0 e vazamento alto não são só "região pequena-aberta qualquer" | **interestadual 27-UF** (benchmark cross-section) + **intra-ES** (invariância de escala) |
| **R2 — incerteza dos fluxos estimados** | bandas em torno dos pontos (IIOAS é gravitacional) | **Nível 68** dá variação ano-a-ano como proxy de robustez estrutural (não substitui o *sweep* de $F$) |
| **R3 — critério replicável do cluster** | grupo definido por leitura de mercado (Apex) | benchmark estatístico cross-UF substitui o cluster *ad hoc* |
| **R4 — janela 2008 × Fundão** | a fotografia é anterior ao choque de 2015 | **Nível 68 2010–2021** vê o choque na série nacional |

**Conclusão de intake:** as matrizes novas não são "mais do mesmo" — cada uma fecha um flanco que o
*referee* deixou aberto **e** abre uma contribuição autônoma. Isso justifica tratar isto como um
**novo ciclo de pesquisa**, não um retoque do artigo de 2008.

---

## 2. Inventário dos ativos novos (com viabilidade **verificada**)

Inspeção estrutural feita nesta sessão (openpyxl, read-only) e cruzada com as notas de layout do acervo
(`_micro.md`, `_inter.md`, `_wiod.md`).

### 2.1 ★ Nível 68 — MIP-BR, 68 setores, 2010–2021 (o ativo intocado)
- **12 arquivos** `.xlsm` (~14 MB cada), um por ano de **2010 a 2021**, layout **idêntico** entre anos
  (mesmas 44 abas: `Capa, Mundo, BR, BR2, 01…23, Ghosh, 01G…04G`).
- Formato padrão **IBGE/NEREUS (Guilhoto)**: abas numeradas seguem a TRU/MIP oficial; aba **`17`**
  carrega a MIP de 68 atividades com colunas de **demanda final desagregada** (Exportação, Consumo do
  Governo, ISFLSF, Famílias, FBCF, Variação de estoque); há aba **`Ghosh`** pronta (para-frente).
- **Viabilidade: ALTA.** Série **consistente e longa** — rara no Brasil subnacional. Atravessa três
  choques (Fundão 2015, recessão 2014–16, COVID 2020). **Pré-requisitos:** (i) localizar nas abas o
  vetor de **Pessoal Ocupado** (existe no padrão IBGE; confirmar a aba/linha) para multiplicador de
  emprego; (ii) **deflacionar** a preços constantes (a série é a valores correntes) — deflatores
  setoriais das Contas Nacionais; (iii) checar quebras de classificação CNAE/IBGE ao longo de 2010–2021.

### 2.2 ★ Intra-ES — ES-2015 (estado) + 10 microrregiões (antes "agenda futura")
- **Estado:** `ESPÍRITO SANTO (2015).xlsm` (~11 MB). **Microrregiões:** 10 arquivos `.xlsb`
  (`CAPARAÓ, CENTRAL SERRANA, CENTRAL SUL, CENTRO-OESTE, LITORAL SUL, METROPOLITANA, NORDESTE,
  NOROESTE, RIO DOCE, SUDOESTE SERRANA`).
- **Layout (de `_micro.md`):** sistema **inter-regional** de **10 microrregiões (R1–R10) × 35 setores
  (S1–S35)** — bloco $Z$ de **350×350** + demanda final + agregados de VA. **Já auditado como viável**
  ([`PLANO_ARTIGO.md`](PLANO_ARTIGO.md) A4): o padrão-plataforma **se confirma** — R1/Metropolitana
  **retém** (vazamento ~8,4%, ~70% da produção do ES) vs. periferia até ~31%.
- **Viabilidade: MÉDIA-ALTA**, com 3 ressalvas honestas já mapeadas: (a) **2015 ≠ 2008** e **35 ≠ 26**
  setores (concordância obrigatória); (b) **sem vetor de emprego** — só **Remunerações** (logo,
  "vazamento de emprego" intra-ES não é replicável; usar VA/remunerações); (c) 1 coluna com $\sum A>1$
  (corrigir balanço); (d) **dependência técnica:** os `.xlsb` exigem `pyxlsb` (não instalado no `.venv`)
  — instalar, ou converter para `.xlsx`/CSV uma vez.

### 2.3 WIOD 2000 (par temporal do 2014 já usado)
- `MIP-Mundo (2000).xlsx` (26 reg. × 23 setores, ISIC rev3) **vs.** `MIP-Mundo (2014).xlsx`
  (43 países × 56 setores, ISIC rev4, layout confirmado em `_wiod.md`).
- **Viabilidade: MÉDIA.** Permite *upstreamness* **2000 vs. 2014** (dinâmica de posição na cadeia), mas
  a ponte **23↔56 setores / rev3↔rev4** e **26 reg.↔43 países** é a parte cara. Resolve o resíduo
  R1-W3 (mistura de safras) ao tornar a comparação temporal **explícita** em vez de implícita.

### 2.4 Substrato de método (não-citáveis, mas operacionais)
`Método IIOAS.xlsx` (exemplo didático, documenta limites), `Tópico 10 — Regionalização (IIOAS).pdf`,
`MIP-26x26-BR-2008.xlsx` (interestadual 27-UF, já parseada em `02_interestadual.py`).

---

## 3. A tese panorâmica (o "olhar mais amplo" pedido)

> **Hipótese-mãe (invariância de escala + dinâmica).** A lógica-plataforma — *gerar encadeamento que
> escoa para um núcleo mais rico, com retorno (feedback) próximo de zero* — não é um traço idiossincrático
> do ES em 2008, mas uma **regularidade estrutural que se reproduz em diferentes escalas geográficas
> (fractal) e que se intensifica ou afrouxa no tempo conforme o ciclo de commodities**.

Essa formulação é forte por dois motivos:
1. **Responde ao ceticismo do parecer de frente.** O Devil's Advocate disse que "plataforma" poderia ser
   tautologia de porte/abertura. A resposta panorâmica não é defensiva — é **empírica**: se o padrão
   reaparece *dentro* do ES (microrregiões) e tem **assinatura distinta** num benchmark de 27 UFs, então
   há estrutura, não artefato. Invariância de escala é evidência, não retórica.
2. **Conecta com a fronteira.** "Posicionamento funcional em CGV e desigualdade *intra-país*" é tema
   ativo (ver §6) — levar isso para a escala **sub-estadual** (microrregiões) é território pouco explorado.

---

## 4. Cardápio priorizado de **novas questões** (RQ)

Cada RQ traz: pergunta · hipótese · método · dado · viabilidade · resíduo-de-parecer que resolve ·
contribuição · limites. Prioridade por **(novidade × viabilidade × resolução de crítica)**.

### 🥇 RQ-A — **A plataforma é fractal?** (intra-ES, escala fina) — *flagship recomendado*
- **Pergunta.** O padrão metrópole-retém / periferia-exporta-encadeamento se reproduz **dentro** do ES,
  entre as 10 microrregiões de planejamento?
- **Hipótese.** Sim: R1/Metropolitana funciona como "núcleo" capixaba (alto retido), e as microrregiões
  primário-exportadoras (Rio Doce/mineração; Caparaó/Noroeste/café) vazam encadeamento para R1 e para
  fora do ES, com feedback intra-ES baixo — **a mesma assimetria, uma escala abaixo**.
- **Método.** Reaproveita `io_core.py` **sem mudança conceitual**: Isard spillover/feedback (inversa
  particionada) com $L$ = microrregião-foco e $M$ = demais; mapa de vazamento por microrregião; ligações
  RH; **extração hipotética** da Metropolitana (quanto da produção do ES desaparece se R1 "sai"?).
- **Dado.** ES-2015 micro (350×350), já auditado viável.
- **Viabilidade.** MÉDIA-ALTA (instalar `pyxlsb`; corrigir 1 coluna; chave R1–R10/S1–S35; aceitar
  sem-emprego).
- **Resolve.** **R1/DA-1** (invariância de escala como evidência de estrutura) **e** R3 (substitui o
  cluster *ad hoc* por um recorte oficial — microrregiões de planejamento).
- **Contribuição.** *Nested platform economy* — plataforma dentro de plataforma. Original na literatura
  regional brasileira (a maioria para em UF). **É o segundo artigo natural.**
- **Limites.** 2015≠2008; fluxos sub-estaduais IIOAS são ainda **mais sintéticos** que os interestaduais;
  sem emprego (usar VA/remunerações).

### 🥈 RQ-B — **Plataforma ou só "estado pequeno-aberto"?** (benchmark 27-UF) — *fecha a crítica-núcleo*
- **Pergunta.** Quanto do feedback≈0 e do vazamento alto do ES é **explicado por porte e abertura**, e
  quanto é **resíduo "ES"**?
- **Hipótese.** O ES tem assinatura acima do previsto pelo porte/abertura na **concentração de destino**
  (Sudeste) e na **upstreamness da pauta**, embora o nível de feedback baixo seja genérico.
- **Método.** Para as **27 UFs** (matriz interestadual 2008, já parseada): computar
  vazamento, feedback, upstreamness e concentração-de-destino de cada estado; **modelo nulo** —
  regredir cada indicador em (PIB, grau de abertura) e ler o **resíduo do ES**; ancorar em Miller (1966)
  e na Tab. 2 de Haddad et al. (2017).
- **Dado.** Só dado **já existente** (interestadual 2008) → **viabilidade ALTA, custo baixo**.
- **Resolve.** **R1, R3, DA-1, DA-2** de uma vez.
- **Contribuição.** Transforma "ES é plataforma" em afirmação **identificada** (com benchmark). Pode
  entrar como **§ de revisão do artigo atual** *ou* virar um *paper* comparativo "Tipologia de estados-
  plataforma no Brasil".
- **Limites.** Cross-section único 2008; null model é associação, não causalidade.

### 🥉 RQ-C — **O Brasil está se re-primarizando? A plataforma no tempo** (Nível 68 SDA) — *o ativo mais rico*
- **Pergunta.** Entre 2010 e 2021, as fontes do crescimento do produto, do emprego e da posição na cadeia
  apontam **adensamento** ou **re-primarização** da estrutura brasileira — e onde Fundão/recessão/COVID
  entram nisso?
- **Hipótese.** Pós-2014 há perda de complexidade (queda de upstreamness média, ganho de peso de cadeias
  de base), coerente com a leitura-plataforma elevada do nível nacional.
- **Método.** **Structural Decomposition Analysis** (Δx = efeito-tecnologia ΔL·y + efeito-demanda L·Δy,
  decomposição polar média) sobre a série de 12 matrizes; **evolução** de multiplicadores, ligações RH e
  **upstreamness Antràs-Chor** ano a ano; **key-sector dynamics**; **extração hipotética** da mineração/
  siderurgia por ano (a "pegada" das cadeias de base ao longo dos choques).
- **Dado.** Nível 68 2010–2021 (12 anos × 68 setores).
- **Viabilidade.** ALTA estruturalmente; exige **deflação** (preços constantes) e localizar **emprego**.
- **Resolve.** **R4** (a janela 2008×Fundão deixa de ser ressalva e vira **objeto**) e dá a R2 uma
  **banda temporal** de robustez (variação ano-a-ano das quantidades estruturais).
- **Contribuição.** Um *paper* autônomo de **mudança estrutural do Brasil 2010–2021** com o método-
  plataforma — alinhado e atualizando a literatura de SDA brasileira (Brasil 1990–2015; ver §6).
- **Limites.** É **nacional** (não ES) — ancora o pano de fundo, mas o ES só tem 2008 e 2015, então a
  série temporal *do ES* não é possível; deflação e harmonização CNAE são trabalho real.

### RQ-D — **Subindo ou descendo a curva do sorriso?** (WIOD 2000 vs 2014)
- **Pergunta.** A posição do Brasil (e, via Brasil, do ES) em CGV se moveu **a montante** (commoditização)
  ou **a jusante** (serviços/valor) entre 2000 e 2014?
- **Método.** Upstreamness/downstreamness de Antràs-Chor nas duas safras WIOD; harmonização rev3↔rev4;
  leitura "hiperglobalização → *slowbalisation*".
- **Viabilidade.** MÉDIA (ponte 23↔56 setores). **Resolve** R1-W3.
- **Contribuição.** Dá **dinâmica** à camada CGV hoje estática (só 2014). Encaixa como seção do flagship
  ou nota de pesquisa curta.

### RQ-E — **A plataforma exporta carbono embutido** (extensão ambiental) — *agenda de maior alcance*
- **Pergunta.** Quanto **CO₂ embutido** o ES "exporta" junto com seu encadeamento (minério, siderurgia,
  celulose)?
- **Método.** IO ambientalmente estendida (vetor de intensidade de emissões setorial via SEEG/IBGE
  acoplado à inversa de Leontief); molde de Carvalho & Perobelli (2009) e Yamano & Guilhoto (2020).
- **Viabilidade.** MÉDIA — depende de **obter satélite de emissões** compatível (não está no acervo).
- **Contribuição.** Liga a tese-plataforma ao debate de **transição justa / royalties-carbono** — alto
  apelo de política (responde R3-W1 do parecer: "so what?" de política).
- **Limites.** Satélite externo; intensidade do ES ≠ média nacional (mesmo viés WIOD do §6).

### RQ-F — **Síntese multiescala** (o guarda-chuva)
- Não é um cálculo novo, é o **enquadramento** que costura A–E: *world → Brasil(t) → 27 UFs → 10
  microrregiões*, com a invariância de escala do par (vazamento, feedback) como fio condutor. É a forma
  natural de um **artigo "amplo"** ou de um **capítulo de dissertação** — e o que melhor materializa o
  "olhar panorâmico" pedido.

---

## 5. Sequenciamento recomendado (o que fazer, em que ordem)

```
Onda 1 (baixo custo, fecha o parecer)   → RQ-B (benchmark 27-UF) — dado já existe; vira § de revisão.
Onda 2 (segundo artigo, alta novidade)  → RQ-A (intra-ES fractal) — instalar pyxlsb, parsear micro.
Onda 3 (artigo autônomo, ativo rico)    → RQ-C (Nível 68 SDA 2010–2021) — deflação + emprego.
Transversais                            → RQ-D (WIOD 2000×2014) como seção; RQ-E (carbono) como agenda.
Guarda-chuva                            → RQ-F enquadra tudo (dissertação / paper amplo).
```

**Recomendação única, se for um só próximo passo:** começar por **RQ-A + RQ-B** combinados — *"A
economia-plataforma é fractal: ela se reproduz dentro do ES (10 microrregiões) e a posição do ES entre
as 27 UFs não é explicada só por porte e abertura."* Resolve as **duas** maiores críticas do parecer,
usa **uma** matriz nova (intra-ES) + **uma** já existente (interestadual), e é uma contribuição clara,
nova e viável. RQ-C (Nível 68) é o **artigo-irmão** mais ambicioso, separado, sobre o Brasil no tempo.

---

## 6. Ancoragem na literatura

### 6.1 Verificada no acervo local (já lida — ver `DEEP_RESEARCH_MATERIAL_IO.md`)
Haddad et al. (2017, RBERU) · Porsse, Peixoto & Palermo (2008, FEE) · Peixoto, Fochezatto & Porsse
(2013, Ensaios FEE) · Figueiredo, Barros & Guilhoto (2004) · Guilhoto et al. (2019, OECD STI) ·
Araújo Júnior (2018) · Tukker & Dietzenbacher (2013, ESR) · OECD (2019, TiVA Guide) · Yamano (2017) ·
Carvalho & Perobelli (2009, Econ. Aplicada) · Yamano & Guilhoto (2020). Miller (1966) e Miller & Blair
(2009) como substrato de método (feedback inter-regional pequeno; inversa particionada; Ghosh).

### 6.2 Localizada por busca externa — **a verificar no texto integral** antes de citar
*(estas vêm de busca na web nesta sessão; tratar como pistas a confirmar, não como citações prontas —
disciplina de integridade da skill.)*
- **SDA / mudança estrutural Brasil:** "Structural changes in the Brazilian economy 1990–2015"
  (*Economic Systems Research* 33(4), 2021); "Structural change and productive interdependence: an
  analysis for Brazil" (*Structural Change and Economic Dynamics*, 2024); "Drivers of employment change
  in Brazil… a structural decomposition analysis" (*Nova Economia*, SciELO). → fundamentam **RQ-C**.
- **Extração hipotética para regiões:** "An extension of the hypothetical extraction method to determine
  key regions: backward and forward dependencies" (*Journal of Economic Structures*, 2025). → método de
  **RQ-A/RQ-B**.
- **Posição em CGV no tempo / desigualdade intra-país:** Antràs & Chor (2021, NBER w28549, "Global Value
  Chains"); Antràs (2020, *Econometrica*, "On the Geography of GVCs"); Antràs et al. (2012, upstreamness);
  "GVCs and within-country inequality: the role of functional positioning" (*Structural Change and
  Economic Dynamics*, 2024). → **RQ-D/RQ-F**.
- **Sistemas inter-regionais BR (atualização de método):** "The Brazilian experience on estimating
  consistent interregional systems: SUIT and IIOAS compared" (*Estudos Econômicos/USP*, 2024). →
  atualiza o substrato IIOAS e a discussão de incerteza (R2).

> **Ação:** antes de qualquer redação (Stage 2), rodar a verificação de fonte da skill sobre §6.2
> (texto integral + DOI) e migrar o que se confirmar para a bibliografia citável.

---

## 7. Apêndice de método — a **ponte de concordância** (o gargalo de todo cruzamento)

Toda comparação entre escalas esbarra em **classificações setoriais distintas**. É o trabalho de
infraestrutura que precede qualquer RQ multiescala:

| Fonte | Setores | Classificação | Ano | Unidade |
|---|---|---|---|---|
| MIP-ES-BR / interestadual | **26** | agregação Guilhoto/IBGE | 2008 | R$ |
| Intra-ES microrregiões | **35** | (S1–S35) | 2015 | R$ |
| WIOD 2000 / 2014 | **23 / 56** | ISIC rev3 / rev4 | 2000/2014 | US$ |
| Nível 68 | **68** | CNAE/IBGE nível 68 | 2010–2021 | R$ |

→ Construir **uma** tabela-ponte mestre (26↔35↔56↔68) é pré-requisito e, por si só, uma **contribuição
de reprodutibilidade** (responde R1-W3). Sem ela, nenhum cruzamento de escala é defensável.

---

## 8. Limites honestos (para não superVender o panorama)

1. **O ES no tempo não existe** no acervo (só 2008 e 2015) — a série temporal é **nacional** (Nível 68).
   A dinâmica capixaba é **inferida** do pano de fundo nacional + dois pontos (2008, 2015), não observada
   ano a ano. Declarar.
2. **Fluxos sempre estimados** (IIOAS gravitacional); na escala micro, ainda mais sintéticos. O resíduo
   R2 (sweep de $F$) continua dependendo de insumos brutos do IIOAS **não disponíveis** nas matrizes
   finalizadas.
3. **Anos e classificações heterogêneos** (2000/2008/2014/2015/2010–2021; 23/26/35/56/68 setores) — a
   ponte do §7 é obrigatória e introduz erro de agregação.
4. **Sem emprego** na intra-ES (só remunerações) e **deflação pendente** no Nível 68.
5. **`.xlsb` exige `pyxlsb`** (dependência ausente) para as 10 microrregiões.
6. **Divulgação de IA:** levantamento, inspeção de matrizes e síntese assistidos por IA (Claude Code),
   com leitura direta do corpus local e das notas de layout; as fontes do §6.2 ainda **não** foram
   verificadas em texto integral.

---

## 9. Entregáveis da Stage 1 (este documento)

- **RQ Brief:** §3 (tese-mãe) + §4 (RQ-A…F priorizadas).
- **Metodologia:** §4 (por RQ) + §7 (ponte) — SDA, extração hipotética, upstreamness temporal,
  Isard multiescala, modelo nulo.
- **Bibliografia:** §6 (verificada + a-verificar, com tier).
- **Síntese:** §0, §1 (resíduos), §5 (sequenciamento), §8 (limites).

**Próximo passo do pipeline:** checkpoint do usuário (escolher a RQ/onda a desenvolver) → Stage 2 (WRITE)
sobre a RQ escolhida. Nada é escrito como artigo antes dessa confirmação.
