# Roteiro de pendências — auditoria metodológica (aba `13_Metodo`)

Complemento a `pesquisa/AUDITORIA.md` (protocolo B1–B7) e à aba `13_Metodo` de
`auditoria/auditoria_dados_es.xlsx`. Registra o que ficou pendente da rodada de auditoria
metodológica das afirmações numéricas (achados J–S) e o que já foi fechado.

## Já verificado nesta rodada (não precisa rodar de novo)

`MIP-ES-BR (2008).xlsx` e `MIP-26x26-BR-2008.xlsx` foram enviadas e usadas para verificação
direta:

- **M** — reestimação do ranking de base/*commodity* sem Alimentos: ver resultado e data em
  `13_Metodo`, achado M (`auditoria/auditoria_dados_es.xlsx`) e no commit correspondente.
- **J** — `es_caracterizacao_2008.csv` regenerado com `mult_emp_I/II` na mesma unidade de
  `emp_dir_Rmi`/`emp_ind_Rmi`; `27_tab_multiplicadores.py` confirmado produzindo a mesma
  Tabela 1 sobre o CSV novo.
- **L** — decisão registrada em `13_Metodo` (Miyazawa computado de fato, ou mantida a
  declaração de identidade algébrica do Apêndice A.3 — ver qual das duas se aplicou).

Se você está lendo isto e ainda não viu o resultado de M/J/L em `13_Metodo`, é porque as
matrizes acima ainda não chegaram a esta sessão — trate a seção abaixo como válida também para
elas, não só para K.

## Pendente: só o achado K

**Por quê só este ficou de fora.** K depende da pasta `Nível 68` inteira (12 arquivos, um por
ano, 2010–2021) — pesada demais para envio, e o achado não afeta nenhum número publicado: é uma
checagem de robustez sobre uma guarda de código, não sobre um resultado do artigo.

### O que rodar

```bash
python3 pesquisa/18_trajetoria_n68.py
```

O script já está corrigido (troca do `pass` silencioso por `assert` no raio espectral, mais o
registro de violações em CSV). Path de entrada esperado pelo script (linha 18):
`C:/Users/DELL/Downloads/Material IO/Matrizes/Nível 68/Nível 68`.

### Critério de aprovação

| Resultado | Interpretação | Ação |
|---|---|---|
| `outputs/diag_hawkins_n68.csv` sai com **só o cabeçalho** (0 linhas) | Nenhum ano viola a soma de coluna de $A$ | Achado K fechado; nada a mudar no artigo |
| CSV com 1+ linhas | Há violação de $\Sigma A_{\cdot j}\ge 1$ em algum ano/coluna | Ver se o setor violador é um dos cinco setores de base que a Figura 2 usa (Petróleo/gás, Minério de ferro, Refino, Metalurgia/sider., Celulose/papel). Se sim, a trajetória daquele setor naquele ano precisa de nota; se não, é órfão do resto da matriz e não afeta o artigo |

Em qualquer caso, o `assert` do raio espectral já impede o script de silenciar uma
não-convergência real de $B=(I-A)^{-1}$ — se ele rodar até o fim, a inversa de Leontief é
finita e não negativa em todos os anos, que é a garantia que falta hoje.

### Depois de rodar

- Atualizar o achado K em `13_Metodo` (aba de `auditoria/auditoria_dados_es.xlsx`) e em
  `pesquisa/28_auditoria_xlsx.py` (lista `ACHADOS`), de "aplicado no código; regeneração
  pendente" para "verificado" com o resultado.
- Se o CSV vier com violações que atingem os cinco setores de base, sinalizar antes de tocar o
  `overleaf/main.tex` — pode exigir mais que uma nota de rodapé.
