# Plano de atualização — do corte 2008 ao painel 2008 → vintage mais recente (2026)

**Decisão (jun/2026):** o artigo deixa de ser uma **fotografia transversal** (MIP 2008 +
WIOD 2014) e passa a ser um **estudo de atualização / dinâmica estrutural**: o padrão
economia-plataforma do ES **persistiu, intensificou ou arrefeceu** entre 2008 e o
vintage mais recente disponível em cada camada de dado?

> Este documento é o **desenho de pesquisa** do pivô. Convive com:
> - [`MAPA_DE_PESQUISA.md`](MAPA_DE_PESQUISA.md) — inventário de dados, estado da arte, fontes (ver C2: NEREUS/IJSN/CECEG).
> - [`PLANO_ARTIGO.md`](PLANO_ARTIGO.md) — roteiro do artigo-base (escopo antigo, congelado).
> - [`src/io_core.py`](../src/io_core.py) — núcleo Isard a ser **generalizado** para multi-vintage.

---

## 0. Reposicionamento da pergunta (RQ)

| | Artigo-base (transversal) | Update (este plano) |
|---|---|---|
| **RQ** | O ES é uma economia-plataforma em 2008? | O perfil-plataforma do ES **muda** entre 2008 e ~2022? Em que direção e por quê? |
| **Unidade** | Corte único | Painel de 2–3 pontos por camada |
| **Método central** | Isard (retido/vazado, spillover/feedback, RH) | Isard **+ SDA** (decomposição da variação) **+ ponte RAS/GRAS** entre vintages |
| **Mecanismo a testar** | Assimetria spillover≫feedback | A assimetria **se aprofundou** após Fundão (2015) e os choques de commodity? |

**Tese a confirmar/refutar:** se o ES é estruturalmente plataforma, o vazamento e a
assimetria spillover/feedback devem ser **robustos no tempo** — não um artefato de 2008.
SDA dirá quanto da variação é **tecnológica** (mudança de coeficientes `A`) vs. **de
demanda final** (mudança de `y`), separando inércia estrutural de choque conjuntural.

## 1. Camadas de dado e seus vintages (cada uma anda em calendário próprio)

| Camada | "2008" (base atual) | Vintage mais recente **com dados em mão** | Fonte / ressalva |
|---|---|---|---|
| MIP **nacional** | base 2010 (MIP 2015) | **2019, nível 68** (planilha CECEG/Celso, recebida jun/2026; "Atualizado em" 2025-05-01) | só a versão "Brasil" está computada na planilha; "Espírito Santo" existe como seletor mas não foi gerado nela |
| **Interestadual** (IIOAS) | 2008 (Haddad et al. 2017) | **bloqueado** — artigo-metodologia 2019 (Haddad, Araújo, Rocha & Vale, *RBERU*; 128 produtos, 68 set., 27 UF, ES=R18) em mãos, mas **sem a matriz numérica**; equipe confirmou que só há dados até 2015 | citar como referência metodológica/Discussão; reabrir se a base de dados aparecer |
| **MIP-ES própria** | — | **2015, nível 35** (planilha CECEG/Celso `ESPIRITO_SANTO_2015.xlsm`, recebida jun/2026) | é TRU **de uma região só** (ES): oferta, "Importação Regional" agregada, margens, impostos — **sem fluxo bilateral ES↔resto do Brasil** explícito; não substitui a inter-regional sozinha |
| **Mundo** (CGV) | WIOD 2014 | **OECD ICIO/TiVA 2022** (ed. 2025) | ES não é país → inferência via Brasil |

> **Implicação honesta (revisada jun/2026):** dado o que está de fato disponível, o painel
> realista não é 2008→2019 — é **2008 → 2015** (o ano em que existe MIP-ES própria). A IIOAS
> 2019 fica como **referência metodológica** (mesma linhagem IIOAS da base 2008) e candidata a
> reabrir o painel para 2019 **se/quando** a matriz numérica completa for obtida; não é tratada
> como camada ativa enquanto só houver o artigo.

## 2. Método (4 blocos, em ordem de dependência)

### 2.1 Concordância setorial
Pré-requisito de tudo. Os vintages têm granularidades diferentes (26 / 35 / 68 setores;
ICIO ~45). Construir **tabela de–para** explícita (base CNAE/IBGE), agregando para o
**maior denominador comum** (provavelmente os ~20–26 setores do artigo-base). Versionar
como `dados/concordancia_setorial.csv` e documentar perdas de resolução.

### 2.2 Deflação a preços constantes
Comparar multiplicadores/vazamento entre 2008 e 2022 em **valores correntes** mistura
preço e quantidade. Aplicar **dupla deflação** (deflatores setoriais do SCN/IBGE) para
um ano-base comum antes de qualquer leitura de "mudança real". Sem isso, SDA é inválida.

### 2.3 Ponte entre vintages — RAS / GRAS
Onde faltar matriz observada para um ano-alvo, **atualizar** a estrutura de um vintage
vizinho aos **totais marginais** (produção/consumo intermediário) das Contas Regionais
mais recentes. **RAS** (biproporcional) como padrão; **GRAS** (Junius & Oosterhaven 2003)
quando houver elementos negativos. Declarar que RAS/GRAS **não cria** mudança tecnológica
real — só redistribui a antiga para novos totais (limite central, ver §4).

### 2.4 Decomposição estrutural — SDA
Sobre dois pontos comparáveis (p.ex. 2008 vs. 2021/2022 deflacionados), decompor a
variação de cada indicador (vazamento, spillover, emprego embutido) em:
- **efeito tecnológico** (Δ na inversa de Leontief `B`, i.e. Δ`A`);
- **efeito de demanda final** (Δ`y`, nível e composição).
Decomposição aditiva clássica (Miller & Blair 2009, cap. 13), média das duas polarizações.

### 2.5 Camada mundo — refazer *upstreamness* em ICIO 2022
Re-rodar Antràs-Chor (`07/08/09_*.py`) sobre **ICIO/TiVA 2022** no lugar de WIOD 2014.
É quase *drop-in* (mesma álgebra), exige só nova concordância 56→~45 e re-validar a
posição da pauta capixaba via Brasil. Entrega de baixo custo / alto valor — moderniza o
ponto mais datado do artigo e abre a dinâmica **2008(/2000) → 2022** na curva do sorriso.

## 3. O que muda no código (`src/io_core.py` e `pesquisa/`)

Hoje `io_core.py` é um esqueleto de **um** vintage (L=ES, M=resto BR; parser ainda TODO).
Generalizações necessárias:

- [ ] **Parametrizar por vintage/ano** (loader recebe ano + layout; hoje hard-coded 52×52).
- [ ] **Camada de concordância** (aplica de–para setorial antes de montar `Z`, `x`, `ocup`).
- [ ] **Deflação** (módulo que aplica deflatores setoriais a preços de ano-base comum).
- [ ] **`ras()` / `gras()`** (atualização biproporcional; testes de convergência).
- [ ] **`sda()`** (decomposição aditiva tecnológico vs. demanda final).
- [ ] Re-rodar `01–05` para cada vintage; novo script `14_sda.py`; `15_painel.py` (séries).
- [ ] `07–09` sobre ICIO 2022.

## 4. Limites (seção que desarma o referee — frontal)

1. **RAS/GRAS extrapola, não observa** — onde a matriz-alvo for atualizada, a "mudança"
   capturada é só de marginais; substituição tecnológica fina fica fora.
2. **Quebra estrutural real — Fundão (2015)** — cai entre os vintages 2011 e 2019/2021;
   paralisou a Samarco e alterou o peso de extração/pelotização. Tratar como **quebra**,
   não tendência. (É também *oportunidade*: o ES é um quase-experimento de choque.)
3. **Quebra metodológica — rebase IBGE 2010→2021** — reclassificação CNAE, novas
   ponderações e cobertura. Variação 2008→2021 mistura mudança real **+** mudança de
   régua estatística. Separar o que der; declarar o resto.
4. **Fluxos interestaduais estimados** (IIOAS: gravidade+RAS) — não observados; herdam as
   hipóteses do modelo. (Contraste com a China, onde o fluxo interprovincial é medido por
   frete/alfândega — ver discussão de política de dados, §6.)
5. **ES não é país no ICIO** — posição em CGV inferida via Brasil + peso da pauta; viés de
   intensidade primária a declarar.

## 5. Sequenciamento (de baixo risco/custo → alto)

| Sprint | Entrega | Depende de | Risco | Status (jun/2026) |
|---|---|---|---|---|
| **S1** | *Upstreamness* em ICIO 2022 (refresh da camada-mundo) | baixar ICIO ed. 2025 | baixo | aberto |
| **S2** | Concordância setorial + deflação versionadas | deflatores IBGE | médio | aberto |
| **S3** | ~~Vintage interestadual 2019 rodado em `01–05`~~ | matriz numérica IIOAS 2019 (NEREUS) | médio | **bloqueado** — só o artigo-metodologia (Haddad et al.) chegou, sem os dados; equipe confirma que só há dados até 2015 |
| **S4** | Matriz CECEG/Celso integrada | **arquivo do Celso** | — | ✅ **recebido** (jun/2026): `MIPBR_2019_Nível_68.xlsm` (nacional 2019/68 set.) + `ESPIRITO_SANTO_2015.xlsm` (ES própria, 2015/35 set., região única). Falta o nacional 2015 (`Matriz_de_Insumo_Produto_2015_Nivel_67.xls`, já citado em `dados/README.md`) para fechar o resíduo resto-do-Brasil 2015 |
| **S4b** *(novo)* | Bi-regional ES×RB **2015** por resíduo (nacional 2015 − ES 2015) | upload do nacional 2015 | médio | a fazer — substitui S3 como âncora do painel |
| **S5** | SDA 2008 vs. 2015 + painel + figuras | S2, S4b | alto | aberto |

**Caminho crítico revisado = S4b** (falta só o nacional 2015 para fechar o resíduo). S3/IIOAS-2019
fica em espera — vira S3' se a matriz numérica aparecer depois, e nesse caso estende o painel
para 3 pontos (2008·2015·2019) em vez de só 2.

## 6. Gancho de política de dados (para a Discussão)

O vazamento que medimos espelha um **vazamento de informação**: ninguém observa o fluxo
inter-regional real — estima-se por gravidade. O Brasil já tem o insumo (NF-e/CT-e na
Receita Federal; o IBGE usou isso na TRU-UF 2018 experimental), mas sem
institucionalização periódica. Comparar com a MRIO chinesa (séries oficiais 1987–2017,
fluxo medido por frete/alfândega + balanço por *cross-entropy*) sustenta a recomendação:
TRU-UF **periódica e mandatória** + mandato recorrente ao IJSN/CECEG. Liga o achado
empírico ao debate de política — e ao próprio CECEG, que faz MIP **e** EGC.

## 7. Referências-âncora (a reconciliar na bibliografia)

- **Isard / SDA / RAS:** Miller & Blair (2009), *Input-Output Analysis*, 2ª ed., Cambridge.
- **GRAS:** Junius & Oosterhaven (2003), *Economic Systems Research*.
- **Regionalização BR:** Guilhoto & Sesso Filho (2005), *Economia Aplicada*.
- **IIOAS:** Haddad, Gonçalves Jr. & Nascimento (2017), RBERU / TD Nereus 02/2017; atualização **2019** (RBERU, 2025).
- **Upstreamness:** Antràs, Chor, Fally & Hillberry (2012), *AER* 102(3); Antràs & Chor (2018), NBER WP 24185.
- **Mundo/CGV:** OECD ICIO & TiVA, edição 2025 (1995–2022).
- **MIP-ES:** IJSN TD 54 e TD 60 (TRU/MIP 2015); Ribeiro et al. (2024), RBERU 18(4) — regionalização em 10 microrregiões.
- **Rebase IBGE:** SCN, nota técnica de mudança de ano-base 2010→2021.

## 8. Decisões abertas (suas)

- **Escopo do painel:** 2 pontos (2008 vs. mais recente) ou 3 (2008 · 2011/2015 · 2019/2021)?
- **Camada-líder:** ancorar no **interestadual** (IIOAS 2008→2019, comparável) ou na **MIP-ES** (IJSN/CECEG)?
- **Prazo:** o pivô tensiona 18/07. Opção: entregar **S1+S3** (refresh mundo + interestadual 2019) no artigo da disciplina e o SDA completo como versão estendida.
