# Auditoria da Lista de Exercícios contra o material do professor

**Data:** 2026-07-24 · **Escopo:** `lista/Lista_Exercicios_Respostas.xlsx` (Q1–Q7)
**Gabarito:** as abas de cálculo do Prof. Celso Bissoli Sessa **dentro dos próprios
arquivos** `MIP-BR 2010/2020 (Nível 68).xlsm` (NEREUS/CECEG).

> Os caminhos `C:\Users\DELL\Downloads\Materiais Aula Insumo Produto` e
> `…\Material IO` são o disco local da máquina do autor (fora do ambiente).
> O material do professor, porém, **acompanha os arquivos MIP-BR**: além das
> TRUs/MIP, cada pasta traz as abas em que ele mesmo calcula a inversa de
> Leontief, a de Ghosh, os índices de ligação, os multiplicadores tipo I/II, o
> modelo fechado e os geradores de impacto. Auditar contra essas abas **é**
> auditar contra o material do professor — e com a vantagem de ser numérico,
> célula a célula.

Reprodução: `python lista/auditoria.py` (exit 0 = tudo dentro da tolerância 1e-9).

---

## 1. Resultado — 26/26 confrontos reproduzem o gabarito (desvio < 1e-13)

| # | Confronto | Aba do professor | 2010 | 2020 |
|---|---|---|---|---|
| 1 | Inversa de Leontief `B=(I−A)⁻¹` | `13` (Matriz (I-A)⁻¹) | 1,3e-15 | 1,6e-15 |
| 2 | Inversa de Ghosh `G=(I−Â)⁻¹` | `Ghosh` | 1,3e-15 | 1,6e-15 |
| 3 | Ligação p/ **trás** (normalizada) | `14` | 2,7e-15 | 2,7e-15 |
| 4 | Ligação p/ **frente** (normalizada) | `14` | 1,1e-14 | 9,8e-15 |
| 5 | Gerador de **emprego** tipo I | `15` | 7,1e-14 | 3,6e-14 |
| 6 | Gerador de **renda** tipo I | `15` | 4,4e-16 | 5,6e-16 |
| 7 | Gerador de **VAB** tipo I | `15` | 1,0e-15 | 1,1e-15 |
| 8 | Gerador de **importação** tipo I | `15` | 3,3e-16 | 2,8e-16 |
| 9 | Gerador de **emprego** tipo II | `22` | 8,5e-14 | 2,8e-14 |
| 10 | Gerador de **renda** tipo II | `22` | 1,3e-15 | 6,7e-16 |
| 11 | Gerador de **VAB** tipo II | `22` | 2,2e-15 | 1,8e-15 |
| 12 | Multiplicador de produção **tipo I** | `23` | 1,8e-15 | 2,2e-15 |
| 13 | Multiplicador de produção **tipo II** | `23` | 4,4e-15 | 4,4e-15 |

Além destes, a matriz **A** calculada por `Z·x̂⁻¹` já reproduzia a aba `13`
(bloco `Matriz A`) com desvio < 1e-15 (checado no pipeline principal), e a
identidade de balanço `x = Z·1 + y` fecha em todos os setores.

---

## 2. Duas correções de convenção encontradas e aplicadas

A auditoria **não passou de primeira**: dois cálculos usavam uma convenção
diferente da do professor. Ambos foram corrigidos no módulo `lista/` (o
pipeline de pesquisa em `src/`/`pesquisa/`, que faz escolhas próprias para o
artigo do ES, ficou intacto).

### 2.1 Fechamento do modelo tipo II — **renda = Valor Adicionado**, não só remunerações

O professor fecha o modelo para as famílias usando o **Valor Adicionado Bruto**
como renda (abas `20`/`22`/`23`): a linha extra é `VA/x` e a coluna extra é
`consumo das famílias / ΣVA`. A versão anterior do `lista/` fechava por
**remunerações** (renda do trabalho apenas), como no artigo do ES
(`pesquisa/17`) — legítimo, mas com números diferentes.

- **Antes** (fechamento por remunerações): multiplicador de produção tipo II
  médio = 3,63; setor 1 (Agricultura) = 2,27.
- **Depois** (fechamento por VA, = professor): média = **3,98**; setor 1 =
  **3,4017**, batendo a aba `23` com desvio 4e-15.

Correção em `Sistema.__init__` (`A2[n,:n]=v_va`, `A2[:n,n]=c_fam/ΣVA`).

### 2.2 Ligação para frente — **soma de linha de Leontief**, não Ghosh

O professor calcula a ligação para frente pela **soma de linha da inversa de
Leontief** (aba `14`, convenção clássica de Rasmussen-Hirschman usada na
tradição aplicada brasileira). A versão anterior usava a **inversa de Ghosh**
(escolha deliberada do `io_core.py`/`pesquisa/01` para o artigo, mais moderna).

Isso muda a contagem de **setores-chave**:

| | 2010 | 2020 |
|---|---|---|
| **Antes** (frente por Ghosh) | 16 | 18 |
| **Depois** (frente por Leontief, = professor) | **11** | **9** |

Correção em `Sistema.rasmussen` (`fl = B.sum(1)/n/B.mean()`). A inversa de
Ghosh permanece na pasta (abas `G_2010`/`G_2020`) como medida alternativa de
sensibilidade da oferta, com nota explícita na aba `Q4_RH`.

---

## 3. Impacto nas respostas

- **Q1 (multiplicadores):** os multiplicadores **tipo I** (produção, emprego,
  renda, VA) já batiam o professor exatamente (geradores das abas `15`/`23`).
  Os **tipo II** foram recalculados para o fechamento por VA e agora coincidem
  com as abas `22`/`23`.
- **Q4 (Rasmussen-Hirschman):** ligação para frente e o conjunto de
  setores-chave passam a seguir a aba `14`. Setores-chave 2020 (11→9):
  celulose/papel, refino, químicos orgânicos, defensivos, borracha/plástico,
  ferro-gusa/ferroligas, produtos de metal, transporte terrestre e atividades
  profissionais.
- **Q2, Q3, Q6, Q7:** usam o **modelo aberto** (inversa de Leontief `B`,
  geradores de impacto e coeficientes diretos), todos já verificados contra as
  abas `13`/`15`. Números **inalterados** pela auditoria.

---

## 4. O que a auditoria confirma sobre o resto da planilha

- Todas as **fórmulas vivas** do Excel recalculam sem erro (3.716 fórmulas,
  0 erros no LibreOffice) e as **19 células de auditoria** fórmula×NumPy
  batem (`*.confere.json`).
- O **selftest sintético** (`--selftest`) continua verde: identidades do modelo
  (tipo II ≥ tipo I; média das ligações = 1; aditividade exata da SDA;
  Sherman-Morrison ≡ laço explícito do campo de influência) mais o recálculo
  conferido contra o NumPy.

**Conclusão:** após as duas correções de convenção, a resolução reproduz o
material de cálculo do professor em todos os 26 pontos auditados, nos dois anos,
com desvio de precisão de máquina.
