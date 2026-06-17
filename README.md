# O Espírito Santo como economia-plataforma

**Encadeamentos, vazamento de multiplicadores e os efeitos *spillover*/*feedback* na cadeia regional de valor — MIP inter-regional ES × Brasil, 2008.**

Felipe Carvalho (`fcarva.eth`) · PPGEco/UFES
Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · 2026/1
JEL: R15 · D57 · C67

---

## Resumo

Este artigo caracteriza a economia do Espírito Santo como uma **economia-plataforma** — pequena, hiperaberta e estruturada em torno de setores cuja demanda final se realiza fora do estado. A partir de uma matriz insumo-produto inter-regional ES × restante do Brasil para 2008 (26 setores por região), aplica-se o modelo de Isard para decompor o multiplicador de produção de cada setor capixaba em parcela **retida** no estado e parcela **vazada** para o restante do Brasil, e para isolar a assimetria entre o efeito **spillover** (a produção que a demanda capixaba puxa para fora) e o efeito **feedback** (o que retorna). A leitura é complementada por uma camada de cadeias globais de valor (WIOD 2014) via índices de *upstreamness* (Antràs-Chor).

## Achados centrais

| Resultado | Valor |
|---|---|
| Injeção na demanda final do ES → **spillover** no restante do Brasil | R$ 60,6 bi → **R$ 22,4 bi** |
| **Feedback** de volta ao ES | **R$ 199 mi (0,26%)** |
| Vazamento médio do multiplicador de produção | **24,9%** (vs. 27,4% — Haddad et al., 2017) |
| Vazamento de emprego (setores pesados) | Refino 61,6% · Alimentos 56,5% · Madeira/papel 50,3% · Metalurgia 49,3% |
| *Upstreamness* da pauta capixaba | **3,19** (vs. média Brasil 1,97); mineração no percentil 98 global |

A interpretação: o mapa do vazamento é, ao mesmo tempo, um mapa de **fragilidade** estrutural e de **oportunidade** de adensamento de cadeia.

## Estrutura do repositório

```
es-insumo-produto/
├── paper/
│   └── es_insumo_produto.tex    # artigo em LaTeX (ver nota abaixo)
├── figuras/
│   ├── spillover_feedback.png   # diagrama de fluxo (assimetria spillover/feedback)
│   └── cgv_smile_curve.png      # curva do sorriso (posição em CGV)
├── src/
│   └── io_core.py               # implementação de referência (Isard, decomposição, RH)
├── dados/
│   └── README.md                # onde colocar a MIP inter-regional e os outputs
├── requirements.txt
├── CITATION.cff
├── Makefile
├── GIT.md
├── LICENSE
└── .gitignore
```

## Reprodução

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# coloque a matriz inter-regional em dados/ (ver dados/README.md), depois:
python src/io_core.py --mip dados/mip_es_br_2008.csv
# compilar o artigo:
make paper
```

## Dados

A espinha empírica é a **matriz insumo-produto inter-regional ES × restante do Brasil (2008)**, 26 setores por região (52 ao todo), R$ milhões correntes. A camada de CGV usa **WIOD 2014** (43 países, 56 setores). Os arquivos de dados **não** são versionados aqui — ver `dados/README.md` para os nomes esperados e as fontes.

## Como citar

```
Carvalho, F. (2026). O Espírito Santo como economia-plataforma:
encadeamentos, vazamento de multiplicadores e os efeitos spillover/feedback
na cadeia regional de valor (MIP inter-regional ES × Brasil, 2008).
Working paper, PPGEco/UFES.
```

Ver também `CITATION.cff`.

---

> **Nota.** Este repositório (`es-insumo-produto`) foi **inicializado a partir do esqueleto de [`es-economia-plataforma`](https://github.com/fcarva/es-economia-plataforma)** como ponto de partida: o pipeline de referência (`src/io_core.py`), a estrutura de pastas e o artigo-semente em `paper/` vêm de lá. **Ajuste o título, o texto e os números** para o conteúdo próprio deste trabalho e **adicione os dados** em `dados/` (ver `dados/README.md`). O `paper/es_insumo_produto.tex` ainda traz, como base, o texto do artigo *economia-plataforma* (resumo, método e bibliografia reaproveitáveis); a figura do *heatmap* da matriz B segue marcada como TODO.
