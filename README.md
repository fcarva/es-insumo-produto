# Estrutura Produtiva do Espírito Santo: uma análise de insumo-produto

**Multiplicadores, setores-chave, demanda, vocação territorial e a face plataforma de uma
economia de base (2008–2021).**

Felipe Carvalho · PPGEco/UFES
Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · 2026/1
JEL: R15 · D57 · C67

---

## O artigo

`paper/es_estrutura_produtiva.tex` caracteriza a economia capixaba pela ótica insumo-produto,
na tradição brasileira de análise de economias estaduais ("Estrutura Produtiva de [Estado]"),
com ancoragem na teoria clássica do desenvolvimento regional (base de exportação — North/Tiebout;
polos de crescimento — Perroux) e apêndices metodológicos completos (Isard/Miyazawa, ligações
puras GHS, modelo nulo de porte, extração hipotética).

### As quatro frentes empíricas

| Frente | Matriz | Achados-âncora |
|---|---|---|
| **Retrato estrutural (2008)** | MIP inter-regional ES × restante do Brasil, 26 setores, com emprego | mult. produção 1,76 (tipo I) / 2,45 (tipo II); emprego concentrado nos trabalho-intensivos; extração-enclave vs transformação-chave; ligações puras: mineração 4,4, metalurgia 3,4; benchmark 27 UFs: ES 2º em base (36,4%), "genérico em tipo, extremo em grau" |
| **Quem puxa (2008)** | idem | demanda externa ao estado induz **61,7% da produção mas só 47,5% do emprego** |
| **Panorama temporal (2010–2021)** | série nacional de 68 setores (NEREUS) | celulose adensa (1,41→1,51); siderurgia recua em 2021 por efeito de preço; extração permanece enclave |
| **Vocação territorial (2015)** | sistema inter-regional das 10 microrregiões (35 setores) | mosaico de vocações (LQ); metrópole retém 90,9% do multiplicador vs 66,2% no Litoral Sul; extração hipotética da metrópole: −13% na periferia |
| **+ Abertura/plataforma** | ES×RB + interestadual 27 UFs + WIOD 2014 | vazamento 24,9%; spillover ao núcleo SP/RJ 52,5% com feedback 0,32%; modelo nulo: ES não é outlier em mecânica (z-scores +0,45/−0,05/+0,03); upstreamness da pauta 3,12 |

## Estrutura do repositório

```
es-insumo-produto/
├── paper/
│   ├── es_estrutura_produtiva.tex   # ARTIGO PRINCIPAL (v3, com apêndices A/B)
│   ├── es_insumo_produto.tex        # v1 arquivada (economia-plataforma)
│   ├── es_plataforma_fractal.tex    # v2 arquivada (invariância de escala)
│   └── paper_creation_process.tex   # registro do processo (Stage 6)
├── pesquisa/
│   ├── 01–28_*.py                   # pipeline reprodutível (scripts numerados)
│   ├── outputs/                     # CSVs e figuras gerados (versionados)
│   ├── SINTESE_CONSOLIDADA.md       # ÍNDICE-MESTRE do projeto (o que existe, o que falta)
│   └── *.md                         # deep researches, resultados, auditorias, pareceres
├── overleaf/                        # pacote autocontido p/ Overleaf (ABNT; espelho do artigo principal)
├── auditoria/                       # pasta de auditoria dos dados (gerada por pesquisa/28_*.py)
├── figuras/                         # artes da v1/slides (as figuras do artigo vivem em pesquisa/outputs/)
├── src/io_core.py                   # funções-núcleo (Isard/Miller-Blair, RH/Ghosh)
└── dados/                           # dados de terceiros NÃO versionados (ver dados/README.md)
```

> **Navegação:** comece por [`pesquisa/SINTESE_CONSOLIDADA.md`](pesquisa/SINTESE_CONSOLIDADA.md)
> — inventário completo do projeto, comparação entre as versões do artigo e plano de melhoria.

## Reprodução

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# coloque as matrizes em dados/ (ver dados/README.md), depois rode os scripts de pesquisa/:
python pesquisa/17_caracterizacao_es_2008.py   # retrato 2008
python pesquisa/18_trajetoria_n68.py           # panorama 2010–2021
python pesquisa/20_caracterizacao_micro.py     # microrregiões 2015
python pesquisa/22_benchmark_caracterizacao.py # benchmark 27 UFs
# compilar o artigo:
make paper
```

Todos os números de manchete foram regenerados do zero a partir das planilhas originais e
auditados (`pesquisa/AUDITORIA_HARD.md`); os CSVs de `pesquisa/outputs/` são versionados como
artefato reprodutível, já que os dados brutos de terceiros não podem ser redistribuídos.

## Dados

(a) MIP inter-regional **ES × restante do Brasil (2008)**, 26 setores por região, com vetores de
emprego e remunerações; (b) MIP **interestadual 27 UFs (2008)**; (c) sistema inter-regional das
**10 microrregiões de planejamento do ES (2015)**, 35 setores; (d) série nacional **Nível 68
(2010–2021)** do NEREUS/USP; (e) **WIOD 2014** para a camada de cadeias globais de valor.
Regionalização pelo método IIOAS (Haddad et al., 2017). Ver `dados/README.md`.

## Como citar

```
Carvalho, F. (2026). Estrutura Produtiva do Espírito Santo: uma análise de
insumo-produto. Working paper, PPGEco/UFES.
```

Ver também `CITATION.cff`.
