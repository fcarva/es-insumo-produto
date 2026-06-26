# Dados

Os arquivos de dados não são versionados (ver `.gitignore`). Coloque aqui:

- `mip_es_br_2008.csv` — matriz insumo-produto **inter-regional ES × restante do Brasil (2008)**,
  26 setores por região (52 ao todo), R$ milhões correntes, contábil e balanceada,
  com vetor de pessoal ocupado por setor.
- `mip_es_br_2015.csv` — idem, **2015**, 35 setores por região (70 ao todo), construída por
  **regionalização CILQ** (Guilhoto & Sesso Filho, 2005) a partir de dado real de ES + residual
  nacional; ver `pesquisa/14_regionaliza_2015.py` e nota metodológica abaixo.
- `concordancia_setorial_68_35.csv` — tabela de–para nível 68 (nacional) → nível 35 (ES/IJSN),
  gerada por `pesquisa/14_regionaliza_2015.py`.
- `fd_es_br_2015.csv` — demanda final por setor/região (2015): componente local vs. importada
  da outra região (SLQ), exportação internacional, injeção `y` para o experimento
  spillover/feedback, e a checagem de auditoria (ver nota abaixo).
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
- `MIPBR_2015_Nivel_68.xlsm` — TRU/MIP **nacional**, 2015, **nível 68** (mesmo motor/estrutura
  do arquivo 2019 acima). Substitui a referência anterior a `Matriz_de_Insumo_Produto_2015_
  Nivel_67.xls` (IBGE): este arquivo é da mesma ferramenta/namespace de código do
  `ESPIRITO_SANTO_2015.xlsm`, o que tornou a concordância setorial direta (ver abaixo).
- Referência metodológica (sem dados numéricos ainda): Haddad, Araújo, Rocha & Vale,
  "Matriz Interestadual de Insumo-Produto para o Brasil, 2019" (*RBERU*) — método IIOAS,
  128 produtos/68 setores/27 regiões (ES=R18). Fica como citação/Discussão até a matriz
  numérica estar disponível; **não é** camada ativa do painel por ora (equipe só tem dados
  até 2015).

### Nota metodológica — construção do `mip_es_br_2015.csv` (CILQ)

Nem a planilha nacional nem a do ES separam, dentro do "Consumo Intermediário de Origem
Doméstica", o que é suprido de dentro da própria região do que vem da outra região do Brasil
— por isso o resíduo nacional−ES sozinho não fecha o par bi-regional (dá só a estrutura
tecnológica do resto do Brasil, sem os blocos cruzados `Z_LM`/`Z_ML` que o modelo de Isard
exige). `pesquisa/14_regionaliza_2015.py` aplica então **CILQ** (cross-industry location
quotient; Guilhoto & Sesso Filho, 2005) sobre os dois "totais domésticos" (Z real do ES e
Z residual do resto do Brasil) para estimar a fração local vs. importada de cada coeficiente,
ancorado no dado real do ES (não é uma regionalização proporcional pura — só o *split* de
origem é estimado). Passos: (1) agrega a malha nacional de 68 para 35 setores via
`concordancia_setorial_68_35.csv` (mapeamento por nome de atividade — alguns agrupamentos são
julgamento documentado no próprio script, ex.: fumo→"Alimentos e bebidas",
farmoquímicos→"Químicos"); (2) resto do Brasil = nacional(35) − ES, por resíduo (ruído de
arredondamento entre as duas planilhas é zerado e reportado, não escondido); (3) CILQ
decompõe `Z_ES`→(`Z_LL`,`Z_ML`) e `Z_RB`→(`Z_MM`,`Z_LM`); SLQ (sem termo cruzado) faz o mesmo
para a demanda final doméstica.

**Auditoria (rodada jun/2026):** matriz 70×70 não-negativa, soma de `A` por coluna ∈ [0, 0,97]
(< 1, condição de Hawkins-Simon ok), `B=(I-A)⁻¹ ≥ 0`. Validação externa: o `Z_LM` estimado
(ES vendendo para uso intermediário no resto do Brasil) tem correlação **0,97** com a
"Exportação Regional" observada na planilha do ES (que mistura uso intermediário e demanda
final de RB — por isso não é esperado bater exatamente, só ser consistente). Vazamento médio
do multiplicador de produção (colunas ES, ponderado pela produção): **12,8%** — não comparável
diretamente aos 24,9% do corte 2008 (classificação mais fina, ano diferente, e fluxo
bilateral estimado por CILQ em vez de observado por survey); ver `pesquisa/PLANO_ATUALIZACAO.md`
para a discussão de limites.

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
