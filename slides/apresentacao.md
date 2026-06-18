---
title: O Espírito Santo como economia-plataforma
tags: apresentação, insumo-produto, PPGEco
slideOptions:
  theme: white
  transition: slide
  slideNumber: true
  width: 1280
  height: 720
  margin: 0.06
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
  color:var(--ink); font-size:32px; font-weight:400;
  letter-spacing:-0.011em; -webkit-font-smoothing:antialiased;
}
.reveal .slides{ text-align:left; }

.reveal h1, .reveal h2, .reveal h3, .reveal h4{
  font-family:'Inter', system-ui, sans-serif;
  color:var(--ink); letter-spacing:-0.022em; text-transform:none; text-shadow:none;
}
.reveal h1{ font-weight:800; font-size:1.5em; line-height:1.1; }
.reveal h2{ font-weight:700; font-size:1.14em; margin-bottom:.5em;
            padding-bottom:.16em; border-bottom:1px solid var(--b200); }
.reveal h3{ font-weight:700; font-size:1.0em; }
.reveal h4{ font-weight:600; }

.reveal p, .reveal li{ line-height:1.42; }
.reveal strong{ color:var(--ink); font-weight:700; }
.reveal em{ color:var(--ink); }
.reveal a{ color:var(--ink); text-decoration:underline; text-underline-offset:2px; text-decoration-color:var(--b300); }

.reveal code{
  font-family:'SFMono-Regular', ui-monospace, Menlo, monospace;
  background:var(--b100); color:var(--ink);
  padding:1px 6px; border-radius:4px; font-size:.84em;
}

.reveal ul, .reveal ol{ margin-left:1.05em; }
.reveal li{ margin:.14em 0; }
.reveal li::marker{ color:var(--b500); }

.reveal blockquote{
  width:100%; background:var(--b50);
  border:1px solid var(--b150); border-left:4px solid var(--ink);
  border-radius:6px; padding:.55em .9em; box-shadow:none;
  font-style:normal; font-size:.9em; color:var(--ink);
}
.reveal blockquote p{ margin:.15em 0; }

.reveal table{ font-size:.82em; margin:.45em 0; border-collapse:collapse; }
.reveal table th{ background:var(--b100); color:var(--ink); font-weight:700;
                  border-bottom:2px solid var(--ink); }
.reveal table td, .reveal table th{ padding:.34em .85em; border:1px solid var(--b150); }
.reveal table tbody tr:nth-child(even) td{ background:var(--b50); }

.reveal mjx-container{ font-size:.96em !important; color:var(--ink); }
.reveal mjx-container[display="true"]{ margin:.45em 0; }

.reveal section img{ max-height:60vh; max-width:100%; height:auto;
                     border:1px solid var(--b200); border-radius:6px; }

.reveal section.center{ text-align:center; }
.reveal section.center ul, .reveal section.center ol{ display:inline-block; text-align:left; }
.reveal section.center h2, .reveal section.center h3{ border-bottom:none; }

/* utilidades: números-destaque e cores de papel (batem com as figuras) */
.reveal .stat{ font-weight:800; font-size:1.4em; line-height:1.05; }
.reveal .es{ color:var(--es); font-weight:700; }
.reveal .nuc{ color:var(--nuc); font-weight:700; }
.reveal .clu{ color:var(--clu); font-weight:700; }

.reveal .footnote{ color:var(--b600); font-size:.62em; font-weight:500; }
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
O ES não é uma versão em miniatura do Brasil, e sim uma economia-plataforma — pequena, hiperaberta, organizada em torno de setores cuja demanda final se realiza fora do estado. Base: matriz inter-regional ES × restante do Brasil (2008, 26 setores), matriz interestadual das 27 UFs (para rastrear o destino do vazamento) e WIOD 2014 (cadeias globais de valor). Todos os números são reprodutíveis a partir do repositório.

---

## O ES é um "Brasil em miniatura"? Não.

**Visão convencional** — uma economia estadual que reproduz, em escala reduzida, a estrutura produtiva do país.

**Economia-plataforma** — pequena, hiperaberta, estruturada em torno de setores cuja **demanda final se realiza fora do estado**.

<br>

Três perguntas organizam a análise:

1. Para onde vai o **multiplicador capixaba** — quanto fica e quanto vaza?
2. **Para onde** vaza — quem absorve o encadeamento que escapa?
3. O **destino** desse multiplicador revela qual estágio em cadeias de valor?

Note:
A intuição comum trata um estado como "mini-país". O trabalho testa e rejeita isso para o ES. A novidade frente à versão anterior: além de "quanto vaza", respondemos "para onde vaza" (decomposição interestadual) e situamos o ES em cadeias de valor (upstreamness).

---

## Contexto — o ES em 2008

### ≈ 2,0% do produto nacional

Economia **hiperaberta**: elevado coeficiente de comércio interestadual — boa parte dos insumos e da demanda cruza a fronteira do estado.

Setores de maior peso, com **demanda final fora do estado**:

- Mineração · Metalurgia · Celulose e papel
- Refino de petróleo · Transporte e porto

Note:
O ponto não é o tamanho (2% do PIB), e sim a estrutura: pauta concentrada em setores de passagem (minério, metalurgia, celulose/papel, refino, complexo logístico-portuário). Pequeno + hiperaberto + concentrado em setores cuja demanda final está fora → tese plataforma.

---

## Dados & fontes

**Núcleo — MIP inter-regional ES × restante do Brasil (2008)**
26 setores por região (52 ao todo), R\$ milhões, contábil e balanceada, com vetor de pessoal ocupado. Regionalização (Guilhoto & Sesso Filho, 2005) + fluxos pelo método IIOAS (Haddad et al., 2017).

**Geografia — matriz interestadual das 27 UFs (2008)** → permite rastrear o *destino* do vazamento, estado a estado.

**Cadeias globais — WIOD 2014 (44 regiões, 56 setores)** → *upstreamness* (Antràs-Chor).

> **Validação cruzada.** Vazamento médio do multiplicador = <span class="stat">24,9%</span> &nbsp;converge com os **27,4%** de Haddad et al. (2017). A bi-regional e a interestadual dão a **mesma** injeção e o mesmo spillover. ✓

Note:
Matriz contábil e perfeitamente balanceada (consistência 0,00%). Acrescentamos a interestadual (27 UFs) — é o que permite o resultado novo de "para onde vaza". Credibilidade: nosso vazamento (24,9%) converge com Haddad (27,4%, outra safra); e a bi-regional e a interestadual se validam mutuamente (mesma injeção, mesmo spillover).

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
A matriz tem quatro blocos: intra na diagonal, inter fora dela. São os blocos de fora da diagonal que carregam o comércio ES↔Brasil — e que permitem, a seguir, separar spillover de feedback. f = demanda final.

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
A vantagem decisiva da inter-regional sobre a matriz isolada é separar spillover de feedback. Spillover = produção que a demanda capixaba puxa para fora; feedback = o que dessa produção retorna ao ES como insumo. É o experimento do Resultado 1.

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
**Ligações de Rasmussen-Hirschman:** para trás = média de coluna de $B$; para frente = inversa de **Ghosh**.

Note:
O multiplicador de produção é a soma de coluna da inversa. A decomposição retido/vazado é a métrica central. O multiplicador de emprego usa o coeficiente de trabalho. Detalhe técnico (auditoria): a ligação para-frente usa a inversa de Ghosh (oferta), não a de Leontief.

---

## Método II — posição em cadeias de valor

**Upstreamness** de Antràs-Chor — distância de um setor à demanda final:

$$
U=(I-G)^{-1}\mathbf{1},\qquad G_{ij}=z_{ij}/x_i
$$

$U$ alto = setor **a montante** (longe do consumo final, fornecedor de insumos). A *upstreamness* da pauta do ES pondera a $U$ setorial do Brasil (WIOD) pela composição das exportações capixabas.

Note:
G é a matriz de alocação (Ghosh), normalizada por linha. U mede quão "longe" do consumidor final um setor está. Como o ES não tem assento próprio no WIOD, inferimos via tecnologia do Brasil ponderada pela pauta capixaba — limite que declaramos.

---

## Resultado 1 — a assimetria *spillover*/*feedback*

**Experimento:** injeta-se a demanda final do ES por produtos do ES, $f^{L}$, com $f^{M}=0$.

| Fluxo | Magnitude |
|---|---|
| **Injeção** (demanda final do ES) | R\$ 51,5 bi |
| põe em movimento | R\$ 81,8 bi de produção |
| → ***Spillover*** — produção puxada no restante do Brasil | **R\$ 18,2 bi** |
| ← ***Feedback*** — o que retorna ao ES | **R\$ 164 mi · <span class="es">0,32%</span>** |

> **O estado puxa o país; o país quase não o puxa de volta.** Do total posto em movimento, **78% fica no ES** e o retorno é desprezível.

<span class="footnote">Convenção Miller-Blair reprodutível (Tipo I). A assimetria é robusta: feedback/injeção fica em 0,15–0,32% sob qualquer convenção.</span>

Note:
O número que prende a plateia. A demanda final do ES (R$51,5 bi) põe em movimento R$81,8 bi de produção: 78% fica no ES, R$18,2 bi vazam (spillover) e só R$164 mi — 0,32% — retornam (feedback). Pausa após o 0,32%. Nota de honestidade: a versão-semente reportava 60,6/22,4/0,26%, que não reproduzem na matriz; adotamos a convenção Miller-Blair reprodutível. A tese qualitativa não muda.

---

## Resultado 2 — para onde vaza: a geografia interestadual

![Destino do spillover do ES — Sankey estratificado](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_sankey.png)

> O <span class="nuc">**Sudeste (ex-ES) absorve 65%**</span> do spillover — <span class="nuc">SP 38%</span>, <span class="nuc">RJ 15%</span>, <span class="clu">MG 13%</span>. O ES alimenta seus vizinhos mais ricos.

Note:
Resultado novo e o mais "noticiável". O vazamento não se dispersa: dois terços ficam no próprio Sudeste, e mais da metade no eixo SP-RJ. O Sankey mostra a estratificação retenção → macrorregião → estado, com SP/RJ em azul (núcleo) e MG/pares em verde (cluster). O encadeamento que escapa é capturado a jusante por economias mais diversificadas.

---

## Resultado 3 — o ES num cluster de estados dinâmicos

![O ES no cluster — destino e abertura](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_cluster.png)

8 estados de crescimento acima da média, **sub-cobertos pelo mercado de capitais** (leitura da Apex Partners) — SC, PR, **ES**, MG, RS, GO, MT, MS; excluem o núcleo SP/RJ. **33,9% do PIB**.

> O ES escoa <span class="nuc">**52,5% ao núcleo SP/RJ**</span> e só <span class="clu">31,5% aos pares</span>. O elo produtivo vai ao centro; o capital não volta — **a contraparte insumo-produto da tese de sub-cobertura de capital**.

Note:
Ponte com um debate de mercado contemporâneo (Apex Partners / Faria Lima): há um cluster de estados dinâmicos sub-cobertos pelo capital, do qual o ES faz parte e que exclui justamente SP/RJ. Nosso resultado é a contraparte estrutural: o ES (e o cluster) gera encadeamento que escoa para o núcleo, com feedback ~0. O cluster é mais aberto que o núcleo (SP é o estado menos aberto do país).

---

## Resultado 4 — vazamento do multiplicador

Em média, **24,9%** (simples) — ou **22,8%** (ponderado pela produção) — do multiplicador capixaba vaza. Dispersão setorial grande:

| Setor | % do multiplicador que vaza |
|---|---|
| Serviços imobiliários *(mais retido)* | 5,3% |
| **Média ES** | **24,9% / 22,8%** |
| Alimentos *(maior vazamento)* | 37,4% |

Setores **locais / de serviço** retêm cadeia; setores de **transformação** vazam.

<span class="footnote">24,9% = média simples entre setores (comparável a Haddad); 22,8% = média ponderada pela produção (comparações entre estados).</span>

Note:
~25% do multiplicador vaza, batendo com a literatura. As duas médias: simples 24,9% (comparável a Haddad), ponderada 22,8% (usada nas comparações interestaduais) — mesma realidade, agregações distintas. Dispersão: imobiliários quase não vaza (5,3%, local/não-comercializável); alimentos vaza muito (37,4%).

---

## Resultado 5 — vazamento de emprego

Nos setores pesados, **metade ou mais** do emprego puxado pela demanda capixaba realiza-se fora do estado.

| Setor | % do emprego que vaza |
|---|---|
| Refino de petróleo | **61,6%** |
| Alimentos | 56,5% |
| Madeira e papel | 50,3% |
| Metalurgia | 49,3% |

> **Núcleo operacional** da tese: o ES movimenta a cadeia, mas o emprego associado se materializa lá fora.

Note:
O vazamento é ainda mais agudo no emprego e concentrado nos setores pesados. Metade ou mais dos postos que a demanda capixaba sustenta nesses setores ficam fora do ES.

---

## Resultado 6 — cadeias globais de valor

![Upstreamness da pauta do ES — WIOD 2014](https://raw.githubusercontent.com/fcarva/es-insumo-produto/main/pesquisa/outputs/es_upstreamness.png)

- *Upstreamness* da pauta capixaba: <span class="es">**3,12**</span> vs. Brasil **1,91** e mundo **2,31**
- Mineração no **percentil ~98** global

> O ES supre insumos primários; a **captura de valor a jusante** (manufatura, marca, serviços) ocorre fora.

Note:
A inter-regional mostra para onde vaza; a CGV mostra o porquê estrutural. ES preso a montante: upstreamness 3,12 contra 1,91 do Brasil; mineração no percentil 98 global. Recomputado do WIOD real (a versão-semente trazia 3,19/1,97 — mesma conclusão). Fornecedor de matéria-prima; o valor a jusante está fora.

---

## Síntese

O mapa do vazamento é, ao mesmo tempo, um mapa de **fragilidade** e de **oportunidade**.

**Fragilidade** — setores que apenas transitam pelo estado (mineração, refino): multiplicador e emprego vazam; o valor realiza-se fora, sobretudo no núcleo SP/RJ.

**Oportunidade** — setores que retêm multiplicador e adensam cadeia (alimentos, serviços): motores efetivos de profundidade do mercado regional.

> A análise insumo-produto operacionaliza a **"vocação local"**: distingue os setores que aprofundam a cadeia regional dos que apenas a atravessam — diagnóstico para teses de adensamento e de **mercado de capitais fora do eixo Rio–SP**.

Note:
A mesma quantidade — o vazamento — tem dupla leitura. Fragilidade: dependência de cadeias externas. Oportunidade: o mapa aponta onde adensar (setores que retêm). Elo com a agenda aplicada e com a leitura de capital do Resultado 3.

---

## Limitações & agenda

1. **Quebra estrutural** — a matriz é de 2008; Fundão (2015) alterou o peso de extração/pelotização. Fluxos interestaduais são *estimados* (IIOAS), não observados. WIOD: ES sem assento próprio → aproximação via Brasil.
2. **Dinâmica intra-ES** — o sistema das microrregiões (2015) mostra o padrão se replicando: a metrópole retém, a periferia vaza.
3. **Série longitudinal 2000 × 2014** — o ES subiu ou desceu na cadeia no boom de commodities? (exige harmonização ISIC + deflação).
4. **MRIO mundial** — destino internacional do valor e do emprego embutidos nas exportações.

Note:
Escopo congelado em 2008 + WIOD 2014 (fotografia transversal). Limitações viram programa: intra-ES (já testado, padrão se replica), série 2000-2014 (capítulo à parte), MRIO mundial. Se perguntarem "por que 2008": é a vintage da matriz inter-regional balanceada disponível, defendida pela inércia estrutural das cadeias de base.

---

<!-- .slide: class="center" -->

## Obrigado

**O ES não é um mini-Brasil — é a plataforma exportadora do país.**

<br>

<span class="footnote">Código, dados e PDF reprodutíveis · github.com/fcarva/es-insumo-produto</span>

<span class="footnote">Isard (1951) · Miller & Blair (2009) · Rasmussen (1956) · Guilhoto & Sesso Filho (2005) · Haddad et al. (2017) · Antràs et al. (2012) · Timmer et al. (WIOD) · Dietzenbacher & Lahr (2013)</span>

Note:
Frase-síntese e abertura para perguntas. Prováveis: (i) por que 2008; (ii) por que os números mudaram da versão anterior — auditoria/reprodutibilidade, convergência com Haddad; (iii) implicação de política — adensar setores que retêm cadeia e a leitura de sub-cobertura de capital. Todo o pipeline é reprodutível no repositório. Obrigado.
