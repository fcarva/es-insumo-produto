# Resultados — Caracterização da economia do ES (backbone C1 + C2)

*Pipeline `academic-pipeline` · **Stage 2 (análise)** do artigo "Estrutura Produtiva do Espírito Santo:
uma análise de insumo-produto". Scripts: `17_caracterizacao_es_2008.py` (C1), `18_trajetoria_n68.py`
(C2), `19_fig_caracterizacao.py` (figuras). Data: 2026-06-26.*

> **Retrato em uma frase.** O ES é uma **economia de base** — seus setores líderes (mineração, petróleo,
> siderurgia, celulose) são **grandes, a montante, exportadores e intensivos em capital**, com **duas
> faces**: a **extração** (petróleo, minério de ferro) é um **enclave de baixa ligação doméstica**,
> enquanto a **transformação** (siderurgia, celulose, refino) carrega os **encadeamentos**. Os líderes
> **geram pouco emprego e renda diretos**; emprego vem dos setores trabalho-intensivos, renda dos serviços.

---

## C1 — Retrato estrutural do ES (2008), bateria completa

`17_caracterizacao_es_2008.py` sobre a MIP-ES-BR 2008 (26 setores do ES, sistema bi-regional 52×52).

### Multiplicadores (média dos 26 setores)
| | tipo I | tipo II (famílias ES endógenas) |
|---|---|---|
| Produção | **1,76** | 2,45 |
| Emprego (empregos/R$ 1 mi dem. final) | **27,9** | 40,4 |
| Renda (das famílias do ES) | 0,29 | 0,36 |

- **Produção** mais alta: Alimentos 2,31 · Refino 2,11 · Material de transporte 2,10 · Químicos 2,10.
- **Emprego** mais alto (trabalho-intensivos): **Têxtil 67,9** · Pecuária 57,0 · Alojamento 50,2 ·
  Serviços privados 49,2 · Agricultura 46,7 — **nenhum** é setor de base.
- **Renda** mais alta: Educação · Administração pública · Saúde · Serviços privados — **serviços/público**.

### Setores-chave (Rasmussen-Hirschman, para-trás>1 **E** para-frente>1)
Refino · Químicos · Borracha/plástico · Cimento/min. não-metálicos · **Metalurgia** · Material elétrico ·
Material de transporte · Eletricidade/gás/água. → a **cadeia industrial de transformação**.

### Polos de crescimento (ligações puras GSH, ponderadas por tamanho)
| setor | PBL | PFL | **PTL** |
|---|---|---|---|
| **Mineração** | 3,54 | 5,17 | **4,43** |
| **Metalurgia** | 1,75 | 4,80 | **3,41** |
| Transporte | 1,82 | 2,92 | 2,42 |
| Comércio | 1,98 | 2,18 | 2,08 |
| Serviços privados | 0,90 | 2,85 | 1,96 |

→ Por **tamanho × conexão**, **Mineração e Metalurgia são os polos** da economia capixaba (forte
ligação para frente — fornecem insumos). Mas no **mapa de ligações** (Fig. `es_setores_chave.png`),
a **Mineração tem para-frente alta (~1,2) e para-trás baixa (~0,9)**: é **fornecedora a montante**, não
setor-chave pleno — a assinatura de **enclave extrativo** (compra pouco internamente).

### Grau de integração (coef. de variação das ligações dos setores do ES)
para-trás **0,162** · para-frente **0,280** — dispersão moderada; a economia é mais homogênea no lado da
demanda (para-trás) que no da oferta (para-frente).

**Tabela completa:** `outputs/es_caracterizacao_2008.csv` (todos os 26 setores × todos os indicadores).

---

## C2 — Panorama temporal (Nível 68, 2010–2021): a base capixaba na estrutura nacional

`18_trajetoria_n68.py` sobre a série nacional Nível 68 (NEREUS/CECEG), 68 setores × 12 anos. Acompanha
os 5 setores que definem o ES (mapeados: [5] petróleo/gás, [6] minério de ferro, [19] refino,
[27] siderurgia, [17] celulose/papel).

### Ligação para trás (Rasmussen-Hirschman), seleção de anos
| setor | 2010 | 2015 (Fundão) | 2020 (COVID) | 2021 |
|---|---|---|---|---|
| **Celulose/papel** | 1,41 | 1,40 | 1,48 | **1,51** ↑ |
| **Metalurgia/sider.** | 1,31 | 1,31 | 1,35 | 1,07 ↓ |
| Refino | 1,16 | 1,19 | 1,17 | 1,15 |
| Petróleo/gás | 0,83 | 0,87 | 0,93 | 0,80 |
| Minério de ferro | 0,80 | **0,94** | 0,86 | 0,82 |

### Leitura estrutural
- **Celulose/papel**: setor-chave **consistente e em alta** (multiplicador 2,85→3,05) — adensamento.
- **Siderurgia**: setor-chave na maior parte do período; **queda forte em 2021** (1,07) — checar
  quebra/reestruturação setorial.
- **Refino**: limítrofe de setor-chave, estável.
- **Petróleo/gás e minério de ferro**: **enclaves** — ligação para trás **abaixo de 1** quase sempre
  (compram poucos insumos domésticos); o minério **picа em 2015–16** (em torno de Fundão) e recua.

→ A **dualidade** do C1 (extração-enclave × transformação-chave) **se confirma no tempo** e na escala
nacional. (Figuras: `es_setores_chave.png`, `es_trajetoria_n68.png`.)

---

## C3 — Vocação econômica das microrregiões (2015)

`20_caracterizacao_micro.py` sobre o sistema inter-regional das 10 microrregiões (35 setores).
**Quociente locacional (LQ)** = quão especializada está a microrregião num setor vs. o estado (>1 =
especializado). (Figura: `es_micro_vocacao.png`.)

| Microrregião | % do ES | Setor dominante (VBP) | Vocação (LQ) |
|---|---|---|---|
| **R1 Metropolitana** | 62,3% | Petróleo e gás | diversificada + **Metalurgia** (LQ 1,6, CST/Tubarão) + serviços |
| **R7 Rio Doce** | 10,6% | Celulose e papel | **Celulose (LQ 8,2)** (Aracruz/Suzano) + metal-mecânica |
| **R5 Central Sul** | 6,2% | Minerais não-metálicos | **Mármore/granito (LQ 7,7)** (Cachoeiro) |
| **R9 Nordeste** | 4,9% | Petróleo e gás | **Agricultura (LQ 4,0)** + petróleo onshore |
| **R8 Centro-Oeste** | 4,4% | Comércio | **Têxtil (LQ 9,6)** (Colatina) + agro |
| **R4 Litoral Sul** | 4,1% | Minério de ferro | **Minério/pelotização (LQ 9,5)** (Anchieta/Samarco) |
| **R10 Noroeste** | 2,1% | Comércio | extr. não-metálicos + **Pecuária (LQ 5,8)** |
| **R6 Caparaó** | 1,9% | Comércio | **Agricultura/café (LQ 5,6)** |
| **R3 Sudoeste Serrana** | 1,9% | Comércio | **Agro (LQ 5,8)** + Alimentos |
| **R2 Central Serrana** | 1,5% | Pecuária | **Pecuária/avicultura (LQ 21,9)** (Santa Maria de Jetibá) |

**Leitura:** o ES é um **mosaico de vocações** — um núcleo metropolitano diversificado (petróleo, aço,
serviços) cercado por territórios especializados: celulose (Rio Doce), rochas ornamentais (Central Sul),
pelotização/minério (Litoral Sul), têxtil (Centro-Oeste) e um interior agropecuário (serranas/Caparaó/
Noroeste). **As vocações validam a chave R1–R10** (Lei 9.768/2011): cada microrregião acende exatamente
no setor que a geografia econômica conhecida prevê. (Setores de maior multiplicador de produção entre
microrregiões: Metalurgia 2,63 · Minério de ferro 2,14 · Minerais não-met. 1,98 · Alimentos 1,93 ·
Celulose 1,89; *Informação 2,78 — afetado pelo desbalanço S23, ver C-fractal §4*.)

## Síntese (o que o backbone entrega para o artigo)

A caracterização IO desenha o ES como **economia de base, dual e pouco geradora de trabalho direto nos
líderes**:
1. **Líderes a montante e de grande porte** (mineração, petróleo, siderurgia, celulose) — altos
   multiplicadores de produção e ligação para frente; são os **polos** (ligações puras).
2. **Mas baixos em emprego/renda direto** — quem multiplica emprego é têxtil/pecuária/serviços; renda,
   serviços/público. É o trade-off clássico da industrialização de base.
3. **Dualidade extração × transformação** — extração (petróleo, minério) é **enclave** (para-trás<1);
   transformação (siderurgia, celulose, refino) é **setor-chave** (para-trás>1), com **celulose** se
   fortalecendo na década.
4. **No tempo (2010–2021)**: adensamento da celulose, volatilidade da siderurgia, extração estável como
   enclave; Fundão (2015) visível no minério.

---

## Conciliação com a "economia-plataforma" (face complementar)

A pedido, o material do artigo "economia-plataforma fractal" (`es_plataforma_fractal.tex`, RQ-A+RQ-B)
foi **incorporado ao artigo de caracterização** como a **face da abertura** — reconciliando os dois:
*caracterização* = que tipo de economia é o ES (estrutura); *plataforma* = como essa estrutura se
relaciona com o resto do Brasil (vaza encadeamento ao núcleo, com retorno ≈ 0, fractalmente).

- **Nova §7 "Abertura, vazamento e a face plataforma"** (`es_estrutura_produtiva.tex`): vazamento (24,9%;
  emprego refino 61,6% etc.) · spillover/feedback (inj 51,5 bi → spillover 18,2 bi/35% → feedback 164
  mi/0,32%; Sudeste 65%, núcleo 52,5%) · **invariância de escala** (feedback~porte R² 0,59 UF / 0,91
  micro; metrópole retém 62%/vaza 8,4%; periferia → metrópole até 76%) + figura `fractal_duas_escalas.png`.
- **Método**: + decomposição de Isard (inversa particionada) `\citep{isard1951,millerblair2009}`.
- **Discussão**: reconciliação "fragilidade setorial + fragilidade **geográfica**" — captura de valor é de
  *composição* E de *posição*; a lógica repete-se da periferia capixaba para a Grande Vitória.
- **Abstract/título**: incluída a dimensão de **abertura**; **+2 refs** (Isard 1951; Miller 1966) → **16
  refs**, todas reais. Compila em **10 páginas**. (O `es_plataforma_fractal.tex` segue arquivado.)

## Limites honestos
1. **Panorama é 2010–2021** (série IO). A camada **2022–2025** exige indicadores **não-IO**
   (Contas Regionais/PIB, COMEX, ANP, RAIS) — quebra de método a declarar.
2. **C2 é nacional** (Nível 68): a trajetória dos setores-base é *proxy* da tendência capixaba via
   composição da pauta, não a estrutura do ES ano a ano (o ES só tem âncoras 2008 e 2015).
3. **Ligações puras ponderadas por tamanho** (GSH) favorecem setores grandes — por isso reportadas
   **junto** com RH (neutra a tamanho); as duas leituras são complementares.
4. **Tipo II** fecha o modelo para as famílias **do ES** (renda dos setores do ES; consumo das famílias
   do ES) — induzido capixaba, declarado.
5. **Queda da siderurgia em 2021** (1,35→1,07) — **investigada e resolvida** (`diag_sider.py`): **não**
   é quebra de classificação (códigos idênticos 2019=2020=2021; siderurgia = cód. 2491 sempre). É um
   **efeito de preço**: a queda concentra-se na cadeia metálica (ferro-gusa ΣA 0,905→0,622, não-ferrosos,
   produtos de metal), coerente com o **salto do preço do aço em 2021** sobre matrizes a **preços
   correntes** (x sobe mais que Z ⇒ a=Z/x cai por efeito nominal). Tratado no texto e nos limites do
   manuscrito; reforça a necessidade de **deflação** para leitura de tendência estrutural.
6. **Divulgação de IA:** análise e código assistidos por IA (Claude Code); todos os números reproduzem
   de `17`/`18` sobre o dado real.

## Próximo passo (pipeline)
Backbone C1+C2 **pronto e verificado**. Falta: (a) **C3** — mapa de setores-chave por microrregião
(2015); (b) extensão **2022–2025** com indicadores não-IO; (c) checagem da quebra siderurgia-2021;
(d) redação do artigo (Stage 2 WRITE) → Stage 2.5 integridade → Stage 3 review. Checkpoint do autor.
