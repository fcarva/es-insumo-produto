# REVIEW FULL MODE — V4 (base: alterações do autor, 21/07/2026)

Auditoria no fluxo full mode (revisão multi-perspectiva + gate de integridade) sobre a
versão enviada pelo autor via Overleaf (zip de 21/07), adotada como **base da entrega
final**. Espelhos auditados: `overleaf/main.tex` (ABNT) e `paper/es_estrutura_produtiva.tex`
(autor-data), corpo idêntico.

## 1. O que o autor alterou (aceito integralmente)

- Terminologia: "vocação territorial" → **"composição territorial da indústria"**
  (subtítulo, §6, parágrafo de método e menções associadas).
- Identificação: ORCID real (0009-0008-8578-9018) e e-mail institucional
  (`felipe.c.santos@edu.ufes.br`) — resolve a pendência da V3.
- Fluidez de prosa: "escola" → "literatura", "perrouxiana" → "de Perroux",
  "tieboutiana" → "de Tiebout", quebras de parágrafo na introdução, resumo enxugado
  (remoção da cláusula final "mecânica comum às pequenas economias...").

## 2. Não-conformidades encontradas e correções aplicadas

| # | Achado | Gravidade | Ação |
|---|---|---|---|
| 1 | **Abstract em inglês removido** na edição. A especificação do Trabalho Final pede "Resumo/Abstract" e a ABNT NBR 6022:2018 exige resumo em língua estrangeira em artigo científico. | Alta (spec) | Restaurado, sincronizado com o resumo PT editado (sem a cláusula final, travessões→vírgulas na lista de setores). Reverter se a remoção foi intencional. |
| 2 | Terminologia residual: "mosaico de vocações" (§6, Discussão, Conclusão), "periferias vocacionadas", "vocações territoriais" (legenda da Fig. 3) conviviam com a nova "composição territorial". | Média (consistência) | Harmonizado para "especializações"/"periferias especializadas". Rótulo interno `fig:vocacao` mantido (não aparece no PDF). |
| 3 | Discussão prescritiva ("Três alavancas", "**Apostar na celulose**") — em desacordo com o caráter descritivo declarado na introdução ("A contribuição não é testar uma hipótese...") e com o pedido do autor. | Alta (pedido do autor) | Reescrita como **caracterização estrutural** (ver §3). |
| 4 | Ponteiro para o Apêndice B removido da abertura da metodologia (edição do autor). Apêndice B continua existindo e referenciado nos apêndices/limitações. | Baixa | Mantido como o autor deixou. |

## 3. Reescrita da Discussão (caracterização estrutural)

O bloco "(i) Adensar a jusante / (ii) Apostar na celulose / (iii) Diversificar com
endereço territorial + royalties" foi substituído por uma caracterização do problema
estrutural, em diálogo com a literatura que extrai conclusões **diferentes** de um
receituário setorial:

- **Cano (1985; 2008)**: a especialização periférica não é falha de política local
  corrigível por seleção de setores; é o modo de integração do território à acumulação
  comandada pelo núcleo.
- **Macedo (2002)** — tese IE-Unicamp orientada por Wilson Cano sobre o caso capixaba
  (1960–2000): a industrialização de base foi decidida de fora (grandes projetos
  federais-exportadores), instalando no ES a ponta a montante de cadeias cuja jusante
  ficou no núcleo/exterior.
- **Caçador & Grassi (2009)**, REN 40(3): crescimento acima da média nacional com base
  científico-tecnológica periférica — crescimento sem mudança estrutural.

Os números do artigo (ligações puras 4,4/3,4; spillover 65% ao Sudeste; feedback 0,32%;
retenção 90,9% vs 66,2%; extração hipotética −13,0%) são relidos como a *mecânica* que
torna o adensamento localmente improvável, não como oportunidades à espera de política.
A trajetória da celulose (1,41→1,51) vira "dado de um setor, não refutação do desenho".
Os royalties permanecem, reenquadrados como característica estrutural (captura pelo
circuito fiscal, não interindustrial), fechando com "não se trata de recomendação, e sim
de caracterização".

## 4. Verificação das novas referências (fontes)

- Macedo, F. C. de (2002). *Integração e dinâmica regional: o caso capixaba (1960–2000)*.
  Tese (Doutorado) — IE-Unicamp, orient. Wilson Cano. [Escavador/Lattes; portal Unicamp]
- Cano, W. (2008). *Desconcentração produtiva regional do Brasil: 1970–2005*. São Paulo:
  Editora Unesp. [catálogo Editora Unesp, ISBN 9788571398313]
- Caçador, S. B.; Grassi, R. A. (2009). Olhar crítico sobre o desempenho recente da
  economia capixaba... *Revista Econômica do Nordeste*, 40(3), 453–480. [portal REN/BNB]

Total: 43 referências (40 da V3 + 3 novas), listas ABNT e autor-data sincronizadas.

## 5. Estado pós-auditoria

- Compilação: 0 erros, 0 citações/referências pendentes nos dois espelhos.
- **20 páginas** (limite 15–20 da especificação, incluindo apêndices) nas duas versões.
- Resumo PT: ~180 palavras (limite 250), com objetivo/metodologia/resultados/contribuição.
- Estrutura: Introdução; Revisão de literatura; Metodologia (dados + instrumentos);
  resultados (§4–§7); Discussão; Limitações; Conclusão; Apêndices; Referências. ✔ spec.

## 6. Pendências (decisão do autor)

1. Confirmar a manutenção do abstract EN restaurado (item 2.1).
2. Especificação pede script "R ou Excel" — o pipeline é Python (`pesquisa/`);
   confirmar aceitação com o professor.
3. Data de entrega: 24/07/2026.
