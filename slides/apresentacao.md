---
title: O Espírito Santo como economia-plataforma
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

.reveal table{ font-size:.8em; margin:.4em 0; border-collapse:collapse; }
.reveal table th{ background:var(--b100); color:var(--ink); font-weight:700;
                  border-bottom:2px solid var(--ink); }
.reveal table td, .reveal table th{ padding:.3em .8em; border:1px solid var(--b150); }
.reveal table tbody tr:nth-child(even) td{ background:var(--b50); }

.reveal mjx-container{ font-size:.95em !important; color:var(--ink); }
.reveal mjx-container[display="true"]{ margin:.4em 0; }

.reveal section img{ max-height:58vh; max-width:100%; height:auto;
                     border:1px solid var(--b200); border-radius:6px; }

.reveal section.center{ text-align:center; }
.reveal section.center ul, .reveal section.center ol{ display:inline-block; text-align:left; }
.reveal section.center h2, .reveal section.center h3{ border-bottom:none; }

/* SLIDE DE FIGURA: imagem domina, texto mínimo */
.reveal section.fig h2{ border-bottom:none; margin-bottom:.12em; font-size:1.0em; }
.reveal section.fig img{ max-height:72vh; border:none; display:block; margin:.25em auto; }
.reveal section.fig blockquote{ font-size:.78em; margin-top:.25em; }

/* DUAS COLUNAS (figura + texto lado a lado) */
.reveal .cols{ display:flex; gap:1.1em; align-items:center; }
.reveal .cols .cfig{ flex:1.5 1 0; }
.reveal .cols .ctxt{ flex:1 1 0; }
.reveal .cols img{ max-height:66vh; }

/* TABELA DENSA (distribuição completa dos 26 setores) */
.reveal section.xs h2{ margin-bottom:.25em; }
.reveal .xs table{ font-size:.5em; width:100%; }
.reveal .xs table td, .reveal .xs table th{ padding:.16em .5em; }
.reveal .xs .footnote{ font-size:.8em; }
.reveal .xs table td:nth-child(5), .reveal .xs table th:nth-child(5){
  border-top:none; border-bottom:none; background:transparent !important; width:.7em; }

/* utilidades */
.reveal .stat{ font-weight:800; font-size:1.4em; line-height:1.05; }
.reveal .es{ color:var(--es); font-weight:700; }
.reveal .nuc{ color:var(--nuc); font-weight:700; }
.reveal .clu{ color:var(--clu); font-weight:700; }
.reveal .hl td{ background:#F0E7DF !important; font-weight:700; }

.reveal .footnote{ color:var(--b600); font-size:.6em; font-weight:500; }
.reveal .slide-number{ color:var(--b500); background:transparent; }
</style>

<!-- .slide: class="center" -->

# O Espírito Santo como economia-plataforma

Encadeamentos, vazamento de multiplicadores e a assimetria *spillover*/*feedback* na cadeia inter-regional de valor

`MIP ES × Brasil 2008 · matriz interestadual 27-UF · WIOD 2014`

<br>

**Felipe Carvalho** · PPGEco/UFES
<span class="footnote">Análise de Insumo-Produto · Prof. Dr. Celso Bissoli Sessa · 2026/1</span>

Note:
O ES não é uma versão em miniatura do Brasil, e sim uma economia-plataforma — pequena, hiperaberta, organizada em torno de setores cuja demanda final se realiza fora do estado. Base: matriz inter-regional ES × restante do Brasil (2008), matriz interestadual das 27 UFs e WIOD 2014. Todos os números são reprodutíveis a partir do repositório.

---

## O Brasil e o Espírito Santo

**Visão convencional** — uma economia estadual que reproduz, em escala reduzida, a estrutura produtiva do país.

**Economia-plataforma** — pequena, hiperaberta, estruturada em torno de setores cuja **demanda final se realiza fora do estado**.

<br>

**Três perguntas organizam a análise:**

1. Para onde vai o **multiplicador capixaba** — quanto fica e quanto vaza?
2. **Para onde** vaza — quem absorve o encadeamento que escapa?
3. Que **estágio na cadeia de valor** esse destino revela?

Note:
A intuição comum trata um estado como "mini-país". O trabalho testa e rejeita isso para o ES. A novidade frente à versão anterior: além de "quanto vaza", respondemos "para onde vaza" (decomposição interestadual) e situamos o ES em cadeias de valor.

---

## Contexto — o ES em 2008

### ≈ 2,0% do produto nacional

Economia **aberta**: elevado coeficiente de comércio interestadual — boa parte dos insumos e da demanda cruza a fronteira do estado.

<br>

Setores de maior peso, com **demanda final fora do estado**:

- Mineração · Metalurgia · Celulose e papel
- Refino de petróleo · Transporte e complexo portuário

Note:
O ponto não é o tamanho (2% do PIB), e sim a estrutura: pauta concentrada em setores de passagem (minério, metalurgia, celulose/papel, refino, complexo logístico-portuário). Pequeno + hiperaberto + concentrado em setores cuja demanda final está fora → tese plataforma.

---

## Dados & fontes

**Núcleo — MIP inter-regional ES × restante do Brasil (2008)**
26 setores por região, R\$ milhões, contábil e balanceada, com vetor de pessoal ocupado. Regionalização (Guilhoto & Sesso Filho, 2005) + fluxos IIOAS (Haddad et al., 2017).

**Geografia — matriz interestadual das 27 UFs (2008)** → rastreia o *destino* do vazamento, estado a estado.

**Cadeias globais — WIOD 2014 (44 regiões, 56 setores)** → *upstreamness* (Antràs-Chor).

> **Validação.** Vazamento médio do multiplicador = <span class="stat">24,9%</span> &nbsp;converge com os **27,4%** de Haddad et al. (2017). A bi-regional e a interestadual dão a **mesma** injeção e o mesmo spillover. ✓

Note:
Matriz contábil e perfeitamente balanceada (consistência 0,00%). A interestadual é o que permite o resultado novo de "para onde vaza". Credibilidade: nosso vazamento converge com Haddad; e a bi-regional e a interestadual se validam mutuamente.

---

## Método I — arcabouço inter-regional (Isard)

Duas regiões: $L$ (ES) e $M$ (restante do Brasil). Coeficientes e inversa de Leontief em blocos:

$$
A=\begin{bmatrix} A^{LL} & A^{LM}\\ A^{ML} & A^{MM}\end{bmatrix},
\qquad
\begin{bmatrix} x^{L}\\ x^{M}\end{bmatrix}=(I-A)^{-1}\begin{bmatrix} f^{L}\\ f^{M}\end{bmatrix}=B\,f
$$

com $A=Z\hat{x}^{-1}$. Os blocos **fora da diagonal** ($A^{LM},A^{ML}$) carregam o comércio entre ES e Brasil.

Note:
Quatro blocos: intra na diagonal, inter fora dela. São os blocos de fora da diagonal que carregam o comércio ES↔Brasil — e que permitem separar spillover de feedback. f = demanda final.

---

## Método I — *spillover* e *feedback*

Resolvendo para a região $L$, a forma reduzida traz o **feedback** explícito:

$$
x^{L}=\underbrace{(I-A^{LL})^{-1}}_{\text{intra}}f^{L}
+\underbrace{\big[(I-A^{LL}-A^{LM}(I-A^{MM})^{-1}A^{ML})^{-1}-(I-A^{LL})^{-1}\big]f^{L}}_{\text{feedback}}
$$

- $\Delta f^{L}$ eleva a produção em $M$ → ***spillover***
- essa produção requer insumos de volta a $L$ → ***feedback***

> O modelo inter-regional **isola a magnitude** de cada efeito — a matriz isolada do ES só mediria o vazamento total, não seu destino.

Note:
A vantagem decisiva da inter-regional é separar spillover de feedback. Spillover = produção que a demanda capixaba puxa para fora; feedback = o que retorna ao ES como insumo. É o experimento do Resultado 1.

---

## Método II — multiplicadores & vazamento

A partir de $B=(I-A)^{-1}$, o **multiplicador de produção** (soma de coluna) decompõe-se em retido e vazado:

$$
O_j=\underbrace{\textstyle\sum_{i\in L} b_{ij}}_{O^{L}_j\ \text{(retido)}}
+\underbrace{\textstyle\sum_{i\in M} b_{ij}}_{O^{M}_j\ \text{(vazado)}}
,\qquad
\text{vazamento}_j=\frac{O^{M}_j}{O_j}
$$

**Emprego** ($w_i=\text{ocupações}_i/x_i$): $\;E_j=\sum_i w_i\,b_{ij}$.
**Upstreamness** (Antràs-Chor): $\;U=(I-G)^{-1}\mathbf{1}$, &nbsp; $G_{ij}=z_{ij}/x_i$.

Note:
O multiplicador de produção é a soma de coluna da inversa; a decomposição retido/vazado é a métrica central. Emprego usa o coeficiente de trabalho. Upstreamness mede a distância ao consumo final — quanto maior, mais "a montante".

---

<!-- .slide: class="fig" -->

## Resultado 1 — o ES move o país, que não o move de volta

![Sankey — destino do spillover do ES](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_sankey.png)

Note:
O número que prende a plateia. A demanda final do ES (R$51,5 bi) põe em movimento R$81,8 bi de produção: 78% fica no ES, R$18,2 bi vazam (spillover) e só R$164 mi — 0,32% — retornam (feedback). A barra de contexto no topo mostra a assimetria; o diagrama estratifica o destino. Pausa após o 0,32%.

---

## Resultado 1 — a assimetria, em números

**Experimento:** injeta-se a demanda final do ES por produtos do ES, $f^{L}$, com $f^{M}=0$.

| Fluxo | Magnitude |
|---|---|
| **Injeção** — demanda final do ES por produtos do ES | R\$ 51,5 bi |
| Produção total posta em movimento | R\$ 81,8 bi |
| → ***Spillover*** — produção no restante do Brasil | **R\$ 18,2 bi** |
| ← ***Feedback*** — retorno ao ES | **R\$ 164 mi · <span class="es">0,32%</span>** |

> **O estado puxa o país; o país quase não o puxa de volta.** Do total posto em movimento, **78% fica no ES**.

<span class="footnote">Convenção Miller-Blair reprodutível (Tipo I). A assimetria é robusta: feedback/injeção = 0,15–0,32% sob qualquer convenção.</span>

Note:
A versão-semente reportava 60,6/22,4/0,26%, que não reproduzem na matriz; adotamos a convenção Miller-Blair reprodutível. A tese qualitativa não muda.

---

<!-- .slide: class="fig" -->

## Resultado 2 — para onde vaza: o Sudeste absorve dois terços

![Destino do spillover por estado e macrorregião](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_spillover_destino.png)

> <span class="nuc">**Sudeste (ex-ES) = 65%**</span> &nbsp;·&nbsp; <span class="nuc">SP 38%</span> · <span class="nuc">RJ 15%</span> · <span class="clu">MG 13%</span>. O ES alimenta seus vizinhos mais ricos.

Note:
O vazamento não se dispersa: dois terços ficam no próprio Sudeste, mais da metade no eixo SP-RJ. SP/RJ em azul (núcleo), MG/pares em verde (cluster). O encadeamento que escapa é capturado a jusante por economias mais diversificadas.

---

<!-- .slide: class="fig" -->

## Resultado 3 — o ES num cluster de estados dinâmicos

![O ES no cluster — destino e abertura](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_cluster.png)

> O ES escoa <span class="nuc">**52,5% ao núcleo SP/RJ**</span> e só <span class="clu">31,5% aos pares</span> — o elo vai ao centro, o capital não volta.

Note:
Ponte com um debate de mercado contemporâneo (Apex Partners): um cluster de estados dinâmicos sub-cobertos pelo capital, do qual o ES faz parte e que exclui justamente SP/RJ. Contraparte estrutural: o ES gera encadeamento que escoa para o núcleo, com feedback ~0.

---

## Resultado 3 — o cluster por dentro

8 estados de crescimento acima da média, **sub-cobertos pelo mercado de capitais** (leitura da Apex Partners) — excluem o núcleo SP/RJ · **33,9% do PIB**.

| Estado | PIB % | Vazam. % | Base/*commodity* % | Setor dominante |
|---|--:|--:|--:|---|
| <span class="es">ES</span> | 2,2 | 22,8 | **36,4** | Mineração |
| MG | 9,5 | 20,9 | 29,6 | Metalurgia |
| SC | 4,1 | 22,5 | 21,7 | Alimentos |
| PR | 6,0 | 22,3 | 28,0 | Alimentos |
| RS | 6,7 | 21,8 | 24,6 | Alimentos |
| GO | 2,6 | 25,1 | 32,8 | Alimentos |
| MT | 1,8 | 27,4 | 43,4 | Agricultura |
| MS | 1,1 | 25,7 | 30,1 | Alimentos |
| SP *(núcleo)* | 32,0 | **14,2** | 18,0 | Serviços |
| RJ *(núcleo)* | 11,2 | 15,6 | 27,4 | Mineração |

<span class="footnote">O ES é o 2º mais intensivo em setores de base (só MT acima) e — com o RJ — o único cujo setor dominante é Mineração. O núcleo SP/RJ é o menos aberto do país.</span>

Note:
Dentro do cluster, o ES é dos mais "commodity" e abertos; o núcleo SP/RJ retém (SP é o menos aberto do país, 14,2%). Isso reforça o caráter-plataforma do ES mesmo entre seus pares dinâmicos.

---

<!-- .slide: class="xs" -->

## Resultado 4 — vazamento do multiplicador: distribuição completa

| Setor | $O_j$ | Vaz. prod. % | Vaz. empr. % | | Setor | $O_j$ | Vaz. prod. % | Vaz. empr. % |
|---|--:|--:|--:|---|---|--:|--:|--:|
| Imobiliário/aluguel | 1,15 | 5,3 | 12,3 | | Refino/coque | 2,11 | 27,8 | **61,6** |
| Educação | 1,31 | 11,6 | 7,1 | | Têxtil/vestuário | 1,87 | 28,1 | 17,8 |
| Financeiro/seguros | 1,47 | 12,8 | 20,6 | | Metalurgia | 1,96 | 29,3 | **49,3** |
| Adm. pública | 1,43 | 15,0 | 16,0 | | Químicos/farma | 2,10 | 29,4 | 41,2 |
| Comércio | 1,42 | 16,0 | 7,6 | | Mat. elétrico/eletrôn. | 1,99 | 29,8 | 34,2 |
| Serviços privados | 1,50 | 17,9 | 8,4 | | Pecuária e pesca | 1,64 | 30,2 | 19,4 |
| Saúde | 1,54 | 19,1 | 14,9 | | Transporte/armaz. | 1,77 | 30,3 | 23,1 |
| Eletricidade/gás/água | 1,83 | 21,0 | 28,4 | | Indústrias diversas | 1,84 | 30,5 | 16,3 |
| Agricultura/silvic. | 1,45 | 21,6 | 9,9 | | Min. não-metálicos | 1,90 | 30,7 | 28,2 |
| Mineração | 1,64 | 22,7 | 42,4 | | Alojamento/alim. | 1,76 | 31,9 | 22,2 |
| Máquinas/equip. | 2,00 | 24,9 | 26,5 | | Madeira/papel | 1,96 | 35,8 | **50,3** |
| Construção | 1,70 | 25,5 | 16,1 | | Borracha/plástico | 2,05 | 36,8 | 32,9 |
| Mat. de transporte | 2,10 | 26,1 | 29,7 | | **Alimentos** | 2,31 | **37,4** | **56,5** |

<span class="footnote">Ordenado pelo vazamento de produção · Média ES: **24,9%** (simples) / **22,8%** (ponderada pela produção). $O_j$ = multiplicador de produção. Setores locais/de serviço retêm; setores de transformação vazam.</span>

Note:
Distribuição completa dos 26 setores, ordenada pelo vazamento de produção. Imobiliário quase não vaza (5,3%, local); alimentos vaza muito (37,4%). No emprego, os setores pesados (refino 61,6, alimentos 56,5, madeira 50,3, metalurgia 49,3) lideram. Médias: 24,9% simples / 22,8% ponderada.

---

## Resultado 5 — o vazamento de emprego é ainda mais agudo

Nos setores pesados, **metade ou mais** do emprego puxado pela demanda capixaba realiza-se fora do estado.

| Setor | % do emprego que vaza |
|---|--:|
| Refino de petróleo | **61,6%** |
| Alimentos | 56,5% |
| Madeira e papel | 50,3% |
| Metalurgia | 49,3% |

> **Núcleo operacional** da tese: o ES movimenta a cadeia, mas o emprego associado se materializa lá fora.

Note:
O vazamento é mais agudo no emprego e concentrado nos setores pesados. Metade ou mais dos postos que a demanda capixaba sustenta nesses setores ficam fora do ES.

---

<!-- .slide: class="fig" -->

## Resultado 6 — o ES está preso a montante da cadeia de valor

![Upstreamness da pauta do ES — WIOD 2014](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_upstreamness.png)

> Pauta do ES: <span class="es">**3,12**</span> &nbsp;·&nbsp; Brasil 1,91 · mundo 2,31 · mineração no **percentil ~98** global.

Note:
A inter-regional mostra para onde vaza; a CGV mostra o porquê estrutural. ES preso a montante: upstreamness 3,12 contra 1,91 do Brasil. Fornecedor de matéria-prima; o valor a jusante (manufatura, marca, serviços) está fora.

---

## Síntese

O mapa do vazamento é, ao mesmo tempo, um mapa de **fragilidade** e de **oportunidade**.

**Fragilidade** — setores que apenas transitam pelo estado (mineração, refino): multiplicador e emprego vazam; o valor realiza-se fora, sobretudo no núcleo SP/RJ.

**Oportunidade** — setores que retêm multiplicador e adensam cadeia (alimentos, serviços): motores efetivos de profundidade do mercado regional.

> A análise insumo-produto operacionaliza a **"vocação local"**: distingue os setores que aprofundam a cadeia dos que apenas a atravessam — base para teses de adensamento e de **mercado de capitais fora do eixo Rio–SP**.

Note:
A mesma quantidade — o vazamento — tem dupla leitura. Fragilidade: dependência externa. Oportunidade: onde adensar (setores que retêm). Elo com a leitura de capital do Resultado 3.

---

## Limitações & agenda

1. **Quebra estrutural** — matriz de 2008; Fundão (2015) alterou o peso de extração/pelotização. Fluxos interestaduais *estimados* (IIOAS). WIOD: ES sem assento → aproximação via Brasil.
2. **Dinâmica intra-ES** — o sistema das microrregiões (2015) mostra o padrão se replicando: a metrópole retém, a periferia vaza.
3. **Série longitudinal 2000 × 2014** — o ES subiu ou desceu na cadeia no boom de commodities?
4. **MRIO mundial** — destino internacional do valor e do emprego das exportações.

Note:
Escopo congelado em 2008 + WIOD 2014. Limitações viram programa: intra-ES (padrão se replica), série 2000-2014, MRIO mundial. "Por que 2008?": é a vintage da matriz balanceada disponível, defendida pela inércia estrutural das cadeias de base.

---

<!-- .slide: class="center" -->

## Obrigado

**O ES não é um mini-Brasil — é a plataforma exportadora do país.**

<br>

<span class="footnote">Código, dados, PDF e estes slides são reprodutíveis · github.com/fcarva/es-insumo-produto</span>

<span class="footnote">Isard (1951) · Miller & Blair (2009) · Rasmussen (1956) · Guilhoto & Sesso Filho (2005) · Haddad et al. (2017) · Antràs et al. (2012) · Timmer et al. (WIOD) · Dietzenbacher & Lahr (2013)</span>

Note:
Frase-síntese e abertura para perguntas. Prováveis: por que 2008; por que os números mudaram (auditoria/reprodutibilidade, convergência com Haddad); implicação de política (adensar setores que retêm; sub-cobertura de capital). Pipeline reprodutível no repositório. Obrigado.
