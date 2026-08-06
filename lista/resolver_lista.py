# -*- coding: utf-8 -*-
"""
resolver_lista.py — Lista de Exercícios (Prof. Celso Bissoli Sessa, entrega 24/07/2026)
resolvida com o arcabouço insumo-produto do repositório (src/io_core.py + convenções
de pesquisa/01, 17, 25). Entrada: MIP-BR 2010 e 2020 (Nível 68, NEREUS/CECEG).
Saída: pasta de trabalho Excel diagramada no padrão visual da planilha do professor
(Calibri, título azul, código/atividade/índice nas colunas B/C/D, dados a partir da
coluna E, sem linhas de grade, totais em verde), com uma aba por questão formulada
sobre as abas de dados — as inversas 68x68 entram como valores documentados; todo o
resto recalcula.

Uso:
  python lista/resolver_lista.py --m2010 "dados/MIP-BR 2010 (Nível 68).xlsm" \
                                 --m2020 "dados/MIP-BR 2020 (Nível 68).xlsm"
  python lista/resolver_lista.py --inspect "dados/MIP-BR 2020 (Nível 68).xlsm"
  python lista/resolver_lista.py --selftest

Questões: Q1 multiplicadores (produção, emprego, renda, VA; tipos I e II) + rankings;
Q2 choques de R$10 bi (exportações da agricultura vs FBCF); Q3 reajuste do salário
mínimo (R$120 bi via UPCF) sobre importações e emprego; Q4 Rasmussen-Hirschman
2010 vs 2020; Q5 campos de influência 2010 (Sonis-Hewings); Q6 extração hipotética
total; Q7 decomposição estrutural 2010-2020 com atualização pelo IPCA.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as CL

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from io_core import coef_tecnicos, ghosh_inversa, leontief_inversa  # noqa: E402
from mip_nereus import (COMPONENTES_DF, MIPAno, carregar_A_conferencia,  # noqa: E402
                        carregar_mip, escrever_sintetico, inspecionar, norm)

# IPCA (IBGE, variação % dez/dez — série histórica oficial); fator acumulado
# atualiza valores de 2010 para preços de 2020 (Questão 7).
IPCA_ANUAL = {2011: 6.50, 2012: 5.84, 2013: 5.91, 2014: 6.41, 2015: 10.67,
              2016: 6.29, 2017: 2.95, 2018: 3.75, 2019: 4.31, 2020: 4.52}
EPS_CAMPO = 0.001          # epsilon do campo de influência (convenção Vale-Perobelli)
SETOR_Q6_PADRAO = "petroleo e gas"   # casado por norm() no nome do setor


# =========================================================================== #
# 1. NÚCLEO DE CÁLCULO (usa io_core; convenções de pesquisa/17)
# =========================================================================== #
class Sistema:
    """Sistema de Leontief de um ano: A, B, Ghosh e fechamento tipo II."""

    def __init__(self, mip: MIPAno):
        self.mip = mip
        n = mip.n
        self.n = n
        self.A = coef_tecnicos(mip.Z, mip.x)
        self.B = leontief_inversa(self.A)
        self.G = ghosh_inversa(mip.Z, mip.x)
        xs = np.where(mip.x == 0, 1.0, mip.x)
        self.w_emp = mip.ocup / xs               # ocupações por R$ 1 milhão
        self.v_renda = mip.rem / xs              # remunerações por R$ 1
        self.v_va = mip.va / xs                  # VA por R$ 1
        self.m_coef = mip.imp_int / xs           # importação intermediária por R$ 1

        # fechamento tipo II (famílias endógenas) na CONVENÇÃO DA PLANILHA DO
        # PROFESSOR (abas 20/22/23 dos arquivos MIP-BR): a renda das famílias é o
        # VALOR ADICIONADO BRUTO (não só as remunerações). Linha adicional = VA por
        # unidade de produção (v_va); coluna adicional = consumo das famílias por
        # unidade da massa de VA. Reproduz a aba 23 (mult. tipo II) e a aba 22
        # (geradores tipo II) com desvio < 1e-14. (O fechamento por remunerações,
        # usado no artigo do ES em pesquisa/17, é uma alternativa mais estreita.)
        hh = mip.va.sum()
        self.hc = mip.y["familias"] / (hh if hh else 1.0)
        A2 = np.zeros((n + 1, n + 1))
        A2[:n, :n] = self.A
        A2[:n, n] = self.hc
        A2[n, :n] = self.v_va
        self.A2 = A2
        self.B2 = np.linalg.inv(np.eye(n + 1) - A2)

    # ---- Q1: multiplicadores tipo I e II ---------------------------------- #
    def multiplicadores(self) -> dict[str, np.ndarray]:
        B, B2n = self.B, self.B2[:self.n, :self.n]
        return {
            "prod_I":  B.sum(0),
            "prod_II": B2n.sum(0),
            "emp_I":   (self.w_emp[:, None] * B).sum(0),
            "emp_II":  (self.w_emp[:, None] * B2n).sum(0),
            "renda_I": (self.v_renda[:, None] * B).sum(0),
            "renda_II": (self.v_renda[:, None] * B2n).sum(0),
            "va_I":    (self.v_va[:, None] * B).sum(0),
            "va_II":   (self.v_va[:, None] * B2n).sum(0),
        }

    # ---- Q4: ligações de Rasmussen-Hirschman na convenção da planilha do
    # professor (aba 14): AMBAS pela inversa de Leontief — para trás pela soma de
    # COLUNA (poder de dispersão) e para frente pela soma de LINHA (sensibilidade
    # da dispersão), normalizadas pela média geral de B. Reproduz a aba 14 com
    # desvio < 1e-14. (A inversa de Ghosh, aba 'Ghosh'/G_20xx, dá uma medida
    # alternativa de sensibilidade da oferta — ver nota da aba Q4_RH.)
    def rasmussen(self) -> tuple[np.ndarray, np.ndarray]:
        n = self.n
        bl = self.B.sum(0) / n / self.B.mean()
        fl = self.B.sum(1) / n / self.B.mean()
        return bl, fl


def indice_setor(mip: MIPAno, padrao: str) -> int:
    alvo = norm(padrao)
    for i, nm in enumerate(mip.nomes):
        if alvo in norm(nm):
            return i
    raise ValueError(f"setor com padrão {padrao!r} não encontrado; exemplos: "
                     f"{mip.nomes[:5]}…")


def q2_cenarios(s: Sistema, choque_mi: float, i_agro: int) -> dict:
    """(a) +choque nas exportações da agricultura; (b) +choque na FBCF (estrutura)."""
    mip = s.mip
    dy_a = np.zeros(s.n); dy_a[i_agro] = choque_mi
    fbcf = mip.y["fbcf"]
    dy_b = choque_mi * fbcf / fbcf.sum()
    out = {}
    for rot, dy in (("a_agro_export", dy_a), ("b_fbcf", dy_b)):
        dx = s.B @ dy
        out[rot] = {"dy": dy, "dx": dx, "dprod": dx.sum(),
                    "dva": float(s.v_va @ dx), "demp": float(s.w_emp @ dx),
                    "dimp": float(s.m_coef @ dx)}
    return out


def grupos_margem(mip: MIPAno) -> tuple[list[int], list[int]]:
    """setores que produzem as margens da cesta: comércio e transporte."""
    idx_c = [i for i, nm in enumerate(mip.nomes) if norm(nm).startswith("comercio")]
    idx_t = [i for i, nm in enumerate(mip.nomes) if norm(nm).startswith("transporte")]
    return idx_c, idx_t


def q3_upcf(s: Sistema, choque_mi: float) -> dict:
    """R$ choque de consumo das famílias repartido pela UPCF — a cesta observada a
    preço de CONSUMIDOR: produtos nacionais a preço básico + importados + impostos
    + margens (aba '12': linhas Importação/Impostos/Margens × coluna Famílias).
    As margens são demanda por serviços de comércio e transporte e voltam ao vetor
    de choque nesses setores (rateio pelo VBP do grupo); impostos não geram
    produção; a parcela importada é vazamento direto. Impactos: importações
    (diretas + induzidas via m = importação intermediária/x) e emprego."""
    mip = s.mip
    c_nac = mip.y["familias"]
    imp = mip.fd_fam.get("importacao", 0.0)
    imposto = mip.fd_fam.get("impostos", 0.0)
    marg_c = mip.fd_fam.get("margens_comercio", 0.0)
    marg_t = mip.fd_fam.get("margens_transporte", 0.0)
    den = float(c_nac.sum() + imp + imposto + marg_c + marg_t)
    cesta = c_nac.copy()
    idx_c, idx_t = grupos_margem(mip)
    for idxs, m in ((idx_c, marg_c), (idx_t, marg_t)):
        if idxs and m:
            w = mip.x[idxs] / mip.x[idxs].sum()
            for k, i in enumerate(idxs):
                cesta[i] += m * w[k]
    dy = choque_mi * cesta / den
    dx = s.B @ dy
    dimp_direta = choque_mi * imp / den
    dimp_induzida = float(s.m_coef @ dx)
    return {"dy": dy, "dx": dx, "den": den,
            "share_imp_cesta": imp / den, "share_imposto": imposto / den,
            "share_margens": (marg_c + marg_t) / den,
            "dimp_direta": dimp_direta, "dimp_induzida": dimp_induzida,
            "dimp_total": dimp_direta + dimp_induzida,
            "dimposto": choque_mi * imposto / den,
            "demp": float(s.w_emp @ dx), "demp_setor": s.w_emp * dx,
            "dprod": float(dx.sum()), "idx_c": idx_c, "idx_t": idx_t}


def q5_campo_influencia(s: Sistema, eps: float = EPS_CAMPO) -> np.ndarray:
    """S[i,j] = soma dos quadrados do campo de influência do elo a_ij
    (Sonis-Hewings). Fórmula fechada por Sherman-Morrison, idêntica ao laço do
    material de apoio em R (Vale & Perobelli) com B(eps) recalculada elo a elo:
      F = (B(eps)-B)/eps = B[:,i] (x) B[j,:] / (1 - eps*B[j,i])
      S[i,j] = (Σ_k B[k,i]^2) (Σ_l B[j,l]^2) / (1 - eps*B[j,i])^2
    """
    B = s.B
    colsq = (B ** 2).sum(0)                    # Σ_k B[k,i]^2
    rowsq = (B ** 2).sum(1)                    # Σ_l B[j,l]^2
    return np.outer(colsq, rowsq) / (1.0 - eps * B.T) ** 2


def q6_extracao(s: Sistema, j: int) -> dict:
    """Extração hipotética TOTAL do setor j (zera linha e coluna de A e a demanda
    final do setor); perda = produção do sistema completo - produção reduzida."""
    A_ex = s.A.copy()
    A_ex[j, :] = 0.0
    A_ex[:, j] = 0.0
    y = s.mip.y_total()
    y_ex = y.copy(); y_ex[j] = 0.0
    x_base = s.B @ y                            # baseline consistente com o modelo
    x_ex = np.linalg.inv(np.eye(s.n) - A_ex) @ y_ex
    perda = x_base - x_ex
    return {"x_base": x_base, "x_ex": x_ex, "perda": perda,
            "perda_total": float(perda.sum()),
            "perda_pct": float(perda.sum() / x_base.sum()),
            "perda_va": float(s.v_va @ perda), "perda_emp": float(s.w_emp @ perda)}


def q7_sda(s0: Sistema, s1: Sistema, fator_ipca: float) -> dict:
    """Decomposição estrutural (SDA) bipolar média (Dietzenbacher-Los):
      Δx = ½(B1-B0)(y0*+y1) + ½(B0+B1)(y1-y0*),  y0* = y0 · fator IPCA.
    A matriz A de 2010 é invariante ao deflator único (coeficientes são razões);
    a atualização pelo IPCA age sobre os NÍVEIS (y e x)."""
    y0f = s0.mip.y_total() * fator_ipca
    y1 = s1.mip.y_total()
    x0f = s0.B @ y0f
    x1 = s1.B @ y1
    dx = x1 - x0f
    tec = 0.5 * (s1.B - s0.B) @ (y0f + y1)
    dem = 0.5 * (s1.B + s0.B) @ (y1 - y0f)
    assert np.allclose(tec + dem, dx, atol=1e-6 * max(1.0, np.abs(dx).max()))
    return {"y0f": y0f, "y1": y1, "x0f": x0f, "x1": x1,
            "dx": dx, "tec": tec, "dem": dem}


# =========================================================================== #
# 2. GERADOR DO EXCEL — diagramação minimalista na paleta FLEXOKI (kepano):
#    fundo claro, cinzas quentes (base 50–800 sobre papel #FFFCF0), pastéis
#    brandos para totais/entradas, bordas suaves e pouca cor forte. Rolagem
#    confortável: cada questão congela apenas título + síntese compacta +
#    cabeçalho da tabela; a leitura longa e os vetores auxiliares ficam
#    abaixo da tabela.
# =========================================================================== #
CALIBRI = "Calibri"
# flexoki — tons de base (sobre papel #FFFCF0)
INK = "FF100F0F"
BASE_800 = "FF403E3C"
BASE_700 = "FF575653"
BASE_600 = "FF6F6E69"
BASE_500 = "FF878580"
BASE_300 = "FFB7B5AC"
BASE_150 = "FFDAD8CE"
BASE_100 = "FFE6E4D9"
BASE_50 = "FFF2F0E5"
AZUL_600 = "FF205EA6"
# pastéis (mistura dos acentos flexoki-400 com o papel)
VERDE_PASTEL = "FFE1E4C2"      # totais / linhas-síntese
AMARELO_PASTEL = "FFF3E6B9"    # entradas editáveis
LARANJA_PASTEL = "FFF8E0C9"    # destaque (setor extraído na Q6)
AZUL_PASTEL = "FFC7D8E1"       # cor das abas de questão

F_TITULO = Font(name=CALIBRI, size=16, bold=True, color=INK)
F_ENUN = Font(name=CALIBRI, size=9.5, color=BASE_600)
F_SECAO = Font(name=CALIBRI, size=10, bold=True, color=BASE_700)
F_SINT = Font(name=CALIBRI, size=10, color=INK)
F_CAB = Font(name=CALIBRI, size=9, bold=True, color=BASE_800)
F_CAB8 = Font(name=CALIBRI, size=8, bold=True, color=BASE_800)
F_TAB = Font(name=CALIBRI, size=9, color="FF282726")
F_TAB_NEG = Font(name=CALIBRI, size=9, bold=True, color=INK)
F_DADO = Font(name=CALIBRI, size=8, color="FF282726")
F_DADO_NEG = Font(name=CALIBRI, size=8, bold=True, color=INK)
F_TXT = Font(name=CALIBRI, size=10, color=BASE_800)
F_NEG = Font(name=CALIBRI, size=10, bold=True, color=BASE_800)
F_IN = Font(name=CALIBRI, size=10, bold=True, color=AZUL_600)
F_AUX = Font(name=CALIBRI, size=8, italic=True, color=BASE_500)

FILL_CAB = PatternFill("solid", fgColor=BASE_150)
FILL_BLOCO = PatternFill("solid", fgColor=BASE_100)
FILL_ZEBRA = PatternFill("solid", fgColor=BASE_50)
FILL_CAIXA = PatternFill("solid", fgColor=BASE_50)
FILL_TOT = PatternFill("solid", fgColor=VERDE_PASTEL)
FILL_IN = PatternFill("solid", fgColor=AMARELO_PASTEL)
FILL_DESTQ = PatternFill("solid", fgColor=LARANJA_PASTEL)

FINA = Side(style="thin", color=BASE_150)
MEIA = Side(style="thin", color=BASE_500)
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)          # grades densas
BORDA_H = Border(top=FINA, bottom=FINA)                               # tabelas de questão
BORDA_CAB = Border(top=FINA, bottom=MEIA)                             # sublinhado do cabeçalho
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
QUEBRA = Alignment(wrap_text=True, vertical="top")
VCENTRO = Alignment(vertical="center")

NUM_MULT = "0.0000"
NUM_MI = "#,##0"
NUM_MI2 = "#,##0.00"
NUM_PCT = "0.00%"
NUM_IDX = "0.000"
NUM_COEF = "0.000000"

LCOL_TXT = 22                   # última coluna (V) das caixas de texto

# geometria comum: dados de matrizes e da aba Dados começam na linha 7, coluna E
MR0, MC0 = 7, 5
COL_DADOS = {"x": "E", "rem": "F", "va": "G", "ocup": "H", "imp": "I",
             "exportacao": "J", "governo": "K", "isflsf": "L", "familias": "M",
             "fbcf": "N", "estoque": "O", "ytot": "P",
             "w_emp": "Q", "v_renda": "R", "v_va": "S", "m_coef": "T"}

TAB_CAPA = "FFB7B5AC"
TAB_DADOS = "FFDAD8CE"
TAB_Q = AZUL_PASTEL


def _nova_aba(wb, nome, titulo, nota, cor_tab, zoom=100):
    """Aba flexoki: coluna A como margem, título 16pt em tinta, enunciado em
    cinza quente logo abaixo, sem linhas de grade."""
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = zoom
    ws.sheet_properties.tabColor = cor_tab
    ws.column_dimensions["A"].width = 1.2
    ws.row_dimensions[1].height = 8
    ws.row_dimensions[2].height = 22
    ws.cell(2, 2, titulo).font = F_TITULO
    ws.cell(2, 2).alignment = VCENTRO
    if nota:
        ws.merge_cells(start_row=3, start_column=2, end_row=3, end_column=LCOL_TXT)
        c = ws.cell(3, 2, nota)
        c.font = F_ENUN; c.alignment = QUEBRA
        ws.row_dimensions[3].height = max(13, 12.5 * math.ceil(len(nota) / 175))
    return ws


def _sintese(ws, linha0, linhas_texto):
    """Síntese compacta (fica na área congelada): 1-3 marcadores curtos."""
    ws.cell(linha0, 2, "Síntese").font = F_SECAO
    r = linha0 + 1
    for t in linhas_texto:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=LCOL_TXT)
        c = ws.cell(r, 2, "•  " + t)
        c.font = F_SINT; c.alignment = QUEBRA
        ws.row_dimensions[r].height = max(13.5, 13 * math.ceil(len(t) / 165))
        r += 1
    return r + 1


def _caixa_leitura(ws, linha0, linhas_texto):
    """Leitura/discussão completa (abaixo da tabela): caixa em cinza-claro."""
    ws.cell(linha0, 2, "Leitura dos resultados").font = F_SECAO
    r = linha0 + 1
    for t in linhas_texto:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=LCOL_TXT)
        c = ws.cell(r, 2, "•  " + t)
        c.font = F_TXT; c.alignment = QUEBRA; c.fill = FILL_CAIXA
        for k in range(3, LCOL_TXT + 1):
            ws.cell(r, k).fill = FILL_CAIXA
        ws.row_dimensions[r].height = max(14, 13.5 * math.ceil(len(t) / 160))
        r += 1
    return r + 1


def _cab_tabela(ws, linha, col0, rotulos, larguras=None, fonte=None):
    ws.row_dimensions[linha].height = 24
    for k, rtl in enumerate(rotulos):
        c = ws.cell(linha, col0 + k, rtl)
        c.font = fonte or F_CAB; c.fill = FILL_CAB
        c.border = BORDA_CAB; c.alignment = CENTRO
        if larguras:
            ws.column_dimensions[CL(col0 + k)].width = larguras[k]


def _linha_total(ws, linha, col_fim, rotulo="TOTAL", col_rotulo=3):
    """linha-síntese em verde-pastel."""
    ws.cell(linha, col_rotulo, rotulo).font = F_TAB_NEG
    for k in range(2, col_fim + 1):
        ws.cell(linha, k).fill = FILL_TOT
        ws.cell(linha, k).border = BORDA_H


def _rotulo_aux(ws, linha, texto):
    ws.cell(linha, 3, texto).font = F_AUX


def _id_setor(ws, r, cod, nome, num, zebra=False):
    """colunas de identificação (B código, C atividade, D nº) de uma linha."""
    ws.cell(r, 2, cod).alignment = CENTRO
    ws.cell(r, 3, nome).alignment = VCENTRO
    ws.cell(r, 4, num).alignment = CENTRO
    if zebra:
        for k in (2, 3, 4):
            ws.cell(r, k).fill = FILL_ZEBRA


def _matriz(ws, M, nomes, cods, fmt=NUM_MULT, extra_rotulo=None):
    """Matriz com Código (B), Atividades (C:D com o índice da linha em D),
    índices 1..n no cabeçalho e dados a partir de E7; zebra suave."""
    nlin, ncol = M.shape
    ws.merge_cells(start_row=6, start_column=3, end_row=6, end_column=4)
    for col, rtl in ((2, "Código"), (3, "Atividades")):
        c = ws.cell(6, col, rtl)
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    ws.cell(6, 4).fill = FILL_CAB; ws.cell(6, 4).border = BORDA
    ws.column_dimensions["B"].width = 6.7
    ws.column_dimensions["C"].width = 52
    ws.column_dimensions["D"].width = 4.4
    for j in range(ncol):
        c = ws.cell(6, MC0 + j, extra_rotulo if j >= len(cods) else j + 1)
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
        ws.column_dimensions[CL(MC0 + j)].width = 10.5
    ws.row_dimensions[6].height = 14
    for i in range(nlin):
        r = MR0 + i
        ws.row_dimensions[r].height = 11.5
        eh_extra = i >= len(nomes)
        zebra = bool(i % 2)
        c = ws.cell(r, 2, extra_rotulo if eh_extra else cods[i])
        c.alignment = CENTRO
        c = ws.cell(r, 3, "Famílias (VA ↔ consumo)" if eh_extra else nomes[i])
        c.alignment = VCENTRO
        c = ws.cell(r, 4, i + 1)
        c.alignment = CENTRO
        for j in range(ncol):
            c = ws.cell(r, MC0 + j, float(M[i, j]))
            c.number_format = fmt; c.alignment = VCENTRO
        for k in range(2, MC0 + ncol):
            c = ws.cell(r, k)
            c.font = F_DADO; c.border = BORDA
            if zebra:
                c.fill = FILL_ZEBRA
    ws.freeze_panes = "E7"


def _ref_mat(aba, i=None, j=None, n=68):
    """faixa de uma linha (i) ou coluna (j) da matriz da aba (dados em E7)."""
    if i is not None:
        return f"{aba}!E{MR0 + i}:{CL(MC0 - 1 + n)}{MR0 + i}"
    return f"{aba}!{CL(MC0 + j)}{MR0}:{CL(MC0 + j)}{MR0 - 1 + n}"


def _celula_dado(tag, col, i):
    return f"Dados_{tag}!${COL_DADOS[col]}${MR0 + i}"


def _faixa_dado(tag, col, n):
    c = COL_DADOS[col]
    return f"Dados_{tag}!${c}$7:${c}${6 + n}"


def _aba_dados(wb, tag, mip: MIPAno):
    """Tabela vertical (setores nas linhas) com vetores e coeficientes por fórmula."""
    ws = _nova_aba(wb, f"Dados_{tag}",
                   f"Dados — MIP Brasil {tag}",
                   "Valores correntes em R$ milhões; ocupações em pessoas. Vetores extraídos "
                   "da aba 12 da MIP-BR (Nível 68), NEREUS/CECEG; coeficientes por unidade de "
                   "produção calculados por fórmula nas colunas Q a T.", TAB_DADOS, zoom=90)
    rot = ["Código", "Atividades", "nº", "VBP (x)", "Remunerações", "VA (PIB)",
           "Ocupações", "Importação intermediária", "Exportações", "Governo",
           "ISFLSF", "Consumo das famílias (nac.)", "FBCF", "Variação de estoques",
           "Demanda final total", "w = ocup/x", "v renda = rem/x", "v VA = VA/x",
           "m = imp/x"]
    _cab_tabela(ws, 6, 2, rot, larguras=[6.7, 52, 4.4] + [12.5] * (len(rot) - 3),
                fonte=F_CAB8)
    n = mip.n
    for i in range(n):
        r = MR0 + i
        ws.row_dimensions[r].height = 11.5
        zebra = bool(i % 2)
        _id_setor(ws, r, mip.cod[i], mip.nomes[i], i + 1)
        vals = [mip.x[i], mip.rem[i], mip.va[i], mip.ocup[i], mip.imp_int[i],
                mip.y["exportacao"][i], mip.y["governo"][i], mip.y["isflsf"][i],
                mip.y["familias"][i], mip.y["fbcf"][i], mip.y["estoque"][i]]
        for k, v in enumerate(vals):
            c = ws.cell(r, 5 + k, float(v))
            c.number_format = NUM_MI2
        ws.cell(r, 16, f"=SUM(J{r}:O{r})").number_format = NUM_MI2
        for col, expr, fmt in (("Q", f"=IF(E{r}=0,0,H{r}/E{r})", NUM_MULT),
                               ("R", f"=IF(E{r}=0,0,F{r}/E{r})", NUM_COEF),
                               ("S", f"=IF(E{r}=0,0,G{r}/E{r})", NUM_COEF),
                               ("T", f"=IF(E{r}=0,0,I{r}/E{r})", NUM_COEF)):
            c = ws[f"{col}{r}"]
            c.value = expr; c.number_format = fmt
        for k in range(2, 21):
            c = ws.cell(r, k)
            c.font = F_DADO; c.border = BORDA
            if zebra:
                c.fill = FILL_ZEBRA
    r_tot = MR0 + n
    _linha_total(ws, r_tot, 20)
    for col in "EFGHIJKLMNOP":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}7:{col}{6 + n})"
        c.font = F_DADO_NEG; c.number_format = NUM_MI2
    ws.freeze_panes = "E7"
    return ws


def _tabela_setorial(ws, rH, cab, larguras, n, m, escreve_linha, destaque=None):
    """esqueleto das tabelas de questão: cabeçalho, zebra, bordas horizontais."""
    _cab_tabela(ws, rH, 2, cab, larguras=larguras)
    for i in range(n):
        r = rH + 1 + i
        _id_setor(ws, r, m.cod[i], m.nomes[i], i + 1)
        escreve_linha(r, i)
        zebra = bool(i % 2)
        for k in range(2, 2 + len(cab)):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA_H
            if destaque is not None and i == destaque:
                c.fill = FILL_DESTQ
            elif zebra:
                c.fill = FILL_ZEBRA
    return rH + 1 + n                                   # linha do TOTAL


def gerar_excel(saida: str, m10: MIPAno, m20: MIPAno, s10: Sistema, s20: Sistema,
                i_agro: int, i_q6: int, sintetico: bool = False) -> dict:
    """Escreve a pasta de trabalho completa; devolve dicionário de conferência
    {celula: valor_python} para validação pós-recálculo."""
    n = m20.n
    confere: dict[str, float] = {}
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # ---------------- Capa ---------------- #
    ws = _nova_aba(wb, "Capa", "Lista de Exercícios — Análise de Insumo-Produto",
                   None, TAB_CAPA)
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 96
    info = [
        ("Disciplina", "Análise de Insumo-Produto · PPGEco/UFES · 2026/1"),
        ("Professor", "Prof. Dr. Celso Bissoli Sessa"),
        ("Aluno", "Felipe Carvalho de Souza Santos"),
        ("Entrega", "24/07/2026"),
        ("Dados", "Matrizes de Insumo-Produto do Brasil, 2010 e 2020 "
                  "(Nível 68, NEREUS/CECEG; R$ milhões correntes)"),
        ("Ferramenta", "Arcabouço do repositório fcarva/es-insumo-produto "
                       "(src/io_core.py; convenções de pesquisa/01, 17 e 25) — "
                       "gerado por lista/resolver_lista.py"),
    ]
    r = 5
    if sintetico:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=LCOL_TXT)
        c = ws.cell(r, 2, f"*** ARQUIVO DE VALIDAÇÃO (selftest): economia SINTÉTICA de "
                          f"{n} setores — NÃO usa dados reais ***")
        c.font = Font(name=CALIBRI, size=12, bold=True, color="FFAF3029")
        r += 2
    for rot, txt in info:
        ws.cell(r, 2, rot).font = Font(name=CALIBRI, size=10, bold=True, color=BASE_600)
        c = ws.cell(r, 3, txt)
        c.font = F_TXT; c.alignment = QUEBRA
        ws.row_dimensions[r].height = max(15, 13 * math.ceil(len(txt) / 95))
        r += 1
    r += 1
    ws.cell(r, 2, "Guia das abas").font = F_SECAO
    r += 1
    guia = [
        ("Metodologia", "Notas metodológicas e todas as premissas assumidas"),
        ("Setores", "Classificação setorial (Nível 68, comum a 2010 e 2020)"),
        ("Q1_Multiplicadores", "Multiplicadores de produção, emprego, renda e VA (tipos I e II) + rankings"),
        ("Q2_Choques", "Choques de R$ 10 bi: exportações da agricultura × FBCF"),
        ("Q3_UPCF", "Reajuste do salário mínimo (R$ 120 bi): importações e emprego"),
        ("Q4_RH", "Rasmussen-Hirschman 2010 × 2020 e setores-chave"),
        ("Q5_CampoInfluencia", "Campos de influência (Sonis-Hewings), Brasil 2010"),
        ("Q6_Extracao", "Extração hipotética total do setor escolhido (2020)"),
        ("Q7_SDA", "Decomposição estrutural 2010→2020 com atualização pelo IPCA"),
        ("Dados_2020 / Dados_2010", "Vetores da MIP e coeficientes diretos (fórmulas)"),
        ("A, B, G, B2", "Coeficientes técnicos, inversa de Leontief, inversa de Ghosh e "
                        "modelo fechado (valores documentados — base das fórmulas)"),
    ]
    _cab_tabela(ws, r, 2, ["Aba", "Conteúdo"], larguras=[30, 96])
    for k, (aba, desc) in enumerate(guia):
        rr = r + 1 + k
        ws.cell(rr, 2, aba).font = F_TAB_NEG
        ws.cell(rr, 3, desc).font = F_TAB
        for cc in (2, 3):
            ws.cell(rr, cc).border = BORDA_H
            ws.cell(rr, cc).alignment = VCENTRO
            if k % 2:
                ws.cell(rr, cc).fill = FILL_ZEBRA
    r = r + len(guia) + 2
    ws.cell(r, 2, "Legenda de células").font = F_SECAO
    legenda = [
        (F_IN, FILL_IN, "Amarelo-pastel, texto azul — entrada editável (choques, IPCA): a pasta recalcula"),
        (F_TAB, FILL_BLOCO, "Cinza-quente — parâmetros lidos da MIP (aba 12)"),
        (F_TAB_NEG, FILL_TOT, "Verde-pastel — linhas-síntese e totais"),
        (F_TAB, None, "Sem preenchimento — fórmula viva sobre as abas de dados/matrizes"),
    ]
    for k, (f, fill, txt) in enumerate(legenda):
        rr = r + 1 + k
        c = ws.cell(rr, 2, "célula")
        c.font = f; c.border = BORDA_H; c.alignment = CENTRO
        if fill:
            c.fill = fill
        ws.cell(rr, 3, txt).font = F_TXT

    # ---------------- Metodologia ---------------- #
    ws = _nova_aba(wb, "Metodologia", "Notas metodológicas e premissas",
                   "Todas as hipóteses assumidas na resolução estão listadas aqui; "
                   "as fórmulas citadas seguem Miller & Blair (2009).", TAB_CAPA)
    met = [
        "1. Modelo aberto: A = Z·x̂⁻¹ sobre os fluxos NACIONAIS (aba 12 da MIP-BR); "
        "B = (I−A)⁻¹ (Leontief); Ghosh: G = (I−x̂⁻¹Z)⁻¹. As matrizes B, G e B2 estão coladas "
        "como VALORES (inversão 68×68 feita externamente em NumPy — conferível por MINVERSE; "
        "a matriz A reproduz a aba 13 do arquivo-fonte com desvio < 1e-15); todas as demais "
        "células derivam delas por fórmula e recalculam.",
        "2. Tipo II: modelo fechado para as famílias na CONVENÇÃO DA PLANILHA DO PROFESSOR "
        "(abas 20/22/23 da MIP) — a renda das famílias é o VALOR ADICIONADO BRUTO: linha "
        "adicional = VA por unidade de produção (v_va); coluna adicional = consumo das famílias "
        "por unidade da massa de VA. Reproduz a aba 23 (mult. tipo II) e a aba 22 (geradores "
        "tipo II) com desvio < 1e-14. O fechamento por remunerações (renda do trabalho apenas), "
        "usado no artigo do ES em pesquisa/17, é uma alternativa mais estreita.",
        "3. Multiplicador de emprego em OCUPAÇÕES por R$ 1 milhão de demanda final; renda e VA "
        "em R$ por R$ de demanda final.",
        "4. Q2: choque de R$ 10 bi = 10.000 (R$ milhões). Cenário (a): tudo na linha de "
        "exportações do setor Agricultura. Cenário (b): distribuído pela estrutura observada "
        "da coluna FBCF (produtos nacionais). Premissa: o choque recai sobre produtos "
        "nacionais nos dois cenários (célula de entrada editável).",
        "5. Q3 (UPCF): o incremento de R$ 120 bi é repartido pela cesta observada do consumo "
        "das famílias a preço de CONSUMIDOR — nacional a preço básico + importados + impostos "
        "+ margens (linhas Importação/Impostos/Margens × coluna Famílias da aba 12; a soma "
        "reproduz exatamente o consumo total). Margens são demanda por serviços de comércio e "
        "transporte e voltam ao vetor de choque nesses setores (rateio pelo VBP do grupo); "
        "impostos não geram produção; a parcela importada é importação DIRETA; a produção "
        "induzida gera importação INDUZIDA via m = importação intermediária/x. Emprego pelo "
        "modelo aberto (o choque JÁ é o consumo induzido).",
        "6. Q4: índices de Rasmussen-Hirschman na convenção da aba 14 da MIP — AMBOS pela "
        "inversa de Leontief, normalizados pela média geral: para trás = soma de coluna de B "
        "(poder de dispersão); para frente = soma de linha de B (sensibilidade da dispersão); "
        "setor-chave: ambos > 1. Reproduz a aba 14 com desvio < 1e-14. A inversa de Ghosh "
        "(abas G_2010/G_2020) é uma medida alternativa de sensibilidade da oferta.",
        f"7. Q5: campo de influência (Sonis & Hewings) com ε = {EPS_CAMPO}; S(i,j) = Σ dos "
        "quadrados de F = [B(ε)−B]/ε para perturbação unitária em a(i,j). Cálculo fechado por "
        "Sherman-Morrison — numericamente idêntico ao laço do material de apoio em R "
        "(Vale & Perobelli). Matriz S colada como valor; agregações por fórmula.",
        "8. Q6: extração hipotética TOTAL (zera linha e coluna do setor em A e sua demanda "
        "final); perda medida contra o baseline modelado x = B·y.",
        "9. Q7: SDA bipolar média (Dietzenbacher & Los): Δx = ½ΔB·(y0*+y1) + ½(B0+B1)·Δy, com "
        "y0* = y(2010)·fator IPCA. O deflator único (IPCA acumulado dez/2010→dez/2020, células "
        "editáveis na aba Q7) não altera A nem B de 2010 — coeficientes são razões —, agindo "
        "apenas sobre os níveis. Limitação declarada: o ideal seriam deflatores setoriais "
        "(duplo deflacionamento); o enunciado pede IPCA.",
        "10. Unidades: R$ milhões correntes do ano de cada matriz (Q7 em preços de 2020).",
        "",
        f"Proveniência 2020: {m20.proveniencia.get('nacional')}",
        f"Proveniência 2010: {m10.proveniencia.get('nacional')}",
        f"Arquivo 2020: {m20.proveniencia.get('arquivo')}",
        f"Arquivo 2010: {m10.proveniencia.get('arquivo')}",
    ]
    r = 5
    for t in met:
        if t:
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=LCOL_TXT)
            c = ws.cell(r, 2, t)
            c.font = F_TXT; c.alignment = QUEBRA
            ws.row_dimensions[r].height = max(15, 13.5 * math.ceil(len(t) / 155))
        else:
            ws.row_dimensions[r].height = 8
        r += 1

    # ---------------- Setores ---------------- #
    ws = _nova_aba(wb, "Setores", "Classificação setorial",
                   "Nível 68 (NEREUS/CECEG) — comum às matrizes de 2010 e 2020.", TAB_CAPA)
    _cab_tabela(ws, 6, 2, ["Código", "Atividades", "nº"], larguras=[8, 70, 5])
    for i in range(n):
        r = MR0 + i
        _id_setor(ws, r, m20.cod[i], m20.nomes[i], i + 1, zebra=bool(i % 2))
        for cc in (2, 3, 4):
            ws.cell(r, cc).font = F_TAB
            ws.cell(r, cc).border = BORDA_H
            if i % 2:
                ws.cell(r, cc).fill = FILL_ZEBRA
    ws.freeze_panes = "A7"

    # ---------------- Dados e matrizes ---------------- #
    _aba_dados(wb, "2020", m20)
    _aba_dados(wb, "2010", m10)
    matrizes = [
        ("A_2020", s20.A, m20, "Matriz A — coeficientes técnicos nacionais (2020)",
         "a(i,j) = Z(i,j)/x(j); reproduz a aba 13 do arquivo-fonte (desvio < 1e-15).", None),
        ("B_2020", s20.B, m20, "Matriz B — inversa de Leontief (2020)",
         "B = (I−A)⁻¹, colada como VALOR (inversão externa NumPy; confira com MINVERSE). "
         "Base das fórmulas das questões.", None),
        ("G_2020", s20.G, m20, "Matriz G — inversa de Ghosh (2020)",
         "G = (I−x̂⁻¹Z)⁻¹, colada como VALOR; usada na ligação para frente (Q4).", None),
        ("B2_2020", s20.B2, m20, "Matriz B2 — modelo fechado para as famílias (2020)",
         "Inversa do sistema com famílias endógenas (tipo II, fechamento por VALOR ADICIONADO "
         "— convenção das abas 20/22/23 da MIP); última linha/coluna = famílias.",
         "FAM"),
        ("A_2010", s10.A, m10, "Matriz A — coeficientes técnicos nacionais (2010)",
         "a(i,j) = Z(i,j)/x(j); reproduz a aba 13 do arquivo-fonte (desvio < 1e-15).", None),
        ("B_2010", s10.B, m10, "Matriz B — inversa de Leontief (2010)",
         "B = (I−A)⁻¹, colada como VALOR; usada em Q4 e Q7.", None),
        ("G_2010", s10.G, m10, "Matriz G — inversa de Ghosh (2010)",
         "G = (I−x̂⁻¹Z)⁻¹, colada como VALOR; usada na ligação para frente (Q4).", None),
    ]
    for nome, M, mp, tit, nota, extra in matrizes:
        ws = _nova_aba(wb, nome, tit, nota, TAB_DADOS, zoom=85)
        _matriz(ws, M, mp.nomes, mp.cod, fmt=NUM_MULT, extra_rotulo=extra)

    fimM = CL(MC0 - 1 + n)                       # última coluna das matrizes

    # ================= Q1 — multiplicadores ================= #
    mult = s20.multiplicadores()
    ws = _nova_aba(wb, "Q1_Multiplicadores",
                   "Questão 1 — Multiplicadores (2020), tipos I e II",
                   "Multiplicadores de produção, emprego, renda e valor adicionado para todos "
                   "os setores. Tipo I: modelo aberto (B_2020). Tipo II: modelo fechado para "
                   "as famílias (B2_2020). Emprego em ocupações por R$ 1 milhão; renda e VA em "
                   "R$ por R$ 1,00 de demanda final.", TAB_Q)
    o_emp = np.argsort(mult["emp_II"])[::-1]
    o_ren = np.argsort(mult["renda_II"])[::-1]
    sint = [
        f"Produção: média {mult['prod_I'].mean():.3f} (tipo I) e {mult['prod_II'].mean():.3f} "
        f"(tipo II). Maior geração de EMPREGO (II): {m20.nomes[o_emp[0]]} "
        f"({mult['emp_II'][o_emp[0]]:.1f} ocup./R$ mi); de RENDA (II): {m20.nomes[o_ren[0]]} "
        f"(R$ {mult['renda_II'][o_ren[0]]:.3f}/R$ 1,00).",
        "Rankings completos de emprego e renda abaixo da tabela principal.",
    ]
    rH = _sintese(ws, 5, sint)
    cab = ["Código", "Atividades", "nº", "Produção I", "Produção II",
           "Emprego I (ocup/R$ mi)", "Emprego II (ocup/R$ mi)", "Renda I", "Renda II",
           "VA I", "VA II", "Rank emprego II", "Rank renda II"]
    r_ini, r_fim = rH + 1, rH + n

    def linha_q1(r, i):
        L = CL(MC0 + i)
        formulas = [
            f"=SUM(B_2020!{L}7:{L}{6 + n})",
            f"=SUM(B2_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'w_emp', n)},B_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'w_emp', n)},B2_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_renda', n)},B_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_renda', n)},B2_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_va', n)},B_2020!{L}7:{L}{6 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_va', n)},B2_2020!{L}7:{L}{6 + n})",
        ]
        for k, f in enumerate(formulas):
            ws.cell(r, 5 + k, f).number_format = NUM_MULT
        ws.cell(r, 13, f"=RANK(H{r},$H${r_ini}:$H${r_fim},0)").alignment = CENTRO
        ws.cell(r, 14, f"=RANK(J{r},$J${r_ini}:$J${r_fim},0)").alignment = CENTRO

    r_tot = _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4] + [11.5] * 10, n, m20, linha_q1)
    confere[f"Q1_Multiplicadores!E{r_ini}"] = float(mult["prod_I"][0])
    confere[f"Q1_Multiplicadores!F{r_ini}"] = float(mult["prod_II"][0])
    confere[f"Q1_Multiplicadores!G{r_ini}"] = float(mult["emp_I"][0])
    confere[f"Q1_Multiplicadores!J{r_ini}"] = float(mult["renda_II"][0])
    topk = min(10, n)
    r = r_tot + 2
    for rot, ordem, col_val in (("Ranking — geração de emprego (tipo II)", o_emp, "H"),
                                ("Ranking — geração de renda (tipo II)", o_ren, "J")):
        ws.cell(r, 2, rot).font = F_SECAO
        _cab_tabela(ws, r + 1, 2, ["#", "Atividades", "", "Multiplicador"])
        for k in range(topk):
            rr = r + 2 + k
            i = int(ordem[k])
            ws.cell(rr, 2, k + 1).alignment = CENTRO
            ws.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=4)
            ws.cell(rr, 3, f"=C{rH + 1 + i}").alignment = VCENTRO
            v = ws.cell(rr, 5, f"={col_val}{rH + 1 + i}")
            v.number_format = NUM_MULT
            for cc in (2, 3, 4, 5):
                ws.cell(rr, cc).font = F_TAB
                ws.cell(rr, cc).border = BORDA_H
                if k % 2:
                    ws.cell(rr, cc).fill = FILL_ZEBRA
        r = r + 2 + topk + 2
    _caixa_leitura(ws, r, [
        f"O efeito induzido pelo consumo das famílias amplia o encadeamento médio em "
        f"{(mult['prod_II'].mean() / mult['prod_I'].mean() - 1) * 100:.1f}% (tipo II vs tipo I).",
        f"Emprego (tipo II): {m20.nomes[o_emp[0]]}, {m20.nomes[o_emp[1]]} e "
        f"{m20.nomes[o_emp[2]]} lideram — setores trabalho-intensivos.",
        f"Renda (tipo II): {m20.nomes[o_ren[0]]}, {m20.nomes[o_ren[1]]} e "
        f"{m20.nomes[o_ren[2]]} lideram.",
    ])
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q2 — choques ================= #
    q2 = q2_cenarios(s20, 10_000.0, i_agro)
    ws = _nova_aba(wb, "Q2_Choques",
                   "Questão 2 — Choques de R$ 10 bilhões (2020)",
                   "Δx = B·Δy. Cenário (a): +R$ 10 bi nas exportações da Agricultura. "
                   "Cenário (b): +R$ 10 bi na formação bruta de capital fixo, distribuídos "
                   "pela estrutura observada da coluna de investimento da MIP.", TAB_Q)
    ganha = "a" if q2["a_agro_export"]["dprod"] >= q2["b_fbcf"]["dprod"] else "b"
    ganha_va = "a" if q2["a_agro_export"]["dva"] >= q2["b_fbcf"]["dva"] else "b"
    sint = [
        f"Produção: (a) ΔX = R$ {q2['a_agro_export']['dprod']:,.0f} mi × (b) ΔX = "
        f"R$ {q2['b_fbcf']['dprod']:,.0f} mi → maior impacto no cenário ({ganha}). "
        f"VAB: (a) R$ {q2['a_agro_export']['dva']:,.0f} mi × (b) R$ {q2['b_fbcf']['dva']:,.0f} mi "
        f"→ cenário ({ganha_va}).",
    ]
    rP = _sintese(ws, 5, sint)
    ws.cell(rP, 2, "Choque (R$ milhões) — célula editável").font = F_NEG
    ce = ws.cell(rP, 5, 10_000.0)
    ce.font = F_IN; ce.fill = FILL_IN; ce.number_format = NUM_MI; ce.border = BORDA
    ws.cell(rP, 7, f"cenário (a) aplica o choque em: {m20.nomes[i_agro]}").font = F_AUX
    Lch = f"$E${rP}"
    rH = rP + 2
    r_tot = rH + 1 + n
    lin_dya = r_tot + 2 + 5 + 2                       # após a caixa de leitura (5 linhas)
    lin_dyb = lin_dya + 1
    cab = ["Código", "Atividades", "nº", "Δx (a)", "ΔVA (a)", "Δocup (a)",
           "Δx (b)", "ΔVA (b)", "Δocup (b)"]

    def linha_q2(r, i):
        bfila = _ref_mat("B_2020", i=i, n=n)
        ws.cell(r, 5, f"=SUMPRODUCT({bfila},$E${lin_dya}:${fimM}${lin_dya})")
        ws.cell(r, 6, f"=E{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 7, f"=E{r}*{_celula_dado('2020', 'w_emp', i)}")
        ws.cell(r, 8, f"=SUMPRODUCT({bfila},$E${lin_dyb}:${fimM}${lin_dyb})")
        ws.cell(r, 9, f"=H{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 10, f"=H{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(5, 11):
            ws.cell(r, k).number_format = NUM_MI if k not in (7, 10) else "#,##0.0"

    _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4] + [12.5] * 6, n, m20, linha_q2)
    _linha_total(ws, r_tot, 10)
    for col in "EFGHIJ":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{rH + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    confere[f"Q2_Choques!E{r_tot}"] = q2["a_agro_export"]["dprod"]
    confere[f"Q2_Choques!H{r_tot}"] = q2["b_fbcf"]["dprod"]
    confere[f"Q2_Choques!F{r_tot}"] = q2["a_agro_export"]["dva"]
    confere[f"Q2_Choques!I{r_tot}"] = q2["b_fbcf"]["dva"]
    _caixa_leitura(ws, r_tot + 2, [
        f"Emprego (memo): (a) {q2['a_agro_export']['demp']:,.0f} ocupações; "
        f"(b) {q2['b_fbcf']['demp']:,.0f}.",
        "O crescimento puxado pelo agronegócio concentra o impulso numa cadeia curta e "
        "intensiva em recursos naturais — multiplica menos VA por real de choque quando a "
        "cadeia é pouco adensada e vaza para importações de insumos.",
        "A formação de capital espalha a demanda por máquinas, construção e serviços "
        "técnicos, eleva a capacidade produtiva FUTURA (efeito não capturado pelo modelo "
        "estático) e tende a gerar mais empregos urbanos.",
        "A comparação numérica diz qual efeito de CURTO PRAZO domina; a escolha de modelo "
        "de desenvolvimento envolve também a dinâmica de longo prazo.",
        "Vetores auxiliares Δy abaixo (referenciados pelas fórmulas da tabela).",
    ])
    _rotulo_aux(ws, lin_dya, "Δy do cenário (a) — vetor auxiliar (colunas E em diante)")
    _rotulo_aux(ws, lin_dyb, "Δy do cenário (b) — vetor auxiliar")
    for j in range(n):
        ca = ws.cell(lin_dya, MC0 + j, f"={Lch}" if j == i_agro else 0)
        cb = ws.cell(lin_dyb, MC0 + j,
                     f"={Lch}*{_celula_dado('2020', 'fbcf', j)}"
                     f"/SUM({_faixa_dado('2020', 'fbcf', n)})")
        for c in (ca, cb):
            c.font = F_AUX; c.number_format = NUM_MI
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q3 — UPCF ================= #
    q3 = q3_upcf(s20, 120_000.0)
    ws = _nova_aba(wb, "Q3_UPCF",
                   "Questão 3 — Reajuste do salário mínimo: +R$ 120 bi de consumo (2020)",
                   "Choque repartido pela UPCF — a cesta observada do consumo das famílias a "
                   "preço de consumidor: produtos nacionais + importados + impostos + margens "
                   "(aba 12 da MIP, coluna Famílias). Margens voltam como demanda de "
                   "comércio/transporte; impostos não geram produção.", TAB_Q)
    sint = [
        f"IMPORTAÇÕES: R$ {q3['dimp_direta']:,.0f} mi diretas + R$ {q3['dimp_induzida']:,.0f} mi "
        f"induzidas = R$ {q3['dimp_total']:,.0f} mi ({q3['dimp_total'] / 120_000:.1%} do choque).",
        f"EMPREGO: {q3['demp']:,.0f} ocupações geradas (ΔX = R$ {q3['dprod']:,.0f} mi) — "
        f"≈ {q3['demp'] / 120:,.0f} ocupações por R$ 1 bi de reajuste.",
    ]
    rP = _sintese(ws, 5, sint)
    rotP = ["Choque (editável)", "Cesta importada", "Impostos na cesta",
            "Margens de comércio", "Margens de transporte", "Cesta total (denom.)"]
    ws.cell(rP, 2, "Parâmetros da UPCF (R$ mi; aba 12 × coluna Famílias)").font = F_NEG
    for k, rtl in enumerate(rotP):
        c = ws.cell(rP + 1, 5 + k, rtl)
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA_CAB; c.alignment = CENTRO
    ws.row_dimensions[rP + 1].height = 22
    rV = rP + 2
    valores = [m20.fd_fam.get("importacao", 0.0), m20.fd_fam.get("impostos", 0.0),
               m20.fd_fam.get("margens_comercio", 0.0),
               m20.fd_fam.get("margens_transporte", 0.0)]
    ce = ws.cell(rV, 5, 120_000.0)
    ce.font = F_IN; ce.fill = FILL_IN; ce.number_format = NUM_MI; ce.border = BORDA
    for k, v in enumerate(valores):
        c = ws.cell(rV, 6 + k, float(v))
        c.font = F_TAB; c.fill = FILL_BLOCO; c.border = BORDA
        c.number_format = NUM_MI
    cd = ws.cell(rV, 10, f"=SUM({_faixa_dado('2020', 'familias', n)})+SUM(F{rV}:I{rV})")
    cd.font = F_TAB_NEG; cd.fill = FILL_TOT; cd.border = BORDA
    cd.number_format = NUM_MI
    Lch = f"$E${rV}"
    C_IMP, C_TAX, C_MGC, C_MGT = (f"$F${rV}", f"$G${rV}", f"$H${rV}", f"$I${rV}")
    DEN = f"$J${rV}"
    soma_xc = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_c"]) or "1"
    soma_xt = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_t"]) or "1"
    rH = rV + 2
    r_tot = rH + 1 + n
    lin_dy = r_tot + 2 + 6 + 2 + 5 + 2               # síntese de impactos + leitura
    cab = ["Código", "Atividades", "nº", "Δ demanda (UPCF)", "Δx induzido",
           "Δ importação induzida", "Δ ocupações"]

    def linha_q3(r, i):
        ws.cell(r, 5, f"={CL(MC0 + i)}{lin_dy}")
        ws.cell(r, 6, f"=SUMPRODUCT({_ref_mat('B_2020', i=i, n=n)},"
                      f"$E${lin_dy}:${fimM}${lin_dy})")
        ws.cell(r, 7, f"=F{r}*{_celula_dado('2020', 'm_coef', i)}")
        ws.cell(r, 8, f"=F{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(5, 9):
            ws.cell(r, k).number_format = NUM_MI if k < 8 else "#,##0.0"

    _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4, 14, 13, 14, 13], n, m20, linha_q3)
    _linha_total(ws, r_tot, 8)
    for col in "EFGH":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{rH + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    r2 = r_tot + 2
    ws.cell(r2, 2, "Síntese dos impactos").font = F_SECAO
    linhas_sint = [
        ("Importação direta (cesta importada da UPCF)",
         f"={Lch}*{C_IMP}/{DEN}", q3["dimp_direta"]),
        ("Importação induzida (insumos da produção)", f"=G{r_tot}", q3["dimp_induzida"]),
        ("IMPORTAÇÕES — TOTAL", None, q3["dimp_total"]),
        ("Impostos sobre produtos (vazamento fiscal, memo)",
         f"={Lch}*{C_TAX}/{DEN}", q3["dimposto"]),
        ("Ocupações geradas — TOTAL", f"=H{r_tot}", q3["demp"]),
    ]
    for k, (rot, formula, valor) in enumerate(linhas_sint):
        rr = r2 + 1 + k
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=5)
        c = ws.cell(rr, 2, rot)
        c.font = F_TAB_NEG; c.border = BORDA_H
        cc = ws.cell(rr, 6)
        cc.value = formula if formula else f"=F{r2 + 1}+F{r2 + 2}"
        cc.font = F_TAB_NEG; cc.number_format = NUM_MI; cc.border = BORDA_H
        if "TOTAL" in rot:
            for col in range(2, 7):
                ws.cell(rr, col).fill = FILL_TOT
        confere[f"Q3_UPCF!F{rr}"] = valor
    _caixa_leitura(ws, r2 + 7, [
        f"Composição da cesta (UPCF): "
        f"{1 - q3['share_imp_cesta'] - q3['share_imposto'] - q3['share_margens']:.1%} produtos "
        f"nacionais a preço básico; {q3['share_imp_cesta']:.1%} importados; "
        f"{q3['share_imposto']:.1%} impostos; {q3['share_margens']:.1%} margens de "
        "comércio/transporte (realocadas como demanda desses serviços).",
        "Parte relevante do estímulo vaza para o exterior (cesta importada + insumos "
        "importados da produção induzida) e para impostos.",
        "O efeito-emprego concentra-se nos setores que atendem diretamente a UPCF — "
        "ver a coluna Δ ocupações da tabela.",
        "Vetor auxiliar Δy da UPCF abaixo (referenciado pelas fórmulas da tabela).",
    ])
    _rotulo_aux(ws, lin_dy, "Δy da UPCF (nacional + margens realocadas) — vetor auxiliar")
    for j in range(n):
        termo = f"{_celula_dado('2020', 'familias', j)}"
        if j in q3["idx_c"]:
            termo += f"+{C_MGC}*{_celula_dado('2020', 'x', j)}/({soma_xc})"
        if j in q3["idx_t"]:
            termo += f"+{C_MGT}*{_celula_dado('2020', 'x', j)}/({soma_xt})"
        c = ws.cell(lin_dy, MC0 + j, f"={Lch}*({termo})/{DEN}")
        c.font = F_AUX; c.number_format = NUM_MI
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q4 — Rasmussen-Hirschman ================= #
    bl10, fl10 = s10.rasmussen()
    bl20, fl20 = s20.rasmussen()
    chave10 = (bl10 > 1) & (fl10 > 1)
    chave20 = (bl20 > 1) & (fl20 > 1)
    ws = _nova_aba(wb, "Q4_RH",
                   "Questão 4 — Rasmussen-Hirschman e setores-chave: 2010 × 2020",
                   "Convenção da aba 14 da MIP: ambos os índices pela inversa de Leontief, "
                   "normalizados pela média geral. Para trás (poder de dispersão) = soma de "
                   "COLUNA de B; para frente (sensibilidade) = soma de LINHA de B. "
                   "Setor-chave: ambos > 1.", TAB_Q)
    novos = [m20.nomes[i] for i in range(n) if chave20[i] and not chave10[i]]
    perdidos = [m20.nomes[i] for i in range(n) if chave10[i] and not chave20[i]]
    sint = [
        f"Setores-chave: {int(chave10.sum())} em 2010 → {int(chave20.sum())} em 2020 "
        "(critério estrito: U trás > 1 e U frente > 1).",
        (("Entraram: " + "; ".join(novos) + ". ") if novos else "Nenhum setor entrou. ")
        + (("Saíram: " + "; ".join(perdidos) + ".") if perdidos else "Nenhum setor saiu."),
    ]
    rH = _sintese(ws, 5, sint)
    cab = ["Código", "Atividades", "nº", "U trás 2010", "U frente 2010", "Chave 2010",
           "U trás 2020", "U frente 2020", "Chave 2020", "Δ trás", "Δ frente", "Mudança"]

    def linha_q4(r, i):
        L = CL(MC0 + i)
        for k, aba_b in enumerate(("B_2010", "B_2020")):
            cb = 5 + k * 3
            # para trás = soma de COLUNA de B; para frente = soma de LINHA de B
            # (convenção da aba 14), ambas normalizadas pela média geral de B.
            ws.cell(r, cb, f"=SUM({aba_b}!{L}7:{L}{6 + n})*{n}"
                           f"/SUM({aba_b}!$E$7:${fimM}${6 + n})")
            ws.cell(r, cb + 1, f"=SUM({_ref_mat(aba_b, i=i, n=n)})*{n}"
                               f"/SUM({aba_b}!$E$7:${fimM}${6 + n})")
            ws.cell(r, cb + 2, f'=IF(AND({CL(cb)}{r}>1,{CL(cb + 1)}{r}>1),"CHAVE","")')
            ws.cell(r, cb + 2).alignment = CENTRO
        ws.cell(r, 11, f"=H{r}-E{r}")
        ws.cell(r, 12, f"=I{r}-F{r}")
        ws.cell(r, 13, f'=IF(G{r}=J{r},"",IF(J{r}="CHAVE","entrou","saiu"))')
        ws.cell(r, 13).alignment = CENTRO
        for k in (5, 6, 8, 9, 11, 12):
            ws.cell(r, k).number_format = NUM_IDX

    r_tot = _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4] + [10.5] * 9, n, m20, linha_q4)
    confere[f"Q4_RH!E{rH + 1}"] = float(bl10[0])
    confere[f"Q4_RH!I{rH + 1}"] = float(fl20[0])
    _caixa_leitura(ws, r_tot + 2, [
        "As colunas Δ mostram onde o encadeamento para trás e para frente mudou na década — "
        "leia em conjunto com a Q7 (SDA): quedas difusas de ligação para trás indicam "
        "substituição de insumos domésticos (por importados ou por serviços); ganhos "
        "concentrados sinalizam adensamento de cadeia.",
        "Convenção: seguimos a aba 14 da MIP (ambos os índices pela inversa de Leontief). A "
        "inversa de Ghosh (abas G_2010/G_2020) oferece uma medida alternativa de "
        "sensibilidade da oferta para frente; sob ela o conjunto de setores-chave é mais "
        "amplo. Para casar com o gabarito da planilha, a classificação-chave usa Leontief.",
    ])
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q5 — campo de influência (2010) ================= #
    S = q5_campo_influencia(s10)
    ws = _nova_aba(wb, "Q5_CampoInfluencia",
                   "Questão 5 — Campos de influência dos setores (Brasil, 2010)",
                   f"Sonis & Hewings; ε = {EPS_CAMPO}. S(i,j) mede quanto uma variação no "
                   "coeficiente a(i,j) se propaga pela economia (Σ dos quadrados de "
                   "[B(ε)−B]/ε). Equivalente exato do laço em R do material de apoio "
                   "(Vale & Perobelli), via Sherman-Morrison. Matriz S como VALOR; médias e "
                   "destaques por fórmula.", TAB_Q, zoom=90)
    Srow = S.mean(1); Scol = S.mean(0)
    o_link = np.dstack(np.unravel_index(np.argsort(S, axis=None)[::-1], S.shape))[0]
    sint = [
        f"Elo de maior campo de influência: a({m10.nomes[o_link[0][0]]} → "
        f"{m10.nomes[o_link[0][1]]}), S = {S[o_link[0][0], o_link[0][1]]:,.1f}.",
        "Vendedores estratégicos (linhas): "
        + "; ".join(m10.nomes[i] for i in np.argsort(Srow)[::-1][:3])
        + ". Compradores estratégicos (colunas): "
        + "; ".join(m10.nomes[j] for j in np.argsort(Scol)[::-1][:3]) + ".",
    ]
    rH = _sintese(ws, 5, sint)
    topk = min(20, n * n)
    r_mat0 = rH + 1 + topk + 2 + 3 + 2               # após leitura (3 linhas)
    ws.column_dimensions["B"].width = 6.7
    ws.column_dimensions["C"].width = 46
    ws.column_dimensions["D"].width = 4.4
    ws.row_dimensions[rH].height = 24
    # cabeçalho do top-20 de elos: vendedor em C:D, comprador em F:I, S em K
    for c0, c1, rtl in ((2, 2, "#"), (3, 4, "Vendedor (i)"),
                        (6, 9, "Comprador (j)"), (11, 11, "S(i,j)")):
        if c1 > c0:
            ws.merge_cells(start_row=rH, start_column=c0, end_row=rH, end_column=c1)
        for cc in range(c0, c1 + 1):
            ws.cell(rH, cc).font = F_CAB
            ws.cell(rH, cc).fill = FILL_CAB
            ws.cell(rH, cc).border = BORDA_CAB
        ws.cell(rH, c0, rtl).alignment = CENTRO
    for k in range(topk):
        i, j = int(o_link[k][0]), int(o_link[k][1])
        r = rH + 1 + k
        ws.cell(r, 2, k + 1).alignment = CENTRO
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(r, 3, m10.nomes[i]).alignment = VCENTRO
        ws.merge_cells(start_row=r, start_column=6, end_row=r, end_column=9)
        ws.cell(r, 6, m10.nomes[j]).alignment = VCENTRO
        v = ws.cell(r, 11, f"={CL(MC0 + j)}{r_mat0 + 1 + i}")
        v.number_format = NUM_MI2
        for cc in range(2, 12):
            ws.cell(r, cc).font = F_TAB
            ws.cell(r, cc).border = BORDA_H
            if k % 2:
                ws.cell(r, cc).fill = FILL_ZEBRA
    _caixa_leitura(ws, rH + topk + 2, [
        "Elos com S alto são os pontos onde mudanças tecnológicas (variações de coeficiente) "
        "mais alteram a inversa de Leontief — candidatos naturais a política industrial.",
        "Coincidem majoritariamente com os setores-chave da Q4.",
        "Matriz S completa abaixo (68×68), com médias por linha e por coluna.",
    ])
    ws.cell(r_mat0 - 1, 2, "Matriz S — linhas = vendedor (i), colunas = comprador (j)").font = F_SECAO
    ws.merge_cells(start_row=r_mat0, start_column=3, end_row=r_mat0, end_column=4)
    for col, rtl in ((2, "Código"), (3, "Atividades")):
        c = ws.cell(r_mat0, col, rtl)
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    ws.cell(r_mat0, 4).fill = FILL_CAB; ws.cell(r_mat0, 4).border = BORDA
    for j in range(n):
        c = ws.cell(r_mat0, MC0 + j, j + 1)
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
        ws.column_dimensions[CL(MC0 + j)].width = 10.5
    c = ws.cell(r_mat0, MC0 + n, "média linha")
    c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    for i in range(n):
        r = r_mat0 + 1 + i
        ws.row_dimensions[r].height = 11.5
        _id_setor(ws, r, m10.cod[i], m10.nomes[i], i + 1)
        for j in range(n):
            c = ws.cell(r, MC0 + j, float(S[i, j]))
            c.number_format = NUM_MI2
        for k in range(2, MC0 + n):
            ws.cell(r, k).font = F_DADO
            ws.cell(r, k).border = BORDA
            if i % 2:
                ws.cell(r, k).fill = FILL_ZEBRA
        c = ws.cell(r, MC0 + n, f"=AVERAGE(E{r}:{fimM}{r})")
        c.font = F_DADO_NEG; c.number_format = NUM_MI2; c.border = BORDA
    r_med = r_mat0 + 1 + n
    _linha_total(ws, r_med, MC0 + n, rotulo="média coluna")
    for j in range(n):
        c = ws.cell(r_med, MC0 + j,
                    f"=AVERAGE({CL(MC0 + j)}{r_mat0 + 1}:{CL(MC0 + j)}{r_med - 1})")
        c.font = F_DADO_NEG; c.number_format = NUM_MI2
    confere[f"Q5_CampoInfluencia!E{r_mat0 + 1}"] = float(S[0, 0])
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q6 — extração hipotética ================= #
    q6 = q6_extracao(s20, i_q6)
    ws = _nova_aba(wb, "Q6_Extracao",
                   "Questão 6 — Extração hipotética total (2020)",
                   f"Setor extraído: {m20.nomes[i_q6]}. Zera-se a linha e a coluna do setor em "
                   "A e sua demanda final; a perda é a diferença entre a produção do sistema "
                   "completo (x = B·y) e a do sistema reduzido. Coluna 'x reduzido' colada como "
                   "VALOR (nova inversão); demais colunas por fórmula.", TAB_Q)
    perda_rel = q6["perda"] / np.where(q6["x_base"] == 0, 1, q6["x_base"])
    o_par = np.argsort(np.where(np.arange(n) == i_q6, -1, perda_rel))[::-1]
    sint = [
        f"Perda agregada: R$ {q6['perda_total']:,.0f} mi ({q6['perda_pct']:.2%} da produção); "
        f"VA: R$ {q6['perda_va']:,.0f} mi; ocupações: {q6['perda_emp']:,.0f}.",
        "Mais paralisados (excluído o próprio): "
        + "; ".join(f"{m20.nomes[i]} ({perda_rel[i]:.1%})" for i in o_par[:3]) + ".",
    ]
    rH = _sintese(ws, 5, sint)
    cab = ["Código", "Atividades", "nº", "x baseline (B·y)", "x reduzido (valor)",
           "Perda", "Perda (% do setor)"]

    def linha_q6(r, i):
        ws.cell(r, 5, float(q6["x_base"][i])).number_format = NUM_MI
        ws.cell(r, 6, float(q6["x_ex"][i])).number_format = NUM_MI
        ws.cell(r, 7, f"=E{r}-F{r}").number_format = NUM_MI
        ws.cell(r, 8, f"=IF(E{r}=0,0,G{r}/E{r})").number_format = NUM_PCT

    r_tot = _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4, 15, 15, 15, 13], n, m20,
                             linha_q6, destaque=i_q6)
    _linha_total(ws, r_tot, 8)
    for col in "EFG":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{rH + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    ws[f"H{r_tot}"] = f"=G{r_tot}/E{r_tot}"
    ws[f"H{r_tot}"].font = F_TAB_NEG; ws[f"H{r_tot}"].number_format = NUM_PCT
    confere[f"Q6_Extracao!G{r_tot}"] = q6["perda_total"]
    _caixa_leitura(ws, r_tot + 2, [
        "A extração mede a dependência estrutural da economia em relação ao setor — compare "
        "com a Q4: setores-chave tendem a paralisar mais cadeias quando extraídos.",
        "A linha destacada em laranja-pastel é o setor extraído (a perda inclui a própria "
        "produção dele).",
    ])
    ws.freeze_panes = f"E{rH + 1}"

    # ================= Q7 — SDA ================= #
    fator = float(np.prod([1 + v / 100 for v in IPCA_ANUAL.values()]))
    q7 = q7_sda(s10, s20, fator)
    ws = _nova_aba(wb, "Q7_SDA",
                   "Questão 7 — Decomposição estrutural 2010→2020 (IPCA)",
                   "SDA bipolar média: Δx = ½ΔB·(y0*+y1) + ½(B0+B1)·Δy, com y0* = y2010 × "
                   "fator IPCA acumulado. O deflator único não altera A/B de 2010 "
                   "(coeficientes são razões) — atualiza apenas os níveis.", TAB_Q)
    dtec, ddem, ddx = q7["tec"].sum(), q7["dem"].sum(), q7["dx"].sum()
    sint = [
        f"Δx total (preços de 2020): R$ {ddx:,.0f} mi = EFEITO TECNOLOGIA (ΔB) "
        f"R$ {dtec:,.0f} mi ({dtec / ddx:.1%}) + EFEITO DEMANDA FINAL (Δy) "
        f"R$ {ddem:,.0f} mi ({ddem / ddx:.1%}). Fator IPCA: {fator:.4f}.",
    ]
    rP = _sintese(ws, 5, sint)
    ws.cell(rP, 2, "IPCA % a.a. (IBGE) — células editáveis").font = F_NEG
    for k, (ano, v) in enumerate(sorted(IPCA_ANUAL.items())):
        c = ws.cell(rP + 1, 5 + k, str(ano))
        c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA_CAB; c.alignment = CENTRO
        c = ws.cell(rP + 2, 5 + k, v)
        c.font = F_IN; c.fill = FILL_IN; c.border = BORDA
        c.number_format = "0.00"; c.alignment = CENTRO
    c = ws.cell(rP + 1, 6 + len(IPCA_ANUAL), "fator acumulado")
    c.font = F_CAB8; c.fill = FILL_CAB; c.border = BORDA_CAB; c.alignment = CENTRO
    fator_expr = "=" + "*".join(f"(1+{CL(5 + k)}{rP + 2}/100)"
                                for k in range(len(IPCA_ANUAL)))
    c_fat = ws.cell(rP + 2, 6 + len(IPCA_ANUAL), fator_expr)
    c_fat.font = F_TAB_NEG; c_fat.fill = FILL_TOT; c_fat.number_format = "0.0000"
    c_fat.border = BORDA; c_fat.alignment = CENTRO
    FAT = f"${CL(6 + len(IPCA_ANUAL))}${rP + 2}"
    rH = rP + 4
    r_tot = rH + 1 + n
    lin_ysum = r_tot + 2 + 3 + 2                     # após a caixa de leitura (3 linhas)
    lin_ydel = lin_ysum + 1
    cab = ["Código", "Atividades", "nº", "x 2010 a preços 2020", "x 2020", "Δx",
           "Efeito tecnologia (ΔB)", "Efeito demanda (Δy)", "Checagem (tec+dem−Δx)"]

    def linha_q7(r, i):
        b0 = _ref_mat("B_2010", i=i, n=n)
        b1 = _ref_mat("B_2020", i=i, n=n)
        ws.cell(r, 5, f"={_celula_dado('2010', 'x', i)}*{FAT}")
        ws.cell(r, 6, f"={_celula_dado('2020', 'x', i)}")
        ws.cell(r, 7, f"=F{r}-E{r}")
        ws.cell(r, 8, f"=0.5*(SUMPRODUCT({b1},$E${lin_ysum}:${fimM}${lin_ysum})"
                      f"-SUMPRODUCT({b0},$E${lin_ysum}:${fimM}${lin_ysum}))")
        ws.cell(r, 9, f"=0.5*(SUMPRODUCT({b1},$E${lin_ydel}:${fimM}${lin_ydel})"
                      f"+SUMPRODUCT({b0},$E${lin_ydel}:${fimM}${lin_ydel}))")
        ws.cell(r, 10, f"=H{r}+I{r}-G{r}")
        for k in range(5, 11):
            ws.cell(r, k).number_format = NUM_MI

    _tabela_setorial(ws, rH, cab, [6.7, 46, 4.4, 15, 14, 14, 15, 15, 14], n, m20, linha_q7)
    _linha_total(ws, r_tot, 10)
    for col in "EFGHIJ":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{rH + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    confere[f"Q7_SDA!H{r_tot}"] = float(q7["tec"].sum())
    confere[f"Q7_SDA!I{r_tot}"] = float(q7["dem"].sum())
    _caixa_leitura(ws, r_tot + 2, [
        "Efeito-demanda dominante com efeito-tecnologia menor é o padrão de uma década de "
        "crescimento extensivo; onde o efeito-tecnologia é negativo houve desadensamento de "
        "cadeia (consistente com as mudanças de ligação da Q4).",
        "A coluna 'checagem' comprova a aditividade exata da decomposição em cada setor.",
        "Vetores auxiliares (y0*+y1 e y1−y0*) abaixo, referenciados pelas fórmulas.",
    ])
    _rotulo_aux(ws, lin_ysum, "y0*+y1 — vetor auxiliar (colunas E em diante)")
    _rotulo_aux(ws, lin_ydel, "y1−y0* — vetor auxiliar")
    for j in range(n):
        y0 = f"{_celula_dado('2010', 'ytot', j)}*{FAT}"
        y1 = f"{_celula_dado('2020', 'ytot', j)}"
        ca = ws.cell(lin_ysum, MC0 + j, f"={y0}+{y1}")
        cb = ws.cell(lin_ydel, MC0 + j, f"={y1}-{y0}")
        for c in (ca, cb):
            c.font = F_AUX; c.number_format = NUM_MI
    ws.freeze_panes = f"E{rH + 1}"

    wb.save(saida)
    return confere


# =========================================================================== #
# 3. SELFTEST — valida identidades e o Excel de ponta a ponta com dados sintéticos
# =========================================================================== #
def selftest(pasta_tmp: str) -> str:
    os.makedirs(pasta_tmp, exist_ok=True)
    f10 = os.path.join(pasta_tmp, "MIP-BR 2010 (sintetica).xlsx")
    f20 = os.path.join(pasta_tmp, "MIP-BR 2020 (sintetica).xlsx")
    escrever_sintetico(f10, 2010)
    escrever_sintetico(f20, 2020)
    m10 = carregar_mip(f10, 2010)
    m20 = carregar_mip(f20, 2020)
    for m in (m10, m20):
        avisos = m.validar()
        assert not any("zerado" in a for a in avisos), avisos
    s10, s20 = Sistema(m10), Sistema(m20)

    mult = s20.multiplicadores()
    assert (s20.B >= -1e-9).all(), "B com entrada negativa"
    assert (mult["prod_II"] >= mult["prod_I"] - 1e-9).all(), "tipo II < tipo I"
    assert (mult["renda_II"] >= mult["renda_I"] - 1e-9).all()

    q2 = q2_cenarios(s20, 10_000.0, i_agro=0)
    for cen in q2.values():
        assert abs(cen["dx"].sum() - cen["dprod"]) < 1e-6
        assert cen["dva"] < cen["dprod"]

    q3 = q3_upcf(s20, 120_000.0)
    assert q3["dimp_total"] > 0 and q3["demp"] > 0
    assert q3["idx_c"] and q3["idx_t"], "grupos de margem não encontrados no sintético"

    bl, fl = s20.rasmussen()
    assert abs(bl.mean() - 1) < 1e-9, "média das ligações para trás deve ser 1"

    S = q5_campo_influencia(s10)
    assert (S > 0).all()
    # confere Sherman-Morrison contra o laço explícito (convenção do material em R)
    i, j = 1, 2
    Aeps = s10.A.copy(); Aeps[i, j] += EPS_CAMPO
    F = (np.linalg.inv(np.eye(s10.n) - Aeps) - s10.B) / EPS_CAMPO
    assert abs((F ** 2).sum() - S[i, j]) < 1e-6 * S[i, j]

    q6 = q6_extracao(s20, j=0)
    assert q6["perda_total"] > 0 and q6["perda_pct"] < 1

    fator = float(np.prod([1 + v / 100 for v in IPCA_ANUAL.values()]))
    q7 = q7_sda(s10, s20, fator)
    assert np.allclose(q7["tec"] + q7["dem"], q7["dx"], atol=1e-6)

    saida = os.path.join(pasta_tmp, "Lista_selftest.xlsx")
    confere = gerar_excel(saida, m10, m20, s10, s20, i_agro=0, i_q6=0, sintetico=True)
    print(f"[selftest] identidades OK; Excel sintético em {saida}")
    print(f"[selftest] células de conferência: {len(confere)} — rode o recálculo "
          "(LibreOffice/Excel) e compare com verificar_recalculo().")
    with open(os.path.join(pasta_tmp, "confere.json"), "w", encoding="utf-8") as fh:
        json.dump(confere, fh, ensure_ascii=False, indent=1)
    return saida


def verificar_recalculo(xlsx: str, confere: dict[str, float], tol=5e-4) -> list[str]:
    """Compara células recalculadas com os valores do NumPy (tolerância relativa)."""
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    erros = []
    for ref, esperado in confere.items():
        aba, cel = ref.split("!")
        obtido = wb[aba][cel].value
        if obtido is None:
            erros.append(f"{ref}: recalculo vazio (esperado {esperado:.4f})")
            continue
        den = max(1.0, abs(esperado))
        if abs(float(obtido) - esperado) / den > tol:
            erros.append(f"{ref}: {obtido} != {esperado} (tol {tol})")
    wb.close()
    return erros


# =========================================================================== #
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--m2010", help="caminho da MIP-BR 2010 (Nível 68) .xlsm/.xlsx")
    ap.add_argument("--m2020", help="caminho da MIP-BR 2020 (Nível 68) .xlsm/.xlsx")
    ap.add_argument("--out", default=str(RAIZ / "lista" / "Lista_Exercicios_Respostas.xlsx"))
    ap.add_argument("--setor-q6", default=SETOR_Q6_PADRAO,
                    help="padrão do nome do setor da extração hipotética (Q6)")
    ap.add_argument("--setor-agro", default="agricultura",
                    help="padrão do nome do setor do choque exportador (Q2a)")
    ap.add_argument("--inspect", metavar="ARQ", help="relata o layout de um arquivo e sai")
    ap.add_argument("--selftest", action="store_true", help="validação com dados sintéticos")
    args = ap.parse_args()

    if args.inspect:
        print(inspecionar(args.inspect))
        return
    if args.selftest:
        selftest(os.environ.get("LISTA_TMP", str(RAIZ / "lista" / "tmp_selftest")))
        return
    if not (args.m2010 and args.m2020):
        ap.error("informe --m2010 e --m2020 (ou use --selftest / --inspect)")

    m10 = carregar_mip(args.m2010, 2010)
    m20 = carregar_mip(args.m2020, 2020)
    for m, arq in ((m10, args.m2010), (m20, args.m2020)):
        for a in m.validar():
            print(f"[aviso {m.ano}] {a}")
        tot = m.x.sum()
        print(f"[{m.ano}] {m.n} setores; VBP total R$ {tot:,.0f} mi")
        if not 5e6 < tot < 5e7:
            print(f"[aviso {m.ano}] VBP total fora da ordem de grandeza esperada para o "
                  "Brasil — confira a unidade (esperado: R$ milhões)")
        A13 = carregar_A_conferencia(arq)
        if A13 is not None and A13.shape == (m.n, m.n):
            A_calc = coef_tecnicos(m.Z, m.x)
            print(f"[{m.ano}] conferência A (Z/x̂) vs aba 13 do arquivo: "
                  f"desvio máximo {np.abs(A_calc - A13).max():.2e}")
        else:
            print(f"[{m.ano}] aba 13 indisponível p/ conferência — seguindo com Z/x̂")
    if [norm(x) for x in m10.nomes] != [norm(x) for x in m20.nomes]:
        print("[aviso] classificações de 2010 e 2020 diferem — Q4/Q7 exigem setores alinhados")

    s10, s20 = Sistema(m10), Sistema(m20)
    i_agro = indice_setor(m20, args.setor_agro)
    i_q6 = indice_setor(m20, args.setor_q6)
    print(f"[Q2a] setor do choque exportador: {m20.nomes[i_agro]}")
    print(f"[Q6] setor extraído: {m20.nomes[i_q6]}")

    confere = gerar_excel(args.out, m10, m20, s10, s20, i_agro, i_q6)
    with open(Path(args.out).with_suffix(".confere.json"), "w", encoding="utf-8") as fh:
        json.dump(confere, fh, ensure_ascii=False, indent=1)
    print(f"[ok] planilha gerada: {args.out}")
    print("=> recalcule as fórmulas (abrir no Excel/LibreOffice ou scripts/recalc) e rode "
          "verificar_recalculo() com o .confere.json para a prova final.")


if __name__ == "__main__":
    main()
