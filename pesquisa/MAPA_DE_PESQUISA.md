# Mapa de pesquisa — *ES como economia-plataforma* (fase exploratória)

Objetivo: levar ao máximo o que é factível no artigo a partir do material de
`Material IO/`, ancorado no estado da arte, entendendo os **limites**.
Apresentação: **sexta, 19/06/2026**.

---

## A. Inventário de dados (o que temos)

| Arquivo | Conteúdo | Dim. | Ano | Unid. | Uso |
|---|---|---|---|---|---|
| `Matrizes/MIP-ES-BR (2008).xlsx` | MIP **bi-regional** ES × Restante do Brasil, balanceada, com demanda final desagregada **e emprego** | 26 set. × 2 reg. | 2008 | R$ mi | **base do artigo** (validada) |
| `MIP-26x26-BR-2008.xlsx` | MIP **interestadual** (27 UFs) — "27R Matriz de Uso" | 27 UF × 26 set. (702) | 2008 | R$ mi | **rastrear destino do vazamento**; ES vs estados |
| `Microrregiões do ES (2015).xlsx` | Sistema inter-regional das **microrregiões de planejamento do ES** | ~12 reg. × 35 set. | 2015 | R$ mi | padrão-plataforma **dentro** do ES |
| `Matrizes/MIP-Mundo (2014).xlsx` | WIOD 2014 (ISIC rev4) | 43 países × 56 set. | 2014 | US$ mi | CGV / *upstreamness* |
| `Matrizes/MIP-Mundo (2000).xlsx` | MIP mundial (ISIC rev3) | 26 reg. × 23 set. | 2000 | US$ mi | CGV — comparação temporal |
| `Método IIOAS.xlsx` | Exemplo didático do método (regionalização) | 5 reg. × 3 set. | — | — | documentar **limites** |
| `Artigos/` + `Haddad et al (2017)` + `Tópico 10` | 15 papers + método | — | — | — | estado da arte |

Unidades não batem entre fontes (R$ vs US$; 2008/2014/2015; 26/35/56 setores):
qualquer cruzamento exige ponte/concordância explícita.

## B. Base validada (✓ feito — `01_es_br_base.py`)

Reproduzimos os números do artigo **direto da MIP-ES-BR real** (consistência
VBP × soma de linha = 0,00%):

| Resultado | Nosso (dado real) | Artigo |
|---|---|---|
| Vazamento médio do mult. de produção (ES) | **24,90%** | 24,9% ✓ |
| Mais retido / mais vazado | Serv. imobiliários **5,3%** / Alimentos **37,4%** | 5,3% / 37,4% ✓ |
| Vazamento de emprego — Refino · Alimentos · Madeira/papel · Metalurgia | **61,6 · 56,5 · 50,3 · 49,3%** | idem ✓ |
| Spillover / feedback (Miller-Blair limpa) | inj. 51,5 bi · spill. 18,2 bi · feedback **164 mi** | 60,6 / 22,4 / 199 (convenção a fixar) |

Tabela setorial completa: `outputs/es_setores_resultados.csv`.
**Pendência:** fixar a convenção exata de injeção/decomposição do spillover/feedback
do artigo original (a assimetria qualitativa se mantém em qualquer convenção).

## B2. Resultados interestaduais (✓ feito — `02_interestadual.py`)

Da matriz **27-UF**, e **consistente com a bi-regional** (mesma injeção f^ES=R$51,5 bi
e spillover=R$18,1 bi — a bi-regional é a colapsada ES-vs-resto da interestadual):

- **Para onde vaza o ES:** SP **37,8%**, RJ **14,7%**, MG **12,9%** → **Sudeste (ex-ES)
  absorve 65,4%** do spillover; Sul 14,8%, Nordeste 11,3%, C-Oeste 4,8%, Norte 3,7%.
  O ES retém+feedback **77,9%** da produção que sua demanda final puxa.
- **Abertura comparada:** ES é **8º/27** em vazamento (22,8%); mais abertos são estados
  de fronteira agro/mineral (MT 27,4%, AM 27,3%); menos aberto **SP (14,2%)**.
- **Leitura:** a tese-plataforma não é só *magnitude* de vazamento, e sim a
  **concentração do destino** (vizinhos ricos do Sudeste) + **feedback ≈ 0**.

Figura para slides: `outputs/es_spillover_destino.png`.
Tabelas: `outputs/es_spillover_destino.csv`, `outputs/estados_abertura.csv`.

## B3. O cluster de estados dinâmicos (ex-núcleo) e a leitura da Apex (✓ — `04_cluster.py`)

A **Apex Partners** (gestora; ≠ Apex-Brasil/agência) identifica 8 estados que crescem
acima da média mas são sub-cobertos pelo mercado de capitais: **SC, PR, ES, MG, RS, GO,
MT, MS** (excluem SP/RJ — o núcleo). Aqui esse conjunto é um **cluster de comparação**
(sem rótulo de marketing; o foco do artigo segue no **ES**). No interestadual 2008:

- Cluster = **33,9% do PIB** (2008) — coerente com a leitura da Apex (34% em 2002 → 39%
  em 2023); núcleo SP+RJ = 43,3%.
- **Destino do spillover do ES:** núcleo SP+RJ **52,5%** · resto do cluster 31,5% · resto
  do país 16%. Com **feedback ≈ 0**: o encadeamento do ES escoa para o núcleo e o valor
  não volta — **contraparte insumo-produto da tese de sub-cobertura de capital**.
- O cluster é sistematicamente **mais aberto** que o núcleo (SP é o 27º/menos aberto) e
  **retém 84,8%** do próprio encadeamento.
- Figura: `outputs/es_cluster.png`; tabelas: `outputs/cluster.csv`, `outputs/cluster_resumo.csv`.
- Fontes: Brazil Journal e NeoFeed (jun/2026). **Ressalva:** o cluster é um agrupamento de
  mercado (definir explicitamente); não é regionalização oficial.

## C. Estado da arte (literatura disponível, por eixo)

- **Método inter-regional brasileiro (IIOAS):** Haddad et al. (2017, ES); "Matriz
  Interestadual IIOAS" (BR); Guilhoto et al. (2019); inter-regional RS/BR 2003;
  Peixoto et al. (2013). → fundamenta a regionalização e suas hipóteses.
- **Cadeias globais de valor:** OECD Guide (2019); Yamano (2017); Yamano & Guilhoto
  (2020); Araújo Jr. (2018); Tukker & Dietzenbacher (2013); Horvat et al. (2020).
  → *upstreamness*/TiVA, posição em CGV.
- **Aplicações regionais/setoriais e extensões:** CO₂ (SP/BR), lácteo (MG),
  agricultura/ferrovia (MT). → modelos de impacto, pegada, SDA.

## D. Cardápio de análises factíveis (priorizado)

1. **[base ✓]** Vazamento, ligações RH, spillover/feedback bi-regional.
2. **[ALTO] Para onde vaza** — usar a interestadual 27-UF: decompor o spillover do ES
   por **destino** (Sudeste, macrorregiões, top estados). Responde o item nº 1 da
   agenda do artigo e é o resultado mais "novo" para a apresentação.
3. **[ALTO] ES vs outros estados** — perfil-plataforma comparado: vazamento/feedback
   de ES contra SP, MG, BA, RS… → mostra se o ES é *outlier* em abertura.
4. **[MÉDIO] CGV / upstreamness** — pauta do ES via Brasil (WIOD 2014); 2000 vs 2014
   para a dinâmica de posição na cadeia.
5. **[MÉDIO] Intra-ES** — microrregiões 2015: o padrão-plataforma se replica dentro
   do ES (metrópole retém, periferia exporta encadeamento)?
6. **[OPC.] Setores-chave** — campo de influência / extração hipotética
   (Dietzenbacher-Lahr); SDA se houver dois anos comparáveis.

## E. Limites (honestos, para a seção de método/agenda)

- Fluxos **interestaduais são estimados** (IIOAS: shares regionais + gravidade/
  distância + RAS), **não observados** — resultados de "destino do vazamento"
  carregam as hipóteses do modelo gravitacional.
- **Anos distintos**: bi-regional/interestadual 2008; microrregiões 2015; mundo
  2014/2000 → comparações temporais exigem ressalva.
- **ES não é país** na MIP-Mundo → posição em CGV é inferida via Brasil + peso da
  pauta capixaba (aproximação).
- **Agregação 26 setores** (bi-regional/interestadual) vs 35 (microrregiões) vs 56
  (mundo) → concordância setorial necessária para qualquer ponte.

## F. Próximos passos (até sexta)

- [x] (2) Parser da interestadual 27-UF + decomposição do spillover do ES por destino.
- [x] (3) Painel ES vs estados (ranking de abertura/vazamento).
- [x] Figura destino do spillover (estados + macrorregião).
- [x] **Cluster de estados dinâmicos** (leitura Apex): ES escoa 52,5% ao núcleo SP+RJ, feedback≈0 + figura.
- [ ] (4) *Upstreamness* da pauta do ES (WIOD 2014; 2000 vs 2014).
- [ ] (5) Intra-ES (microrregiões 2015): a plataforma se replica dentro do ES?
- [ ] Fixar a convenção de spillover/feedback do artigo original (60,6/22,4/199).
- [ ] Esclarecer referência a **"panteras/Apex"** (qual agregação regional?).
