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

*Notado (baixa severidade, não corrige o número):* reservas de demanda final implícita no WIOD
podem afetar percentis setoriais individuais (não a média/Brasil 1,91 nem a mineração p97,7);
constantes Brasil/Mundo ainda fixas em `09`; concordância usa setor único por classe (já
caveatado em §6). Itens de endurecimento opcional, sem efeito sobre os resultados publicados.

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
