# Plano de melhorias — rodada editorial (pós-Accept condicional)

*Plano para a próxima rodada de trabalho sobre `paper/es_estrutura_produtiva.tex`, montado a
partir de auditoria do repositório em 2026-07-16 (artigo lido na íntegra; 6 figuras inspecionadas
uma a uma; pareceres e síntese conferidos). Escopo = os cinco pedidos do autor: **(A)** resumo
mais curto, **(B)** melhorar todos os gráficos, **(C)** corrigir e acrescentar o que passou,
**(D)** organizar a diagramação, **(E)** organizar as ideias de economia regional com base na
literatura de insumo-produto.*

**Ponto de partida:** artigo v3 com ~20 págs., 36 refs., Apêndices A/B aprovados pelo
theorist-toolbox (resta só F1, que depende da máquina do autor); pacote RBERU pronto
(`SUBMISSAO_RBERU.md`). Esta rodada é **editorial** — não mexe em números auditados nem em
convenções fechadas.

---

## 0. Visão geral

| Eixo | O que faz | Esforço | Depende de |
|---|---|---|---|
| **A** Resumo | 422 → ≤200 palavras (esqueleto de 7 frases; minuta abaixo) | 1–2 h | — |
| **B** Figuras | padrão transversal + correções figura a figura + regeneração | ½–1 dia | CSVs versionados (já no repo) |
| **C** Correções/acréscimos | erro "quatro/cinco", Sankey ≠ texto, **abstract EN ausente**, refs que ficaram de fora | ½ dia | verificação de refs |
| **D** Diagramação | **babel ausente**, microtype, captions, floats, versão anonimizada | 2–3 h | recompilação |
| **E** Teoria regional | nova seção "Quadro analítico" organizando as lentes ↔ instrumentos I-P | ½ dia | — |

**Sequência sugerida:** D.1–D.3 + C.1 (mecânicos, 30 min) → B (figuras) → A (resumo) →
E (quadro analítico) → C.4–C.6 + abstract EN → recompilar + varredura final (C.3, D.8).
Total estimado: **~2 dias de trabalho**.

---

## Eixo A — Resumo mais curto

**Diagnóstico.** O resumo atual tem **422 palavras** num único parágrafo e carrega 15+ números
(multiplicadores médios, LQs, z-scores, trajetórias setoriais). Periódicos brasileiros do tier da
RBERU praticam 100–250 palavras; além do limite, o resumo hoje *conta o artigo inteiro* em vez de
vender os 4 achados.

**Regra de corte.** O resumo guarda apenas os números-manchete, um por achado:

1. quem puxa: **61,7% da produção / 47,5% do emprego**;
2. benchmark: **2º estado mais intensivo em base** ("genérico em tipo, extremo em grau");
3. território: retenção **90,9% (metrópole) vs 66,2% (Litoral Sul)**;
4. abertura: escoa ao núcleo SP–RJ com **feedback ~0** — e a mecânica é a prevista pelo porte
   (especificidade = composição).

Todo o resto (1,76/2,45; têxtil 67,9; celulose 1,41→1,51; LQ 8,2/9,5/21,9; 24,9%/52,5%/0,32%)
já está no corpo — sai do resumo sem perda.

**Minuta (~190 palavras, a validar pelo autor):**

> Este artigo caracteriza a estrutura produtiva do Espírito Santo pela ótica insumo-produto, na
> tradição brasileira de análise de economias estaduais, combinando a matriz inter-regional
> ES×restante do Brasil de 2008 (26 setores, com emprego), a série nacional de 68 setores
> (2010–2021) e o sistema inter-regional das dez microrregiões de planejamento (2015). O retrato
> é o de uma economia de base dual: os setores líderes — mineração, petróleo, siderurgia e
> celulose — concentram encadeamento (as maiores ligações puras), mas geram pouco emprego e
> renda diretos; a extração opera como enclave, a transformação como setor-chave. A decomposição
> pela demanda final quantifica o descolamento: a demanda externa ao estado induz 61,7% da
> produção, mas apenas 47,5% do emprego. Um benchmark com as 27 unidades da federação mostra que
> a dualidade é genérica em tipo, mas extrema em grau — o ES é o segundo estado mais intensivo
> em setores de base. No território, um núcleo metropolitano diversificado que retém 90,9% de
> seu multiplicador contrasta com periferias especializadas que vazam; na abertura, o
> encadeamento escoa ao núcleo São Paulo–Rio com feedback quase nulo — mecânica prevista pelo
> porte do estado: a especificidade capixaba é composicional.

**Aceite:** ≤200 palavras (contagem automatizada); nenhum número que apareça **só** no resumo;
palavras-chave e JEL mantidos.

---

## Eixo B — Figuras (todas)

**Viabilidade verificada:** os 7 scripts de figura leem **apenas CSVs versionados** de
`outputs/` — as figuras são 100% regeneráveis neste ambiente (`pip install matplotlib pandas`),
sem os dados brutos de `dados/`.

### B.0 Padrão transversal (aplicar às seis)

| # | Regra | Motivo |
|---|---|---|
| 1 | **Remover título/subtítulo/fonte embutidos** no PNG; a legenda LaTeX assume tudo | hoje cada figura tem duas legendas (a embutida estilo-Nexo + a caption); periódico pede caption única |
| 2 | **Vírgula decimal** em todos os eixos e anotações | figuras usam ponto (0.7, 8.2) e o texto vírgula — inconsistente em PT-BR |
| 3 | **Acentos corretos** nos rótulos | "Mineracao", "Comercio", "Min nao-metal" na fig. de upstreamness |
| 4 | **Exportar PDF vetorial** (além do PNG) e usar o PDF no `.tex` | nitidez em impressão; PNG 160 dpi é limítrofe |
| 5 | Fundo **branco/transparente uniforme** | o Sankey está em creme (`PAPER`), as demais em transparente |
| 6 | Corrigir `OUT = "C:/Users/DELL/..."` **hardcoded** nos 7 scripts (pathlib relativo, como já feito nos scripts 24/25) | hoje nenhum script de figura roda fora da máquina do autor |
| 7 | Tamanho de fonte e margens consistentes entre figuras; rótulos legíveis a 100% do tamanho final (`\linewidth` de texto 11pt) | as seis têm tamanhos e densidades díspares |

### B.1–B.6 Correções específicas

| Figura (arquivo) | Problemas verificados | Correção |
|---|---|---|
| **1. Setores-chave** (`fig_setores_chave.png`, script `19`) | rodapé "Fonte:" **sobreposto** ao rótulo do eixo x; dos 9 setores-chave, só 3 rotulados; "Refino de petról" truncado; "Alimentos" cortado na borda direita | rotular **todos** os pontos vermelhos (anti-colisão via offsets ou `adjustText`); margens maiores; rotular os 4 quadrantes (chave / dependente / forte-a-frente / independente) |
| **2. Trajetória N68** (`fig_trajetoria_n68.png`, script `19`) | rótulos "Minério de ferro" e "Petróleo/gás" **colidem** no fim das linhas; xlabel "ano" redundante | separar os rótulos finais verticalmente; remover xlabel; manter Fundão/COVID como marcas discretas |
| **3. Vocação micro** (`fig_micro_vocacao.png`, script `21`) | gridlines brancas **cortam as anotações** dentro das células (9,6 / 21,9 fatiados); cap do LQ em 6 e o critério "10 de 35 setores exibidos" só no rodapé embutido | remover as linhas internas de célula (ou usá-las como borda fina); anotações com vírgula; **mover cap e critério de seleção para a caption LaTeX** |
| **4. Sankey** (`es_sankey.png`, script `11`) | **números divergem do texto**: figura diz spillover "R$ 18,1 bi" (texto: 18,2) e cabeçalho "R$ 81,9 bi / retido 78% / vaza 22%" (experimento antigo; convenção fechada: injeção 51,5 / spillover 18,2 / feedback 0,32%); fundo creme; caption diz "constam do subtítulo" (dependente do título embutido que será removido) | regenerar na convenção Miller-Blair V3 registrada em `MAPA_DE_PESQUISA.md` B; caption **autossuficiente** com injeção/spillover/feedback; fundo padrão |
| **5. Fractal duas escalas** (`fractal_duas_escalas.png`, script `16`) | unidades dos eixos não declaradas (log de produção em R$ mi? share em %?); rodapé colado no eixo; "MESMA" em caixa alta (tom jornalístico) | declarar unidades nos xlabels; respiro no rodapé; opcional: anotar o z-score do ES no painel nacional (amarra com a Tabela de z-scores) |
| **6. Upstreamness** (`es_upstreamness.png`, script `09`) | rótulos **sem acento** (Mineracao, Comercio, Agric/silvic, Min nao-metal); anotações "U=… · % da pauta" atravessadas pelas linhas de referência Brasil/Mundo | acentuar; reposicionar anotações (fora das barras ou acima das linhas); declarar na caption a ordenação (por peso na pauta) |

### B.7 Housekeeping de figuras

- `figuras/` (que o README chama de "figuras finais") está **obsoleto**: `es_setores_chave.png`,
  `es_micro_vocacao.png`, `es_trajetoria_n68.png` são cópias antigas das de `outputs/`;
  `cgv_smile_curve.png` e `spillover_feedback.png` são da v1 (geradas por `src/make_figuras.py`,
  que é do deck da v1). Decidir **uma** fonte de verdade (sugestão: o `.tex` consome só
  `outputs/`; `figuras/` passa a guardar apenas as artes da v1/slides, com nota no README).
- Alvo `make figuras` aponta para `src/make_figuras.py` (v1) — retarget para os scripts
  `03/05/09/11/16/19/21` ou documentar.
- O `.tex` hoje puxa 5 figuras de `outputs/` e 1 (`fractal_duas_escalas.png`) de `figuras/` —
  unificar após a regeneração (o script `16` grava como `fig_fractal.png` em outputs).

**Aceite:** seis figuras regeneradas sem título embutido, vírgula decimal, zero colisões de
texto; números da fig. 4 idênticos aos do texto; `.tex` compilando com os novos arquivos;
scripts rodando de qualquer máquina (sem caminho absoluto).

---

## Eixo C — Corrigir e acrescentar o que passou

### C.1 Erros objetivos no texto (corrigir já)

1. §Limitações abre com "**Quatro** limites são declarados" e lista **(i)–(v)** — são cinco.
2. Caption da fig. 4 (Sankey) remete ao "subtítulo" da figura — ver B.4.
3. Após regenerar figuras: varredura número↔figura↔texto↔CSV (os asserts dos scripts já
   cobrem texto↔CSV; falta o elo figura).

### C.2 **Abstract em inglês ausente** (bloqueador de submissão)

O manuscrito tem só o Resumo em PT. A RBERU (como praxe dos periódicos brasileiros) exige
**title, abstract e keywords em inglês**. Acrescentar após o resumo enxuto do Eixo A (tradução
1:1 da versão curta — mais um motivo para encurtar primeiro). Conferir na norma da revista se há
exigências adicionais de formato (posição, itálico, limite próprio).

### C.3 Referências que ficaram de fora (retomar da `SINTESE_CONSOLIDADA.md` §3/§4.3)

| Ref | Para quê | Onde entra |
|---|---|---|
| **Richardson (1985)**, "Input-output and economic base multipliers: looking backward and forward", *Journal of Regional Science* | a ponte canônica base-de-exportação ↔ multiplicadores I-P — sustenta exatamente a costura North/Tiebout×tipo II que o artigo faz por conta própria | Eixo E (quadro analítico) |
| **Guilhoto et al. (2010, Nordeste)** e **Ichihara & Guilhoto (2008, municípios SP)** | precedentes diretos do recorte multiestadual e intra-estadual — completam o parágrafo do gênero | Eixo E / §Introdução |
| **Flegg & Tohmo (2016)**, **Többen & Kronenberg (2015, CHARM)**, **Riddington et al. (2006)** | bloco de incerteza da regionalização não-censitária que caiu na migração v1→v3 e que respondia à cobrança R2 do parecer v1 ("sensibilidade/incerteza") | §Dados (2ª fronteira) e §Limitações (i)(iii) |
| Estudos do gênero SC/MA (a verificar) | fechariam a moldura "melhores caracterizações estaduais → ES"; a rede bloqueou as fontes primárias na rodada anterior | tentar verificação de metadados de novo; **só citar se verificar** |

*Regra do projeto mantida: nenhuma referência entra sem metadados verificados.*

### C.4 O que **não** entra nesta rodada (continua agenda declarada)

- **F1** (CSVs das Tabelas 1 e 4): depende de `fechar_R1.bat` na máquina do autor — segue como
  única pendência do parecer; nada a fazer no repo.
- **P6/P7** (matriz 2019 + satélite de CO₂): hosts bloqueados neste ambiente; a infraestrutura
  (`26_ancora_2019.py`, `23_carbono_plataforma.py`) já está pronta e fail-closed.

---

## Eixo D — Diagramação

### D.1 Bugs de preâmbulo (correção imediata, alto impacto)

1. **`babel` não é carregado** — o texto inteiro em português está sendo hifenizado com padrões
   de inglês. Adicionar `\usepackage[english,brazilian]{babel}` (o `english` habilita o abstract
   EN de C.2) e remover os `\renewcommand{\abstractname}/{\refname}` manuais, que o babel cobre.
2. Adicionar `\usepackage{microtype}` (protrusão/expansão — melhora mancha e reduz overfull) e
   `\usepackage{lmodern}` (fontes vetoriais melhores que CM bitmap-like em alguns viewers).
3. `\usepackage[font=small,labelfont=bf]{caption}` — separa visualmente as legendas (hoje
   longas, no mesmo corpo do texto).

### D.2 Floats e tabelas

- Trocar `[ht]` por `[tbp]` nas 6 figuras e 5 tabelas e conferir a deriva página a página
  (com captions `small` e resumo curto, o miolo reflui).
- `tab:setores` (26 linhas + 2 de média, no meio de §7): avaliar **movê-la para o Apêndice B**
  (o texto já destaca os extremos em prosa) ou deixá-la em float page dedicada — decidir na
  recompilação.
- Conferir que toda figura/tabela aparece **depois** da primeira referência no texto.

### D.3 Rosto, anonimização e norma da revista

- Criar chave `\newif\ifanon` no preâmbulo: versão cega (sem autor/afiliação/agradecimentos/link
  do repositório) exigida pela avaliação da RBERU — item já no checklist de submissão.
- Conferir template/normas RBERU (corpo 12pt? espaçamento? sistema de citação ABNT ou
  autor-data?) e só então decidir se migra a bibliografia manual (`thebibliography`) para
  `.bib` — **não migrar por higiene**: a lista atual está estável e auditada (36↔36).
- Padronizar microtipografia: `R\$\,`, travessões, `\,\times\,`, ordinais (º via
  `\textordmasculine` já ok).

### D.4 Verificação visual final

Recompilar (3 passadas) e revisar o PDF página a página: viúvas/órfãs, captions órfãs de
figura, quebras de coluna nas tabelas, hifenização pós-babel. Registrar contagem final de
páginas (meta: não crescer além das ~20 atuais mesmo com o Eixo E — o resumo curto e as captions
`small` compensam a seção nova).

---

## Eixo E — Economia regional organizada pela literatura de insumo-produto

**Diagnóstico.** As pontes teóricas existem, mas estão **espalhadas**: North/Tiebout/Perroux na
introdução (¶2), North/Tiebout de novo no retrato (§4), Perroux nas ligações puras (§4),
Cano/Friedmann/Miller na plataforma (§7), e a Discussão (§8) refaz o triângulo em uma frase. O
leitor não encontra, em lugar nenhum, o **mapa** que liga cada lente teórica ao instrumento I-P
que a operacionaliza — que é exatamente o que o gênero "Estrutura Produtiva de [Estado]" tem de
melhor a oferecer.

**Proposta.** Nova seção curta (~1 página), entre a Introdução e os Dados:
**§2 "Quadro analítico: a teoria regional na linguagem de insumo-produto"**, com três blocos e
uma tabela-síntese:

| Lente teórica | Autores | Instrumento I-P | Onde o artigo mede |
|---|---|---|---|
| Base de exportação | North (1955); Tiebout (1956); Richardson (1985) | decomposição da produção/emprego pela demanda final; fechamento tipo II | §Retrato: 61,7% / 47,5%; mult. 27,9→40,4 |
| Polos de crescimento e encadeamentos | Perroux (1955); Hirschman (1958); Rasmussen (1956) | índices RH; ligações puras GHS (Cella 1984; Guilhoto et al. 2005) | §Retrato: setores-chave; polos mineração 4,4 / metalurgia 3,4 |
| Centro-periferia e interdependência inter-regional | Isard (1951); Miller (1966); Miyazawa (1966); Cano (1985); Friedmann (1966) | partição inter-regional; spillover/feedback; extração hipotética; modelo nulo de porte | §Território e §Plataforma: retenção 90,9/66,2; feedback 0,32%; −13% |

Conteúdo dos três blocos: (i) cada lente em 3–4 frases, já com a tradução operacional ("a base
de exportação *é medida por*…"); (ii) o parágrafo do **gênero brasileiro** consolidado aqui
(precedentes MT/RS/PA/MG + NE/municípios-SP de C.3, e os antecedentes capixabas Sessa et al.
2017 / Ribeiro et al. 2024 — hoje na introdução); (iii) fecho de meia frase: as três lentes são
três leituras do mesmo sistema $x=(I-A)^{-1}y$.

**Efeitos colaterais controlados:**

- A **Introdução emagrece** (fica: motivação, lacuna, as três perguntas, contribuição) — ganha o
  espaço que a seção nova ocupa.
- No corpo, as passagens teóricas viram **remissões** ao quadro ("é a fotografia da base de
  exportação — §2"), eliminando a repetição North/Tiebout que hoje existe entre §1 e §4.
- A **Discussão mantém** o parágrafo-síntese ("três descrições do mesmo dado") — ele passa a
  colher o que §2 plantou.
- **Não renumerar perguntas nem promessas**: o parecer elogiou a consistência
  introdução↔corpo; a seção nova não pode quebrar (i)-(ii)-(iii).

**Aceite:** nenhuma citação teórica duplicada entre §1/§2/corpo; tabela-síntese com todas as
células remetendo a resultados que o artigo de fato reporta; página total estável.

---

## Critérios de aceite globais da rodada

1. Compilação limpa: 0 referências indefinidas, 0 citações órfãs (`36+novas ↔ bibliografia`).
2. Resumo ≤200 palavras + abstract EN equivalente.
3. Seis figuras regeneradas segundo B.0, com os números da fig. 4 = texto = CSV.
4. Nenhum número auditado alterado (os asserts dos scripts 17/18/20/22 continuam passando).
5. `git diff` do `.tex` revisável por eixo (commits separados por eixo, como nas rodadas
   anteriores).

## Fora de escopo (decidido)

- Reabrir a convenção spillover/feedback (fechada em `MAPA_DE_PESQUISA.md` B).
- Esperar/baixar a matriz 2019 (P6) — segue agenda declarada no texto.
- Reescrever Apêndices A/B (aprovados pelo theorist-toolbox; só recebem toques de diagramação).
- Migração da bibliografia para `.bib` sem exigência da norma (risco > ganho).
