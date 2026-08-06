# Lista de Exercícios — Análise de Insumo-Produto (2026/1)

Resolução da lista do Prof. Celso Bissoli Sessa (entrega 24/07/2026) com o
arcabouço do repositório (`src/io_core.py` + convenções de `pesquisa/01`, `17`
e `25`). A resposta é uma pasta de trabalho Excel (`.xlsx`) com uma aba por
questão, **formulada** sobre as abas de dados: as inversas 68×68 (Leontief,
Ghosh e modelo fechado) entram como valores documentados; multiplicadores,
índices, choques, rankings e a SDA recalculam por fórmula.

## Dados (não versionados — ver `.gitignore`)

Coloque em `dados/` as matrizes nacionais da série Nível 68 (NEREUS/CECEG),
as mesmas de `C:\Users\DELL\Downloads\Material IO\Matrizes\Nível 68`:

- `MIP-BR 2010 (Nível 68).xlsm`
- `MIP-BR 2020 (Nível 68).xlsm`

## Uso

```bash
python lista/resolver_lista.py --m2010 "dados/MIP-BR 2010 (Nível 68).xlsm" \
                               --m2020 "dados/MIP-BR 2020 (Nível 68).xlsm"
# layout estranho? inspecione o arquivo:
python lista/resolver_lista.py --inspect "dados/MIP-BR 2020 (Nível 68).xlsm"
# validação de ponta a ponta com economia sintética (sem dados reais):
python lista/resolver_lista.py --selftest
# auditoria HARD contra as abas de cálculo do professor (dentro dos .xlsm):
python lista/auditoria.py
```

## Auditoria

`lista/auditoria.py` confronta o solver, célula a célula, com as abas em que o
**próprio professor** calcula a inversa de Leontief (`13`), a de Ghosh
(`Ghosh`), os índices de ligação (`14`), os geradores tipo I/II (`15`/`22`) e os
multiplicadores tipo I/II (`23`) — 26 confrontos, nos dois anos, todos com
desvio de precisão de máquina (< 1e-13). O relatório está em
[`AUDITORIA_LISTA.md`](AUDITORIA_LISTA.md), incluindo as **duas correções de
convenção** que a auditoria motivou (fechamento tipo II por valor adicionado;
ligação para frente pela soma de linha de Leontief).

Saída: `lista/Lista_Exercicios_Respostas.xlsx` (+ `.confere.json` com células
de auditoria fórmula×NumPy — use `verificar_recalculo()` após abrir/recalcular).

## Questões e métodos

| # | Método |
|---|---|
| Q1 | Multiplicadores de produção, emprego, renda e VA, tipos I e II (fechamento p/ famílias: linha de remunerações × coluna de consumo/massa salarial), com rankings de emprego e renda |
| Q2 | Δx = B·Δy: +R$ 10 bi em exportações da Agricultura × +R$ 10 bi na FBCF (estrutura observada); comparação de ΔX e ΔVAB |
| Q3 | +R$ 120 bi de consumo repartidos pela UPCF (cesta nacional+importada); importações diretas + induzidas (m = importação intermediária/x) e emprego |
| Q4 | Rasmussen-Hirschman 2010×2020 (para trás por Leontief, para frente por Ghosh), setores-chave e mudanças |
| Q5 | Campos de influência 2010 (Sonis-Hewings, ε=0,001) — forma fechada Sherman-Morrison, idêntica ao laço do material de apoio em R |
| Q6 | Extração hipotética total (linha+coluna+demanda final do setor zeradas); perda agregada e setores mais paralisados |
| Q7 | SDA bipolar média (Dietzenbacher-Los) com y(2010) atualizado pelo fator IPCA acumulado (variações anuais IBGE, editáveis na aba) |

O `--selftest` gera dois arquivos sintéticos no MESMO layout NEREUS, roda o
pipeline inteiro, checa identidades (tipo II ≥ tipo I; média das ligações = 1;
aditividade exata da SDA; Sherman-Morrison ≡ laço explícito) e produz um Excel
cujas fórmulas, após recálculo, são conferidas contra o NumPy.
