# Deep research — extensão CARBONO-PLATAFORMA (insumo-produto ambientalmente estendido)

*Pipeline `academic-pipeline` · **Stage 1 RESEARCH** (modo agenda) · idioma PT-BR · data: 2026-06-26.
Objetivo: estimar quanto **CO₂ incorporado** o ES "exporta" junto com seu encadeamento — a face
ambiental da economia-plataforma. Pipeline reprodutível: `pesquisa/23_carbono_plataforma.py`.*

> **Integridade primeiro.** Este dossiê escopa o método, o dado e a literatura, e entrega um pipeline
> **pronto para rodar**. Ele **não produz número de emissão sem dado real** — `23_*` exige um vetor de
> CO₂ verificável (SEEG / Haddad et al. 2025 / IBGE) e **para** se ele não existir. Nenhuma estimativa
> de carbono é reportada até que o vetor seja fornecido.

---

## 0. A tese (face ambiental da plataforma)

A caracterização mostrou que o ES é uma **economia de base, a montante**, que vaza encadeamento ao
núcleo com retorno ≈ 0. A extensão natural: o ES não exporta só **valor adicionado**, mas **carbono
incorporado** — mineração/pelotização, siderurgia, refino e celulose são intensivos em CO₂. A pergunta:
**quanto de CO₂ está embutido na produção/pauta capixaba, e quanto "vaza"** (é emitido para servir
demanda de fora)? É o análogo ambiental do vazamento do multiplicador.

---

## 1. Método — insumo-produto ambientalmente estendido (EEIO)

Padrão de Miller & Blair (2009, cap. de extensões ambientais), na linha de \[Leontief 1970]:
- **Intensidade direta:** $f_i = \mathrm{CO_2}_i / x_i$ (tCO₂ por R\$ de produção do setor $i$).
- **Multiplicador de carbono:** $m = f'(I-A)^{-1} = f'B$ → tCO₂ por R\$ de demanda final (direto+indireto).
- **CO₂ incorporado** na demanda final $y$: $E = f'B\,y$.
- **Vazamento de carbono** (analogia do vazamento do multiplicador): parcela de $m_j$ **emitida fora do
  ES** — soma sobre as linhas do RB de $f\!\cdot\!B$. Mede quanto da pegada da demanda capixaba se
  realiza em emissões de outras regiões.
- **Carbono da pauta** (analogia da *upstreamness*): $\sum_j w^{\text{exp}}_j m_j$, com $w^{\text{exp}}$
  = composição das exportações do ES. Quanto de CO₂ por R\$ exportado.
- **Produção vs. consumo:** CO₂ emitido NO ES (*production-based*) × CO₂ embutido no consumo final do ES
  (*consumption-based*); a diferença é o **carbono líquido exportado** — o cerne da tese.

**Hipótese declarada:** tecnologia de emissão **nacional** aplicada a ES e RB (mesma simplificação da
camada CGV/upstreamness). Refinável com intensidades **estaduais** (Haddad 2025 / SEEG-UF).

---

## 2. Dados — fontes do vetor de CO₂ (ranqueadas por aderência)

| Fonte | O que dá | Aderência | Acesso |
|---|---|---|---|
| **Haddad et al. (2025)** — satélite de CO₂ da MIIP 2019 | CO₂ por **68 setores × 27 UFs** (ES!), 2019 | ★★★ (alinhado à IO, ES-específico, recente) | dados suplementares na **RBERU** (baixar) |
| **SEEG** (Observatório do Clima) | emissões por **atividade econômica × UF** (ES), série anual | ★★ (precisa mapear p/ setores IO) | `plataforma.seeg.eco.br` (download por atividade) |
| **IBGE — Contas Econômicas Ambientais (emissões atmosféricas)** | CO₂ por atividade, alinhado às Contas Nacionais | ★★ (experimental/parcial) | IBGE (SIDRA / estudos ambientais) |
| **Carvalho & Perobelli (2009)** | coeficientes de CO₂ setoriais publicados (parcial, 2009) | ★ (poucos setores, antigo) | artigo (SciELO) |

**Recomendação:** começar pelo **satélite de Haddad et al. (2025)** — é o mais aderente (68 setores, ES,
2019, mesma família IIOAS da nossa interestadual) — e validar com **SEEG-ES**. O vetor entra em
`dados/co2_intensidade.csv` (26 linhas, ordem dos setores do ES; ver `23_*` para o template exato).

> **Contexto (não-IO, para a introdução):** o ES concentra a maior pelotização do mundo (Vale, ~28 Mt/ano)
> e a usina de Tubarão (ArcelorMittal, ~7,5 Mt/ano de aço) — setores entre os mais intensivos em CO₂ do
> país (mineração+siderurgia ≈ 107 Mt CO₂/ano no Brasil). Há, ademais, um debate de **mercado regulado
> de carbono** no ES — implicação de política direta.

---

## 3. Literatura (verificada / a verificar)

- **Carvalho, T. S. & Perobelli, F. S. (2009).** *Avaliação da intensidade de emissões de CO₂ setoriais
  e na estrutura de exportações: um modelo inter-regional SP/restante do Brasil.* Econ. Aplicada 13(1),
  99–124. → **molde exato** (IO inter-regional + CO₂ + pauta exportadora). Já no acervo.
- **Yamano, N. & Guilhoto, J. J. M. (2020).** *CO₂ emissions embodied in international trade…, OECD ICIO.*
  → contabilidade consumo vs. produção; "outsourcing" de emissões. Já no acervo.
- **Haddad et al. (2025)** — a MIIP 2019 **com satélite de CO₂/energia/água** → o dado e o método-irmão.
- *(substrato)* Miller & Blair (2009, extensões ambientais); Leontief (1970, environmental repercussions)
  — a verificar para citação formal.

---

## 4. O pipeline (pronto) e o passo de dado

`pesquisa/23_carbono_plataforma.py`:
1. Carrega a MIP-ES-BR 2008 (Z, demanda final, VBP) — reusa o parser validado.
2. Lê `dados/co2_intensidade.csv` (vetor de intensidade direta por setor). **Se ausente, PARA** e imprime
   a especificação + a ordem dos 26 setores (sem inventar dado).
3. Computa: multiplicador de carbono por setor, **vazamento de carbono**, **carbono da pauta**, CO₂
   *production-based* e *consumption-based*. Salva `outputs/carbono_plataforma.csv`.

**Para obter os números reais (1 passo de dado):** baixar o satélite de CO₂ (Haddad 2025 suplementar
**ou** SEEG-ES por atividade), agregar aos 26 setores e salvar como `dados/co2_intensidade.csv`. O
pipeline roda em segundos e devolve a bateria de carbono.

---

## 5. Contribuição esperada e limites

**Contribuição:** fecha o arco da tese — a economia-plataforma exporta **valor a montante E carbono
incorporado**; conecta o diagnóstico estrutural à pauta climática (transição justa, royalties-carbono,
mercado regulado capixaba). Original na escala estadual capixaba.

**Limites honestos:** (i) tecnologia de emissão **nacional** (não estadual) na 1ª passada — refinável;
(ii) safra do CO₂ (2019/Haddad ou série SEEG) ≠ safra da MIP-ES-BR (2008) → ponte temporal declarada,
ou rodar sobre a MIIP 2019 quando disponível; (iii) escopo de gases (CO₂ vs CO₂e/GEE — fixar);
(iv) só emissões **operacionais** dos setores (não ciclo de vida).

## 6. Próximo passo
Obter o vetor de CO₂ (Haddad 2025 / SEEG-ES) → `dados/co2_intensidade.csv` → rodar `23_*` → integrar a
bateria de carbono como **§ agenda ambiental** do artigo (ou nota de pesquisa autônoma). Eu computo e
redijo assim que o vetor estiver disponível.
