# Dados

Os arquivos de dados não são versionados (ver `.gitignore`). Coloque aqui:

- `mip_es_br_2008.csv` — matriz insumo-produto **inter-regional ES × restante do Brasil (2008)**,
  26 setores por região (52 ao todo), R$ milhões correntes, contábil e balanceada,
  com vetor de pessoal ocupado por setor.
- `wiod_2014/` — World Input-Output Database 2014 (43 países, 56 setores) para a camada de CGV.
- `outputs/` — resultados gerados por `src/io_core.py` (multiplicadores, decomposição retido/vazado,
  spillover/feedback, ligações de Rasmussen-Hirschman, upstreamness).

## Camada de atualização (pivô 2008→2015, ver `pesquisa/PLANO_ATUALIZACAO.md`)

Recebidas do Prof. Celso Bissoli Sessa (CECEG/UFES) em jun/2026, ambas planilhas `.xlsm`
(motor de macro completo TRU→MIP→multiplicadores, Leontief e Ghosh):

- `MIPBR_2019_Nivel_68.xlsm` — TRU/MIP **nacional**, 2019, **nível 68** (68 atividades × 128
  produtos), inclui vetor de emprego (aba `01`, "Fator Trabalho (Ocupações)"). Última
  atualização registrada na planilha: 2025-05-01. Só a região "Brasil" está computada;
  o seletor "Espírito Santo" existe na aba `BR` mas não foi gerado nesta exportação.
- `ESPIRITO_SANTO_2015.xlsm` — TRU/MIP do **Espírito Santo**, 2015, **nível 35** (códigos
  IJSN/TD60), **região única** (oferta, "Importação Regional" agregada, margens, impostos) —
  **não** tem fluxo bilateral ES↔resto do Brasil explícito; precisa de contraparte nacional
  para fechar o resíduo "resto do Brasil".
- **Falta:** MIP nacional **2015** (`Matriz_de_Insumo_Produto_2015_Nivel_67.xls`, ver abaixo) —
  necessária para construir resto-do-Brasil(2015) = nacional(2015) − ES(2015) e montar o
  par bi-regional ES×RB 2015 na mesma estrutura do `mip_es_br_2008.csv`.
- Referência metodológica (sem dados numéricos ainda): Haddad, Araújo, Rocha & Vale,
  "Matriz Interestadual de Insumo-Produto para o Brasil, 2019" (*RBERU*) — método IIOAS,
  128 produtos/68 setores/27 regiões (ES=R18). Fica como citação/Discussão até a matriz
  numérica estar disponível; **não é** camada ativa do painel por ora (equipe só tem dados
  até 2015).

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
