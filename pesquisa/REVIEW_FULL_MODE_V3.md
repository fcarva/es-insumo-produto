# Peer Review (full mode) — Rodada 4: versão pós-rodada editorial

*Skill `academic-paper-reviewer` v1.10.0 (github.com/imbad0202/academic-research-skills), modo
**full** (EIC + R1/R2/R3 + Devil's Advocate → síntese editorial). Manuscrito:
`paper/es_estrutura_produtiva.tex` @ commit `b59ada1` (21 págs., 43 refs., resumo 181 palavras +
abstract EN, §2 "Quadro analítico", 6 figuras vetoriais). Rodadas anteriores:
`REVIEW_FULL_MODE.md` (v1), `REVIEW_CARACTERIZACAO.md` + `REVIEW_FULL_MODE_V2.md` (v3,
Minor→Accept condicional), `REVIEW_THEORIST_TOOLBOX.md` (apêndices; resta F1). Idioma: PT.
Data: 2026-07-17.*

*Regras de ferro observadas: (i) os 5 pareceristas avaliaram de forma independente, sem
cruzar relatórios; (ii) a síntese só consolida o que está nos relatórios da Fase 1; (iii) os
revisores NÃO editaram o manuscrito — este documento é o único produto da rodada; (iv) achado
CRITICAL do Devil's Advocate impede decisão Accept.*

---

## Fase 0 — Análise de campo e configuração do painel

| Item | Diagnóstico |
|---|---|
| Disciplina primária | Economia regional / análise de insumo-produto |
| Disciplina secundária | Teoria do desenvolvimento regional (base de exportação, polos, centro-periferia) |
| Paradigma | Estrutural-descritivo (caracterização; sem pretensão causal — declarado) |
| Método | Bateria IO completa + benchmark interestadual + modelo nulo + HEM |
| Periódico-alvo | RBERU (Qualis A4–B1); pacote de submissão pronto (`SUBMISSAO_RBERU.md`) |
| Maturidade | Alta: 3 rodadas de parecer + rodada editorial aplicada; pendência única herdada (F1) |

**Painel:** EIC — editor de ciência regional brasileira (perfil RBERU), foco em adequação ao
periódico e prontidão de submissão · **R1 Metodologia** — economista de insumo-produto, foco em
cadeia número→artefato, consistência figura↔texto↔apêndice · **R2 Domínio** — economista
regional, foco na nova §2 (quadro analítico) e na moldura de literatura · **R3 Perspectiva** —
geografia econômica/política pública, foco na leitura de política da Discussão · **Devil's
Advocate** — desafia o argumento central ("especificidade composicional") e a promessa de
reprodutibilidade.

---

## Fase 1 — Pareceres independentes

### Parecer EIC (editor-chefe)

**Recomendação:** Minor Revision (banda superior) · **Confiança:** 5/5

**Síntese.** O manuscrito caracteriza a estrutura produtiva do ES com três sistemas IO e uma
bateria completa, agora organizada por um quadro analítico explícito (§2) que conversa
diretamente com o repertório desta revista (5 referências RBERU, incluindo o precedente
catarinense recém-incorporado). A primeira página está finalmente pronta para submissão: resumo
de 181 palavras + título/abstract/keywords em inglês. A qualidade editorial subiu de forma
visível (figuras vetoriais com legenda única e vírgula decimal; hifenização PT correta). Restam
retoques de idioma no abstract EN e a pendência reprodutível herdada (F1), que segue fora do
manuscrito e nas mãos do autor.

**Forças.** S1: encaixe de gênero e de casa — a conversa com Haddad et al. (2017; 2025), Sesso
Filho & Guilhoto (2010), Ribeiro et al. (2024) e Bittencourt et al. (2023) é a conversa da
própria revista. S2: primeira página autossuficiente (resumo enxuto + abstract EN) — condição
de mesa de submissão cumprida. S3: §2 dá ao leitor da revista o mapa lente→instrumento que o
gênero raramente explicita.

**Fraquezas.**
- **W-EIC-1 (MINOR, abstract EN):** "extraction operates as an *enclave*, while manufacturing
  emerges as key sector**s**" — concordância quebrada (sujeito singular, predicativo plural).
  *Fix:* "…while manufacturing concentrates the key sectors" (ou equivalente).
- **W-EIC-2 (observação, fora do manuscrito):** conferência final das normas RBERU
  (template/citação/limites) permanece a fazer no ato da submissão — site da revista
  inacessível deste ambiente; item já registrado no checklist.

### Parecer R1 (metodologia e reprodutibilidade)

**Recomendação:** Minor Revision · **Confiança:** 5/5

**Síntese.** A cadeia número→artefato saiu mais forte da rodada editorial: as 6 figuras agora
regeneram de CSVs versionados por scripts portáveis, com PDF vetorial e conferência
figura↔texto↔CSV registrada (celulose 1,41→1,51; spillover 18,1/37,8/52,5/65,4; 8
setores-chave). A conciliação 18,1 (interestadual) × 18,2 (bi-regional) foi a decisão certa —
mas a legenda aponta para um apêndice que ainda não a contém. A pendência F1 (CSVs das Tabelas
2 e 5) segue aberta e continua sendo o único bloqueio a um APPROVE pleno, nos termos já
acordados na rodada theorist-toolbox.

**Forças.** S1: reprodutibilidade das figuras fechada (antes: caminho `C:/Users/DELL/...` em 7
scripts; figura Sankey em convenção antiga divergindo do texto). S2: compilação limpa (0 refs
indefinidas, 0 overfull) com babel/microtype. S3: convenção decimal unificada (vírgula) entre
texto, tabelas e figuras.

**Fraquezas.**
- **W-R1-1 (MAJOR, legenda da Figura 4 × Apêndice B.3):** a legenda diz que a diferença
  18,1/18,2 bi "é de agregação (Apêndice B.3)", mas o B.3 (`ap:medias`) concilia apenas as
  médias de **vazamento** (24,9/22,9/22,8/27,4%) — o total transbordado não está lá. Remissão
  quebrada em conteúdo, não em `\ref`. *Fix (1 frase):* acrescentar ao B.3 a conciliação do
  transbordamento total (18,2 bi bi-regional × 18,1 bi interestadual, mesma injeção), ou
  remover a remissão da legenda.
- **W-R1-2 (MINOR, convenção de fonte nas legendas):** as legendas de figura citam ora o script
  *da figura* (Figs. 1, 3, 4, 6: `19_*`, `21_*`, `11_*`, `09_*`), ora o script *do dado*
  (Fig. 2: `18_*`; Fig. 5: `14_*`/`15_*`); as tabelas citam sempre o script do dado. *Fix:*
  padronizar as figuras na convenção das tabelas (script gerador do dado sobre o CSV), que é a
  que rastreia o número à origem.
- **W-R1-3 (BLOCKING herdado, fora do manuscrito = F1):** `decomposicao_fd.csv` e
  `micro_multiplicadores.csv` seguem ausentes do repositório; Tabelas 2 e 5 não são
  reproduzíveis da origem. Compromisso vigente: APPROVE automático quando os CSVs chegarem com
  asserts `[OK]` (`fechar_R1.bat`).

### Parecer R2 (domínio e literatura)

**Recomendação:** Minor Revision · **Confiança:** 4/5

**Síntese.** A nova §2 resolve a dispersão teórica apontada em rodadas anteriores: as três
lentes (North/Tiebout; Perroux/Hirschman/Rasmussen; Isard/Miller/Miyazawa + Cano/Friedmann)
aparecem uma única vez, com tabela-síntese lente→instrumento→resultado, e o corpo passa a
remeter em vez de reexpor — a Discussão colhe o que a §2 planta. Richardson (1985) é exatamente
a ponte que faltava entre base econômica e multiplicadores IO. Dois reparos de precisão
bibliográfica.

**Forças.** S1: §2 com a tabela-síntese é a contribuição didática do artigo ao gênero. S2: o
parágrafo do gênero agora cobre MG→MT→RS→PA→SC + o recorte multiestadual (NE) e o
intra-estadual (municípios SP). S3: bloco de incerteza da regionalização restaurado (FLQ 2016;
CHARM 2015; gravitacional 2006) em §3 e §10 — responde a cobrança antiga (R2 da rodada 1, v1).

**Fraquezas.**
- **W-R2-1 (MAJOR, claim bibliográfico não demonstrado):** §2 fecha afirmando que benchmark
  interestadual e modelo nulo são "dois instrumentos de aferição **que o gênero raramente
  emprega**" — afirmação sobre a frequência na literatura sem levantamento que a sustente.
  *Fix:* remover a alegação de raridade e dizer apenas o que os instrumentos fazem (separar
  regularidade do método × específico do estado).
- **W-R2-2 (MINOR, enquadramento de Bittencourt et al. 2023):** o estudo catarinense lê a
  *indústria* por intensidade tecnológica sobre a MIP-SC 2018; listá-lo como elo direto da
  sequência "estrutura produtiva de [estado]" estica o gênero. *Fix:* reformular para "e, em
  Santa Catarina, a leitura da indústria estadual sobre a MIP de 2018".
- **W-R2-3 (observação):** a tabela da §2 antecipa números de resultados (61,7%; 90,9/66,2;
  −13%) antes das seções que os derivam — aceitável porque a coluna se chama "onde o artigo
  mede", mas o autor deve estar ciente de que há editor que pedirá a tabela sem números.

### Parecer R3 (perspectiva: geografia econômica e política)

**Recomendação:** Accept com retoque · **Confiança:** 4/5

**Síntese.** A leitura de política é o ponto alto da Discussão: três alavancas derivadas do
próprio dado (adensar a jusante da base mineral; celulose como ramo de trajetória favorável;
diversificação com endereço territorial), fechadas pela releitura dos royalties como mecanismo
central de captura de valor — argumento raro no gênero, que costuma parar nos multiplicadores.
O endereçamento sub-estadual (metrópole × periferias vocacionadas) dá tração prática ao mapa de
LQ. Único reparo: a condicionalidade temporal das alavancas está declarada longe delas.

**Forças.** S1: royalties como política estrutural amarrada ao modelo nulo (retorno via
encadeamento limitado pelo porte → captura fiscal como canal restante) — síntese original.
S2: alavanca (iii) conecta LQ→extração hipotética→mitigação de risco de mono-dependência.
S3: agenda ambiental (carbono-plataforma) declarada com aparato pronto.

**Fraquezas.**
- **W-R3-1 (MINOR, condicionalidade temporal):** as alavancas derivam do retrato de 2008 + pano
  de fundo nacional 2010–2021; a ressalva de safra existe, mas está só em §10 (Limitações).
  *Fix (meia frase):* condicionar na própria abertura das alavancas ("condicionais às safras
  das âncoras — §10").

### Parecer Devil's Advocate

**Contra-argumento mais forte (síntese).** "A tese final — 'a especificidade capixaba é
composicional' — depende da régua que mede composição. A classificação base/*commodity* inclui
Alimentos, o que infla a parcela de base dos concorrentes agrícolas e pode mover o ES no
ranking em que ele é '2º mais intensivo em base'. O artigo declara a escolha e registra a
reestimação como checagem de replicação (nota da Tabela 4), e protege o claim com o traço que
independe do rótulo (setor dominante mineral — só ES, PA, RJ); ainda assim, o número-manchete
'36,4%; 2º' viaja no resumo e na conclusão sem a régua junto. Não invalida o retrato — mas o
leitor apressado levará o ranking sem a nota."

**Issues.**
- **DA-1 (MAJOR, sensibilidade da régua composicional):** o ranking "2º em base (36,4%)" é
  sensível à inclusão de Alimentos no rótulo; a defesa existe (nota da Tabela 4 + setor
  dominante), mas a reestimação declarada nunca foi executada. *Mitigação atual:* claim
  protegido pelo traço rótulo-independente. *Fix mínimo:* nenhum no texto; executar a checagem
  `22_*/10_*` quando o dado bruto estiver disponível (mesmo evento de F1). *Não-CRITICAL*
  porque a fragilidade está declarada no próprio manuscrito.
- **DA-2 (CRITICAL condicional, herdado = F1):** o manuscrito vende "retrato sistemático — e
  reprodutível" (§1) e "rotinas reprodutíveis" (§3) enquanto 2 das 6 tabelas não têm CSV no
  repositório. Enquanto F1 estiver aberto, a promessa central de método está parcialmente
  descoberta → **decisão não pode ser Accept** (regra de ferro #4). Fecha-se sozinho com
  `fechar_R1.bat`.
- **DA-3 (observação, não-defeito):** "escalas aninhadas" com $R^2=0{,}91$ sobre $n=10$ é
  sugestivo, não inferencial — o texto já o declara (Apêndice A.8 e §10); manter a disciplina
  de linguagem nas futuras reescritas.

**Caminhos alternativos ignorados:** nenhum material novo — as alternativas (deflação da série,
âncora 2019, carbono) já estão declaradas como agenda. **Stakeholders ausentes:** trabalho/
sindicatos e finanças municipais aparecem só de passagem; aceitável no escopo descritivo.
**Teste "e daí?":** passa — as três alavancas + royalties respondem.

---

## Fase 2 — Síntese editorial

### Quadro de recomendações

| Revisor | Recomendação | Confiança |
|---|---|---|
| EIC | Minor (banda superior) | 5 |
| R1 Metodologia | Minor | 5 |
| R2 Domínio | Minor | 4 |
| R3 Perspectiva | Accept com retoque | 4 |
| Devil's Advocate | Minor (CRITICAL condicional em F1) | 5 |

**Escores (rubrica 0–100, média ponderada do painel):** originalidade 76 · rigor metodológico
80 · suficiência de evidência 78 · literatura 82 · clareza 84 · contribuição 78 · reporte 82 →
**ponderado ≈ 79** (faixa 65–79 = Minor Revision; teto imposto também pela regra de ferro #4
enquanto F1 estiver aberto).

### Consenso

- **[CONSENSUS-5]** A rodada editorial elevou a prontidão de submissão (1ª página completa,
  figuras reprodutíveis, quadro analítico) sem alterar números auditados.
- **[CONSENSUS-4]** (silente: R3) Restam apenas retoques textuais pontuais; nenhum problema
  novo de método ou de dado foi introduzido pela rodada editorial.
- **[CONSENSUS-5]** F1 segue sendo a única pendência estrutural; está fora do manuscrito e já
  tem mecanismo pronto (`fechar_R1.bat`).

### Divergências e arbitragem

- **Severidade de W-R2-1 ("raramente emprega"):** R2 classifica MAJOR (claim bibliográfico sem
  levantamento); EIC leria como estilo. *Arbitragem:* acolher R2 pelo princípio conservador —
  o custo do fix é uma frase; o custo de manter é um flanco em parecer real.
- **DA-1 × R1:** R1 não listou a sensibilidade da régua (foco em cadeia de artefato); DA sim.
  *Arbitragem:* mantém-se como está no manuscrito (declarada + protegida) e registra-se a
  execução da checagem no mesmo evento de F1. Sem mudança de texto.

### Decisão editorial

**MINOR REVISION (banda superior) → Accept condicional**, mantendo o compromisso das rodadas
anteriores: **APPROVE automático quando F1 fechar** (CSVs com asserts `[OK]`). Os itens desta
rodada são todos de execução imediata e nenhum exige re-review de painel; verificação por
re-review documental basta.

### Revision Roadmap (priorizado)

| # | Origem | Item | Esforço |
|---|---|---|---|
| 1 | W-R1-1 | Apêndice B.3: acrescentar a conciliação do transbordamento total (18,2 bi bi-regional × 18,1 bi interestadual) que a legenda da Fig. 4 referencia | 1 frase |
| 2 | W-EIC-1 | Abstract EN: consertar "manufacturing emerges as key sectors" | 1 linha |
| 3 | W-R2-1 | §2: remover "que o gênero raramente emprega" (manter só a função dos instrumentos) | 1 frase |
| 4 | W-R2-2 | §2: reenquadrar Bittencourt et al. (2023) como leitura da indústria sobre a MIP-SC 2018 | 1 frase |
| 5 | W-R1-2 | Legendas das figuras: padronizar fonte na convenção das tabelas (script do dado sobre CSV) | 6 legendas |
| 6 | W-R3-1 | Discussão: condicionar as alavancas às safras das âncoras na própria abertura | meia frase |
| 7 | F1/DA-2 | (autor, máquina local) `fechar_R1.bat` → CSVs das Tabelas 2 e 5 + checagem DA-1 | 1 clique |

*Itens 1–6 aplicáveis nesta sessão; item 7 permanece com o autor. Após 1–6 + recompilação,
manuscrito segue em Accept condicional a F1.*
