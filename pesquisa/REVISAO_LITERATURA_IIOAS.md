# Revisão de literatura — Regionalização e o método IIOAS de insumo-produto inter-regional

*Apoio ao artigo "O Espírito Santo como economia-plataforma". Metodologia da skill
`academic-research-skills` (literature_strategist): busca por **encadeamento de citações
(Layer 2, backward tracking)** a partir da bibliografia de Haddad et al. (2017), seguida de
bibliografia anotada, matriz fonte × tema, identificação de lacunas e mapeamento por seção.*

---

## 1. Estratégia de busca (reprodutível)

| Item | Especificação |
|---|---|
| **Semente (core paper)** | Haddad, E. A.; Gonçalves Júnior, C. A.; Nascimento, T. O. (2017). *Matriz interestadual de insumo-produto para o Brasil: uma aplicação do método IIOAS*. RBERU 11(4):424–446. |
| **Conceitos-núcleo** | (i) regionalização de matrizes de IO; (ii) modelos inter-regionais (Isard / Chenery-Moses); (iii) métodos não-censitários (LQ/FLQ, CHARM, gravitacional, RAS); (iv) IIOAS; (v) ponte CGV/upstreamness. |
| **Layer 2 — citation chaining** | Varredura das 30 referências de Haddad (2017): marcam-se como *must-include* as citadas em ≥ 2 trabalhos-núcleo e as foundationais. |
| **Layer 1/3/4 (complemento)** | Fontes primárias lidas no acervo `Material IO/Artigos/` (Porsse-Peixoto-Palermo 2008; Guilhoto et al. 2019; Araújo Júnior 2018) + fontes de qualidade de dado MRIO (Tukker & Dietzenbacher 2013; OECD 2019). |
| **Critérios de inclusão** | Periódico/working paper revisado ou obra seminal; relevância direta a regionalização/inter-regional/CGV; idioma PT/EN. |
| **Saturação** | Atingida: alvo de fontes cumprido, todo tema com ≥ 3 fontes, fechamento do laço de citações na bibliografia de Haddad, cobertura de obras seminais (1951–1956) + recentes (2017–2019). |

**Triagem:** 30 referências na semente → 24 candidatas após título/escopo → **22 incluídas**
(15 de Haddad 2017 + 7 complementares). Cobertura: 5 obras seminais (Isard 1951; Leontief et al.
1953; Chenery 1956; Moses 1955; Round 1983) e fontes recentes (2015–2019).

---

## 2. Bibliografia anotada (por tema)

### Tema 1 — Fundações do modelo inter-regional de insumo-produto

**Isard, W. (1951).** *Interregional and regional input-output analysis* (REStat 33(4):318–328).
- **Tipo/Método:** teórico-seminal. **Achado-chave:** propõe o modelo inter-regional "ideal",
  com matriz de coeficientes particionada em blocos intra (LL, MM) e inter-regionais (LM, ML) e
  inversa de Leontief particionada — base da decomposição *spillover/feedback*.
- **Relevância:** é o aparato exato da Eq. (1)–(2) do artigo. **Qualidade:** seminal (alta).
  **Uso:** §Método.

**Chenery, H. B. (1956)** e **Moses, L. N. (1955, AER 45:803–826).**
- **Tipo:** seminais. **Achado-chave:** modelo multirregional de *coeficientes de coluna*
  (Chenery-Moses): supõe que a participação regional na aquisição de cada insumo é a mesma para
  todos os usuários da região de destino — simplificação que torna operável a regionalização
  quando os fluxos O-D plenos são desconhecidos. **Relevância:** é a hipótese que o IIOAS adota
  no passo de regionalização (Haddad 2017, §3.3). **Uso:** §Dados/§Método.

**Leontief, W. et al. (1953).** *Studies in the structure of the American economy.*
- **Achado-chave:** primeiras incursões regionais/inter-regionais do modelo de Leontief.
  **Uso:** nota histórica em §Introdução/§Método.

**Miller, R. E.; Blair, P. D. (2009).** *Input-Output Analysis: Foundations and Extensions* (2ª ed.).
- **Tipo:** livro-texto de referência. **Achado-chave:** formaliza decomposição de multiplicadores,
  efeitos *feedback* inter-regionais (tipicamente pequenos), ligações de Rasmussen-Hirschman e a
  inversa de Ghosh (ligação para frente). **Relevância:** convenção metodológica central do artigo.
  **Uso:** §Método, §Discussão. *(Já citado.)*

### Tema 2 — Métodos não-censitários de regionalização

**Round, J. I. (1983).** *Nonsurvey techniques: a critical review* (Int. Reg. Sci. Review 8(3):189–212).
- **Tipo:** revisão crítica seminal. **Achado-chave:** estabelece a distinção censitário/não-censitário
  e classifica as técnicas (quocientes locacionais, gravitacionais, iterativas); argumenta que sistemas
  reais são **híbridos**. **Relevância:** enquadra o IIOAS como método híbrido e justifica o uso de
  fluxos estimados (Limitação ii do artigo). **Qualidade:** seminal. **Uso:** §Dados/§Limitações.

**Flegg, A. T.; Mastonardi, L. J.; Romero, C. A. (2016).** *Evaluating the FLQ and AFLQ formulae…
Córdoba, Argentina* (Economic Systems Research 18(1):21–37).
- **Tipo:** empírico comparativo. **Achado-chave:** avalia o quociente locacional de Flegg (FLQ/AFLQ)
  contra outras estimativas regionais; mostra sensibilidade dos coeficientes regionais ao parâmetro de
  ajuste. **Relevância:** alternativa de regionalização (LQ) ao IIOAS — contraponto metodológico.
  **Uso:** §Dados (justificativa de escolha do método).

**Többen, J.; Kronenberg, T. (2015).** *Construction of multi-regional IO tables using the CHARM method*
(Economic Systems Research 27(4):487–507).
- **Tipo:** metodológico. **Achado-chave:** o método CHARM (Cross-Hauling Adjusted Regionalization)
  corrige o *cross-hauling* (importação e exportação simultâneas do mesmo bem) que LQs ignoram.
  **Relevância:** estado-da-arte não-censitário; alternativa ao gravitacional do IIOAS. **Uso:** §Dados.

**Riddington, G.; Gibson, H.; Anderson, J. (2006).** *Comparison of gravity, survey and LQ-based local
tables* (Regional Studies 40(9):1069–1081).
- **Tipo:** comparativo empírico (Escócia). **Achado-chave:** compara diretamente gravitacional × LQ ×
  survey; o gravitacional aproxima melhor os fluxos observados que o LQ. **Relevância:** sustenta a
  escolha do componente gravitacional do IIOAS. **Uso:** §Dados/§Limitações.

**Hulu, E.; Hewings, G. J. D. (1993).** *Interregional IO models for Indonesia under limited information*
(Urban & Reg. Dev. Studies 5(2):135–153).
- **Achado-chave:** construção inter-regional sob informação limitada (5 regiões da Indonésia, 1980/85).
  **Relevância:** precedente direto do "limited information" do IIOAS. **Uso:** §Método.

**Dixon, P. B.; Rimmer, M. T. (2004).** *Disaggregation of results… to the state level* (CoPS WP 145).
- **Achado-chave:** técnica de coeficientes geradores de demanda usada no passo de regionalização do
  IIOAS (Eqs. 16–17 de Haddad 2017). **Uso:** §Método.

### Tema 3 — O método IIOAS e suas aplicações

**Haddad, E. A. et al. — família IIOAS internacional:** Líbano (2014, J. Dev. Econ. Policies 16(1):5–45);
Marrocos (2013, OCP Policy Center); Açores (2015, em *The region and trade*); **Colômbia** (2016,
Borradores de Economía 923, Banco de la República) — base metodológica do IIOAS; Egito (2016, *J. Econ.
Structures* 5(1):1–33, abordagem ICGE).
- **Tipo:** aplicações metodológicas. **Achado-chave:** o IIOAS é um método híbrido consistente com a
  matriz nacional, replicável para qualquer país que publique TRUs e possua sistema de informações
  setoriais regionalizadas; combina dados oficiais (IBGE), coeficientes Chenery-Moses e fluxos
  gravitacionais (impedância via tempos de viagem). **Relevância:** define o método-substrato do artigo.
  **Uso:** §Dados/§Método. *(Haddad 2017 já citado.)*

**Haddad, E. A.; Gonçalves Jr., C. A.; Nascimento, T. O. (2017)** — *core paper*.
- **Achado-chave (verificado no PDF):** Tabela 2 (p. 440) decompõe o multiplicador de produção por UF
  em parcela intra e inter-regional; **ES: inter-regional 27,4%** do multiplicador total. O *abstract*
  destaca AM, **ES** e MT como os estados em que a demanda final de outras UFs e do exterior mais
  influencia a produção local. **Relevância:** âncora numérica e tese do artigo. **Uso:** §Resultados/§Discussão.

### Tema 4 — A tradição brasileira de IO inter-regional

**Guilhoto, J. J. M.; Sesso Filho, U. A. (2005, Econ. Aplicada 9(2):277–299; 2010, Econ. & Tecnologia 23(4)).**
- **Achado-chave:** método de estimação da matriz nacional de IO a partir de dados preliminares das
  Contas Nacionais — base de regionalização brasileira. **Uso:** §Dados. *(2005 já citado.)*

**Guilhoto, J. J. M.; Azzoni, C. R.; Ichihara, S. M.; Kadota, D. K.; Haddad, E. A. (2010).** *Matriz de
insumo-produto do Nordeste e Estados.* Banco do Nordeste.
- **Achado-chave:** sistema inter-regional para o NE brasileiro — precedente nacional de
  regionalização multiestadual. **Uso:** §Dados/§Introdução.

**Domingues, E. P.; Haddad, E. A. (2002).** *Matriz inter-regional Minas Gerais/Resto do Brasil.*
- **Achado-chave:** primeiro MG/RB; documenta vazamento e transbordamento de MG. **Relevância:**
  antecedente direto da leitura bi-regional do artigo. **Uso:** §Introdução/§Discussão.

**Porsse, A. A.; Peixoto, F. C.; Palermo, P. U. (2008).** *Matriz de IO inter-regional Rio Grande do
Sul-Restante do Brasil 2003* (FEE TD 38) — lido na íntegra; lineage de Porsse-Haddad-Ribeiro (2004,
RS-RB 1998) e Porsse-Haddad-Pontual (2003).
- **Tipo:** metodológico-empírico (40 setores, 2 regiões, TRU 2003). **Achado-chave (verificado):**
  *"os efeitos de transbordamento da economia gaúcha para o Restante do Brasil são elevados e mais
  intensos do que no caso contrário"* (**assimetria spillover/feedback**) e *"os vazamentos regionais
  do RS são relativamente menores nos setores agroindustriais e mais elevados nos demais setores
  industriais, especialmente… metal-mecânico"*. **Relevância:** ANTECEDENTE DIRETO da tese do artigo
  — mesma formulação de Isard particionada (Eqs. 7–8) e mesmo padrão qualitativo (assimetria +
  vazamento setorialmente diferenciado). **Qualidade:** alta. **Uso:** §Introdução/§Discussão (âncora forte).

**Ichihara, S. M.; Guilhoto, J. J. M. (2008).** *Interregional IO… municípios de São Paulo.* ERSA.
- **Achado-chave:** sistema intermunicipal (SP) — paralelo da agenda intra-estadual do artigo
  (microrregiões do ES). **Uso:** §Agenda de pesquisa.

**Zhang, Z.; Shi, M.; Zhao, Z. (2015, ESR 27(2):238–256).**
- **Achado-chave:** sistema inter-regional para 30 províncias chinesas (2002) — comparador internacional
  de regionalização multirregional. **Uso:** §Introdução.

### Tema 5 — Ponte para cadeias globais de valor (CGV) e *upstreamness*

**Antràs, P.; Chor, D.; Fally, T.; Hillberry, R. (2012, AER 102(3):412–416).**
- **Achado-chave:** índice de *upstreamness* U=(I−G)⁻¹·1 (distância ao consumo final). **Uso:** §Método/§Resultados. *(Já citado.)*

**Guilhoto, J. J. M.; Hewings, G. J. D.; Johnstone, N.; Webb, C.; Yamano, N. (2019).** *Exploring changes
in world production and trade: insights from the 2018 ICIO/TiVA* (OECD STI WP 2019/04) — lido.
- **Achado-chave:** base ICIO/TiVA (64 países, 36 setores, 2005–2015); discute participação em CGV,
  *upgrading* para estágios de maior valor adicionado, e serviços embutidos em exportações. **Relevância:**
  (i) base MRIO alternativa à WIOD para a agenda internacional do artigo; (ii) o tema de *upgrading*
  fundamenta o argumento de "adensamento de cadeia". **Uso:** §Agenda/§Discussão.

**Araújo Júnior, I. F. de (2018).** *Três ensaios sobre a análise das cadeias globais de valor* (Tese,
UFJF) — usada no tratamento WIOD (E).
- **Achado-chave:** reporta posição do Brasil em CGV por *ranking* (157º/188), com a maquinaria
  Antràs-Chor/Miller-Temurshoev (2017). **Relevância:** prática de reporte por nível+ranking. **Uso:** §Limitações.

**Timmer, M. P. et al. (2015, RIE 23(3):575–605)** — guia da WIOD; **Tukker, A.; Dietzenbacher, E. (2013,
ESR 25(1):1–19)** — introdução/crítica de bases MRIO (entradas negativas, discrepâncias); **OECD (2019)**
— Guia TiVA (demanda final = consumo + FBCF + variação de estoques). **Uso:** §Dados/§Limitações. *(Adicionados em E.)*

---

## 3. Matriz fonte × tema

| Fonte | T1 Fundações | T2 Não-censitário | T3 IIOAS | T4 Brasil inter-reg. | T5 CGV | Qual. |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Isard (1951) | **main** | | x | | | Alta |
| Chenery (1956) / Moses (1955) | **main** | x | x | | | Alta |
| Miller & Blair (2009) | **main** | | | x | x | Alta |
| Round (1983) | | **main** | x | | | Alta |
| Flegg et al. (2016) | | **main** | | | | Média |
| Többen & Kronenberg (2015) | | **main** | | | | Alta |
| Riddington et al. (2006) | | **main** | x | | | Média |
| Hulu & Hewings (1993) | x | x | **main** | | | Média |
| Dixon & Rimmer (2004) | | x | **main** | | | Média |
| Haddad et al. (Col./Eg./Açores/Líbano) | | x | **main** | | | Alta |
| **Haddad et al. (2017)** | | x | **main** | **main** | | Alta |
| Guilhoto & Sesso Filho (2005/10) | | x | | **main** | | Alta |
| Guilhoto et al. NE (2010) | | | x | **main** | | Alta |
| Domingues & Haddad (2002) | | | x | **main** | | Alta |
| **Porsse, Peixoto & Palermo (2008)** | x | | x | **main** | | Alta |
| Ichihara & Guilhoto (2008) | | x | | **main** | | Média |
| Zhang et al. (2015) | | x | | x | | Média |
| Antràs et al. (2012) | | | | | **main** | Alta |
| Guilhoto et al. OECD (2019) | | | | x | **main** | Alta |
| Araújo Júnior (2018) | | | | | **main** | Média |
| Timmer et al. (2015) | | | | | **main** | Alta |

Cada tema tem ≥ 3 fontes (saturação temática atendida).

---

## 4. Síntese e lacunas (contribuição do artigo)

**Convergências.** (i) A regionalização sob informação limitada é, na prática, **híbrida**
(Round 1983) — combina coeficientes Chenery-Moses, LQ/CHARM ou modelos gravitacionais; o IIOAS é
uma instância gravitacional+oficial dessa família. (ii) A tradição brasileira (MG: Domingues-Haddad
2002; RS: Porsse et al. 2008; NE: Guilhoto et al. 2010) documenta de forma robusta dois fatos que o
artigo reencontra no ES: **assimetria spillover/feedback** e **vazamento setorialmente diferenciado**
(menor no agro, maior no metal-mecânico/industrial).

**Debates/divergências.** Qual método não-censitário aproxima melhor os fluxos O-D? LQ subestima
*cross-hauling* (daí CHARM — Többen-Kronenberg 2015); o gravitacional aproxima melhor fluxos observados
(Riddington et al. 2006) mas exige matriz de impedância. O IIOAS opta pelo gravitacional + Chenery-Moses.

**Lacunas que o artigo preenche:**
1. **Destino interestadual do vazamento.** A literatura brasileira trata o destino como "Resto do Brasil"
   agregado (Porsse et al. 2008; Domingues-Haddad 2002). O artigo **desagrega para as 27 UFs** — mostra
   que 65,4% do *spillover* do ES vai ao Sudeste e 52,5% ao núcleo SP/RJ.
2. **Ponte IIOAS × CGV.** Haddad (2017) decompõe multiplicadores por UF mas não os liga à posição em
   cadeias de valor; Antràs-Chor/Guilhoto-OECD (2019) medem *upstreamness* mas não o destino doméstico.
   O artigo **junta as duas camadas** (vazamento interestadual + *upstreamness* da pauta).
3. **O ES como objeto.** A tradição empírica concentra-se em MG, RS, SP e NE; o ES — economia-plataforma
   exportadora — é subestudado. O artigo o caracteriza com o aparato consolidado.

---

## 5. Fontes recomendadas por seção do artigo

| Seção | Fontes a mobilizar |
|---|---|
| §1 Introdução | Domingues & Haddad (2002); Porsse et al. (2008); Guilhoto et al. NE (2010); Zhang et al. (2015) |
| §2 Dados | Round (1983); Chenery (1956)/Moses (1955); Flegg et al. (2016); Többen & Kronenberg (2015); Riddington et al. (2006); Dixon & Rimmer (2004); Guilhoto & Sesso Filho (2005) |
| §3 Método | Isard (1951); Miller & Blair (2009); Hulu & Hewings (1993); Antràs et al. (2012) |
| §5 Discussão | Porsse et al. (2008) e Domingues & Haddad (2002) — ancorar a assimetria; Guilhoto et al. OECD (2019) — *upgrading* |
| §6 Limitações | Round (1983); Riddington et al. (2006); Tukker & Dietzenbacher (2013); OECD (2019); Araújo Júnior (2018) |
| §7 Agenda | Ichihara & Guilhoto (2008) — intra-estadual; Guilhoto et al. OECD (2019) — MRIO/TiVA |

---

## 6. Melhorias propostas ao artigo (aplicadas — ver `es_insumo_produto.tex`)
1. **§2 (Dados):** parágrafo situando o IIOAS no leque de métodos não-censitários de regionalização
   (LQ/FLQ, CHARM, gravitacional; híbrido na acepção de Round 1983), justificando a escolha.
2. **§5 (Discussão):** ancorar a assimetria *spillover/feedback* do ES nos precedentes brasileiros
   (RS: Porsse et al. 2008; MG: Domingues & Haddad 2002) — a evidência capixaba **converge** com a
   tradição e a **estende** ao recorte interestadual.
3. **§7 (Agenda):** apontar OECD ICIO/TiVA (Guilhoto et al. 2019) como rota MRIO para a extensão
   internacional.
4. **Bibliografia:** novas entradas (Round 1983; Flegg et al. 2016; Többen & Kronenberg 2015;
   Riddington et al. 2006; Dixon & Rimmer 2004; Domingues & Haddad 2002; Porsse et al. 2008;
   Guilhoto et al. 2019).
