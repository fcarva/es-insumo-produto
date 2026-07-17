# Resposta aos pareceristas — "Estrutura Produtiva do Espírito Santo" (Rodada 1)

*Pipeline `academic-pipeline` · **Stage 4 REVISE**. Decisão da Stage 3: Major Revision (4 obrigatórios).
Cada item é rastreado com status explícito. Data: 2026-06-26.*

## Itens obrigatórios (Required)

### R1 — Benchmark interestadual (específico × genérico) — **FULLY ADDRESSED**
*Fonte: DA-1, R2-W2, EIC-W1.* Novo `22_benchmark_caracterizacao.py` computa as métricas-chave nas 27 UFs.
Adicionados ao manuscrito: novo parágrafo "O ES é típico ou extremo?" (§4) + **Tabela~\ref{tab:bench}** +
frase no resumo. **Resultado honesto:** a dualidade extração-enclave é **genérica em tipo** (o ES é
mediano em multiplicador de produção — 1,66, 14º — e em ligação para trás — 0,92, 14º), mas **extrema em
grau** (2º em base/commodity 36,4%; 24º em multiplicador de emprego; o emprego do setor líder é só 39% da
média estadual, 2º mais baixo do país). Conclusão incorporada: *o ES não é contraexemplo, é caso-limite.*
→ Responde diretamente à objeção mais forte do Devil's Advocate.

### R2 — Reposicionar o objeto temporal — **FULLY ADDRESSED**
*Fonte: R1-W1/W2, DA-2.* §5 reescrito com ressalva de objeto **antes** da análise: a série 2010–2021 é o
**pano de fundo nacional dos setores-base** (extração, siderurgia, refino, celulose), não a trajetória da
estrutura capixaba — "leitura de tendência dos setores, não do estado". O caveat de **preços correntes /
deflação** já consta de §Limites (e o recuo da siderurgia-2021 é tratado como efeito de preço). O título
mantém "(2008–2021)" agora coerente com a leitura declarada.

### R3 — Literatura do ES — **FULLY ADDRESSED**
*Fonte: R2-W1.* Adicionadas e contrastadas: **\citet{sessa2017ubu}** (impacto da Cia. Siderúrgica de Ubu,
Anchieta — pela MIP do ES) em §1; **\citet{ribeiro2024dinamica}** (regionalização da MIP-2015 nas 10
microrregiões, com multiplicadores de produção/emprego/renda) em §1 **e** em §6, onde se explicita que
este artigo usa a **mesma matriz de 2015** e que o quociente locacional **adiciona** a dimensão de
especialização ao retrato de setores-chave daqueles autores (convergência declarada). Ambas no
bibliography com volume/número/páginas verificados (DOIs conferidos).

### R4 — Política operacional — **FULLY ADDRESSED**
*Fonte: R3-W1/W2.* §7 reescrito com **três alavancas do próprio dado**: (i) adensar a jusante da base
mineral (minério→aço→produtos de metal, ancorado nas ligações puras e na metalurgia como setor-chave);
(ii) apostar na celulose (único setor-base com ligação para trás **crescente** na série, 1,41→1,51);
(iii) diversificar com **endereço territorial** (vocação de cada microrregião). Acrescentado parágrafo de
**royalties** como mecanismo central de captura de valor, ancorado no peso do petróleo (~¼ do PIB) e no
achado do benchmark (líder de baixo emprego).

## Itens sugeridos (Suggested) — Rodada 2 (todos atacados)
- **S1 (correlação PTL × VBP)** — **FULLY ADDRESSED**: computada (`17_*`) — Pearson **0,96**; ligação pura
  é largamente tamanho, seu acréscimo é a reordenação pela conexão (promove madeira/papel, cimento,
  eletricidade). Nota de rodapé no §4.
- **S2 (justificar fechamento tipo II)** — **FULLY ADDRESSED**: §Método agora explicita que o tipo II
  fecha para as famílias do ES e fornece um **limite inferior** do induzido (parte do consumo vaza ao RB).
- **S3 (moldura doença holandesa/maldição de recursos)** — **FULLY ADDRESSED + ancorado na literatura
  NACIONAL de IO** (deep research dedicado, `DEEP_RESEARCH_S3_DESINDUSTRIALIZACAO.md`): §Discussão ancora o
  perfil no debate brasileiro de desindustrialização/primarização examinado **pelas mesmas ferramentas
  (RH)** — \citet{morceiro2012} (erosão de encadeamentos) e \citet{nassif2015} (que **relativizam** a tese,
  citados honestamente como céticos) —, com o conceito em \citet{oreiro2010} e a raiz teórica em
  \citet{cordenneary1982}. 4 refs verificadas; manuscrito agora com **14 referências**.
- **S4 (C3 padrão não-óbvio)** — **FULLY ADDRESSED**: novo achado (`20_*`) — a **concentração** (HHI) da
  composição setorial **não acompanha o porte** (corr ≈ 0), mas a vocação: os **enclaves extrativos**
  (Litoral Sul/minério 0,18; Nordeste/petróleo 0,14) são os mais mono-estruturais, reproduzindo no
  território o padrão-enclave da escala setorial. Incorporado ao §6.

## Compilação (após S1–S4)
`paper/es_estrutura_produtiva.pdf` — **8 páginas, 3 figuras, 2 tabelas, 11 referências** (+ Corden-Neary);
compila sem erro nem citação indefinida. 4 obrigatórios + 4 sugeridos = **todos FULLY ADDRESSED**.

## Estado da compilação
`paper/es_estrutura_produtiva.pdf` — **7 páginas, 3 figuras, 2 tabelas, 10 referências**; compila sem
erro nem citação indefinida. Os 4 itens obrigatórios estão **FULLY ADDRESSED**; 0 concern silenciado.

---

# Rodada 3 — parecer da versão com apêndices (`REVIEW_FULL_MODE_V2.md`)

*Decisão da rodada: Minor Revision (banda superior) → Accept condicional a R1–R4. Data: 2026-07-10.*

## Itens obrigatórios

### R1 — Rastro reprodutível das Tabelas 1 e 4 — **PENDENTE (autor)**
Único item que depende da máquina local: rodar `pesquisa/25_decomposicao_fd.py` e
`pesquisa/24_micro_mult_chave.py` sobre o `Material IO`, conferir os asserts de
autoverificação (`[OK] todos os numeros publicados reproduzidos`) e commitar
`outputs/decomposicao_fd.csv` + `outputs/micro_multiplicadores.csv`. Status muda para
FULLY ADDRESSED com o commit dos 2 CSVs.

### R2 — Conciliação 8,4% × 9,1% (Metropolitana) — **FULLY ADDRESSED**
Nota adicionada à legenda da Tabela~`tab:micro`: a retenção da tabela é a **razão das somas
ponderadas** ($\sum w O^{intra}/\sum w O$ = 90,9%), distinta da **média ponderada das razões
setoriais** usada em §7/Apêndice B.2 (vazamento 8,4% ⇒ retenção 91,6%); as duas agregações
descrevem o mesmo fluxo. Mesma solução do precedente 24,9/22,8 (nota de rodapé).

### R3 — Resumo absorve o modelo nulo; "hiperaberta" moderada — **FULLY ADDRESSED**
Abstract reescrito: "hiperaberta" → "aberta" + frase nova: *"um modelo nulo sobre as 27 UFs
mostra que essa mecânica é a prevista para o porte do estado (o ES não é outlier em nenhuma
métrica de decomposição): o que a abertura transporta de específico é a composição"*.
"Hiperaberta" também moderada no §1.

### R4 — Sensibilidade da classificação base/commodity — **ADDRESSED (via declaração + reformulação)**
O ranking ex-Alimentos **não é recomputável** dos CSVs versionados (só agregados por UF);
adotado o caminho alternativo sancionado pelo parecer: nota de rodapé no §4 que (i) declara a
inclusão de Alimentos no rótulo (`10_cluster_setorial.py`) e seu efeito de elevar as parcelas,
(ii) apresenta o traço independente do rótulo — o ES é um dos 3 únicos estados (com PA e RJ)
cujo setor dominante é a extrativa mineral — e (iii) registra a reestimação ex-Alimentos como
checagem de replicação sobre `22_*`/`10_*`.

## Itens sugeridos (todos atacados)
- **S1 (escopo da injeção do HEM)** — **FULLY ADDRESSED**: Apêndice A.9 declara que a extração
  usa a demanda final intra-estadual; o −13,0% deve ser lido sob essa injeção.
- **S2 (Miyazawa não explorado)** — **FULLY ADDRESSED**: Apêndice A.3 agora reporta o número —
  o efeito do multiplicador externo capixaba, $(\Delta_{LL}-I)\Delta_L y^L$, é exatamente o
  feedback de R$ 164 mi (0,32%); a amplificação externa é praticamente nula.
- **S3 (Tiebout em uma oração)** — **FULLY ADDRESSED**: ponte explícita com o fechamento
  tipo II (mult. de emprego 27,9 → 40,4 por R$ 1 mi; média do `es_caracterizacao_2008.csv`,
  verificada) — o circuito induzido é o canal tieboutiano.
- **S4 (precedentes PA/SC/MA)** — **PARTIALLY ADDRESSED (honesto)**: Pará verificado por
  convergência dupla e citado — Sesso Filho & Guilhoto (2010), RBERU 4(2):81–104
  (`sessofilho2010para`, §1). SC (Revista Catarinense de Economia) e MA **não** atingiram
  confirmação sólida de autoria/ano (fontes primárias bloqueadas pela rede; metadados de busca
  ambíguos) e ficaram FORA, conforme a disciplina de citação da skill; registrados como agenda.
- **S5 (política amarrada aos números novos)** — **FULLY ADDRESSED**: alavanca (iii) cita o
  −13,0% (mono-dependência do núcleo); parágrafo de royalties amarrado ao modelo nulo (retorno
  via encadeamento abaixo até do previsto para o porte ⇒ captura fiscal como canal restante).

## Estado da compilação (rodada 3)
`paper/es_estrutura_produtiva.pdf` — **19 páginas, 6 figuras, 5 tabelas + 2 apêndices,
36 referências**; compila sem erro nem citação indefinida (3 passadas de pdflatex; checagem
estrutural: 36 cites ↔ 36 bibitems, 28 refs com label, ambientes balanceados).
3 obrigatórios FULLY + 1 pendente-do-autor (R1) + 5 sugeridos atacados (S4 parcial, honesto).

---

# Rodada 4 — resposta ao parecer full-mode da versão pós-editorial (`REVIEW_FULL_MODE_V3.md`)

*Stage 4 REVISE sobre a decisão da rodada 4: Minor Revision (banda superior) → Accept
condicional a F1. Data: 2026-07-17. Itens 1–6 do Revision Roadmap aplicados nesta rodada;
item 7 (= F1) permanece com o autor.*

## Itens do roadmap

- **1 (W-R1-1, legenda Fig. 4 × Apêndice B.3)** — **FULLY ADDRESSED**: B.3 ganhou a
  conciliação do transbordamento total que a legenda referencia — **R$ 18,2 bi**
  (bi-regional) × **R$ 18,1 bi** (interestadual, 27 UFs), mesma injeção; a remissão da
  legenda agora aponta para conteúdo existente.
- **2 (W-EIC-1, abstract EN)** — **FULLY ADDRESSED**: "manufacturing emerges as key
  sectors" → "manufacturing **concentrates** the key sectors" (concordância).
- **3 (W-R2-1, claim de raridade)** — **FULLY ADDRESSED**: §2 não afirma mais que o gênero
  "raramente emprega" os instrumentos; diz apenas o que eles fazem ("acrescido de dois
  instrumentos de aferição — o benchmark interestadual e o modelo nulo de porte — que
  separam...").
- **4 (W-R2-2, enquadramento de SC)** — **FULLY ADDRESSED**: Bittencourt et al. (2023)
  reenquadrado como "a leitura da indústria estadual sobre a MIP de 2018" — sem esticar o
  gênero. *Nota:* atualiza o S4 da rodada 1 — SC agora TEM precedente verificado (RBERU
  17(1), 90–112, conferido via RePEc/IDEAS); MA segue fora (metadados inacessíveis).
- **5 (W-R1-2, convenção de fonte nas legendas)** — **FULLY ADDRESSED**: as 6 figuras agora
  citam o **script gerador do dado** sobre o CSV (17, 18, 20, 02, 14/15, 08), a mesma
  convenção das tabelas; os scripts de figura (09/11/16/19/21) seguem documentados no
  repositório e no Makefile (`make figuras`).
- **6 (W-R3-1, condicionalidade temporal)** — **FULLY ADDRESSED**: abertura das alavancas
  agora declara "condicionais, como toda a leitura de política aqui, às safras das âncoras
  (§Limitações)".
- **7 (F1/DA-2)** — **PENDENTE DO AUTOR** (inalterado): `fechar_R1.bat` na máquina local
  fecha os CSVs das Tabelas 2 e 5 e habilita a checagem DA-1 (reestimação do ranking de base
  sem Alimentos, sobre `22_*`/`10_*`).

## Estado da compilação (rodada 4)
