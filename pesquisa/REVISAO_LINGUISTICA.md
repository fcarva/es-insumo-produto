# Revisão linguística e editorial — `es_estrutura_produtiva.tex` / `overleaf/main.tex`

Revisão da versão "base do autor (alterações de 21/07) + auditoria full mode", feita antes do
envio ao professor. Foco: português brasileiro (concordância, regência, sintaxe), consistência
terminológica e tipografia. Os itens do bloco A pedem **decisão do autor**; os dos blocos B, C e D
são correções objetivas, entregues como pares *localizar → substituir* aplicáveis direto no Overleaf.

Os números foram conferidos contra `pesquisa/outputs/` e batem (ver bloco E).

---

## A. Pontos que pedem decisão antes do envio

### A1. O abstract em inglês desapareceu

O cabeçalho da versão nova diz `abstract EN restaurado (NBR 6022)`, mas **não há bloco em inglês no
corpo do arquivo**. A versão em `overleaf/main.tex` (linhas 74–101) e em
`paper/es_estrutura_produtiva.tex` (linhas 65–92) tem o `\begin{otherlanguage}{english} … Keywords:
input-output; productive structure; … \end{otherlanguage}`.

Sintoma correlato: `\usepackage[english,brazilian]{babel}` carrega `english` sem que nada no
documento use o idioma.

**Ação:** recuperar o bloco do arquivo commitado e recolocá-lo depois das palavras-chave em
português. Se a intenção era de fato removê-lo, corrigir o comentário do cabeçalho.

### A2. O roteiro da introdução não cobre a §7

A introdução anuncia **três** perguntas, mapeadas em §4 (retrato), §5 (panorama) e §6 (território).
A §7 — abertura, *spillover*/*feedback*, face plataforma — fica de fora do roteiro, embora seja
citada no **título**, no **resumo** e na **conclusão**, e sustente boa parte da discussão.

**Ação:** acrescentar uma quarta pergunta ao parágrafo, algo como
`(iv) \emph{como} seu encadeamento se reparte entre o que fica no estado e o que escoa ao núcleo
industrial (\S\ref{sec:plataforma})`.

### A3. §2 mudou de nome, mas o corpo do texto ainda a chama de "quadro analítico"

O título passou a ser *"Revisão de literatura: a teoria regional na ótica de insumo-produto"*, e o
`\label` continua `sec:quadro`. Duas passagens ainda remetem ao nome antigo:

- §7: `configura, pois, a relação \emph{centro-periferia} do quadro analítico (\S\ref{sec:quadro})`
- Discussão: `as três lentes do quadro analítico (\S\ref{sec:quadro}) convergindo sobre o mesmo sistema`

**Ação:** trocar "do quadro analítico" por "da revisão" / "das três lentes da §2", ou reverter o
título. O `\label` pode ficar como está (não aparece impresso).

### A4. "Estados de crescimento dinâmico" nunca é definido

A expressão aparece três vezes (§4, Tabela 3, §7) e o único qualificador é o aposto
`--- sub-cobertos pelo mercado de capitais, excluído o núcleo SP/RJ ---`, que introduz um critério
externo, sem fonte e sem explicação. O leitor não tem como saber por que MG, SC, PR, RS, GO, MT e MS
formam esse grupo, e a comparação de razão de *feedback* (0,49%) depende dele.

**Ação:** uma frase de definição no primeiro uso, com a fonte do critério, ou substituir por um
rótulo autoexplicativo (p. ex. "os oito estados do Sul/Sudeste-MG e Centro-Oeste").

### A5. O parágrafo dos *royalties* extrapola o que o artigo mede

`as participações governamentais são o principal canal pelo qual a riqueza que transita pelo
território nele se fixa` — o artigo não apresenta nenhum dado fiscal, e a §8 declara que as
implicações de política ficam como "inferências condicionais". Além disso, o tema entra sem
preparação: é a única menção a *royalties* no texto inteiro.

**Ação:** ou hedge (`são um canal decisivo`, `tornam-se o canal de retorno mais visível`) ou
acrescentar a referência que sustenta a afirmação.

### A6. Fundão: "justamente" sugere causalidade não testada

`o minério de ferro registra seu pico de integração justamente em 2015--2016, em torno do rompimento
de Fundão, recuando em seguida`

"Justamente" + "em torno de" insinua nexo causal que a série não testa (e o pico pode ser efeito
nominal de preço, exatamente a ressalva feita duas linhas acima para o aço).

**Sugestão:** `o minério de ferro registra seu pico de integração em 2015--2016, coincidindo com o
rompimento da barragem de Fundão, e recua em seguida`.

### A7. Comentário meta-editorial na seção de limitações

`A auditoria desta versão separou os \emph{claims} diretamente derivados das matrizes, os
\emph{proxies} nacionais e as implicações de política, mantendo estas últimas como inferências
condicionais.`

Isso descreve o processo de revisão, não o artigo, e usa dois anglicismos evitáveis.

**Sugestão:** `Distinguem-se, ao longo do texto, os resultados diretamente derivados das matrizes,
as aproximações obtidas de séries nacionais e as implicações de política — estas últimas mantidas
como inferências condicionais.`

### A8. Dados da introdução sem fonte

`cerca de 2\% do produto nacional`, `cerca de um quarto do produto estadual` e o advérbio `hoje`
(sem ano de referência, num artigo cuja matriz é de 2008) pedem nota ou citação — Contas Regionais
do IBGE, com o ano.

### A9. Título: dois ajustes

`Multiplicadores, setores-chave, demanda, composição territorial da indústria e a face plataforma…`

- `demanda` sozinho não diz nada → `decomposição da demanda final`;
- `composição territorial **da indústria**` é mais estreito do que a §6, que cobre agropecuária,
  rochas, têxtil e serviços → basta `composição territorial`.

---

## B. Sintaxe, concordância e regência — correções objetivas

Pares *localizar → substituir*. Ordenados pela gravidade.

### B1. Inverte a tese de North (crítico)

```
comandado pela demanda externa ao invés da região \citep{north1955}
→
comandado pela demanda externa à região \citep{north1955}
```
`ao invés de` significa "ao contrário de"; a frase, como está, diz o oposto do que North propõe.

### B2. Dois-pontos quebra a frase

```
Para o Espírito Santo, contribuições como: \citet{sessa2017ubu} avaliam
→
Para o Espírito Santo, há contribuições pontuais: \citet{sessa2017ubu} avaliam
```

### B3. `Esse` → `Este` (referência ao próprio artigo)

```
Esse artigo busca responder a três perguntas
→
Este artigo busca responder a três perguntas
```

### B4. Concordância: sujeito singular, verbo atraído pela lista

```
e o ajuste biproporcional GRAS \citep{junius2003gras} ---, que entram aqui como critério
→
e o ajuste biproporcional GRAS \citep{junius2003gras} ---, que entra aqui como critério
```
O sujeito é `a regionalização`, não os métodos listados no aposto.

### B5. Gerúndio sem sujeito correspondente

```
Comparando o ES às 27 unidades da federação na matriz interestadual de 2008
(Tabela~\ref{tab:cluster}), a resposta é precisa
→
A comparação do ES com as 27 unidades da federação na matriz interestadual de 2008
(Tabela~\ref{tab:cluster}) dá uma resposta precisa
```

### B6. Sujeito plural, predicativo singular

```
os setores-chave (ambos os índices acima de 1) são a cadeia industrial de transformação: refino
→
os setores-chave (ambos os índices acima de 1) concentram-se na cadeia industrial de transformação: refino
```

### B7. Concordância do nome do setor

```
A \textbf{celulose e papel} é o setor-chave mais consistente
→
O setor de \textbf{celulose e papel} é o mais consistente entre os setores-chave
```
(a segunda metade também evita "o setor-chave mais consistente… é setor-chave")

### B8. Artigo faltando

```
chegam, pela via dos indicadores de inovação, a caracterização convergente
→
chegam, pela via dos indicadores de inovação, a uma caracterização convergente
```

### B9. Período sem verbo (§6)

```
Ao seu redor, territórios especializados, cada qual com um quociente locacional elevado em seu setor:
→
Ao seu redor dispõem-se territórios especializados, cada qual com um quociente locacional elevado em seu setor:
```

### B10. Período sem verbo (§7)

```
a periferia está para o ES como o ES está para o Sudeste --- dentro do estado, o mesmo desenho que
a tradição regional brasileira lê entre o ES e o núcleo industrial paulista.
→
a periferia está para o ES como o ES está para o Sudeste --- reproduz-se, dentro do estado, o mesmo
desenho que a tradição regional brasileira lê entre o ES e o núcleo industrial paulista.
```

### B11. `cuja jusante`

```
a ponta \emph{a montante} de cadeias cuja jusante permaneceu no núcleo ou no exterior
→
a ponta \emph{a montante} de cadeias cujos elos a jusante permaneceram no núcleo ou no exterior
```

### B12. Lista quebrada + sintagma vazio (introdução)

```
Falta, contudo, uma caracterização estrutural que reúna a bateria completa de indicadores, um
\emph{benchmark} interestadual que busque identificar as peculiaridades do Estado do Espírito Santo
a partir de um horizonte temporal.
→
Falta, contudo, uma caracterização estrutural que reúna a bateria completa de indicadores e a situe
num \emph{benchmark} interestadual, capaz de distinguir o que na economia capixaba é regularidade do
que lhe é peculiar.
```
`a partir de um horizonte temporal` não tem referente: o *benchmark* da §4 é um corte de 2008, não
uma série.

### B13. Correlação truncada

```
que busca separar o que é regularidade e especificidade dentro da estrutura produtiva
→
que busca separar o que é regularidade do que é especificidade na estrutura produtiva
```
Mesma frase, ainda no fim da §2:
```
Este artigo traz o formato ao Espírito Santo, o \emph{benchmark} interestadual, que busca
→
Este artigo traz esse formato ao Espírito Santo e lhe acrescenta um \emph{benchmark} interestadual, que busca
```

### B14. Ordem invertida ilegível (nota de rodapé das ligações puras)

```
promove acima do que o porte diria setores bem articulados mas não os maiores (madeira/papel,
cimento, eletricidade)
→
promove setores bem articulados, embora não os maiores (madeira/papel, cimento, eletricidade),
acima da posição que o porte lhes daria
```

### B15. Vírgula antes de `mas` adversativo

```
tem \emph{ligação para frente} elevada ($\approx1{,}2$) mas \emph{ligação para trás} baixa
→
tem \emph{ligação para frente} elevada ($\approx1{,}2$), mas \emph{ligação para trás} baixa
```

### B16. Regência: `subir de … a` → `de … para`

```
sua ligação para trás sobe de 1,41 (2010) a 1,51 (2021)
→
sua ligação para trás sobe de 1,41 (2010) para 1,51 (2021)
```

### B17. Comparativo ambíguo

```
Um padrão menos óbvio que o mapa de especialização emerge ao medir
→
Um padrão menos óbvio do que o do mapa de especialização emerge ao medir
```

### B18. Elipse verbal sem vírgula (resumo)

```
a extração opera como \emph{enclave}, a transformação como setor-chave
→
a extração opera como \emph{enclave}; a transformação, como setor-chave
```

### B19. `mais 16,1\%` lê-se como "outros 16,1%"

```
e o governo, com 13,1\%, mais 16,1\%.
→
e o governo, com 13,1\% da produção, responde por 16,1\% do emprego.
```

### B20. O número 27,9 é uma média, não "a geração de empregos"

```
a geração de empregos (27,9 por R\$ 1 milhão de demanda final, no tipo I) concentra-se
→
a geração de empregos (média de 27,9 por R\$ 1 milhão de demanda final, no tipo I) concentra-se
```

### B21. Gerúndio adjunto pesado (§5)

```
é coerente com o \emph{salto de preços do aço} em 2021 incidindo sobre matrizes a preços correntes
→
é coerente com o \emph{salto de preços do aço} em 2021, que incide sobre matrizes a preços correntes
```

### B22. Concordância de número dentro do mesmo período (§5)

```
sua ligação para trás permanece \emph{abaixo da unidade} em quase todos os anos --- compram poucos
insumos domésticos ---
→
suas ligações para trás permanecem \emph{abaixo da unidade} em quase todos os anos --- compram
poucos insumos domésticos ---
```
(o sujeito são dois setores: "a extração de petróleo e gás **e** a extração de minério de ferro")

### B23. Pleonasmo e repetição (introdução)

```
organizada em torno de setores industriais intensivos em \emph{commodities}, como por exemplo os
setores de minério de ferro e pelotização, siderurgia, petróleo e gás, celulose e rochas ornamentais
→
organizada em torno de setores de base intensivos em \emph{commodities}: minério de ferro e
pelotização, siderurgia, petróleo e gás, celulose e rochas ornamentais
```
"Industriais" também é impreciso — extração de petróleo e de minério não são indústria de
transformação, e é justamente esse o argumento do artigo.

### B24. Outros ajustes curtos

```
Em um período de quatro décadas, a economia capixaba trocou de motor
→ Em quatro décadas, a economia capixaba mudou de motor

organiza uma revisão de literatura a partir da ótica da teoria do desenvolvimento regional
→ organiza uma revisão de literatura sob a ótica da teoria do desenvolvimento regional

os resultados reportados são os que se rastreiam diretamente às três matrizes disponíveis
→ os resultados reportados são os que remontam diretamente às três matrizes disponíveis

o peso das atividades dos residentes, voltadas ao mercado interno
→ o peso das atividades residentes, voltadas ao mercado interno
  (é a forma usada no resto do texto)

Essa lógica-plataforma não é idiossincrática do ES perante o Brasil
→ Essa lógica-plataforma não é exclusiva da relação entre o ES e o Brasil

eleger a celulose, único setor-base cuja ligação para trás \emph{cresce}
→ eleger a celulose como prioridade, único setor de base cuja ligação para trás \emph{cresce}

O par retém-no-núcleo / vaza-da-periferia configura
→ O par retenção-no-núcleo / vazamento-na-periferia configura

mostrar, na escala estadual, uma economia já estruturalmente \emph{especializada em base}
→ mostrar, na escala estadual, uma economia já estruturalmente \emph{especializada em setores de base}

o ES é o segundo estado cujo setor líder menos emprega
→ o ES tem o segundo menor emprego relativo do setor líder no país
```

### B25. `exporta valor a montante` contradiz o próprio argumento

```
assim como exporta valor a montante, a economia de base capixaba exporta \emph{carbono incorporado}
```
A tese do artigo é que o valor é capturado **a jusante e fora** do estado; a frase, como está, diz
que o ES exporta valor. O paralelo pretendido é entre **exportar produto bruto** e **exportar
carbono**.

**Sugestão:** `assim como escoa ao núcleo o encadeamento que gera, a economia de base capixaba
exporta \emph{carbono incorporado}`.

### B26. `multiplicadores de Rasmussen-Hirschman` (Discussão)

Em todo o resto do texto são **índices** ou **ligações** — multiplicador é outra coisa no artigo.
```
documenta, por multiplicadores de Rasmussen-Hirschman e indicadores de conteúdo importado
→
documenta, por índices de ligação de Rasmussen--Hirschman e indicadores de conteúdo importado
```

---

## C. Consistência terminológica

| Item | Ocorrências divergentes | Sugestão |
|---|---|---|
| `pouco emprego e renda direta` (resumo) vs. `pouco emprego e renda diretos` (conclusão) | 2 | padronizar em `pouco emprego e pouca renda direta` |
| `escalas encaixadas` (§2) vs. `escalas aninhadas` (§7, título de parágrafo, e Discussão) | 3 | `escalas aninhadas` |
| `os reais polos de crescimento` (§3) vs. `os verdadeiros polos` (§4) | 2 | `os verdadeiros polos` |
| `Seção~\ref{}` (introdução) vs. `\S\ref{}` (todo o resto) | 1 vs. ~20 | `\S\ref{}` |
| `Rasmussen-Hirschman` (corpo) vs. `Rasmussen--Hirschman` (apêndice) | ~8 vs. 2 | en dash `--` em todos: são dois autores, não um nome composto (o mesmo vale para `Herfindahl--Hirschman` e `Hawkins--Simon`, já corretos) |
| itálico de estrangeirismos: `benchmark`, `spillover`, `feedback`, `enclave`, `commodities`, `versus` | ora `\emph{}`, ora redondo (`Um benchmark` no resumo, `o benchmark confirma` na Discussão, `estado versus restante` na introdução) | definir `\newcommand{\ing}[1]{\emph{#1}}` e aplicar, ou grafar tudo em redondo depois da primeira ocorrência |
| `neutra ao tamanho` / `neutros ao porte` | 3 | `insensível ao tamanho` / `neutro em relação ao porte` (a regência `neutro a` é calco) |
| `trabalho-intensivos`, `commodity-exportadores` | 2 | `intensivos em trabalho`, `exportadores de \emph{commodities}` (`primário-exportadora` pode ficar: é forma consagrada) |
| `sub-cobertos` | 1 | `subcobertos` (prefixo `sub` só leva hífen antes de `b`, `r` e `h`) |
| `não-censitária`, `não-metálicos`, `não-negativa`, `não-insumo-produto` | ~8 | pelo Acordo de 1990, `não` como prefixo não leva hífen: `não censitária`, `não metálicos`, `não negativa`. `inter-regional` está **correto** (prefixo terminado em `r` antes de `r`). Se preferir manter a convenção da área, ao menos uniformize |

---

## D. Tipografia e LaTeX

1. **Vírgula solta + espaço duplo** (§2, fim do parágrafo dos polos):
   `identificam os polos de crescimento de Perroux,  (\S\ref{sec:retrato})` →
   `identificam os polos de crescimento de Perroux (\S\ref{sec:retrato})`.
2. **Espaços duplos** em mais três pontos, todos onde parece ter havido uma citação removida:
   `São polos na acepção de Perroux  (\S\ref{sec:quadro})`; `a ressalva de Tiebout  reaparece`;
   `O canal de Tiebout ` (espaço em fim de linha); e `{\footnotesize North (1955);  Tiebout (1956)`
   na Tabela 1. Nenhum quebra a compilação, mas vale conferir se a intenção era manter
   `\citeyearpar{perroux1955}` / `\citeyearpar{tiebout1956}` ali.
3. **Texto colado ao `\label`**: `\label{sec:quadro} Três lentes da teoria…` — quebrar a linha depois
   do `\label` (é o padrão do resto do arquivo).
4. **Falta linha em branco** antes de `\paragraph{Multiplicadores e retenção territorial.}` na §6.
5. **Rótulos do apêndice nunca citados**: `ap:leontief`, `ap:isard`, `ap:rh`, `ap:puras`, `ap:fd`,
   `ap:lq`, `ap:robustez`. Ou referenciá-los nos parágrafos correspondentes da §3 (que é onde o
   leitor vai querer o ponteiro), ou removê-los.
6. **`GHS` nunca é expandido** — aparece só no título `\subsection{Ligações puras (GHS)}`. Abrir na
   primeira ocorrência: "Guilhoto, Sonis e Hewings".
7. **ABNT NBR 10520 — `&` nas citações**: os rótulos opcionais dos `\bibitem` usam `\&`
   (`\bibitem[Caçador \& Grassi(2009)]`, e mais 11 casos: Carvalho, Corden, Domingues, Flegg\&Webber,
   Guilhoto\&Sesso Filho, Ichihara, Junius, Miller\&Blair, Oreiro, Sesso Filho\&Guilhoto, Többen).
   Com `natbib` isso imprime "Caçador & Grassi (2009)" no corpo do texto; a norma pede **"e"**.
   Trocar `\&` por `e` **apenas dentro dos colchetes** — a lista de referências em si está correta.

---

## E. Conferência dos números (tudo confere)

| Afirmação no texto | Fonte | Valor apurado |
|---|---|---|
| 61,7% da produção puxada de fora | `decomposicao_fd.csv` | 32,69 + 29,06 = **61,75** ✔ |
| 47,5% do emprego | idem | 29,64 + 17,86 = **47,50** ✔ |
| Retenção da Metropolitana 90,9% | `micro_multiplicadores.csv` | **90,88** ✔ |
| Multiplicador pond. da Metropolitana 1,64 / 62,3% do VBP | idem | **1,6414** / **62,28** ✔ |
| Queda de 13,0% sem a metrópole | `extracao_hipotetica.csv` | **12,98** ✔ |
| *Spillover*: SP 37,8 + RJ 14,7 = 52,5% (núcleo); + MG 12,9 = 65,4% | §7 | aritmética fecha ✔ |
| Totais da Tabela 2 | `decomposicao_fd.csv` | 104.621,7 mi e 1.611.736 ocupações ✔ |

**Única ressalva de arredondamento:** o texto diz **61,7%** (correto a partir do dado bruto, 61,75),
mas quem somar as duas primeiras linhas da Tabela 2 obtém **32,7 + 29,1 = 61,8**. Vale uma nota de
rodapé na tabela (`as parcelas somam 61,75\% antes do arredondamento`) para o leitor não estranhar.
O mesmo vale para o total de emprego: 1.611,7 mil no corpo, 1.611,8 se somadas as parcelas da tabela.

---

## F. Passagens que valem reescrever por inteiro

### F1. Introdução, 3º parágrafo

> Falta, contudo, uma caracterização estrutural que reúna a bateria completa de indicadores e a situe
> num *benchmark* interestadual, capaz de distinguir o que na economia capixaba é regularidade do que
> lhe é peculiar. Este artigo busca responder a quatro perguntas: (i) *que tipo de economia* é o ES —
> quais são seus multiplicadores, setores-chave e polos de crescimento, e *quem puxa* sua produção e
> seu emprego (§4); (ii) *como* a posição estrutural de seus setores de base evoluiu (§5); (iii)
> *qual a composição industrial* de cada um de seus territórios (§6); e (iv) *como* seu encadeamento
> se reparte entre o que fica no estado e o que escoa ao núcleo industrial brasileiro (§7). A
> contribuição não é testar uma hipótese, mas oferecer um retrato insumo-produto da economia do
> Espírito Santo.

### F2. §2, abertura

> Três lentes da teoria do desenvolvimento regional organizam a leitura que este artigo faz da
> economia do Espírito Santo, e cada uma tem tradução direta na análise de insumo-produto (Tabela 1).
> A primeira é a *base de exportação*: o crescimento de uma economia regional é comandado pela
> demanda externa à região (North, 1955), ao que Tiebout (1956) contrapôs o peso das atividades
> residentes, voltadas ao mercado interno, na ocupação e no multiplicador local. Richardson (1985)
> formalizou a ponte com o método: o multiplicador de base econômica é o caso agregado do
> multiplicador insumo-produto, que o desagrega setor a setor. A lente se operacionaliza aqui na
> decomposição da produção e do emprego segundo os componentes da demanda final — que mede
> diretamente *quem puxa* a economia (§4) — e no fechamento de tipo II, que endogeneiza o circuito
> induzido pelos residentes.

(a versão atual encadeia três `pela/pelo` em duas linhas: "operacionalizada **pela** decomposição …
**pela** demanda final … e **pelo** fechamento")

### F3. §2, fecho

> Este artigo traz esse formato ao Espírito Santo e lhe acrescenta um *benchmark* interestadual, que
> busca separar o que é regularidade do que é especificidade na estrutura produtiva capixaba.

### F4. §6, último parágrafo (hoje com 5 linhas e três orações encaixadas)

> Esta leitura dialoga com Ribeiro et al. (2024), que regionalizaram a mesma matriz de 2015 e
> identificaram setores-chave por microrregião — alimentos, eletricidade, minerais não metálicos —
> pela geração de emprego e renda. O quociente locacional e a retenção acrescentam a esse retrato as
> dimensões da *especialização* e do *fluxo*: não apenas onde os multiplicadores são altos, mas em
> que cada território é especializado e quanto do encadeamento fica nele. Os dois resultados
> convergem para o mesmo desenho — um estado polarizado entre núcleo e periferias especializadas.

---

## G. Do lado positivo

Registro, porque também importa na revisão: a arquitetura do argumento está sólida e a §2 amarra
teoria e método de um jeito que a maioria dos artigos do gênero não faz. Vários fechos são
particularmente bons e não devem ser mexidos:

- "A transformação carrega os encadeamentos; a extração os dispensa."
- "a dualidade é genérica em tipo, mas extrema em grau"
- "não medem oportunidades de adensamento à espera de política: medem a mecânica que torna o
  adensamento localmente improvável"
- "O encadeamento a jusante da base capixaba existe; apenas se realiza em outro lugar."
- "O que é próprio do ES … não é a mecânica do vazamento, mas a composição de base que essa mecânica
  genérica transporta."

A nota da Tabela 5 conciliando as duas formas de agregar a retenção (90,9% vs. 91,6%), o
Apêndice B.2 com as três médias de vazamento e o Apêndice B.3 com as quatro convenções de *feedback*
são exatamente o tipo de coisa que desarma o parecerista antes que ele pergunte.
