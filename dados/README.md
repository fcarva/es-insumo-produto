# Dados

Os arquivos de dados não são versionados (ver `.gitignore`). Coloque aqui:

- `mip_es_br_2008.csv` — matriz insumo-produto **inter-regional ES × restante do Brasil (2008)**,
  26 setores por região (52 ao todo), R$ milhões correntes, contábil e balanceada,
  com vetor de pessoal ocupado por setor.
- `wiod_2014/` — World Input-Output Database 2014 (43 países, 56 setores) para a camada de CGV.
- `outputs/` — resultados gerados por `src/io_core.py` (multiplicadores, decomposição retido/vazado,
  spillover/feedback, ligações de Rasmussen-Hirschman, upstreamness).

## Fontes
- Regionalização da matriz nacional: Guilhoto & Sesso Filho (2005).
- Estimação de fluxos inter-regionais (IIOAS): Haddad et al. (2017).
- WIOD: Timmer et al.

## Dados locais já disponíveis (na máquina)
Há matrizes **nacionais** em `Downloads/Documentos/Planilhas/`:
- `Matriz_de_Insumo_Produto_2015_Nivel_67.xls` (IBGE, 67 setores);
- `Matriz_Insumo-Produto_MIP_35x35.xlsx` (35 setores).

Servem para a versão **nacional** e para checagem, mas o modelo inter-regional
deste artigo exige a MIP **ES × restante do Brasil**: regionalize a nacional
(Guilhoto & Sesso Filho, 2005) ou use a estimativa IIOAS (Haddad et al., 2017).
