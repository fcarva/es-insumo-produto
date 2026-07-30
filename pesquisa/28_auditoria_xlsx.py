# -*- coding: utf-8 -*-
"""
28_auditoria_xlsx.py — gera auditoria/auditoria_dados_es.xlsx: a pasta de auditoria
dos dados do artigo, para entrega ao professor.

Diagramacao replicada de Lista_Exercicios_Respostas.xlsx (o trabalho da disciplina):
Calibri, coluna A como goteira, titulo na linha 2, nota metodologica na linha 3,
bloco "Sintese" e cabecalho cinza-quente com fios horizontais e zebra. A paleta e os
fios foram extraidos celula a celula do arquivo de referencia.

As celulas derivadas sao FORMULAS VIVAS (AVERAGE/SUMPRODUCT/SUM), nao constantes: a
aba 12_Verificacao recomputa cada numero publicado a partir das abas de dados, calcula
o desvio e classifica o status. Uma auditoria que nao recalcula nao audita.

Numeros: lidos de outputs/*.csv. Prosa (integridade, defeitos, proveniencia,
referencias, camada 2015): autoral, embutida aqui como literal.

Somente funcoes pre-2007 nas formulas (AVERAGE, SUM, SUMPRODUCT, ABS, IF): o
verificador roda LibreOffice, que nao avalia XLOOKUP/FILTER/UNIQUE.
"""
import os, csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
OUT  = os.path.join(AQUI, "outputs")
DEST = os.path.join(RAIZ, "auditoria")

# ---- paleta e tipografia, extraidas de Lista_Exercicios_Respostas.xlsx ----------
FT = "Calibri"
TITULO, NOTA, SECAO   = "FF100F0F", "FF6F6E69", "FF575653"
CORPO, ROTULO, AZUL   = "FF282726", "FF403E3C", "FF205EA6"
F_CAB, F_ZEBRA        = "FFDAD8CE", "FFF2F0E5"
F_ENTRADA, F_PARAM    = "FFF3E6B9", "FFE6E4D9"
F_SINTESE             = "FFE1E4C2"
FIO, FIO_FORTE        = "FFDAD8CE", "FF878580"
COR_ABA               = "FFB7B5AC"

MULT, PCT, MI, EMP, DLT = "0.0000", "0.00", "#,##0.0", "#,##0", "0.0000"


def fio(baixo=FIO):
    return Border(top=Side(style="thin", color=FIO),
                  bottom=Side(style="thin", color=baixo))


def moldura(ws, titulo, nota, bullets, ncols):
    """Titulo (linha 2), nota (3) e bloco Sintese. Devolve a linha do cabecalho."""
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = COR_ABA
    ws.column_dimensions["A"].width = 1.2
    ws.row_dimensions[1].height = 7.5
    ws.row_dimensions[2].height = 21.75
    ws.row_dimensions[3].height = 24.75
    ult = get_column_letter(1 + max(ncols, 2))

    ws["B2"] = titulo
    ws["B2"].font = Font(name=FT, size=16, bold=True, color=TITULO)
    ws["B3"] = nota
    ws["B3"].font = Font(name=FT, size=9.5, color=NOTA)
    ws["B3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(f"B3:{ult}3")

    if not bullets:
        return 6
    ws["B5"] = "Síntese"
    ws["B5"].font = Font(name=FT, size=10, bold=True, color=SECAO)
    for i, t in enumerate(bullets):
        r = 6 + i
        ws.row_dimensions[r].height = 13.5
        c = ws.cell(r, 2, "•  " + t)
        c.font = Font(name=FT, size=10, color=TITULO)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(f"B{r}:{ult}{r}")
    return 6 + len(bullets) + 1


def tabela(ws, hrow, colunas, linhas, larguras, realce=None, zebra=True):
    """colunas = [(rotulo, formato|None, alinhamento|None)]; realce = {i_linha: cor}."""
    realce = realce or {}
    ws.row_dimensions[hrow].height = 24
    for j, (rot, _f, _a) in enumerate(colunas):
        c = ws.cell(hrow, 2 + j, rot)
        c.font = Font(name=FT, size=9, bold=True, color=ROTULO)
        c.fill = PatternFill("solid", fgColor=F_CAB)
        c.border = fio(FIO_FORTE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for i, linha in enumerate(linhas):
        r = hrow + 1 + i
        cor = realce.get(i, F_ZEBRA if (zebra and i % 2 == 1) else None)
        negrito = i in realce
        for j, (_rot, fmt, al) in enumerate(colunas):
            v = linha[j] if j < len(linha) else None
            c = ws.cell(r, 2 + j, v)
            c.font = Font(name=FT, size=9, bold=negrito, color=CORPO)
            c.border = fio()
            if cor:
                c.fill = PatternFill("solid", fgColor=cor)
            if fmt:
                c.number_format = fmt
            c.alignment = Alignment(horizontal=al or "left", vertical="center",
                                    wrap_text=(al in (None, "left")))
    for col, w in larguras.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = ws.cell(hrow + 1, 2).coordinate
    return hrow + 1 + len(linhas)


def ler(nome):
    with open(os.path.join(OUT, nome), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def f(r, c):
    return float(r[c])


# =================================================================== dados =======
setores   = ler("es_setores_resultados.csv")
caract    = ler("es_caracterizacao_2008.csv")
decomp    = ler("decomposicao_fd.csv")
clus_set  = ler("cluster_setorial.csv")
clus_uf   = ler("cluster.csv")
clus_res  = ler("cluster_resumo.csv")
bench     = {r["UF"]: r for r in ler("benchmark_caracterizacao.csv")}
destino   = ler("es_spillover_destino.csv")
micro     = sorted(ler("micro_multiplicadores.csv"), key=lambda r: -f(r, "share_VBP_pct"))
hem       = ler("extracao_hipotetica.csv")[0]
traj      = ler("trajetoria_n68.csv")
with open(os.path.join(OUT, "micro_LQ.csv"), encoding="utf-8") as fh:
    lq = list(csv.reader(fh))

wb = Workbook()
wb.remove(wb.active)

ABAS = [
    ("01_Setores",        "Resultados setoriais do ES: multiplicador, vazamentos e ligações R-H (26 setores)"),
    ("02_Multiplicadores","Multiplicadores tipos I e II, ligações e ligações puras (26 setores)"),
    ("03_DemandaFinal",   "Decomposição da produção e do emprego pelos componentes da demanda final"),
    ("04_Cluster",        "O ES entre os estados de crescimento dinâmico e o núcleo SP/RJ"),
    ("05_Estados",        "As 27 UFs: cluster, vazamento e abertura; métricas-resumo"),
    ("06_Spillover",      "Injeção, spillover, feedback e produção retida (agregados)"),
    ("07_Destino",        "Destino interestadual do spillover (26 UFs) e concentração no Sudeste"),
    ("08_Micro",          "Multiplicadores e retenção por microrregião (2015) + extração hipotética"),
    ("09_Micro_LQ",       "Quocientes locacionais: 35 setores × 10 microrregiões (2015)"),
    ("10_Trajetoria",     "Setores de base na estrutura nacional, 2010–2021 (série Nível 68)"),
    ("11_Camada2015",     "Camada 2015 — regionalização CILQ: registro documental"),
    ("12_Verificacao",    "Verificação número-a-número: artigo ↔ fonte, com recomputação viva"),
    ("13_Integridade",    "Integridade contábil e reprodutibilidade"),
    ("14_Referencias",    "Integridade das referências bibliográficas"),
    ("15_Defeitos",       "Defeitos encontrados na auditoria e status das correções"),
    ("16_Proveniencia",   "Mapa script → output → o que computa"),
]

# ================================================================== 00_Capa ======
ws = wb.create_sheet("00_Capa")
ws.sheet_view.showGridLines = False
ws.sheet_properties.tabColor = COR_ABA
ws.column_dimensions["A"].width = 1.2
ws.column_dimensions["B"].width = 30.0
ws.column_dimensions["C"].width = 96.0
ws.row_dimensions[1].height = 7.5
ws.row_dimensions[2].height = 21.75

ws["B2"] = "Auditoria dos dados do artigo"
ws["B2"].font = Font(name=FT, size=16, bold=True, color=TITULO)
ws["B3"] = "Estrutura Produtiva do Espírito Santo: uma análise de insumo-produto"
ws["B3"].font = Font(name=FT, size=11, color=NOTA)
ws.merge_cells("B3:C3")

META = [
    ("Autor",      "Felipe Carvalho — PPGEco/UFES"),
    ("Orientador", "Prof. Dr. Celso Bissoli Sessa"),
    ("Disciplina", "Análise de Insumo-Produto — 2026/1"),
    ("Data",       "julho de 2026"),
    ("Objeto",     "MIP inter-regional ES × restante do Brasil (2008); matriz interestadual "
                   "27 UFs (2008); série nacional Nível 68 (2010–2021); sistema inter-regional "
                   "das 10 microrregiões de planejamento (2015)"),
    ("Convenção",  "spillover/feedback de Isard–Miller-Blair, variante V3 (inversa particionada)"),
]
for i, (k, v) in enumerate(META):
    r = 5 + i
    ws.cell(r, 2, k).font = Font(name=FT, size=10, bold=True, color=NOTA)
    c = ws.cell(r, 3, v)
    c.font = Font(name=FT, size=10, color=ROTULO)
    c.alignment = Alignment(wrap_text=True, vertical="top")

r = 5 + len(META) + 1
ws.cell(r, 2, "Proveniência dos dados").font = Font(name=FT, size=10, bold=True, color=SECAO)
c = ws.cell(r + 1, 2,
    "Todos os números do artigo são reproduzíveis a partir dos CSVs de resultado em "
    "pesquisa/outputs/ (versionados no git), transcritos aqui aba a aba, e recomputados por "
    "fórmula na aba 12_Verificacao. As matrizes-fonte cruas (MIP ES–RB 2008/2015, séries do "
    "Nível 68, planilhas do IJSN/CECEG) NÃO estão no repositório — ficam na máquina do autor. "
    "Portanto esta auditoria confere os resultados publicados contra os artefatos derivados "
    "versionados; a re-execução do zero dos scripts exige re-suprir as matrizes-fonte.")
c.font = Font(name=FT, size=9.5, color=ROTULO)
c.alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells(start_row=r + 1, start_column=2, end_row=r + 1, end_column=3)
ws.row_dimensions[r + 1].height = 58

r += 3
ws.cell(r, 2, "Guia das abas").font = Font(name=FT, size=10, bold=True, color=SECAO)
hr = r + 1
for j, rot in enumerate(("Aba", "Conteúdo")):
    c = ws.cell(hr, 2 + j, rot)
    c.font = Font(name=FT, size=9, bold=True, color=ROTULO)
    c.fill = PatternFill("solid", fgColor=F_CAB)
    c.border = fio(FIO_FORTE)
    c.alignment = Alignment(horizontal="center", vertical="center")
for i, (nome, desc) in enumerate(ABAS):
    rr = hr + 1 + i
    for j, v in enumerate((nome, desc)):
        c = ws.cell(rr, 2 + j, v)
        c.font = Font(name=FT, size=9, bold=(j == 0), color=TITULO if j == 0 else CORPO)
        c.border = fio()
        c.alignment = Alignment(wrap_text=True, vertical="center")
        if i % 2 == 1:
            c.fill = PatternFill("solid", fgColor=F_ZEBRA)

r = hr + len(ABAS) + 3
ws.cell(r, 2, "Legenda de células").font = Font(name=FT, size=10, bold=True, color=SECAO)
LEGENDA = [
    (F_ENTRADA, AZUL,  True,  "Amarelo-pastel, texto azul — entrada editável (parâmetros de cenário)"),
    (F_PARAM,   CORPO, False, "Cinza-quente — parâmetro lido da MIP ou do CSV de origem"),
    (F_SINTESE, TITULO, True, "Verde-pastel — linhas-síntese, totais e médias"),
    (None,      CORPO, False, "Sem preenchimento — fórmula viva sobre as abas de dados"),
]
for i, (fill, tinta, bold, txt) in enumerate(LEGENDA):
    rr = r + 1 + i
    c = ws.cell(rr, 2, "célula")
    c.font = Font(name=FT, size=9, bold=bold, color=tinta)
    c.border = fio()
    c.alignment = Alignment(horizontal="center")
    if fill:
        c.fill = PatternFill("solid", fgColor=fill)
    d = ws.cell(rr, 3, txt)
    d.font = Font(name=FT, size=10, color=ROTULO)

# ============================================================== 01_Setores ======
ws = wb.create_sheet("01_Setores")
h = moldura(ws, "Resultados setoriais do ES (26 setores, 2008)",
    "Fonte: 01_es_br_base.py → outputs/es_setores_resultados.csv. Vazamento = parcela do "
    "multiplicador que se realiza fora do ES. Ligações de Rasmussen-Hirschman: para trás pela "
    "inversa de Leontief, para frente pela inversa de Ghosh.",
    ["As duas últimas linhas são fórmulas: média simples e média ponderada pelo VBP.",
     "Vazamento médio de produção: 24,9% (simples) e 22,9% (ponderado) — os dois valores do artigo."], 10)
D0 = h + 1
D1 = D0 + len(setores) - 1
linhas = [[r["setor"], f(r, "mult_producao"), f(r, "retido_ES"), f(r, "vazado_RB"),
           f(r, "vazamento_prod_%"), f(r, "mult_emprego"), f(r, "vazamento_emprego_%"),
           f(r, "ligacao_tras"), f(r, "ligacao_frente"), f(r, "VBP")] for r in setores]
COLS = "CDEFGHIJ"
linhas.append(["Média (simples)"] + [f"=AVERAGE({c}{D0}:{c}{D1})" for c in COLS] + [f"=SUM(K{D0}:K{D1})"])
linhas.append(["Média (ponderada pelo VBP)"] +
              [f"=SUMPRODUCT({c}{D0}:{c}{D1},$K${D0}:$K${D1})/SUM($K${D0}:$K${D1})" for c in COLS] + [None])
tabela(ws, h, [("Setor", None, "left"), ("Mult. produção", MULT, "right"),
    ("Retido no ES", MULT, "right"), ("Vazado p/ RB", MULT, "right"),
    ("Vazam. produção (%)", PCT, "right"), ("Mult. emprego", MI, "right"),
    ("Vazam. emprego (%)", PCT, "right"), ("Ligação trás", MULT, "right"),
    ("Ligação frente", MULT, "right"), ("VBP (R$ mi)", MI, "right")],
    linhas, {"B": 40, "C": 12, "D": 11, "E": 11, "F": 12, "G": 12, "H": 12, "I": 10, "J": 10, "K": 13},
    realce={len(setores): F_SINTESE, len(setores) + 1: F_SINTESE})
SET_D0, SET_D1 = D0, D1

# ======================================================= 02_Multiplicadores =====
ws = wb.create_sheet("02_Multiplicadores")
h = moldura(ws, "Multiplicadores dos 26 setores do ES, tipos I e II (2008)",
    "Fonte: 17_caracterizacao_es_2008.py → outputs/es_caracterizacao_2008.csv. Tipo II fecha o "
    "modelo para as famílias do ES. Emprego em ocupações por R$ 1 milhão de demanda final; renda "
    "em R$ por R$ 1. PTL = ligação pura total padronizada pela média dos 26 setores.",
    ["Fonte da Tabela 1 do artigo, gerada por 27_tab_multiplicadores.py.",
     "A linha de média é fórmula: produção 1,76/2,45; emprego 27,9/40,4; renda 0,289/0,362."], 11)
M0 = h + 1
M1 = M0 + len(caract) - 1
ordem = sorted(caract, key=lambda r: -f(r, "mult_prod_I"))
linhas = [[r["setor"], f(r, "mult_prod_I"), f(r, "mult_prod_II"),
           f(r, "mult_emp_I") / 1e6, f(r, "mult_emp_II") / 1e6,
           f(r, "mult_renda_I"), f(r, "mult_renda_II"),
           f(r, "lig_tras"), f(r, "lig_frente"), f(r, "PTL_idx"),
           "sim" if r["chave_RH"].strip() in ("1", "1.0") else "—"] for r in ordem]
linhas.append(["Média (simples)"] + [f"=AVERAGE({c}{M0}:{c}{M1})" for c in "CDEFGHIJK"] + [None])
tabela(ws, h, [("Setor", None, "left"), ("Produção I", MULT, "right"), ("Produção II", MULT, "right"),
    ("Emprego I", MI, "right"), ("Emprego II", MI, "right"), ("Renda I", MULT, "right"),
    ("Renda II", MULT, "right"), ("Ligação trás", MULT, "right"), ("Ligação frente", MULT, "right"),
    ("PTL (padron.)", MULT, "right"), ("Setor-chave", None, "center")],
    linhas, {"B": 40, "C": 10, "D": 10, "E": 10, "F": 10, "G": 9, "H": 9, "I": 10, "J": 10, "K": 11, "L": 10},
    realce={len(caract): F_SINTESE})
MUL_D0, MUL_D1 = M0, M1

# ========================================================= 03_DemandaFinal =====
ws = wb.create_sheet("03_DemandaFinal")
h = moldura(ws, "Quem puxa a economia: decomposição pela demanda final (2008)",
    "Fonte: 25_decomposicao_fd.py → outputs/decomposicao_fd.csv, via x⁽ᵏ⁾ = B·y⁽ᵏ⁾. A aditividade "
    "é exata: a soma dos componentes reproduz produção e emprego totais.",
    ["A linha TOTAL e a linha-síntese são fórmulas, não constantes copiadas.",
     "Demanda externa ao estado = 61,75% da produção e 47,50% do emprego (headline do artigo: 61,7 e 47,5)."], 5)
comp = [r for r in decomp if r["componente"] != "TOTAL"]
C0 = h + 1
C1 = C0 + len(comp) - 1
CT = C1 + 1  # linha do TOTAL
# As colunas de percentual sao CALCULADAS sobre a coluna de valor, nao copiadas do CSV:
# somar os percentuais ja arredondados do CSV daria um TOTAL de 100,01.
linhas = [[r["componente"], f(r, "producao_mi"), f"=C{C0+i}/C${CT}*100",
           f(r, "emprego"), f"=E{C0+i}/E${CT}*100"] for i, r in enumerate(comp)]
linhas.append(["TOTAL", f"=SUM(C{C0}:C{C1})", f"=SUM(D{C0}:D{C1})",
               f"=SUM(E{C0}:E{C1})", f"=SUM(F{C0}:F{C1})"])
linhas.append([f"Demanda externa ao estado (linhas {C0}+{C0+1})",
               f"=C{C0}+C{C0+1}", f"=D{C0}+D{C0+1}", f"=E{C0}+E{C0+1}", f"=F{C0}+F{C0+1}"])
tabela(ws, h, [("Componente da demanda final", None, "left"), ("Produção (R$ mi)", MI, "right"),
    ("Produção (%)", PCT, "right"), ("Emprego (ocupações)", EMP, "right"), ("Emprego (%)", PCT, "right")],
    linhas, {"B": 44, "C": 16, "D": 13, "E": 18, "F": 13},
    realce={len(comp): F_SINTESE, len(comp) + 1: F_SINTESE})
FD_TOT, FD_EXT = C1 + 1, C1 + 2

# ============================================================== 04_Cluster =====
ws = wb.create_sheet("04_Cluster")
h = moldura(ws, "Benchmark: o ES entre os estados de crescimento dinâmico (2008)",
    "Fonte da Tabela 3 do artigo: 10_cluster_setorial.py → outputs/cluster_setorial.csv (PIB, "
    "vazamento, setor dominante) unido por UF a 22_benchmark_caracterizacao.py → "
    "outputs/benchmark_caracterizacao.csv (base, multiplicadores, ligação, líder÷média). Os "
    "indicadores do benchmark são médias PONDERADAS PELA PRODUÇÃO sobre a matriz INTERESTADUAL; "
    "diferem, por isso, das médias simples bi-regionais da aba 01 (1,76 e 27,9). "
    "'Base/commodity' inclui Alimentos — escolha declarada, que eleva a parcela de todos os estados.",
    ["O ES é o 2º mais intensivo em setores de base (36,42%), atrás só de Mato Grosso.",
     "Nos indicadores neutros à composição o ES é exatamente mediano: mult. de produção 1,6582 e "
     "ligação para trás 0,9211 são a própria mediana das 27 UFs."], 10)
CL0 = h + 1
linhas = []
for r in clus_set:
    b = bench.get(r["estado"], {})
    linhas.append([r["estado"], r["grupo"], f(r, "pib_share_%"), f(r, "vazamento_%"),
                   f(b, "base_pct") if b else None, f(b, "mult_producao") if b else None,
                   f(b, "emprego_Rmi") if b else None, f(b, "ligacao_tras") if b else None,
                   f(b, "dom_emp_gap") if b else None, r["setor_dominante"]])
i_es = next(i for i, r in enumerate(clus_set) if r["estado"] == "ES")
tabela(ws, h, [("Estado", None, "center"), ("Grupo", None, "center"), ("PIB (%)", PCT, "right"),
    ("Vazamento (%)", PCT, "right"), ("Base/commodity (%)", PCT, "right"),
    ("Mult. produção (pond.)", MULT, "right"), ("Mult. emprego (pond.)", PCT, "right"),
    ("Ligação trás (pond.)", MULT, "right"), ("Líder ÷ média", MULT, "right"),
    ("Setor dominante", None, "left")],
    linhas, {"B": 9, "C": 11, "D": 10, "E": 13, "F": 16, "G": 15, "H": 15, "I": 14, "J": 12, "K": 22},
    realce={i_es: F_SINTESE})
CLU_ES = CL0 + i_es

# ============================================================== 05_Estados =====
ws = wb.create_sheet("05_Estados")
h = moldura(ws, "As 27 UFs: cluster, vazamento e abertura (2008)",
    "Fontes: 04_cluster.py e 02_interestadual.py → outputs/cluster.csv, estados_abertura.csv e "
    "cluster_resumo.csv. 'es_spillover_%' é a parcela do spillover do ES absorvida por cada UF.",
    ["O ES não recebe spillover de si mesmo — a linha do ES tem 0 na última coluna.",
     "Métricas-resumo do cluster na tabela lateral, à direita."], 6)
E0 = h + 1
E1 = E0 + len(clus_uf) - 1
linhas = []
for r in clus_uf:
    b = bench.get(r["estado"], {})
    linhas.append([r["estado"], r["cluster"] or "—", f(r, "pib_share_2008_%"), f(r, "vazamento_%"),
                   int(f(r, "rank_abertura")), f(r, "es_spillover_%"),
                   f(b, "base_pct") if b else None, f(b, "mult_producao") if b else None,
                   f(b, "emprego_Rmi") if b else None, f(b, "ligacao_tras") if b else None,
                   f(b, "dom_emp_gap") if b else None])
i_es2 = next(i for i, r in enumerate(clus_uf) if r["estado"] == "ES")
linhas.append(["Mediana (27 UFs)", None, None, None, None, None] +
              [f"=MEDIAN({c}{E0}:{c}{E1})" for c in "HIJKL"])
tabela(ws, h, [("Estado", None, "center"), ("Cluster", None, "center"), ("PIB 2008 (%)", PCT, "right"),
    ("Vazamento (%)", PCT, "right"), ("Rank abertura", EMP, "center"),
    ("Spillover do ES (%)", PCT, "right"), ("Base/commodity (%)", PCT, "right"),
    ("Mult. produção (pond.)", MULT, "right"), ("Mult. emprego (pond.)", PCT, "right"),
    ("Ligação trás (pond.)", MULT, "right"), ("Líder ÷ média", MULT, "right")],
    linhas, {"B": 14, "C": 9, "D": 12, "E": 13, "F": 12, "G": 16, "H": 16, "I": 15, "J": 15, "K": 14, "L": 12},
    realce={i_es2: F_SINTESE, len(clus_uf): F_SINTESE})
UF_MED = E1 + 1
ROT = {"es_spill_cluster": "ES → demais pares do cluster (%)",
       "es_spill_nucleo": "ES → núcleo SP+RJ (%)", "es_spill_resto": "ES → resto do país (%)",
       "bloco_dentro": "Bloco: dentro do cluster (%)", "bloco_nucleo": "Bloco: núcleo (%)",
       "bloco_resto": "Bloco: resto (%)", "pib_share_cluster_2008": "PIB do cluster 2008 (%)",
       "pib_share_nucleo_2008": "PIB do núcleo 2008 (%)",
       "es_spill_total_mi": "Spillover total do ES (R$ mi)",
       "es_retido_mi": "Produção retida no ES (R$ mi)"}
for j, rot in enumerate(("Métrica-resumo do cluster", "Valor")):
    c = ws.cell(h, 14 + j, rot)
    c.font = Font(name=FT, size=9, bold=True, color=ROTULO)
    c.fill = PatternFill("solid", fgColor=F_CAB)
    c.border = fio(FIO_FORTE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for i, r in enumerate(clus_res):
    rr = h + 1 + i
    a = ws.cell(rr, 14, ROT.get(r["metrica"], r["metrica"]))
    b = ws.cell(rr, 15, f(r, "valor_pct"))
    b.number_format = MI if r["metrica"].endswith("_mi") else PCT
    for c in (a, b):
        c.font = Font(name=FT, size=9, color=CORPO)
        c.border = fio()
        c.fill = PatternFill("solid", fgColor=F_PARAM)
        c.alignment = Alignment(vertical="center", horizontal="right" if c is b else "left")
ws.column_dimensions["N"].width = 32
ws.column_dimensions["O"].width = 13

# ============================================================ 06_Spillover =====
ws = wb.create_sheet("06_Spillover")
h = moldura(ws, "Assimetria spillover / feedback — agregados (2008)",
    "Fontes: 01_es_br_base.py e 13_audit_contrafactual.py → outputs/audit_contrafactual.csv "
    "(cenário Baseline) e cluster_resumo.csv. Valores em R$ milhões de 2008.",
    ["As três últimas linhas são razões calculadas por fórmula sobre as de cima.",
     "O feedback é 0,32% da injeção — a interdependência é quase unilateral."], 3)
S0 = h + 1
INJ, SPI, RET, FBK = S0, S0 + 1, S0 + 3, S0 + 4
linhas = [
    ["Injeção na demanda final do ES (R$ mi)", 51483.42917956512, "f^ES por produtos do ES (cenário Baseline)"],
    ["Spillover — produção induzida no RB (R$ mi)", 18162.84947285308, "recorte bi-regional"],
    ["Spillover total do ES (R$ mi) — recorte interestadual", 18122.9, "cluster_resumo; é o valor do Sankey"],
    ["Produção retida no ES (R$ mi)", 63727.2, "cluster_resumo"],
    ["Feedback — retorno ao ES via RB (R$ mi)", 163.645887585044, "ordens de grandeza abaixo do spillover"],
    ["Feedback ÷ injeção (%)", f"=C{FBK}/C{INJ}*100", "headline do artigo: 0,32%"],
    ["Spillover ÷ injeção (%)", f"=C{SPI}/C{INJ}*100", "headline do artigo: 35% da injeção"],
    ["Produção retida (%) = retido ÷ (retido + spillover total)",
     f"=C{RET}/(C{RET}+C{RET-1})*100", "78% fica no ES / 22% vaza"],
]
tabela(ws, h, [("Métrica", None, "left"), ("Valor", MULT, "right"), ("Observação", None, "left")],
    linhas, {"B": 52, "C": 16, "D": 46}, realce={5: F_SINTESE, 6: F_SINTESE, 7: F_SINTESE})
SPI_FBK_PCT = S0 + 5

# ============================================================== 07_Destino =====
ws = wb.create_sheet("07_Destino")
h = moldura(ws, "Destino interestadual do spillover do ES (2008)",
    "Fonte: 02_interestadual.py → outputs/es_spillover_destino.csv. As 26 UFs receptoras "
    "(o ES não figura, por não receber spillover de si mesmo). 'Pegada total' inclui os efeitos "
    "de segunda ordem.",
    ["As duas linhas-síntese somam por fórmula as UFs do Sudeste e do núcleo SP–RJ.",
     "Sudeste (excl. ES) absorve 65,44%; o núcleo São Paulo–Rio, 52,50%."], 4)
T0 = h + 1
linhas = [[r["regiao"], f(r, "spillover_RS_mi"), f(r, "pct_spillover"), f(r, "pegada_total_RS_mi")]
          for r in destino]
pos = {r["regiao"]: T0 + i for i, r in enumerate(destino)}
mg, rj, sp = pos["MG"], pos["RJ"], pos["SP"]
linhas.append(["Sudeste excl. ES (MG+RJ+SP)", f"=C{mg}+C{rj}+C{sp}",
               f"=D{mg}+D{rj}+D{sp}", f"=E{mg}+E{rj}+E{sp}"])
linhas.append(["Núcleo SP+RJ", f"=C{rj}+C{sp}", f"=D{rj}+D{sp}", f"=E{rj}+E{sp}"])
tabela(ws, h, [("UF de destino", None, "center"), ("Spillover (R$ mi)", MI, "right"),
    ("% do spillover", PCT, "right"), ("Pegada total (R$ mi)", MI, "right")],
    linhas, {"B": 26, "C": 17, "D": 15, "E": 19},
    realce={len(destino): F_SINTESE, len(destino) + 1: F_SINTESE})
DES_SUD, DES_NUC = T0 + len(destino), T0 + len(destino) + 1

# ================================================================ 08_Micro =====
ws = wb.create_sheet("08_Micro")
h = moldura(ws, "Multiplicadores e retenção territorial por microrregião (2015)",
    "Fontes: 24_micro_mult_chave.py → outputs/micro_multiplicadores.csv e a extração hipotética "
    "de outputs/extracao_hipotetica.csv. Retenção = parcela do multiplicador que se realiza dentro "
    "da própria microrregião, pela razão das somas ponderadas.",
    ["A metrópole retém 90,88% do multiplicador; o Litoral Sul extrativo, 66,2%.",
     "Removida a Metropolitana do sistema, a produção das demais cairia 12,98%."], 7)
MI0 = h + 1
linhas = [[r["regiao"], r["nome"], f(r, "share_VBP_pct"), f(r, "mult_prod_simples"),
           f(r, "mult_prod_pond"), f(r, "retencao_intra_pct"), f(r, "mult_renda_pond")]
          for r in micro]
fim = tabela(ws, h, [("Região", None, "center"), ("Microrregião", None, "left"),
    ("% do VBP do ES", PCT, "right"), ("Mult. produção (simples)", MULT, "right"),
    ("Mult. produção (ponderado)", MULT, "right"), ("Retenção intra (%)", PCT, "right"),
    ("Mult. renda (ponderado)", MULT, "right")],
    linhas, {"B": 9, "C": 22, "D": 13, "E": 15, "F": 16, "G": 13, "H": 15},
    realce={0: F_SINTESE})
MIC_METRO = MI0
MIC_LITORAL = MI0 + next(i for i, r in enumerate(micro) if "Litoral" in r["nome"])

hr = fim + 2
ws.cell(hr, 2, "Extração hipotética da Região Metropolitana").font = Font(
    name=FT, size=10, bold=True, color=SECAO)
for j, rot in enumerate(("Experimento", "Região extraída", "Injeção (R$ mi)", "Perda na periferia (%)")):
    c = ws.cell(hr + 1, 2 + j, rot)
    c.font = Font(name=FT, size=9, bold=True, color=ROTULO)
    c.fill = PatternFill("solid", fgColor=F_CAB)
    c.border = fio(FIO_FORTE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for j, v in enumerate((hem["experimento"], hem["regiao_extraida"],
                       f(hem, "injecao_mi"), f(hem, "perda_producao_periferia_pct"))):
    c = ws.cell(hr + 2, 2 + j, v)
    c.font = Font(name=FT, size=9, color=CORPO)
    c.border = fio()
    c.fill = PatternFill("solid", fgColor=F_PARAM)
    if j >= 2:
        c.number_format = MI if j == 2 else PCT
        c.alignment = Alignment(horizontal="right")
HEM_CEL = f"'08_Micro'!E{hr + 2}"

# ============================================================= 09_Micro_LQ =====
ws = wb.create_sheet("09_Micro_LQ")
h = moldura(ws, "Quociente locacional por setor e microrregião (2015)",
    "Fonte: 20_caracterizacao_micro.py → outputs/micro_LQ.csv. LQ acima da unidade indica que o "
    "setor se concentra no território mais do que na média estadual. Base da Figura 3 do artigo.",
    ["As especializações citadas no artigo: celulose no Rio Doce, minério no Litoral Sul, "
     "têxtil no Centro-Oeste, pecuária na Central Serrana.",
     "'Rochas ornamentais' do texto corresponde a Minerais não-metálicos no Central Sul."], 11)
LQ0 = h + 1
micros = lq[0][1:]
linhas = [[r[0]] + [float(x) for x in r[1:]] for r in lq[1:]]
tabela(ws, h, [("Setor", None, "left")] + [(m, MULT, "right") for m in micros], linhas,
    {"B": 26, **{get_column_letter(3 + i): 11 for i in range(len(micros))}})
lq_row = {r[0]: LQ0 + i for i, r in enumerate(lq[1:])}
lq_col = {m: get_column_letter(3 + i) for i, m in enumerate(micros)}

# =========================================================== 10_Trajetoria =====
ws = wb.create_sheet("10_Trajetoria")
h = moldura(ws, "Setores de base do ES na estrutura nacional, 2010–2021",
    "Fonte: 18_trajetoria_n68.py → outputs/trajetoria_n68.csv (série Nível 68, preços correntes). "
    "É a tendência DOS SETORES no país, não da estrutura capixaba: o ES tem apenas as âncoras de "
    "2008 e 2015. Base da Figura 2 do artigo.",
    ["Celulose e papel é o setor-chave mais consistente: ligação para trás de 1,4073 a 1,5056.",
     "Petróleo/gás e minério de ferro ficam abaixo da unidade em quase todo o período — enclaves."], 13)
anos = sorted({int(r["ano"]) for r in traj})
ss = ["Celulose/papel", "Metalurgia/sider.", "Refino", "Petróleo/gás", "Minério de ferro"]
val = {(r["setor"], int(r["ano"])): r for r in traj}
TR0 = h + 1
linhas = [[s] + [f(val[(s, a)], "ligacao_tras") for a in anos] for s in ss]
fim = tabela(ws, h, [("Setor (ligação para trás)", None, "left")] + [(str(a), MULT, "right") for a in anos],
    linhas, {"B": 24, **{get_column_letter(3 + i): 8.5 for i in range(len(anos))}})
tr_row = {s: TR0 + i for i, s in enumerate(ss)}
hr = fim + 2
linhas2 = [[s] + [f(val[(s, a)], "mult_producao") for a in anos] for s in ss]
tabela(ws, hr, [("Setor (multiplicador de produção)", None, "left")] + [(str(a), MULT, "right") for a in anos],
    linhas2, {}, zebra=True)
tr2_row = {s: hr + 1 + i for i, s in enumerate(ss)}
ws.freeze_panes = ws.cell(TR0, 2).coordinate
COL_2010 = get_column_letter(3 + anos.index(2010))
COL_2021 = get_column_letter(3 + anos.index(2021))

# ========================================================== 11_Camada2015 =====
PROSA = {
 "11_Camada2015": (
  "Camada de atualização 2015 — regionalização CILQ (registro de auditoria)",
  "Fonte: dados/README.md (nota metodológica + auditoria jun/2026). Os dados brutos de 2015 estão "
  "ausentes do repositório: esta aba é registro documental, não recomputação.",
  ["Item", "Descrição", "Status/valor"],
  [["Método", "CILQ (Guilhoto & Sesso Filho, 2005) sobre os totais domésticos ES e RB; só o split de origem é estimado; SLQ para a demanda final", ""],
   ["Dimensão", "matriz 70×70 (35 setores × 2 regiões), não negativa", "OK"],
   ["Soma de A por coluna", "∈ [0; 0,97] — < 1, condição de Hawkins-Simon", "OK"],
   ["Inversa de Leontief", "B = (I−A)⁻¹ ≥ 0", "OK"],
   ["Validação externa", "Z_LM estimado (ES→uso intermediário no RB) vs 'Exportação Regional' observada na planilha do ES", "correlação 0,97"],
   ["Vazamento médio (colunas ES, ponderado)", "12,8%", "resultado 2015"],
   ["Comparador 2008 correto", "22,9% ponderado (mesma agregação, modelo bi-regional) — NÃO os 24,9% (média simples)", "correção hard-mode"],
   ["Viés do CILQ puro", "sem a correção FLQ (Flegg, Webber & Elliott 1995; Flegg & Webber 2000) o CILQ subestima o vazamento quanto menor a região; ES ~2% do PIB → 12,8% é limite inferior", "limitação declarada"],
   ["Situação dos dados", "as matrizes brutas de 2015 NÃO estão no container — registro documental da auditoria", "documental"]],
  {"B": 34, "C": 84, "D": 20}),
 "13_Integridade": (
  "Integridade contábil e reprodutibilidade",
  "Fontes: pesquisa/AUDITORIA.md (B1–B5) e pesquisa/AUDITORIA_HARD.md (§0, §3).",
  ["Verificação", "Resultado", "Fonte"],
  [["Identidade contábil", "VBP = soma da linha da MIP — erro máximo 0,00%", "AUDITORIA.md B1 / HARD §0"],
   ["Coeficientes válidos (Hawkins-Simon)", "Soma de A por coluna < 1: 0,748 (bi-regional) / 0,895 (interestadual)", "AUDITORIA.md B1"],
   ["Inversa de Leontief não negativa", "B = (I−A)⁻¹ ≥ 0 em todas as matrizes", "AUDITORIA.md B1"],
   ["Cross-validação", "Injeção (R$ 51,5 bi) e spillover (R$ 18,2 bi) batem entre o recorte bi-regional (01) e o interestadual (02)", "AUDITORIA.md B1"],
   ["Reprodução do zero", "os números-título regeneram do zero e conferem (vazamento 24,9/22,8; spillover; feedback)", "AUDITORIA_HARD §0"],
   ["Robustez do feedback", "Feedback ≈ 0 invariante à convenção adotada — banda 0,15–0,32%", "AUDITORIA.md B5 / HARD §3"],
   ["Convenção adotada", "Miller-Blair V3 (inversa particionada). O paper-semente (60,6/22,4/0,199) não reproduz; V3 dá 51,5/18,2/164", "06_reconciliacao.py"],
   ["Setor S23 do sistema microrregional", "coluna soma 1,07 (herança da regionalização); excluído, o vazamento da Metropolitana passa de 8,4% para 7,9% e a ordenação da retenção não muda", "Apêndice B.1 do artigo"],
   ["Ligações R-H", "Para trás pela inversa de Leontief; para frente pela inversa de Ghosh (corrigido)", "AUDITORIA.md B2/B4"]],
  {"B": 34, "C": 84, "D": 26}),
 "14_Referencias": (
  "Integridade das referências (protocolo B7)",
  "Fontes: pesquisa/AUDITORIA.md §B7 e pesquisa/AUDITORIA_HARD.md §1. Verificam-se aqui as "
  "referências que sustentam números do artigo; as entradas de Antràs et al. e de Timmer et al. "
  "saíram da lista final junto com a camada de upstreamness, e por isso não figuram mais.",
  ["Referência", "Detalhe bibliográfico", "Veredito", "Observação"],
  [["Guilhoto & Sesso Filho (2005)", "Economia Aplicada, 9(2), 277–299", "VERIFICADA", "confere"],
   ["Isard (1951)", "The Review of Economics and Statistics, 33(4), 318–328", "VERIFICADA", "confere"],
   ["Miller & Blair (2009)", "Input-Output Analysis, 2ª ed., Cambridge UP (ISBN 9780521517133)", "VERIFICADA", "confere"],
   ["Haddad, Gonçalves Jr. & Nascimento (2017)", "Revista Brasileira de Estudos Regionais e Urbanos, 11(4), 424–446", "CORRIGIDA (GRAVE)", "citava 'inter-regional...ES...Working paper'; é a matriz INTERESTADUAL / BRASIL / artigo em revista (27 estados)"],
   ["→ comparador 27,4% de Haddad", "parcela inter-regional do multiplicador total do ES = 27,4% (Tabela 2, p. 440)", "VERIFICADO", "era UNVERIFIABLE_ACCESS no B7; confirmado contra o PDF em AUDITORIA_HARD §1"],
   ["Ribeiro et al. (2024)", "RBERU, 18(4), 596–622 — DOI 10.54766/rberu.v18i4.1111", "VERIFICADA", "mesma matriz de 2015 regionalizada; contraste da §6"],
   ["Sessa et al. (2017)", "Economia e Desenvolvimento, 28(2) — DOI 10.5902/1414650921397", "VERIFICADA", "matriz capixaba; impacto de Ubu"]],
  {"B": 34, "C": 60, "D": 18, "E": 62}),
 "15_Defeitos": (
  "Defeitos encontrados na auditoria e status das correções",
  "Fonte: pesquisa/AUDITORIA_HARD.md §2 e §5. Nenhum defeito corrompe número publicado. Os itens "
  "B e E dizem respeito à camada de upstreamness/WIOD, que a revisão final do artigo abandonou — "
  "ficam registrados como histórico do processo.",
  ["ID", "Severidade", "Descrição", "Status"],
  [["A", "🔴 Grave", "Citação de Haddad (título/escopo/tipo errados no .tex)", "APLICADO — entrada corrigida"],
   ["B", "🟠 Médio", "WIOD (Timmer 2015) na bibliografia mas nunca citado no corpo, sendo a fonte de toda a camada de upstreamness", "APLICADO na época; a camada saiu da revisão final"],
   ["C", "🟠 Médio", "src/io_core.py com código morto/incorreto: feedback ≡ 0 por construção; ligação para-frente por Leontief", "APLICADO — corrigido (feedback 163,6 mi)"],
   ["D", "🟠 Médio", "02_interestadual.py aborta no console cp1252 (UnicodeEncodeError no 'Σ') antes de gravar os CSVs", "APLICADO — guarda reconfigure('utf-8') propagada"],
   ["E", "🟡 Menor", "Distribuição global do WIOD contaminada (49/2464 com demanda final < 0)", "APLICADO na época; a camada saiu da revisão final"],
   ["F", "🟡 Menor", "13_audit_contrafactual.py com verdicts hard-coded; magnitudes de 2 cenários exageradas na narrativa", "APLICADO — verdicts tornados condicionais"],
   ["G", "🟢 Cosmético", "Arredondamentos/rótulos: spillover 18,1 (Sankey) vs 18,2; 65 vs 65,4; 61,7 vs 61,8 na soma das parcelas", "documentado (não é erro)"],
   ["H", "🟢 Declarado", "Escolhas de definição: 'base/commodity' inclui Alimentos; PIB por valor adicionado", "declarado/transparente"],
   ["I", "🟠 Médio", "a versão anterior desta pasta auditava a revisão antiga do artigo (§4.1–§4.5, upstreamness) e não cobria os números da versão final", "APLICADO — abas e verificação sincronizadas nesta edição"]],
  {"B": 6, "C": 15, "D": 78, "E": 44}),
}
for nome in ("11_Camada2015", "13_Integridade", "14_Referencias", "15_Defeitos"):
    tit, nota, cab, dados, larg = PROSA[nome]
    ws = wb.create_sheet(nome)
    h = moldura(ws, tit, nota, [], len(cab))
    tabela(ws, h, [(c, None, "center" if i == 0 and len(c) < 4 else "left")
                   for i, c in enumerate(cab)], dados, larg)

# ========================================================= 12_Verificacao =====
ws = wb.create_sheet("12_Verificacao")
h = moldura(ws, "Verificação número-a-número: artigo ↔ fonte",
    "Cada afirmação do artigo, o valor publicado, a aba-fonte, o valor RECOMPUTADO POR FÓRMULA "
    "sobre essa aba, o desvio e o status. Critério: ✓ bate (|Δ| ≤ 0,05) · ~ arredondamento "
    "(|Δ| ≤ 0,6, esperado por casas decimais ou por duas agregações) · ⚑ verificar.",
    ["As colunas 'Recomputado', 'Δ' e 'Status' são fórmulas vivas: mudando a aba-fonte, mudam aqui.",
     "Seções conforme a revisão final: §4 retrato · §5 panorama · §6 território · §7 plataforma."], 7)
S = "'01_Setores'"; M = "'02_Multiplicadores'"; D = "'03_DemandaFinal'"
C = "'04_Cluster'"; T = "'07_Destino'"; MC = "'08_Micro'"; L = "'09_Micro_LQ'"; TR = "'10_Trajetoria'"
CLAIMS = [
 ("§7", "Vazamento médio de produção (média simples)", 24.9,
  "01_Setores · AVERAGE da coluna F", f"=AVERAGE({S}!F{SET_D0}:F{SET_D1})"),
 ("§7", "Vazamento médio de produção (ponderado pelo VBP)", 22.9,
  "01_Setores · SUMPRODUCT(F;VBP)/SUM(VBP)",
  f"=SUMPRODUCT({S}!F{SET_D0}:F{SET_D1},{S}!K{SET_D0}:K{SET_D1})/SUM({S}!K{SET_D0}:K{SET_D1})"),
 ("§7", "Serviços imobiliários — vazamento de produção", 5.2,
  "01_Setores · linha do setor", f"=INDEX({S}!F{SET_D0}:F{SET_D1},MATCH(\"Serviços imobiliários e aluguel\",{S}!B{SET_D0}:B{SET_D1},0))"),
 ("§7", "Alimentos — vazamento de produção", 37.4,
  "01_Setores · linha do setor", f"=INDEX({S}!F{SET_D0}:F{SET_D1},MATCH(\"Alimentos, bebidas e fumo\",{S}!B{SET_D0}:B{SET_D1},0))"),
 ("§7", "Refino — vazamento de emprego", 61.6,
  "01_Setores · linha do setor", f"=INDEX({S}!H{SET_D0}:H{SET_D1},MATCH(\"Refino de petróleo, coque e álcool\",{S}!B{SET_D0}:B{SET_D1},0))"),
 ("§7", "Metalurgia — vazamento de emprego", 49.3,
  "01_Setores · linha do setor", f"=INDEX({S}!H{SET_D0}:H{SET_D1},MATCH(\"Metalurgia\",{S}!B{SET_D0}:B{SET_D1},0))"),
 ("§4 / Tab.1", "Multiplicador de produção médio, tipo I", 1.76,
  "02_Multiplicadores · AVERAGE", f"=AVERAGE({M}!C{MUL_D0}:C{MUL_D1})"),
 ("§4 / Tab.1", "Multiplicador de produção médio, tipo II", 2.45,
  "02_Multiplicadores · AVERAGE", f"=AVERAGE({M}!D{MUL_D0}:D{MUL_D1})"),
 ("§4 / Tab.1", "Multiplicador de emprego médio, tipo I", 27.9,
  "02_Multiplicadores · AVERAGE", f"=AVERAGE({M}!E{MUL_D0}:E{MUL_D1})"),
 ("§4 / Tab.1", "Multiplicador de emprego médio, tipo II", 40.4,
  "02_Multiplicadores · AVERAGE", f"=AVERAGE({M}!F{MUL_D0}:F{MUL_D1})"),
 ("§4", "Mineração — ligação pura total padronizada", 4.4,
  "02_Multiplicadores · coluna PTL", f"=INDEX({M}!K{MUL_D0}:K{MUL_D1},MATCH(\"Mineração\",{M}!B{MUL_D0}:B{MUL_D1},0))"),
 ("§4", "Metalurgia — ligação pura total padronizada", 3.4,
  "02_Multiplicadores · coluna PTL", f"=INDEX({M}!K{MUL_D0}:K{MUL_D1},MATCH(\"Metalurgia\",{M}!B{MUL_D0}:B{MUL_D1},0))"),
 ("§4 / Tab.2", "Demanda externa ao estado — % da produção", 61.7,
  "03_DemandaFinal · linha-síntese", f"={D}!D{FD_EXT}"),
 ("§4 / Tab.2", "Demanda externa ao estado — % do emprego", 47.5,
  "03_DemandaFinal · linha-síntese", f"={D}!F{FD_EXT}"),
 ("§4 / Tab.2", "Produção total do ES (R$ bi)", 104.6,
  "03_DemandaFinal · TOTAL ÷ 1000", f"={D}!C{FD_TOT}/1000"),
 ("§4 / Tab.2", "Emprego total do ES (mil ocupações)", 1611.7,
  "03_DemandaFinal · TOTAL ÷ 1000", f"={D}!E{FD_TOT}/1000"),
 ("§4 / Tab.3", "ES — base/commodity (%)", 36.4,
  "04_Cluster · linha do ES", f"={C}!F{CLU_ES}"),
 ("§4 / Tab.3", "ES — mult. de produção ponderado (interestadual)", 1.66,
  "04_Cluster · linha do ES", f"={C}!G{CLU_ES}"),
 ("§4 / Tab.3", "ES — mult. de emprego ponderado", 25.4,
  "04_Cluster · linha do ES", f"={C}!H{CLU_ES}"),
 ("§4 / Tab.3", "ES — ligação para trás ponderada", 0.92,
  "04_Cluster · linha do ES", f"={C}!I{CLU_ES}"),
 ("§4 / Tab.3", "ES — emprego do líder ÷ média do estado", 0.39,
  "04_Cluster · linha do ES", f"={C}!J{CLU_ES}"),
 ("§4 / Tab.3", "Mediana das 27 UFs — base/commodity (%)", 21.0,
  "05_Estados · MEDIAN da coluna", f"='05_Estados'!H{UF_MED}"),
 ("§4 / Tab.3", "Mediana das 27 UFs — mult. de emprego", 42.5,
  "05_Estados · MEDIAN da coluna", f"='05_Estados'!J{UF_MED}"),
 ("§4 / Tab.3", "Mediana das 27 UFs — líder ÷ média", 0.65,
  "05_Estados · MEDIAN da coluna", f"='05_Estados'!L{UF_MED}"),
 ("§7", "Sudeste excl. ES absorve (%)", 65.4,
  "07_Destino · MG+RJ+SP", f"={T}!D{DES_SUD}"),
 ("§7", "Núcleo SP+RJ absorve (%)", 52.5,
  "07_Destino · RJ+SP", f"={T}!D{DES_NUC}"),
 ("§7", "Feedback ÷ injeção (%)", 0.32,
  "06_Spillover · razão calculada", f"='06_Spillover'!C{SPI_FBK_PCT}"),
 ("§6 / Tab.5", "Metropolitana — retenção do multiplicador (%)", 90.9,
  "08_Micro · linha R1", f"={MC}!G{MIC_METRO}"),
 ("§6 / Tab.5", "Litoral Sul — retenção do multiplicador (%)", 66.2,
  "08_Micro · linha do Litoral Sul", f"={MC}!G{MIC_LITORAL}"),
 ("§6 / Tab.5", "Metropolitana — % do VBP do ES", 62.3,
  "08_Micro · linha R1", f"={MC}!D{MIC_METRO}"),
 ("§6", "Extração da metrópole — perda na periferia (%)", 13.0,
  "08_Micro · extração hipotética", f"={HEM_CEL}"),
 ("§6", "Celulose no Rio Doce — LQ", 8.2,
  "09_Micro_LQ · Celulose e papel × Rio Doce", f"={L}!{lq_col['Rio Doce']}{lq_row['Celulose e papel']}"),
 ("§6", "Minério no Litoral Sul — LQ", 9.5,
  "09_Micro_LQ · Extr. minério de ferro × Litoral Sul", f"={L}!{lq_col['Litoral Sul']}{lq_row['Extr. minério de ferro']}"),
 ("§6", "Têxtil no Centro-Oeste — LQ", 9.6,
  "09_Micro_LQ · Têxtil/vestuário × Centro-Oeste", f"={L}!{lq_col['Centro-Oeste']}{lq_row['Têxtil/vestuário']}"),
 ("§6", "Pecuária na Central Serrana — LQ", 21.9,
  "09_Micro_LQ · Pecuária × Central Serrana", f"={L}!{lq_col['Central Serrana']}{lq_row['Pecuária']}"),
 ("§6", "Rochas ornamentais no Central Sul — LQ", 7.7,
  "09_Micro_LQ · Minerais não-metálicos × Central Sul", f"={L}!{lq_col['Central Sul']}{lq_row['Minerais não-metálicos']}"),
 ("§5 / Fig.2", "Celulose — ligação para trás em 2010", 1.41,
  "10_Trajetoria · Celulose/papel", f"={TR}!{COL_2010}{tr_row['Celulose/papel']}"),
 ("§5 / Fig.2", "Celulose — ligação para trás em 2021", 1.51,
  "10_Trajetoria · Celulose/papel", f"={TR}!{COL_2021}{tr_row['Celulose/papel']}"),
 ("§5", "Celulose — multiplicador de produção em 2010", 2.85,
  "10_Trajetoria · 2º bloco", f"={TR}!{COL_2010}{tr2_row['Celulose/papel']}"),
 ("§5", "Celulose — multiplicador de produção em 2021", 3.05,
  "10_Trajetoria · 2º bloco", f"={TR}!{COL_2021}{tr2_row['Celulose/papel']}"),
 ("§4 / Tab.3", "Participação do ES no PIB nacional (%)", 2.2,
  "04_Cluster · linha do ES (a introdução arredonda para 'cerca de 2%')", f"={C}!D{CLU_ES}"),
]
V0 = h + 1
linhas = []
for i, (loc, claim, art, fonte, form) in enumerate(CLAIMS):
    r = V0 + i
    # ROUND antes de comparar: sem isso, |Δ| = 0,05 cai de um lado ou do outro do
    # limite conforme a representação binaria, e linhas equivalentes saem classificadas
    # de forma diferente.
    linhas.append([loc, claim, art, fonte, form, f"=F{r}-D{r}",
                   f'=IF(ABS(ROUND(G{r},4))<=0.05,"✓",IF(ABS(ROUND(G{r},4))<=0.6,"~","⚑"))'])
fim = tabela(ws, h, [("Local", None, "center"), ("Afirmação no artigo", None, "left"),
    ("Valor no artigo", MULT, "right"), ("Aba-fonte e fórmula", None, "left"),
    ("Recomputado", MULT, "right"), ("Δ", DLT, "right"), ("Status", None, "center")],
    linhas, {"B": 12, "C": 46, "D": 13, "E": 40, "F": 13, "G": 11, "H": 9})
c = ws.cell(fim + 1, 2,
    f"Resumo: {len(CLAIMS)} afirmações verificadas. Os desvios remanescentes são de arredondamento "
    "— o artigo publica 1 ou 2 casas decimais, e alguns números convivem em duas agregações "
    "(bi-regional × interestadual), conciliadas no Apêndice B.2 do artigo.")
c.font = Font(name=FT, size=9, color=NOTA)
c.alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells(start_row=fim + 1, start_column=2, end_row=fim + 1, end_column=8)
ws.row_dimensions[fim + 1].height = 30

# ========================================================= 16_Proveniencia =====
ws = wb.create_sheet("16_Proveniencia")
h = moldura(ws, "Proveniência — mapa script → output → o que computa",
    "Trilha de reprodução do pipeline pesquisa/ (28 scripts). Listam-se os que alimentam as "
    "tabelas e figuras da revisão final e esta auditoria; os scripts leem as matrizes-fonte da "
    "máquina do autor. Os links das fontes no artigo apontam para o commit 116a350.",
    [], 3)
PROV = [
 ("01_es_br_base.py", "es_setores_resultados.csv", "Base bi-regional 2008: multiplicadores, vazamentos, spillover/feedback e ligações R-H"),
 ("02_interestadual.py", "es_spillover_destino.csv; estados_abertura.csv", "Interestadual 27 UFs: destino do vazamento por UF e ranking de abertura"),
 ("04_cluster.py", "cluster.csv; cluster_resumo.csv", "Situa o ES no cluster de 8 estados vs núcleo SP/RJ"),
 ("06_reconciliacao.py", "(console)", "Reconciliação de convenções de injeção/decomposição → adota a V3 (Miller-Blair)"),
 ("10_cluster_setorial.py", "cluster_setorial.csv", "Tabela comparativa do cluster (PIB, abertura, multiplicador, base/commodity, setor dominante)"),
 ("11_fig_sankey.py", "es_sankey.pdf", "Figura 4: Sankey estratificado do destino do spillover"),
 ("12_tab_setores.py", "tab_setores.tex", "Tabela 5 do artigo: os 26 setores, com médias simples e ponderada"),
 ("13_audit_contrafactual.py", "audit_contrafactual.csv", "Cenários contrafactuais; fornece a injeção e o spillover do recorte bi-regional"),
 ("14_benchmark_ufs.py", "benchmark_ufs.csv", "Modelo nulo das 27 UFs: o porte explica o feedback, não o vazamento"),
 ("17_caracterizacao_es_2008.py", "es_caracterizacao_2008.csv", "Retrato estrutural de 2008: multiplicadores I/II, ligações R-H e ligações puras"),
 ("18_trajetoria_n68.py", "trajetoria_n68.csv", "Panorama temporal 2010–2021 dos setores de base na estrutura nacional"),
 ("19_fig_caracterizacao.py", "fig_setores_chave.pdf; fig_trajetoria_n68.pdf", "Figuras 1 e 2 do artigo"),
 ("20_caracterizacao_micro.py", "caracterizacao_micro.csv; micro_LQ.csv", "Caracterização territorial 2015: quocientes locacionais das 10 microrregiões"),
 ("21_fig_micro.py", "fig_micro_vocacao.pdf", "Figura 3: heatmap de LQ por setor e microrregião"),
 ("22_benchmark_caracterizacao.py", "benchmark_caracterizacao.csv", "Benchmark interestadual da caracterização (Tabela 3 do artigo)"),
 ("24_micro_mult_chave.py", "micro_multiplicadores.csv; extracao_hipotetica.csv", "Multiplicadores, retenção territorial e extração hipotética da metrópole"),
 ("25_decomposicao_fd.py", "decomposicao_fd.csv; decomposicao_fd_setorial.csv", "Quem puxa a economia: decomposição pela demanda final (Tabela 2)"),
 ("26_ancora_2019.py", "(console)", "Segunda âncora: reestima a bateria central na matriz interestadual de 2019"),
 ("27_tab_multiplicadores.py", "tab_multiplicadores.tex", "Tabela 1 do artigo: multiplicadores dos 26 setores, tipos I e II"),
 ("28_auditoria_xlsx.py", "auditoria/auditoria_dados_es.xlsx", "Esta pasta de auditoria"),
 ("estilo.py", "(nenhum)", "Paleta e tema das figuras, importado pelos scripts de figura"),
]
tabela(ws, h, [("Script", None, "left"), ("Output(s) gerado(s)", None, "left"),
    ("O que computa", None, "left")], [list(p) for p in PROV],
    {"B": 30, "C": 42, "D": 88})

# =================================================================== saida =====
os.makedirs(DEST, exist_ok=True)
# as abas de prosa sao criadas em bloco antes da 12_Verificacao; reordena pelo prefixo
# numerico para que as guias aparecam em 00..16.
wb._sheets.sort(key=lambda s: s.title)
caminho = os.path.join(DEST, "auditoria_dados_es.xlsx")
wb.save(caminho)
print("salvo:", os.path.relpath(caminho, RAIZ))
print(f"abas: {len(wb.sheetnames)} | afirmacoes verificadas: {len(CLAIMS)}")
