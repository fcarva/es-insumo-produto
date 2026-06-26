# Auditoria — *O Espírito Santo como economia-plataforma*

Trilho de auditoria da Fase B (disciplina Prof. Celso Bissoli Sessa, PPGEco/UFES).

## B1 — Contábil / numérica / reprodutibilidade
- MIP-ES-BR balanceada: consistência VBP × soma de linha = **0,00%**.
- Coeficientes válidos: $\Sigma A_{\cdot j}<1$ em todas as matrizes; $B=(I-A)^{-1}\ge 0$.
- Pipeline reprodutível: `01`–`11` rodam do zero (Python 3.13 + numpy/pandas/openpyxl/matplotlib)
  e reproduzem os números reportados. Dados de terceiros **não** versionados (`Material IO/`).
- Cross-validação: a injeção f^ES (R\$ 51,5 bi) e o spillover (R\$ 18,2 bi) batem entre a
  matriz bi-regional (`01`) e a interestadual (`02`) — são a mesma economia em dois recortes.

## B2 — Metodológica
- Notação idêntica a Miller & Blair (2009): partição de $A$ e da inversa de Leontief $L$ em
  $LL/LM/ML/MM$; \emph{spillover}/\emph{feedback} de Isard (Eq. 2 do paper).
- Ligações de Rasmussen-Hirschman: **para trás** pela inversa de Leontief, **para frente** pela
  inversa de Ghosh (corrigido em B4).
- \emph{Upstreamness} de Antràs-Chor (2012), $U=(I-G)^{-1}\mathbf 1$, com $G$ normalizada por linha.
- Âncoras: Haddad et al. (2017) e Guilhoto & Sesso Filho (2005) para o método regional brasileiro.

## B3 — Limites (declarados no paper, §6)
1. **Quebra estrutural:** matriz de 2008; rompimento de Fundão (2015) alterou o peso da
   extração/pelotização — valores nominais defasados.
2. **Fluxos estimados:** inter-regionais/interestaduais por IIOAS (gravitacional), não observados.
3. **Aproximação WIOD:** o ES não tem assento próprio; \emph{upstreamness} via tecnologia do
   Brasil ponderada pela pauta capixaba (viés declarado). Concordância 26→56 aproximada.
4. **Defesa:** inércia estrutural das cadeias de base legitima a fotografia 2008/2014.

## B4 — Revisão de código (`/code-review`, 3 revisores)
**Resultado:** nenhum bug corrompe número reportado no paper; a matemática-núcleo foi
confirmada correta e bate com os alvos. Corrigido:
- ligação para-frente passou a usar a inversa de **Ghosh** (era Leontief);
- **de-hardcode** do Sankey (lê `es_spill_total_mi`/`es_retido_mi` do CSV; rótulo derivado);
- guarda `x<=0` + `assert` $\Sigma A<1$ no cluster; remoção de variável morta.

*Endurecimento aplicado:* de-hardcode de Brasil/Mundo na Fig. 4 (lê `upstream_resumo.csv`);
checagem de identidade contábil do WIOD — **49/2464 setores (2%)** têm demanda final implícita
< 0 (estoques/discrepância), mas $U$ permanece finito e $\ge 1$ e a média do Brasil (1,91) e a
mineração (p97,7) não são afetadas. A concordância de setor único segue caveatada em §6 — sem
efeito sobre os resultados publicados.

## B5 — Checklist de *referee*
| Critério | Avaliação |
|---|---|
| Pergunta de pesquisa clara | ✅ três perguntas explícitas (§1) |
| Identificação/método sólido | ✅ Isard/Miller-Blair, notação padrão |
| Reprodutibilidade | ✅ scripts reproduzem todos os números |
| Robustez | ✅ assimetria \emph{feedback}≈0 invariante à convenção (0,15–0,32%); cross-validação bi-regional × interestadual |
| Contribuição vs literatura | ✅ decomposição do **destino** interestadual do vazamento + ponte com o cluster |
| Honestidade dos limites | ✅ §6 frontal (Fundão, IIOAS, WIOD, inércia) |
| Risco residual | os 60,6/22,4/0,199 do paper-semente não reproduzem → adotada convenção Miller-Blair (V3), reprodutível |

**Veredito:** metodologicamente defensável e reprodutível; pronto para a entrega da disciplina.

## B6 — Auditoria de conteúdo (revisão cruzada do manuscrito)
Cruzamento independente de números, fórmulas e literatura confirmou: destino 65,4% (SP+RJ+MG),
split do cluster fechando 100%, Sankey (R\$ 18,1 ≈ 18,2 bi) e *upstreamness* 3,12; e o
equacionamento (Isard/Miller-Blair, \emph{feedback}, Antràs-Chor). **Único ajuste:** conciliar
**24,9%** (média simples entre setores, §4.1, comparável a Haddad) com **22,8%** (média
ponderada pela produção, Tab.~3/Fig.~3) — resolvido por nota de rodapé na §4.1.

## B7 — Verificação de integridade das referências (jun/2026, via `academic-pipeline`/`integrity_verification_agent`)
Aplicado manualmente o protocolo de verificação de referências (Fase A — existência e exatidão
bibliográfica) da skill `academic-pipeline` às 6 entradas de `paper/es_insumo_produto.tex`
(WebSearch item a item; WebFetch para texto completo bloqueado neste ambiente — ver nota abaixo).

| Referência | Veredito | Observação |
|---|---|---|
| Antràs et al. (2012), *AER* 102(3) | **VERIFIED** | Título, autores, volume/páginas conferem exatamente. |
| Guilhoto \& Sesso Filho (2005), *Economia Aplicada* 9(2) | **VERIFIED** | Idem. |
| Isard (1951), *Rev. Econ. Stat.* 33(4) | **VERIFIED** | Idem. |
| Miller \& Blair (2009), Cambridge UP, 2ª ed. | **VERIFIED** | ISBN 9780521517133 confirmado. |
| Timmer et al. (2015), *Rev. Int. Econ.* 23(3) | **CORRIGIDO (MEDIUM)** | Bibitem omitia o subtítulo "the case of global automotive production" — completado. |
| **Haddad et al. (2017)** | **CORRIGIDO (SERIOUS — mismatch)** | Bibitem citava título e veículo incorretos: "Matriz inter-regional de insumo-produto para o **Espírito Santo**: método IIOAS" / "Working paper". O artigo real é **"Matriz interestadual de insumo-produto para o Brasil: uma aplicação do método IIOAS"**, publicado em *Revista Brasileira de Estudos Regionais e Urbanos*, 11(4), 424–446 (também circula como TD NEREUS 02/2017) — é a matriz dos **27 estados**, não uma matriz dedicada ao ES. Autores e ano estavam corretos; título e veículo, não. Corrigido em `paper/es_insumo_produto.tex`. |

**Limite desta rodada (Fase E — verificação de claims, não concluída):** o paper cita "os 27,4%
estimados por \citet{haddad2017iioas}" (§4.1) como comparador para o vazamento médio simples do
ES (24,9%). Não foi possível confirmar esse número específico contra o texto/tabelas originais
de Haddad et al. (2017): `WebFetch` está bloqueado para URLs arbitrárias neste ambiente (403 em
todos os domínios testados, incluindo Wikipedia — política de proxy, não falha pontual), e
`WebSearch` só retorna resumos/abstracts, não o conteúdo de tabelas internas do PDF. Veredito:
**UNVERIFIABLE_ACCESS** (não confundir com erro confirmado) — recomenda-se que quem tiver acesso
direto ao PDF (NEREUS TD 02/2017) confirme manualmente o número antes da próxima rodada de
auditoria "hard mode".

*Corroboração parcial (direção, não magnitude):* o abstract do artigo — recuperado por WebSearch —
afirma que **Amazonas, Espírito Santo e Mato Grosso** são os estados cuja produção local é **mais
influenciada pela demanda final de outros estados e do exterior** (e que SP/RJ são os mais
autossuficientes). Isso é qualitativamente consistente com o vazamento alto do ES no nosso paper e
torna os 27,4% plausíveis em direção; a magnitude exata, porém, segue não confirmada (está nas
tabelas internas do PDF, fora do alcance de WebSearch).
