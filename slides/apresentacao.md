---
title: Estrutura Produtiva do Espírito Santo — uma análise de insumo-produto
tags: apresentação, insumo-produto, PPGEco
slideOptions:
  theme: white
  transition: slide
  slideNumber: true
  width: 1280
  height: 720
  margin: 0.04
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --paper:#FFFCF0; --ink:#100F0F;
  --b50:#F2F0E5; --b100:#E6E4D9; --b150:#DAD8CE; --b200:#CECDC3;
  --b300:#B7B5AC; --b500:#878580; --b600:#6F6E69;
  --es:#9E4A3C; --nuc:#3F6B97; --clu:#5E6B2E;   /* papéis = cores das figuras */
}

html, body, .reveal-viewport, .reveal, .reveal .slides{ background-color:var(--paper) !important; }
.reveal .backgrounds, .reveal .slide-background{ background-color:var(--paper) !important; }
.reveal .slides section{ background-color:transparent; }

.reveal{
  font-family:'Inter', -apple-system, system-ui, sans-serif;
  color:var(--ink); font-size:30px; font-weight:400;
  letter-spacing:-0.011em; -webkit-font-smoothing:antialiased;
}
.reveal .slides{ text-align:left; }

.reveal h1, .reveal h2, .reveal h3, .reveal h4{
  font-family:'Inter', system-ui, sans-serif;
  color:var(--ink); letter-spacing:-0.022em; text-transform:none; text-shadow:none;
}
.reveal h1{ font-weight:800; font-size:1.5em; line-height:1.1; }
.reveal h2{ font-weight:700; font-size:1.08em; margin-bottom:.4em;
            padding-bottom:.14em; border-bottom:1px solid var(--b200); }
.reveal h3{ font-weight:700; font-size:1.0em; }
.reveal h4{ font-weight:600; }

.reveal p, .reveal li{ line-height:1.38; }
.reveal strong{ color:var(--ink); font-weight:700; }
.reveal em{ color:var(--ink); }
.reveal a{ color:var(--ink); text-decoration:underline; text-underline-offset:2px; text-decoration-color:var(--b300); }

.reveal code{
  font-family:'SFMono-Regular', ui-monospace, Menlo, monospace;
  background:var(--b100); color:var(--ink);
  padding:1px 6px; border-radius:4px; font-size:.84em;
}

.reveal ul, .reveal ol{ margin-left:1.05em; }
.reveal li{ margin:.12em 0; }
.reveal li::marker{ color:var(--b500); }

.reveal blockquote{
  width:100%; background:var(--b50);
  border:1px solid var(--b150); border-left:4px solid var(--ink);
  border-radius:6px; padding:.5em .85em; box-shadow:none;
  font-style:normal; font-size:.88em; color:var(--ink);
}
.reveal blockquote p{ margin:.12em 0; }

/* TABELAS — padrão Nexo/Flexoki: réguas horizontais, sem grade, números tabulares */
.reveal table{ font-size:.8em; margin:.5em 0; border-collapse:collapse;
               font-variant-numeric:tabular-nums; }
.reveal table th{ background:transparent; color:var(--b600); font-weight:600;
                  text-transform:uppercase; letter-spacing:.03em; font-size:.74em;
                  border:none; border-bottom:1.5px solid var(--ink);
                  padding:.4em .7em; vertical-align:bottom; }
.reveal table td{ border:none; border-bottom:1px solid var(--b150); padding:.3em .7em; }
.reveal table tbody tr:last-child td{ border-bottom:1.5px solid var(--ink); }
.reveal th.n, .reveal td.n{ text-align:right; }                 /* coluna numérica */

/* linhas de destaque/realce */
.reveal tr.es-row td{ background:#F0E7DF; }                       /* ES em foco */
.reveal tr.nuc-row td{ background:#ECF1F6; color:var(--b600); }   /* núcleo SP/RJ, recuado */
.reveal tr.sum-row td{ background:var(--b50); font-weight:700; color:var(--ink);
                       border-top:1.5px solid var(--ink); border-bottom:1.5px solid var(--ink); }

/* tabelas compactas */
.reveal .t3{ width:100%; font-size:.7em; }
.reveal .t3 th, .reveal .t3 td{ padding:.2em .65em; line-height:1.25; }
.reveal .t3 td, .reveal .t3 th{ text-align:right; }
.reveal .t3 td:first-child, .reveal .t3 th:first-child,
.reveal .t3 td:last-child, .reveal .t3 th:last-child{ text-align:left; }

/* slides de tabela: espaçamento vertical compacto */
.reveal section.tight h2{ margin-bottom:.2em; }
.reveal section.tight p{ margin:.3em 0; line-height:1.3; }
.reveal section.tight .t3{ margin:.3em 0; }
.reveal section.xs p{ margin:.25em 0; }

.reveal mjx-container{ font-size:.95em !important; color:var(--ink); }
.reveal mjx-container[display="true"]{ margin:.4em 0; }

.reveal section img{ max-height:58vh; max-width:100%; height:auto;
                     border:1px solid var(--b200); border-radius:6px; }

.reveal section.center{ text-align:center; }
.reveal section.center ul, .reveal section.center ol{ display:inline-block; text-align:left; }
.reveal section.center h2, .reveal section.center h3{ border-bottom:none; }

/* SLIDE DE FIGURA: imagem domina, texto mínimo (max-height em px = coord. do slide) */
.reveal section.fig h2{ border-bottom:none; margin-bottom:.12em; font-size:1.0em; }
.reveal section.fig img{ max-height:550px; border:none; display:block; margin:.25em auto; }
.reveal section.fig1 img{ max-height:628px; }
.reveal section.fig blockquote{ font-size:.78em; margin-top:.25em; }

/* utilidades */
.reveal .stat{ font-weight:800; font-size:1.4em; line-height:1.05; }
.reveal .es{ color:var(--es); font-weight:700; }
.reveal .nuc{ color:var(--nuc); font-weight:700; }
.reveal .clu{ color:var(--clu); font-weight:700; }
.reveal .hl td{ background:#F0E7DF !important; font-weight:700; }

.reveal .footnote{ color:var(--b600); font-size:.6em; font-weight:500;
                    display:block; line-height:1.25; margin-top:.25em; }
.reveal .slide-number{ color:var(--b500); background:transparent; }
</style>

<!-- .slide: class="center" -->

# Estrutura Produtiva do Espírito Santo
## uma análise de insumo-produto

Multiplicadores, setores-chave, demanda, vocação territorial e a face plataforma de uma economia de base

`MIP ES × Brasil 2008 · série N68 2010–2021 · 10 microrregiões 2015 · 27 UFs · WIOD`

<br>

**Felipe Carvalho** · PPGEco/UFES
<span class="footnote">Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · 2026/1</span>

Note:
Caracterização da economia capixaba no gênero clássico brasileiro "Estrutura Produtiva de [Estado]" — a bateria completa de insumo-produto, em quatro frentes: retrato 2008, quem puxa a demanda, pano de fundo temporal 2010–2021 e vocação territorial 2015, mais a face da abertura. Todos os números reproduzíveis do repositório.

---

## Uma economia atípica — e uma lacuna

**O ES em duas linhas:** ≈2% do produto nacional; trocou de motor **duas vezes** em 40 anos — café → indústria de base (anos 1980: CST, Samarco, Aracruz) → **petróleo** (~¼ do produto estadual).

**O gênero:** a escola brasileira consolidou o formato "Estrutura Produtiva de [Estado]" — MT (Figueiredo et al. 2004), RS (Porsse et al. 2008), **Pará** (Sesso Filho & Guilhoto 2010)...

**A lacuna:** para o ES, só contribuições pontuais (Ubu: Sessa et al. 2017; microrregiões: Ribeiro et al. 2024). **Falta a caracterização abrangente.**

> **Três perguntas descritivas:** (i) *que tipo de economia* é o ES — e **quem a puxa**? (ii) como seus setores de base evoluíram **no tempo**? (iii) qual a **vocação** de cada território?

Note:
Não é teste de hipótese: é caracterização sistemática e reprodutível, no formato que o campo consolidou para outros estados e nunca fez de forma abrangente para o ES.

---

## As duas lentes da teoria regional

**Base de exportação** — o crescimento regional é comandado pela demanda **externa** (North 1955); a réplica de Tiebout (1956): as atividades **residentes** e o mercado interno importam.

**Polos de crescimento** — o crescimento aparece em **pontos**: indústrias motrizes que irradiam encadeamentos (Perroux 1955).

<br>

> A bateria insumo-produto **operacionaliza as duas lentes**: a decomposição da demanda final mede a base exportadora; as ligações puras medem os polos.

Note:
O artigo ancora a caracterização nas duas tradições fundadoras — e o dado capixaba conversa com as duas: North aparece na produção puxada de fora, Tiebout no emprego que fica com o mercado interno, Perroux nos polos identificados pelas ligações puras.

---

## Dados & método

| Matriz | Recorte | Papel |
|---|---|---|
| **ES × restante do BR (2008)** | 26 setores, c/ **emprego** | retrato estrutural + quem puxa |
| Interestadual **27 UFs (2008)** | 26 setores/UF | benchmark + destino do vazamento |
| **Série nacional N68** | 68 setores, 2010–2021 | pano de fundo temporal |
| **10 microrregiões ES (2015)** | 35 setores | vocação territorial |
| WIOD 2014 | 44 países, 56 setores | posição em cadeias globais |

**Bateria:** multiplicadores (produção/emprego/renda, tipos I e II) · Rasmussen-Hirschman (frente por **Ghosh**) · **ligações puras** (GHS) · LQ/HHI · decomposição da demanda final · Isard/Miyazawa · **modelo nulo de porte** · **extração hipotética**.

<span class="footnote">Regionalização IIOAS (Haddad et al. 2017). Formulário completo nos Apêndices A/B do artigo; pipeline reprodutível `pesquisa/01–26` + CSVs versionados.</span>

Note:
Três matrizes-âncora + benchmark + CGV. O método está todo em apêndice no artigo, equação a equação — Isard aditivo, Miyazawa multiplicativo, GHS na linhagem de Cella, modelo nulo, HEM.

---

## Retrato 2008 — os líderes não empregam

Multiplicador de produção médio: **1,76** (tipo I) · **2,45** (tipo II).

**O contraste central do retrato:**

| Quem multiplica... | Setores |
|---|---|
| **Produção** | alimentos (2,31) · refino (2,11) · mat. transporte · químicos |
| **Emprego** (27,9/R$ mi) | **têxtil (67,9)** · pecuária (57) · alojamento (50) · serviços (49) |
| **Renda** | educação · adm. pública · saúde · serviços |

> Os setores que **lideram** a economia capixaba não são os que **empregam** nem os que **distribuem renda** — nenhum trabalho-intensivo é setor de base.

Note:
O trade-off clássico da industrialização de base, agora medido: produção nos pesados, emprego nos trabalho-intensivos, renda nos serviços/público.

---

<!-- .slide: class="fig" -->

## Retrato 2008 — dualidade: enclave × setor-chave

![Mapa de ligações dos 26 setores](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/fig_setores_chave.png)

> Setores-chave = **transformação** (refino, químicos, metalurgia...). A **mineração**: frente ≈1,2, trás ≈0,9 — fornecedora a montante, **enclave**. Ligações puras (polos perrouxianos): **mineração 4,4 · metalurgia 3,4**.

Note:
A dualidade que organiza o artigo: extração-enclave (compra pouco internamente) vs transformação-chave. Pelas ligações puras — ponderadas por tamanho, na linhagem Cella→GHS — mineração e metalurgia são os polos de crescimento no sentido de Perroux.

---

## Quem puxa a economia — North e Tiebout no dado

$x^{(k)}=B\,y^{(k)}$: produção e emprego atribuídos a cada componente da demanda final.

| Componente | Produção | Emprego |
|---|--:|--:|
| **Demanda externa** (RB + exportações) | **61,7%** | **47,5%** |
| Consumo das famílias ES | 18,8% | 25,7% |
| Governo + ISFLSF ES | 13,1% | 16,1% |
| FBCF + estoques ES | 6,3% | 10,7% |

> O motor da produção está **fora** (North); o emprego fica desproporcionalmente com o **mercado interno** (Tiebout). O canal tieboutiano é o **tipo II**: o induzido eleva o multiplicador de emprego de 27,9 → **40,4**.

<span class="footnote">Refino/metalurgia/mineração: >96% puxados de fora. Adm. pública/educação/saúde: ≥90% domésticos. Variação de estoques negativa em 2008 (desova de crise).</span>

Note:
A fotografia insumo-produto da base de exportação — com a nuance distributiva: quem produz para fora não é quem emprega. 61,7% da produção vs 47,5% do emprego.

---

<!-- .slide: class="tight" -->

## Benchmark 27 UFs — genérico em tipo, extremo em grau

<table class="t3">
<thead>
<tr><th>Métrica</th><th>ES</th><th>posição</th><th>mediana 27 UFs</th><th>leitura</th></tr>
</thead>
<tbody>
<tr><td>Mult. de produção (pond.)</td><td>1,66</td><td>14º</td><td>1,66</td><td>exatamente mediano</td></tr>
<tr><td>Ligação para trás (pond.)</td><td>0,92</td><td>14º</td><td>0,92</td><td>exatamente mediano</td></tr>
<tr class="es-row"><td>Setores de base (%)</td><td><strong>36,4</strong></td><td><strong>2º</strong></td><td>21,0</td><td>extremo (só MT acima)</td></tr>
<tr class="es-row"><td>Mult. de emprego (/R$ mi)</td><td>25,4</td><td>24º</td><td>42,5</td><td>entre os menores</td></tr>
<tr class="es-row"><td>Emprego do líder ÷ média</td><td>0,39</td><td>2º menor</td><td>0,65</td><td>líder que não emprega</td></tr>
</tbody>
</table>

> O ES não é contraexemplo da regularidade — é um de seus **casos-limite**: a economia onde a base pesa mais e menos emprego direto distribui. Setor dominante = **Mineração**: só ES, PA e RJ no país.

<span class="footnote">Médias ponderadas pela produção, matriz interestadual (por isso ≠ 1,76/27,9 da bi-regional — nota de conciliação no artigo). Classificação de base declarada em nota (inclui Alimentos).</span>

Note:
A resposta ao "específico × genérico": nos indicadores neutros à composição o ES é mediano; é na composição e no emprego que ele é extremo.

---

<!-- .slide: class="fig" -->

## O tempo (2010–2021) — celulose adensa, extração dispensa

![Trajetória das ligações dos setores-base](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/fig_trajetoria_n68.png)

> **Celulose**: 1,41 → **1,51** (único setor-base que adensa). **Siderurgia**: recuo em 2021 = **efeito de preço** do aço (matrizes a preços correntes — diagnóstico próprio). **Extração**: sempre <1 — enclave.

<span class="footnote">Ressalva de objeto: série NACIONAL — tendência dos setores, não do estado (o ES só tem âncoras 2008 e 2015).</span>

Note:
A dualidade do retrato persiste no tempo. A queda da siderurgia em 2021 foi investigada (diag_sider.py): não é quebra de classificação, é o salto do preço do aço sobre coeficientes a preços correntes.

---

<!-- .slide: class="fig" -->

## O território (2015) — um mosaico de vocações

![Quociente locacional por setor e microrregião](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/fig_micro_vocacao.png)

> Núcleo metropolitano diversificado (62% da produção) cercado por especializações: **celulose** no Rio Doce (LQ 8,2) · **rochas** no Central Sul (7,7) · **pelotização** no Litoral Sul (9,5) · **têxtil** no Centro-Oeste (9,6) · **pecuária** na Central Serrana (21,9).

Note:
Cada território acende exatamente no setor que a geografia econômica conhecida prevê — a vocação valida a chave das microrregiões. Os enclaves extrativos são também os territórios mais mono-estruturais (HHI).

---

## O território — centro e periferia, medidos

| Microrregião | % VBP | Mult. (pond.) | **Retenção intra** | Mult. renda |
|---|--:|--:|--:|--:|
| Metropolitana | 62,3 | 1,64 | **90,9%** | 0,37 |
| Rio Doce | 10,6 | 1,64 | 74,3% | 0,31 |
| Litoral Sul | 4,1 | 1,76 | **66,2%** | 0,34 |
| Caparaó | 1,9 | 1,42 | 88,2% | 0,39 |

**A metrópole retém; a periferia extrativa compra na metrópole.**

> **Extração hipotética:** removida a Metropolitana do sistema, a produção das demais microrregiões cairia <span class="stat es">−13,0%</span>

<span class="footnote">Multiplicador simples ≈ idêntico entre regiões (tecnologia IIOAS comum): o que difere é composição e retenção. Retenção = razão das somas ponderadas (conciliação com o vazamento 8,4% em nota do artigo).</span>

Note:
O desenho centro-periferia deixa de ser qualitativo: a periferia depende do núcleo capixaba como o estado depende do Sudeste. Nenhum plano sub-estadual dispunha desse número.

---

<!-- .slide: class="fig" -->

## A face plataforma — vazamento e destino

![Sankey — destino do spillover do ES](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_sankey.png)

> Vazamento médio **24,9%** · spillover R$ 18,2 bi · **feedback 0,32%** · núcleo SP+RJ absorve **52,5%**. No emprego, os pesados vazam metade ou mais (refino **61,6%**).

Note:
A herança do trabalho anterior, agora como UMA seção da caracterização: a economia de base realiza parte do seu encadeamento fora — e o destino é concentrado nos vizinhos ricos.

---

<!-- .slide: class="fig" -->

## Mas a mecânica é a prevista para o porte

![Invariância de escala — feedback × porte nas duas escalas](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/figuras/fractal_duas_escalas.png)

> **Modelo nulo** ($m_r=\alpha+\beta\ln x_r+\varepsilon$): o ES **não é outlier** em nenhuma métrica (z: +0,45 · −0,05 · +0,03); feedback observado **abaixo** do previsto. Retorno é privilégio de núcleo: SP+RJ **1,97%** vs 0,49%. MG (60%) e RS (55%) escoam **mais** ao núcleo que o ES (52,5%).

<span class="footnote">R² = 0,59 (27 UFs) e 0,91 (10 microrregiões): a mesma mecânica de posição-e-porte nas duas escalas.</span>

Note:
O teste que poderia derrubar a retórica — e foi publicado: a mecânica do vazamento é genérica. O que é específico do ES não é a decomposição, é a COMPOSIÇÃO que ela transporta. Honestidade que virou diferencial no parecer.

---

<!-- .slide: class="fig" -->

## A contraparte global — fornecedor a montante

![Upstreamness da pauta do ES — WIOD 2014](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_upstreamness.png)

> Pauta do ES: <span class="es">**3,12**</span> · Brasil 1,91 · mundo 2,31 · mineração 33ª de 2.279 (~p99). O valor a jusante realiza-se em outras regiões e países.

Note:
Tradução em escala de cadeia global do mesmo diagnóstico: economia de base, a montante. Tratamento da base WIOD (185 pares excluídos) documentado no Apêndice B.

---

## Síntese — três descrições do mesmo dado

**O ES é uma economia de base, dual e puxada de fora**: líderes grandes, a montante, intensivos em capital — que geram encadeamento, mas pouco emprego e renda diretos.

| Lente | O que o dado mostra |
|---|---|
| **North** (base de exportação) | demanda externa puxa **61,7%** da produção |
| **Perroux** (polos motrizes) | mineração (4,4) e metalurgia (3,4) concentram o encadeamento |
| **Cano/Friedmann** (centro-periferia) | o valor escoa ao núcleo — do Litoral Sul à Grande Vitória, do ES ao Sudeste, em **escalas aninhadas** |

Note:
Base exportadora que comanda a produção, polos que concentram o encadeamento e hierarquia centro-periferia que captura o valor: três descrições do mesmo dado — o parágrafo-síntese do artigo.

---

## Política — três alavancas + o canal que resta

**(i) Adensar a jusante da base mineral** — minério → aço → produtos de metal: a metalurgia já é setor-chave; estender a cadeia retém encadeamento que hoje escoa.

**(ii) Apostar na celulose** — único setor-base cuja ligação para trás **cresce** (1,41→1,51).

**(iii) Diversificar com endereço territorial** — rochas, têxtil, agroindústria; a extração hipotética dá a medida do risco mitigado (**−13%** sem a metrópole).

> **Royalties**: se o retorno via encadeamento é estruturalmente limitado para o porte (feedback *abaixo* do previsto), a **captura fiscal** é o canal de retorno que resta — destiná-la ao adensamento é política estrutural.

Note:
As alavancas saem do próprio dado. E o modelo nulo dá o fecho ao argumento fiscal: não adianta esperar o retorno pelo encadeamento; ele não vem, para nenhum estado desse porte.

---

## Limitações & agenda

1. **Âncoras, não série**: o ES tem 2008 e 2015; a série 2010–2021 é nacional (tendência dos setores) e a preços correntes (deflação pendente).
2. **Fluxos estimados** (IIOAS); sistema microrregional sem vetor de emprego e com um setor desbalanceado (sensibilidade S23 no Apêndice B).
3. **Agenda imediata — a segunda âncora**: matriz interestadual **2019** (Haddad et al. 2025; 68 setores, satélites de emprego e CO₂) → comparação 2008×2019 (`26_ancora_2019.py`, pronto) e **carbono-plataforma** (`23_*`, pronto): a base exporta valor a montante **e carbono incorporado**.

Note:
Limites declarados de frente — e cada um com o pipeline correspondente já montado no repositório, esperando só o dado.

---

<!-- .slide: class="center" -->

## Obrigado

**Uma economia de base, dual, puxada de fora — cuja especificidade não está na mecânica do vazamento, mas na composição que ela transporta.**

<br>

<span class="footnote">Artigo (19 págs., 36 refs., apêndices metodológicos), código, tabelas e estes slides são reprodutíveis · github.com/fcarva/es-insumo-produto</span>

<span class="footnote">North (1955) · Tiebout (1956) · Perroux (1955) · Isard (1951) · Miyazawa (1966) · Rasmussen (1956) · Hirschman (1958) · Cella (1984) · Guilhoto-Sonis-Hewings (2005) · Miller & Blair (2009) · Haddad et al. (2017, 2025) · Antràs et al. (2012)</span>

Note:
Frase-síntese e perguntas. Prováveis: por que 2008 (âncora disponível + inércia estrutural; 2019 é a agenda); a diferença 1,76 vs 1,66 (simples/bi-regional vs ponderado/interestadual — nota no artigo); o que mudou com o modelo nulo (a tese-plataforma virou pano de fundo; a especificidade é composicional). Obrigado.
