# Pacote de submissão — RBERU (Revista Brasileira de Estudos Regionais e Urbanos)

*Manuscrito: "Estrutura Produtiva do Espírito Santo: uma análise de insumo-produto"
(19 págs., 6 figuras, 5 tabelas, 2 apêndices, 36 referências). Preparado em 2026-07-13.
Trilha interna: 3 rodadas de parecer simulado (`REVIEW_*`) com todos os itens aplicados
(`RESPOSTA_AOS_PARECERISTAS.md`); pendência única: CSVs das Tabelas 1 e 4 (`fechar_R1.bat`).*

## Por que a RBERU

1. **O artigo dialoga com a própria revista**: quatro referências centrais são da RBERU —
   Haddad et al. (2017, o método IIOAS e a matriz que o artigo usa), Haddad et al. (2025, a
   matriz 2019 declarada como agenda), Sesso Filho & Guilhoto (2010, o precedente do gênero
   para o Pará) e Ribeiro et al. (2024, a regionalização capixaba com que o artigo conversa
   diretamente). É a conversa continuando no mesmo lugar.
2. **Gênero da casa**: "Estrutura Produtiva de [Estado]" é formato consolidado na RBERU.
3. **Calibragem dos pareceres**: as 3 rodadas internas usaram como EIC o perfil de editor de
   ciência regional brasileira; a decisão final (Minor superior → Accept condicional) foi
   calibrada para esse tier (Qualis A4–B1).

*Alternativas, se desejar*: Nova Economia, EconomiA, Ensaios FEE — exigiriam recalibrar a
ênfase (mais teoria em Nova Economia; mais política em Ensaios FEE).

---

## Carta ao editor (minuta)

> Prezado(a) Editor(a) da Revista Brasileira de Estudos Regionais e Urbanos,
>
> Submetemos à apreciação o artigo **"Estrutura Produtiva do Espírito Santo: uma análise de
> insumo-produto"**, que caracteriza a economia capixaba no formato que a literatura desta
> revista consolidou para outros estados — a exemplo de Sesso Filho e Guilhoto (2010) para o
> Pará — e que, para o Espírito Santo, permanecia lacunar: as contribuições existentes são
> pontuais (avaliação de impacto de um projeto siderúrgico; regionalização microrregional),
> sem a caracterização estrutural abrangente.
>
> A partir de três sistemas insumo-produto — a matriz inter-regional ES × restante do Brasil
> de 2008 (com vetor de emprego), a série nacional de 68 setores (2010–2021) e o sistema
> inter-regional das dez microrregiões de planejamento (2015) —, o artigo aplica a bateria
> completa do método (multiplicadores tipos I e II; ligações de Rasmussen-Hirschman com o
> lado da oferta pela inversa de Ghosh; ligações puras; quocientes locacionais; decomposição
> da produção pela demanda final; decomposição inter-regional de Isard) e a ancora nas duas
> lentes fundadoras da teoria do desenvolvimento regional: a base de exportação (North;
> Tiebout) e os polos de crescimento (Perroux).
>
> Quatro resultados organizam o retrato. Primeiro, os setores líderes — mineração, petróleo,
> siderurgia, celulose — concentram encadeamento, mas não emprego nem renda diretos; a
> decomposição pela demanda final quantifica o descolamento: a demanda externa ao estado
> induz 61,7% da produção, mas apenas 47,5% da ocupação. Segundo, um benchmark com as 27
> unidades da federação mostra que essa dualidade é genérica em tipo, mas extrema em grau —
> o ES é o segundo estado mais intensivo em setores de base e um dos que menos emprego
> geram por seu setor dominante. Terceiro, no território, o estado é um mosaico de vocações
> em torno de um núcleo metropolitano cuja extração hipotética derrubaria em 13% a produção
> da periferia. Quarto — e cremos que de interesse metodológico para os leitores da revista —,
> um modelo nulo de porte mostra que a mecânica da abertura capixaba (vazamento, feedback,
> concentração de destino) é a prevista para o tamanho do estado: a especificidade do ES não
> está na decomposição, e sim na composição que ela transporta. O aparato completo está em
> dois apêndices, e todos os resultados são reproduzíveis a partir de repositório público com
> scripts e tabelas versionados.
>
> O manuscrito é inédito, não está sob avaliação em outro periódico, e declara em seção
> própria os limites das fontes (fluxos estimados pelo método IIOAS; safras e agregações
> heterogêneas; série nacional a preços correntes). Declaramos ainda que a preparação do
> manuscrito contou com assistência de ferramentas de IA para código, verificação numérica e
> revisão, sob direção e responsabilidade integral do autor.
>
> Respeitosamente,
> Felipe Carvalho (PPGEco/UFES)

## Destaques de contribuição (para o formulário de submissão)

1. Primeira caracterização estrutural **abrangente** da economia capixaba via insumo-produto,
   no gênero consolidado da literatura regional brasileira (bateria completa + três matrizes).
2. Decomposição da produção **e do emprego** pela demanda final: a demanda externa puxa
   61,7% da produção mas 47,5% da ocupação — a divisão North/Tiebout medida no dado.
3. Benchmark interestadual (27 UFs) + **modelo nulo de porte**: separa o que é regularidade
   de tamanho (mecânica do vazamento/feedback) do que é específico do ES (composição de
   base; setor dominante mineral — só ES, PA e RJ).
4. Extração hipotética da metrópole (**−13%** na produção da periferia): a primeira medida de
   dependência sistêmica intraestadual para o ES, com leitura direta de política territorial.
5. Reprodutibilidade integral: pipeline público de 26 scripts com autoverificação, tabelas
   versionadas e apêndices metodológicos equação a equação.

## Checklist de submissão

- [x] Rodar `fechar_R1.bat` (rastro reprodutível das tabelas de decomposição e territorial) — **fechado em 2026-07-17** (commit `9cc83ea`; asserts `[OK]`; paridade reconferida)
- [ ] Conferir normas RBERU (template, anonimização para avaliação cega — remover nome/agradecimentos do PDF cego)
- [ ] Gerar versão anonimizada do `.tex` (autor/afiliação/repositório mascarados)
- [ ] Carta ao editor (acima) + destaques no formulário
- [ ] Declaração de ineditismo e de uso de IA (parágrafo da carta)
- [ ] Após aceite da disciplina (18/07): tag de release no repositório (ex.: `v2.0-caracterizacao`)
