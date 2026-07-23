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

        # fechamento tipo II (famílias endógenas): linha = renda (remunerações),
        # coluna = consumo das famílias / massa de remunerações  [pesquisa/17]
        hh = mip.rem.sum()
        self.hc = mip.y["familias"] / (hh if hh else 1.0)
        A2 = np.zeros((n + 1, n + 1))
        A2[:n, :n] = self.A
        A2[:n, n] = self.hc
        A2[n, :n] = self.v_renda
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

    # ---- Q4: ligações de Rasmussen-Hirschman (backward Leontief, forward Ghosh)
    def rasmussen(self) -> tuple[np.ndarray, np.ndarray]:
        n = self.n
        bl = self.B.sum(0) / n / self.B.mean()
        fl = self.G.sum(1) / n / self.G.mean()
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
# 2. GERADOR DO EXCEL — diagramação no padrão da planilha do professor
#    (Calibri; título 26 azul em B2; margem na coluna A; código/atividade/índice
#    nas colunas B/C/D; dados a partir de E; sem linhas de grade; cabeçalhos em
#    azul-escuro; linhas de síntese em verde; abas coloridas por grupo)
# =========================================================================== #
CALIBRI = "Calibri"
AZUL_TITULO = "FF0070C0"
AZUL_CAB = "FF305496"          # accent1 -25% (cabeçalhos da planilha-fonte)
AZUL_TAB_CAPA = "FF002060"     # cor das abas iniciais da planilha-fonte
CINZA_TAB = "FF808080"
CINZA_BLOCO = "FFD9D9D9"       # linhas de decomposição (padrão da aba 12)
CINZA_CAIXA = "FFF2F2F2"       # caixa de resposta
VERDE_TOT = "FF00B050"         # linhas-síntese (padrão das abas 12/13)
AMARELO_IN = "FFFFFF00"

F_TITULO = Font(name=CALIBRI, size=26, bold=True, color=AZUL_TITULO)
F_NOTA = Font(name=CALIBRI, size=10, bold=True, color="FF000000")
F_CAB = Font(name=CALIBRI, size=8, bold=True, color="FFFFFFFF")
F_DADO = Font(name=CALIBRI, size=8)
F_DADO_NEG = Font(name=CALIBRI, size=8, bold=True)
F_TAB = Font(name=CALIBRI, size=9)
F_TAB_NEG = Font(name=CALIBRI, size=9, bold=True)
F_TXT = Font(name=CALIBRI, size=10)
F_NEG = Font(name=CALIBRI, size=10, bold=True)
F_SECAO = Font(name=CALIBRI, size=11, bold=True, color=AZUL_CAB)
F_IN = Font(name=CALIBRI, size=10, bold=True, color="FF0000FF")   # entrada editável
F_AUX = Font(name=CALIBRI, size=8, italic=True, color="FF808080")

FILL_CAB = PatternFill("solid", fgColor=AZUL_CAB)
FILL_TOT = PatternFill("solid", fgColor=VERDE_TOT)
FILL_BLOCO = PatternFill("solid", fgColor=CINZA_BLOCO)
FILL_CAIXA = PatternFill("solid", fgColor=CINZA_CAIXA)
FILL_IN = PatternFill("solid", fgColor=AMARELO_IN)
FINA = Side(style="thin", color="FF9E9E9E")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
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


def _nova_aba(wb, nome, titulo, nota, cor_tab):
    """Aba no padrão da planilha-fonte: coluna A estreita, linha 1 baixa, título
    26pt azul em B2, nota em negrito em B3 (caixa com quebra), sem grade."""
    ws = wb.create_sheet(nome)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = cor_tab
    ws.column_dimensions["A"].width = 0.9
    ws.row_dimensions[1].height = 6.6
    ws.row_dimensions[2].height = 33.6
    ws.cell(2, 2, titulo).font = F_TITULO
    ws.cell(2, 2).alignment = VCENTRO
    if nota:
        ws.merge_cells(start_row=3, start_column=2, end_row=3, end_column=LCOL_TXT)
        c = ws.cell(3, 2, nota)
        c.font = F_NOTA; c.alignment = QUEBRA
        ws.row_dimensions[3].height = max(15, 13 * math.ceil(len(nota) / 165))
    return ws


def _caixa_resposta(ws, linha0, linhas_texto):
    """Caixa 'Resposta' organizada: um marcador por linha, fundo cinza-claro."""
    ws.cell(linha0, 2, "Resposta / leitura dos resultados").font = F_SECAO
    r = linha0 + 1
    for t in linhas_texto:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=LCOL_TXT)
        c = ws.cell(r, 2, "•  " + t)
        c.font = F_TXT; c.alignment = QUEBRA; c.fill = FILL_CAIXA
        for k in range(3, LCOL_TXT + 1):
            ws.cell(r, k).fill = FILL_CAIXA
        ws.row_dimensions[r].height = max(14, 13.5 * math.ceil(len(t) / 155))
        r += 1
    return r + 1                                    # linha livre após a caixa


def _cab_tabela(ws, linha, col0, rotulos, larguras=None):
    ws.row_dimensions[linha].height = 24
    for k, rtl in enumerate(rotulos):
        c = ws.cell(linha, col0 + k, rtl)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
        if larguras:
            ws.column_dimensions[CL(col0 + k)].width = larguras[k]


def _linha_total(ws, linha, col_ini, col_fim, rotulo="TOTAL", col_rotulo=3):
    """linha-síntese verde no padrão da planilha-fonte."""
    ws.cell(linha, col_rotulo, rotulo).font = F_TAB_NEG
    for k in range(2, col_fim + 1):
        ws.cell(linha, k).fill = FILL_TOT
        ws.cell(linha, k).border = BORDA
    _ = col_ini


def _rotulo_aux(ws, linha, texto):
    c = ws.cell(linha, 3, texto)
    c.font = F_AUX


def _matriz(ws, M, nomes, cods, fmt=NUM_MULT, extra_rotulo=None):
    """Matriz na gramática da planilha-fonte: Código (B), Atividades (C:D com o
    índice da linha em D), índices 1..n no cabeçalho e dados a partir de E7."""
    nlin, ncol = M.shape
    ws.merge_cells(start_row=6, start_column=3, end_row=6, end_column=4)
    for col, rtl in ((2, "Código"), (3, "Atividades")):
        c = ws.cell(6, col, rtl)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    ws.cell(6, 4).fill = FILL_CAB; ws.cell(6, 4).border = BORDA
    ws.column_dimensions["B"].width = 6.7
    ws.column_dimensions["C"].width = 62
    ws.column_dimensions["D"].width = 4.4
    for j in range(ncol):
        c = ws.cell(6, MC0 + j, extra_rotulo if j >= len(cods) else j + 1)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
        ws.column_dimensions[CL(MC0 + j)].width = 10.5
    ws.row_dimensions[6].height = 15
    for i in range(nlin):
        r = MR0 + i
        ws.row_dimensions[r].height = 11
        eh_extra = i >= len(nomes)
        c = ws.cell(r, 2, extra_rotulo if eh_extra else cods[i])
        c.font = F_DADO; c.border = BORDA; c.alignment = CENTRO
        c = ws.cell(r, 3, "Famílias (renda ↔ consumo)" if eh_extra else nomes[i])
        c.font = F_DADO; c.border = BORDA; c.alignment = VCENTRO
        c = ws.cell(r, 4, i + 1)
        c.font = F_DADO; c.border = BORDA; c.alignment = CENTRO
        for j in range(ncol):
            c = ws.cell(r, MC0 + j, float(M[i, j]))
            c.font = F_DADO; c.border = BORDA
            c.number_format = fmt; c.alignment = VCENTRO
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
                   f"DADOS — MIP BRASIL {tag}",
                   "(valores correntes em R$ milhões; ocupações em pessoas) — vetores extraídos "
                   "da aba 12 da MIP-BR (Nível 68), NEREUS/CECEG; coeficientes por unidade de "
                   "produção calculados por fórmula nas colunas Q a T.", CINZA_TAB)
    rot = ["Código", "Atividades", "nº", "VBP (x)", "Remunerações", "VA (PIB)",
           "Ocupações", "Importação intermediária", "Exportações", "Governo",
           "ISFLSF", "Consumo das famílias (nac.)", "FBCF", "Variação de estoques",
           "Demanda final total", "w = ocup/x", "v renda = rem/x", "v VA = VA/x",
           "m = imp/x"]
    _cab_tabela(ws, 6, 2, rot,
                larguras=[6.7, 62, 4.4] + [12.5] * (len(rot) - 3))
    n = mip.n
    for i in range(n):
        r = MR0 + i
        ws.row_dimensions[r].height = 11
        ws.cell(r, 2, mip.cod[i]).alignment = CENTRO
        ws.cell(r, 3, mip.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
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
    r_tot = MR0 + n
    _linha_total(ws, r_tot, 2, 20)
    for col in "EFGHIJKLMNOP":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}7:{col}{6 + n})"
        c.font = F_DADO_NEG; c.number_format = NUM_MI2
    ws.freeze_panes = "E7"
    return ws


def _linha_indices(ws, linha, n, rotulo):
    """cabeçalho auxiliar 1..n (para linhas de vetor nas abas de questão)."""
    _rotulo_aux(ws, linha, rotulo)
    for j in range(n):
        c = ws.cell(linha, MC0 + j)
        c.font = F_AUX


def gerar_excel(saida: str, m10: MIPAno, m20: MIPAno, s10: Sistema, s20: Sistema,
                i_agro: int, i_q6: int, sintetico: bool = False) -> dict:
    """Escreve a pasta de trabalho completa; devolve dicionário de conferência
    {celula: valor_python} para validação pós-recálculo."""
    n = m20.n
    confere: dict[str, float] = {}
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # ---------------- Capa ---------------- #
    ws = _nova_aba(wb, "Capa", "LISTA DE EXERCÍCIOS — ANÁLISE DE INSUMO-PRODUTO",
                   None, AZUL_TAB_CAPA)
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 92
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
        c.font = Font(name=CALIBRI, size=12, bold=True, color="FFC00000")
        r += 2
    for rot, txt in info:
        ws.cell(r, 2, rot).font = F_NEG
        c = ws.cell(r, 3, txt)
        c.font = F_TXT; c.alignment = QUEBRA
        ws.row_dimensions[r].height = max(15, 13 * math.ceil(len(txt) / 90))
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
    _cab_tabela(ws, r, 2, ["Aba", "Conteúdo"], larguras=[34, 92])
    for k, (aba, desc) in enumerate(guia):
        rr = r + 1 + k
        ws.cell(rr, 2, aba).font = F_TAB_NEG
        ws.cell(rr, 3, desc).font = F_TAB
        for cc in (2, 3):
            ws.cell(rr, cc).border = BORDA
            ws.cell(rr, cc).alignment = VCENTRO
    r = r + len(guia) + 2
    ws.cell(r, 2, "Legenda de células").font = F_SECAO
    legenda = [
        (F_IN, FILL_IN, "Azul sobre amarelo — entrada editável (choques, IPCA): a pasta recalcula"),
        (F_TAB, FILL_BLOCO, "Cinza — decomposições e parâmetros lidos da MIP (aba 12)"),
        (F_TAB_NEG, FILL_TOT, "Verde — linhas-síntese/totais (padrão da planilha-fonte)"),
        (F_TAB, None, "Sem preenchimento — fórmula viva sobre as abas de dados/matrizes"),
    ]
    for k, (f, fill, txt) in enumerate(legenda):
        rr = r + 1 + k
        c = ws.cell(rr, 2, "célula")
        c.font = f; c.border = BORDA; c.alignment = CENTRO
        if fill:
            c.fill = fill
        ws.cell(rr, 3, txt).font = F_TXT

    # ---------------- Metodologia ---------------- #
    ws = _nova_aba(wb, "Metodologia", "NOTAS METODOLÓGICAS E PREMISSAS",
                   "Todas as hipóteses assumidas na resolução estão listadas aqui; "
                   "as fórmulas citadas seguem Miller & Blair (2009).", AZUL_TAB_CAPA)
    met = [
        "1. Modelo aberto: A = Z·x̂⁻¹ sobre os fluxos NACIONAIS (aba 12 da MIP-BR); "
        "B = (I−A)⁻¹ (Leontief); Ghosh: G = (I−x̂⁻¹Z)⁻¹. As matrizes B, G e B2 estão coladas "
        "como VALORES (inversão 68×68 feita externamente em NumPy — conferível por MINVERSE; "
        "a matriz A reproduz a aba 13 do arquivo-fonte com desvio < 1e-15); todas as demais "
        "células derivam delas por fórmula e recalculam.",
        "2. Tipo II: modelo fechado para as famílias — coluna adicional = consumo das famílias "
        "por unidade de massa de remunerações; linha adicional = remunerações por unidade de "
        "produção (idêntico a pesquisa/17 do repositório).",
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
        "6. Q4: ligação para trás pela inversa de Leontief e para frente pela inversa de GHOSH "
        "(Miller & Blair, 2009), normalizadas pela média geral; setor-chave: ambas > 1.",
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
        r += 1

    # ---------------- Setores ---------------- #
    ws = _nova_aba(wb, "Setores", "CLASSIFICAÇÃO SETORIAL",
                   "Nível 68 (NEREUS/CECEG) — comum às matrizes de 2010 e 2020.",
                   AZUL_TAB_CAPA)
    _cab_tabela(ws, 6, 2, ["Código", "Atividades", "nº"], larguras=[8, 70, 5])
    for i in range(n):
        r = MR0 + i
        for cc, v in ((2, m20.cod[i]), (3, m20.nomes[i]), (4, i + 1)):
            c = ws.cell(r, cc, v)
            c.font = F_TAB; c.border = BORDA
            c.alignment = CENTRO if cc != 3 else VCENTRO

    # ---------------- Dados e matrizes ---------------- #
    _aba_dados(wb, "2020", m20)
    _aba_dados(wb, "2010", m10)
    matrizes = [
        ("A_2020", s20.A, m20, "MATRIZ A — COEFICIENTES TÉCNICOS NACIONAIS (2020)",
         "a(i,j) = Z(i,j)/x(j); reproduz a aba 13 do arquivo-fonte (desvio < 1e-15).", None),
        ("B_2020", s20.B, m20, "MATRIZ B — INVERSA DE LEONTIEF (2020)",
         "B = (I−A)⁻¹, colada como VALOR (inversão externa NumPy; confira com MINVERSE). "
         "Base das fórmulas das questões.", None),
        ("G_2020", s20.G, m20, "MATRIZ G — INVERSA DE GHOSH (2020)",
         "G = (I−x̂⁻¹Z)⁻¹, colada como VALOR; usada na ligação para frente (Q4).", None),
        ("B2_2020", s20.B2, m20, "MATRIZ B2 — MODELO FECHADO PARA AS FAMÍLIAS (2020)",
         "Inversa do sistema com famílias endógenas (tipo II); última linha/coluna = famílias.",
         "FAM"),
        ("A_2010", s10.A, m10, "MATRIZ A — COEFICIENTES TÉCNICOS NACIONAIS (2010)",
         "a(i,j) = Z(i,j)/x(j); reproduz a aba 13 do arquivo-fonte (desvio < 1e-15).", None),
        ("B_2010", s10.B, m10, "MATRIZ B — INVERSA DE LEONTIEF (2010)",
         "B = (I−A)⁻¹, colada como VALOR; usada em Q4 e Q7.", None),
        ("G_2010", s10.G, m10, "MATRIZ G — INVERSA DE GHOSH (2010)",
         "G = (I−x̂⁻¹Z)⁻¹, colada como VALOR; usada na ligação para frente (Q4).", None),
    ]
    for nome, M, mp, tit, nota, extra in matrizes:
        ws = _nova_aba(wb, nome, tit, nota, CINZA_TAB)
        _matriz(ws, M, mp.nomes, mp.cod, fmt=NUM_MULT, extra_rotulo=extra)

    fimM = CL(MC0 - 1 + n)                       # última coluna das matrizes

    # ================= Q1 — multiplicadores ================= #
    mult = s20.multiplicadores()
    ws = _nova_aba(wb, "Q1_Multiplicadores",
                   "QUESTÃO 1 — MULTIPLICADORES (2020), TIPOS I E II",
                   "Multiplicadores de produção, emprego, renda e valor adicionado para todos "
                   "os setores. Tipo I: modelo aberto (matriz B_2020). Tipo II: modelo fechado "
                   "para as famílias (matriz B2_2020). Emprego em ocupações por R$ 1 milhão; "
                   "renda e VA em R$ por R$ 1,00 de demanda final.", "FF0070C0")
    o_emp = np.argsort(mult["emp_II"])[::-1]
    o_ren = np.argsort(mult["renda_II"])[::-1]
    resp = [
        f"Multiplicador de produção médio (2020): {mult['prod_I'].mean():.3f} (tipo I) e "
        f"{mult['prod_II'].mean():.3f} (tipo II) — o efeito induzido pelo consumo das famílias "
        f"amplia o encadeamento médio em {(mult['prod_II'].mean() / mult['prod_I'].mean() - 1) * 100:.1f}%.",
        f"Maior capacidade de GERAÇÃO DE EMPREGO (tipo II): {m20.nomes[o_emp[0]]} "
        f"({mult['emp_II'][o_emp[0]]:.1f} ocup./R$ mi), seguido de {m20.nomes[o_emp[1]]} e "
        f"{m20.nomes[o_emp[2]]} — setores trabalho-intensivos lideram.",
        f"Maior capacidade de GERAÇÃO DE RENDA (tipo II): {m20.nomes[o_ren[0]]} "
        f"(R$ {mult['renda_II'][o_ren[0]]:.3f} por R$ 1,00), seguido de {m20.nomes[o_ren[1]]} e "
        f"{m20.nomes[o_ren[2]]}.",
        "Rankings de emprego e renda nas duas tabelas à direita; a tabela principal traz os "
        "oito multiplicadores por setor com a posição em cada ranking.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    cab = ["Código", "Atividades", "nº", "Produção I", "Produção II",
           "Emprego I (ocup/R$ mi)", "Emprego II (ocup/R$ mi)", "Renda I", "Renda II",
           "VA I", "VA II", "Rank emprego II", "Rank renda II"]
    _cab_tabela(ws, r0, 2, cab, larguras=[6.7, 46, 4.4] + [11.5] * 10)
    r_ini, r_fim = r0 + 1, r0 + n
    for i in range(n):
        r = r0 + 1 + i
        L = CL(MC0 + i)
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
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
            c = ws.cell(r, 5 + k, f)
            c.number_format = NUM_MULT
        ws.cell(r, 13, f"=RANK(H{r},$H${r_ini}:$H${r_fim},0)").alignment = CENTRO
        ws.cell(r, 14, f"=RANK(J{r},$J${r_ini}:$J${r_fim},0)").alignment = CENTRO
        for k in range(2, 15):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
    confere[f"Q1_Multiplicadores!E{r_ini}"] = float(mult["prod_I"][0])
    confere[f"Q1_Multiplicadores!F{r_ini}"] = float(mult["prod_II"][0])
    confere[f"Q1_Multiplicadores!G{r_ini}"] = float(mult["emp_I"][0])
    confere[f"Q1_Multiplicadores!J{r_ini}"] = float(mult["renda_II"][0])
    topk = min(10, n)
    for bloco, (rot, ordem, col_val) in enumerate(
            [("RANKING — GERAÇÃO DE EMPREGO (TIPO II)", o_emp, "H"),
             ("RANKING — GERAÇÃO DE RENDA (TIPO II)", o_ren, "J")]):
        c0 = 16 + bloco * 4
        ws.cell(r0 - 1, c0, rot).font = F_SECAO
        _cab_tabela(ws, r0, c0, ["#", "Atividades", "Multiplicador"],
                    larguras=[4, 40, 12])
        for k in range(topk):
            r = r0 + 1 + k
            i = int(ordem[k])
            ws.cell(r, c0, k + 1).alignment = CENTRO
            ws.cell(r, c0 + 1, f"=C{r0 + 1 + i}").alignment = VCENTRO
            v = ws.cell(r, c0 + 2, f"={col_val}{r0 + 1 + i}")
            v.number_format = NUM_MULT
            for cc in range(c0, c0 + 3):
                ws.cell(r, cc).font = F_TAB
                ws.cell(r, cc).border = BORDA
    ws.freeze_panes = f"E{r0 + 1}"

    # ================= Q2 — choques ================= #
    q2 = q2_cenarios(s20, 10_000.0, i_agro)
    ws = _nova_aba(wb, "Q2_Choques",
                   "QUESTÃO 2 — CHOQUES DE R$ 10 BILHÕES (2020)",
                   "Δx = B·Δy. Cenário (a): +R$ 10 bi nas exportações da Agricultura. "
                   "Cenário (b): +R$ 10 bi na formação bruta de capital fixo, distribuídos "
                   "pela estrutura observada da coluna de investimento da MIP.", "FF0070C0")
    ganha = "a" if q2["a_agro_export"]["dprod"] >= q2["b_fbcf"]["dprod"] else "b"
    ganha_va = "a" if q2["a_agro_export"]["dva"] >= q2["b_fbcf"]["dva"] else "b"
    resp = [
        f"Produção nacional: cenário (a) gera ΔX = R$ {q2['a_agro_export']['dprod']:,.0f} mi; "
        f"cenário (b) gera ΔX = R$ {q2['b_fbcf']['dprod']:,.0f} mi → maior impacto no "
        f"cenário ({ganha}).",
        f"Valor adicionado: (a) ΔVAB = R$ {q2['a_agro_export']['dva']:,.0f} mi; "
        f"(b) ΔVAB = R$ {q2['b_fbcf']['dva']:,.0f} mi → maior impacto no cenário ({ganha_va}).",
        f"Emprego (memo): (a) {q2['a_agro_export']['demp']:,.0f} ocupações; "
        f"(b) {q2['b_fbcf']['demp']:,.0f}.",
        "Implicações: o crescimento puxado pelo agronegócio concentra o impulso numa cadeia "
        "curta e intensiva em recursos naturais — multiplica menos VA por real de choque quando "
        "a cadeia é pouco adensada e vaza para importações de insumos; já a formação de capital "
        "espalha a demanda por máquinas, construção e serviços técnicos, eleva a capacidade "
        "produtiva FUTURA (efeito não capturado pelo modelo estático) e tende a gerar mais "
        "empregos urbanos. A comparação numérica diz qual efeito de CURTO PRAZO domina; a "
        "escolha de modelo de desenvolvimento envolve também a dinâmica de longo prazo.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    ws.cell(r0, 2, "Choque (R$ milhões)").font = F_NEG
    ce = ws.cell(r0, 5, 10_000.0)
    ce.font = F_IN; ce.fill = FILL_IN; ce.number_format = NUM_MI; ce.border = BORDA
    ws.cell(r0 + 1, 2, f"Setor do cenário (a): {m20.nomes[i_agro]}").font = F_AUX
    Lch = f"$E${r0}"
    lin_dya, lin_dyb = r0 + 3, r0 + 4
    _rotulo_aux(ws, lin_dya, "Δy do cenário (a) — vetor auxiliar (colunas E em diante)")
    _rotulo_aux(ws, lin_dyb, "Δy do cenário (b) — vetor auxiliar")
    for j in range(n):
        ca = ws.cell(lin_dya, MC0 + j, f"={Lch}" if j == i_agro else 0)
        cb = ws.cell(lin_dyb, MC0 + j,
                     f"={Lch}*{_celula_dado('2020', 'fbcf', j)}"
                     f"/SUM({_faixa_dado('2020', 'fbcf', n)})")
        for c in (ca, cb):
            c.font = F_AUX; c.number_format = NUM_MI
    r1 = lin_dyb + 2
    _cab_tabela(ws, r1, 2, ["Código", "Atividades", "nº", "Δx (a)", "ΔVA (a)",
                            "Δocup (a)", "Δx (b)", "ΔVA (b)", "Δocup (b)"],
                larguras=[6.7, 46, 4.4] + [12.5] * 6)
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
        bfila = _ref_mat("B_2020", i=i, n=n)
        ws.cell(r, 5, f"=SUMPRODUCT({bfila},$E${lin_dya}:${fimM}${lin_dya})")
        ws.cell(r, 6, f"=E{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 7, f"=E{r}*{_celula_dado('2020', 'w_emp', i)}")
        ws.cell(r, 8, f"=SUMPRODUCT({bfila},$E${lin_dyb}:${fimM}${lin_dyb})")
        ws.cell(r, 9, f"=H{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 10, f"=H{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(2, 11):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
            if k >= 5:
                c.number_format = NUM_MI if k not in (7, 10) else "#,##0.0"
    r_tot = r1 + 1 + n
    _linha_total(ws, r_tot, 2, 10)
    for col in "EFGHIJ":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    confere[f"Q2_Choques!E{r_tot}"] = q2["a_agro_export"]["dprod"]
    confere[f"Q2_Choques!H{r_tot}"] = q2["b_fbcf"]["dprod"]
    confere[f"Q2_Choques!F{r_tot}"] = q2["a_agro_export"]["dva"]
    confere[f"Q2_Choques!I{r_tot}"] = q2["b_fbcf"]["dva"]
    ws.freeze_panes = f"E{r1 + 1}"

    # ================= Q3 — UPCF ================= #
    q3 = q3_upcf(s20, 120_000.0)
    ws = _nova_aba(wb, "Q3_UPCF",
                   "QUESTÃO 3 — REAJUSTE DO SALÁRIO MÍNIMO: +R$ 120 BI DE CONSUMO (2020)",
                   "Choque repartido pela UPCF — a cesta observada do consumo das famílias a "
                   "preço de consumidor: produtos nacionais + importados + impostos + margens "
                   "(aba 12 da MIP, coluna Famílias). Margens voltam como demanda de "
                   "comércio/transporte; impostos não geram produção.", "FF0070C0")
    resp = [
        f"Composição da cesta (UPCF): {1 - q3['share_imp_cesta'] - q3['share_imposto'] - q3['share_margens']:.1%} "
        f"produtos nacionais a preço básico; {q3['share_imp_cesta']:.1%} importados; "
        f"{q3['share_imposto']:.1%} impostos; {q3['share_margens']:.1%} margens de "
        "comércio/transporte (realocadas como demanda desses serviços).",
        f"IMPORTAÇÕES: diretas R$ {q3['dimp_direta']:,.0f} mi (cesta importada) + induzidas "
        f"R$ {q3['dimp_induzida']:,.0f} mi (insumos da produção, m = importação/x) = "
        f"R$ {q3['dimp_total']:,.0f} mi ({q3['dimp_total'] / 120_000:.1%} do choque).",
        f"EMPREGO: {q3['demp']:,.0f} ocupações geradas pela produção induzida "
        f"(ΔX = R$ {q3['dprod']:,.0f} mi) — cerca de {q3['demp'] / 120:,.0f} ocupações "
        "por R$ 1 bi de reajuste.",
        f"Memo: R$ {q3['dimposto']:,.0f} mi do choque viram impostos sobre produtos "
        "(não geram produção). O efeito-emprego concentra-se nos setores que atendem a UPCF "
        "(coluna Δ ocupações abaixo).",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    ws.cell(r0, 2, "Choque (R$ milhões)").font = F_NEG
    ce = ws.cell(r0, 5, 120_000.0)
    ce.font = F_IN; ce.fill = FILL_IN; ce.number_format = NUM_MI; ce.border = BORDA
    Lch = f"$E${r0}"
    itens_cesta = [
        ("Cesta importada (aba 12: Importação × Famílias)",
         m20.fd_fam.get("importacao", 0.0)),
        ("Impostos na cesta (aba 12: Impostos × Famílias)",
         m20.fd_fam.get("impostos", 0.0)),
        ("Margens de comércio (aba 12: Margens/Comércio × Famílias)",
         m20.fd_fam.get("margens_comercio", 0.0)),
        ("Margens de transporte (aba 12: Margens/Transporte × Famílias)",
         m20.fd_fam.get("margens_transporte", 0.0)),
    ]
    for k, (rot, v) in enumerate(itens_cesta):
        rr = r0 + 1 + k
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=4)
        c = ws.cell(rr, 2, rot)
        c.font = F_TAB; c.fill = FILL_BLOCO; c.border = BORDA
        cc = ws.cell(rr, 5, float(v))
        cc.font = F_TAB; cc.fill = FILL_BLOCO; cc.border = BORDA
        cc.number_format = NUM_MI
    r_den = r0 + 5
    ws.merge_cells(start_row=r_den, start_column=2, end_row=r_den, end_column=4)
    ws.cell(r_den, 2, "Cesta total das famílias (denominador da UPCF)").font = F_TAB_NEG
    cd = ws.cell(r_den, 5, f"=SUM({_faixa_dado('2020', 'familias', n)})"
                           f"+SUM(E{r0 + 1}:E{r0 + 4})")
    cd.font = F_TAB_NEG; cd.number_format = NUM_MI
    for cc in (2, 3, 4, 5):
        ws.cell(r_den, cc).fill = FILL_TOT
        ws.cell(r_den, cc).border = BORDA
    DEN = f"$E${r_den}"
    C_IMP, C_TAX, C_MGC, C_MGT = (f"$E${r0 + 1}", f"$E${r0 + 2}",
                                  f"$E${r0 + 3}", f"$E${r0 + 4}")
    soma_xc = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_c"]) or "1"
    soma_xt = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_t"]) or "1"
    lin_dy = r_den + 2
    _rotulo_aux(ws, lin_dy, "Δy da UPCF (nacional + margens realocadas) — vetor auxiliar")
    for j in range(n):
        termo = f"{_celula_dado('2020', 'familias', j)}"
        if j in q3["idx_c"]:
            termo += f"+{C_MGC}*{_celula_dado('2020', 'x', j)}/({soma_xc})"
        if j in q3["idx_t"]:
            termo += f"+{C_MGT}*{_celula_dado('2020', 'x', j)}/({soma_xt})"
        c = ws.cell(lin_dy, MC0 + j, f"={Lch}*({termo})/{DEN}")
        c.font = F_AUX; c.number_format = NUM_MI
    r1 = lin_dy + 2
    _cab_tabela(ws, r1, 2, ["Código", "Atividades", "nº", "Δ demanda (UPCF)",
                            "Δx induzido", "Δ importação induzida", "Δ ocupações"],
                larguras=[6.7, 46, 4.4, 14, 13, 14, 13])
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
        ws.cell(r, 5, f"={CL(MC0 + i)}{lin_dy}")
        ws.cell(r, 6, f"=SUMPRODUCT({_ref_mat('B_2020', i=i, n=n)},"
                      f"$E${lin_dy}:${fimM}${lin_dy})")
        ws.cell(r, 7, f"=F{r}*{_celula_dado('2020', 'm_coef', i)}")
        ws.cell(r, 8, f"=F{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(2, 9):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
            if k >= 5:
                c.number_format = NUM_MI if k < 8 else "#,##0.0"
    r_tot = r1 + 1 + n
    _linha_total(ws, r_tot, 2, 8)
    for col in "EFGH":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    r2 = r_tot + 2
    ws.cell(r2 - 1, 2, "Síntese dos impactos").font = F_SECAO
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
        c.font = F_TAB_NEG; c.border = BORDA
        cc = ws.cell(rr, 6)
        cc.value = formula if formula else f"=F{r2 + 1}+F{r2 + 2}"
        cc.font = F_TAB_NEG; cc.number_format = NUM_MI; cc.border = BORDA
        if "TOTAL" in rot:
            for col in range(2, 7):
                ws.cell(rr, col).fill = FILL_TOT
        confere[f"Q3_UPCF!F{rr}"] = valor
    ws.freeze_panes = f"E{r1 + 1}"

    # ================= Q4 — Rasmussen-Hirschman ================= #
    bl10, fl10 = s10.rasmussen()
    bl20, fl20 = s20.rasmussen()
    chave10 = (bl10 > 1) & (fl10 > 1)
    chave20 = (bl20 > 1) & (fl20 > 1)
    ws = _nova_aba(wb, "Q4_RH",
                   "QUESTÃO 4 — RASMUSSEN-HIRSCHMAN E SETORES-CHAVE: 2010 × 2020",
                   "Ligação para trás: soma de coluna da inversa de Leontief normalizada pela "
                   "média geral (U trás). Para frente: soma de linha da inversa de GHOSH "
                   "normalizada (U frente). Setor-chave: ambas > 1.", "FF0070C0")
    novos = [m20.nomes[i] for i in range(n) if chave20[i] and not chave10[i]]
    perdidos = [m20.nomes[i] for i in range(n) if chave10[i] and not chave20[i]]
    resp = [
        f"Setores-chave em 2010: {int(chave10.sum())}; em 2020: {int(chave20.sum())} "
        f"(critério RH estrito: U trás > 1 e U frente > 1).",
        ("Entraram no grupo-chave até 2020: " + "; ".join(novos)) if novos
        else "Nenhum setor entrou no grupo-chave entre 2010 e 2020.",
        ("Saíram do grupo-chave: " + "; ".join(perdidos)) if perdidos
        else "Nenhum setor saiu do grupo-chave entre 2010 e 2020.",
        "Transformações estruturais: as colunas Δ mostram onde o encadeamento para trás e "
        "para frente mudou na década — leia em conjunto com a Q7 (SDA): quedas difusas de "
        "ligação para trás indicam substituição de insumos domésticos (por importados ou por "
        "serviços), enquanto ganhos concentrados sinalizam adensamento de cadeia.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    cab = ["Código", "Atividades", "nº", "U trás 2010", "U frente 2010", "Chave 2010",
           "U trás 2020", "U frente 2020", "Chave 2020", "Δ trás", "Δ frente", "Mudança"]
    _cab_tabela(ws, r0, 2, cab, larguras=[6.7, 46, 4.4] + [10.5] * 9)
    for i in range(n):
        r = r0 + 1 + i
        L = CL(MC0 + i)
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
        for k, (aba_b, aba_g) in enumerate((("B_2010", "G_2010"), ("B_2020", "G_2020"))):
            cb = 5 + k * 3
            ws.cell(r, cb, f"=SUM({aba_b}!{L}7:{L}{6 + n})*{n}"
                           f"/SUM({aba_b}!$E$7:${fimM}${6 + n})")
            ws.cell(r, cb + 1, f"=SUM({_ref_mat(aba_g, i=i, n=n)})*{n}"
                               f"/SUM({aba_g}!$E$7:${fimM}${6 + n})")
            ws.cell(r, cb + 2, f'=IF(AND({CL(cb)}{r}>1,{CL(cb + 1)}{r}>1),"CHAVE","")')
            ws.cell(r, cb + 2).alignment = CENTRO
        ws.cell(r, 11, f"=H{r}-E{r}")
        ws.cell(r, 12, f"=I{r}-F{r}")
        ws.cell(r, 13, f'=IF(G{r}=J{r},"",IF(J{r}="CHAVE","entrou","saiu"))')
        ws.cell(r, 13).alignment = CENTRO
        for k in range(2, 14):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
            if k in (5, 6, 8, 9, 11, 12):
                c.number_format = NUM_IDX
    confere[f"Q4_RH!E{r0 + 1}"] = float(bl10[0])
    confere[f"Q4_RH!I{r0 + 1}"] = float(fl20[0])
    ws.freeze_panes = f"E{r0 + 1}"

    # ================= Q5 — campo de influência (2010) ================= #
    S = q5_campo_influencia(s10)
    ws = _nova_aba(wb, "Q5_CampoInfluencia",
                   "QUESTÃO 5 — CAMPOS DE INFLUÊNCIA DOS SETORES (BRASIL, 2010)",
                   f"Sonis & Hewings; ε = {EPS_CAMPO}. S(i,j) mede quanto uma variação no "
                   "coeficiente a(i,j) se propaga pela economia (Σ dos quadrados de [B(ε)−B]/ε). "
                   "Equivalente exato do laço em R do material de apoio (Vale & Perobelli), "
                   "via Sherman-Morrison. Matriz S como VALOR; médias e destaques por fórmula.",
                   "FF0070C0")
    Srow = S.mean(1); Scol = S.mean(0)
    o_link = np.dstack(np.unravel_index(np.argsort(S, axis=None)[::-1], S.shape))[0]
    resp = [
        f"Elo de maior campo de influência: a({m10.nomes[o_link[0][0]]} → "
        f"{m10.nomes[o_link[0][1]]}), S = {S[o_link[0][0], o_link[0][1]]:,.1f}.",
        "Setores cujas LINHAS mais influenciam (vendedores estratégicos): "
        + "; ".join(m10.nomes[i] for i in np.argsort(Srow)[::-1][:3]) + ".",
        "Setores cujas COLUNAS mais influenciam (compradores estratégicos): "
        + "; ".join(m10.nomes[j] for j in np.argsort(Scol)[::-1][:3]) + ".",
        "Interpretação: elos com S alto são os pontos onde mudanças tecnológicas (variações "
        "de coeficiente) mais alteram a inversa de Leontief — candidatos naturais a política "
        "industrial; coincidem majoritariamente com os setores-chave da Q4.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    topk = min(20, n * n)
    ws.cell(r0 - 1, 16, "TOP ELOS a(i,j) POR CAMPO DE INFLUÊNCIA").font = F_SECAO
    _cab_tabela(ws, r0, 16, ["#", "Vendedor (i)", "Comprador (j)", "S(i,j)"],
                larguras=[4, 36, 36, 12])
    r_mat0 = r0 + topk + 3
    for k in range(topk):
        i, j = int(o_link[k][0]), int(o_link[k][1])
        r = r0 + 1 + k
        ws.cell(r, 16, k + 1).alignment = CENTRO
        ws.cell(r, 17, m10.nomes[i]).alignment = VCENTRO
        ws.cell(r, 18, m10.nomes[j]).alignment = VCENTRO
        v = ws.cell(r, 19, f"={CL(MC0 + j)}{r_mat0 + 1 + i}")
        v.number_format = NUM_MI2
        for cc in range(16, 20):
            ws.cell(r, cc).font = F_TAB
            ws.cell(r, cc).border = BORDA
    ws.cell(r_mat0 - 1, 2, "MATRIZ S — linhas = vendedor (i), colunas = comprador (j); "
                           "médias por fórmula nas bordas").font = F_SECAO
    ws.merge_cells(start_row=r_mat0, start_column=3, end_row=r_mat0, end_column=4)
    for col, rtl in ((2, "Código"), (3, "Atividades")):
        c = ws.cell(r_mat0, col, rtl)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    ws.cell(r_mat0, 4).fill = FILL_CAB; ws.cell(r_mat0, 4).border = BORDA
    ws.column_dimensions["B"].width = 6.7
    ws.column_dimensions["C"].width = 46
    ws.column_dimensions["D"].width = 4.4
    for j in range(n):
        c = ws.cell(r_mat0, MC0 + j, j + 1)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    c = ws.cell(r_mat0, MC0 + n, "média linha")
    c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    for i in range(n):
        r = r_mat0 + 1 + i
        ws.row_dimensions[r].height = 11
        ws.cell(r, 2, m10.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m10.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
        for j in range(n):
            c = ws.cell(r, MC0 + j, float(S[i, j]))
            c.number_format = NUM_MI2
        for k in range(2, MC0 + n):
            ws.cell(r, k).font = F_DADO
            ws.cell(r, k).border = BORDA
        c = ws.cell(r, MC0 + n, f"=AVERAGE(E{r}:{fimM}{r})")
        c.font = F_DADO_NEG; c.number_format = NUM_MI2; c.border = BORDA
    r_med = r_mat0 + 1 + n
    _linha_total(ws, r_med, 2, MC0 + n, rotulo="média coluna")
    for j in range(n):
        c = ws.cell(r_med, MC0 + j,
                    f"=AVERAGE({CL(MC0 + j)}{r_mat0 + 1}:{CL(MC0 + j)}{r_med - 1})")
        c.font = F_DADO_NEG; c.number_format = NUM_MI2
    confere[f"Q5_CampoInfluencia!E{r_mat0 + 1}"] = float(S[0, 0])
    ws.freeze_panes = f"E{r0 + 1}"

    # ================= Q6 — extração hipotética ================= #
    q6 = q6_extracao(s20, i_q6)
    ws = _nova_aba(wb, "Q6_Extracao",
                   f"QUESTÃO 6 — EXTRAÇÃO HIPOTÉTICA TOTAL (2020)",
                   f"Setor extraído: {m20.nomes[i_q6]}. Zera-se a linha e a coluna do setor em "
                   "A e sua demanda final; a perda é a diferença entre a produção do sistema "
                   "completo (x = B·y) e a do sistema reduzido. Coluna 'x reduzido' colada como "
                   "VALOR (nova inversão); demais colunas por fórmula.", "FF0070C0")
    perda_rel = q6["perda"] / np.where(q6["x_base"] == 0, 1, q6["x_base"])
    o_par = np.argsort(np.where(np.arange(n) == i_q6, -1, perda_rel))[::-1]
    resp = [
        f"Perda de produção agregada: R$ {q6['perda_total']:,.0f} mi "
        f"({q6['perda_pct']:.2%} da produção total) — inclui o próprio setor extraído.",
        f"Perda de VA: R$ {q6['perda_va']:,.0f} mi; ocupações comprometidas: "
        f"{q6['perda_emp']:,.0f}.",
        "Setores mais paralisados (excluído o próprio, em % da sua produção): "
        + "; ".join(f"{m20.nomes[i]} ({perda_rel[i]:.1%})" for i in o_par[:3]) + ".",
        "Leitura: a extração mede a dependência estrutural da economia em relação ao setor — "
        "compare com a Q4: setores-chave tendem a paralisar mais cadeias quando extraídos.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    _cab_tabela(ws, r0, 2, ["Código", "Atividades", "nº", "x baseline (B·y)",
                            "x reduzido (valor)", "Perda", "Perda (% do setor)"],
                larguras=[6.7, 46, 4.4, 15, 15, 15, 13])
    for i in range(n):
        r = r0 + 1 + i
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
        ws.cell(r, 5, float(q6["x_base"][i])).number_format = NUM_MI
        ws.cell(r, 6, float(q6["x_ex"][i])).number_format = NUM_MI
        ws.cell(r, 7, f"=E{r}-F{r}").number_format = NUM_MI
        ws.cell(r, 8, f"=IF(E{r}=0,0,G{r}/E{r})").number_format = NUM_PCT
        for k in range(2, 9):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
        if i == i_q6:
            for k in range(2, 9):
                ws.cell(r, k).fill = FILL_BLOCO
    r_tot = r0 + 1 + n
    _linha_total(ws, r_tot, 2, 8)
    for col in "EFG":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{r0 + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    ws[f"H{r_tot}"] = f"=G{r_tot}/E{r_tot}"
    ws[f"H{r_tot}"].font = F_TAB_NEG; ws[f"H{r_tot}"].number_format = NUM_PCT
    confere[f"Q6_Extracao!G{r_tot}"] = q6["perda_total"]
    ws.freeze_panes = f"E{r0 + 1}"

    # ================= Q7 — SDA ================= #
    fator = float(np.prod([1 + v / 100 for v in IPCA_ANUAL.values()]))
    q7 = q7_sda(s10, s20, fator)
    ws = _nova_aba(wb, "Q7_SDA",
                   "QUESTÃO 7 — DECOMPOSIÇÃO ESTRUTURAL 2010→2020 (IPCA)",
                   "SDA bipolar média: Δx = ½ΔB·(y0*+y1) + ½(B0+B1)·Δy, com y0* = y2010 × "
                   "fator IPCA acumulado. O deflator único não altera A/B de 2010 "
                   "(coeficientes são razões) — atualiza apenas os níveis.", "FF0070C0")
    dtec, ddem, ddx = q7["tec"].sum(), q7["dem"].sum(), q7["dx"].sum()
    resp = [
        f"Fator IPCA acumulado dez/2010→dez/2020: {fator:.4f} (variações anuais do IBGE nas "
        "células editáveis abaixo).",
        f"Δx total (preços de 2020): R$ {ddx:,.0f} mi — decomposto em EFEITO TECNOLOGIA "
        f"(mudança de coeficientes, ΔB): R$ {dtec:,.0f} mi ({dtec / ddx:.1%}) e EFEITO "
        f"DEMANDA FINAL (Δy): R$ {ddem:,.0f} mi ({ddem / ddx:.1%}).",
        "Leitura: efeito-demanda dominante com efeito-tecnologia menor é o padrão de uma "
        "década de crescimento extensivo; onde o efeito-tecnologia é negativo houve "
        "desadensamento de cadeia (consistente com as mudanças de ligação da Q4). A coluna "
        "'checagem' comprova a aditividade exata da decomposição em cada setor.",
    ]
    r0 = _caixa_resposta(ws, 5, resp)
    ws.cell(r0, 2, "IPCA % a.a. (IBGE)").font = F_NEG
    for k, (ano, v) in enumerate(sorted(IPCA_ANUAL.items())):
        c = ws.cell(r0 + 1, 5 + k, str(ano))
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
        c = ws.cell(r0 + 2, 5 + k, v)
        c.font = F_IN; c.fill = FILL_IN; c.border = BORDA
        c.number_format = "0.00"; c.alignment = CENTRO
    c = ws.cell(r0 + 1, 6 + len(IPCA_ANUAL), "fator acumulado")
    c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA; c.alignment = CENTRO
    fator_expr = "=" + "*".join(f"(1+{CL(5 + k)}{r0 + 2}/100)"
                                for k in range(len(IPCA_ANUAL)))
    c_fat = ws.cell(r0 + 2, 6 + len(IPCA_ANUAL), fator_expr)
    c_fat.font = F_TAB_NEG; c_fat.number_format = "0.0000"
    c_fat.border = BORDA; c_fat.alignment = CENTRO
    FAT = f"${CL(6 + len(IPCA_ANUAL))}${r0 + 2}"
    lin_ysum, lin_ydel = r0 + 4, r0 + 5
    _rotulo_aux(ws, lin_ysum, "y0*+y1 — vetor auxiliar (colunas E em diante)")
    _rotulo_aux(ws, lin_ydel, "y1−y0* — vetor auxiliar")
    for j in range(n):
        y0 = f"{_celula_dado('2010', 'ytot', j)}*{FAT}"
        y1 = f"{_celula_dado('2020', 'ytot', j)}"
        ca = ws.cell(lin_ysum, MC0 + j, f"={y0}+{y1}")
        cb = ws.cell(lin_ydel, MC0 + j, f"={y1}-{y0}")
        for c in (ca, cb):
            c.font = F_AUX; c.number_format = NUM_MI
    r1 = lin_ydel + 2
    _cab_tabela(ws, r1, 2, ["Código", "Atividades", "nº", "x 2010 a preços 2020",
                            "x 2020", "Δx", "Efeito tecnologia (ΔB)",
                            "Efeito demanda (Δy)", "Checagem (tec+dem−Δx)"],
                larguras=[6.7, 46, 4.4, 15, 14, 14, 15, 15, 14])
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 2, m20.cod[i]).alignment = CENTRO
        ws.cell(r, 3, m20.nomes[i]).alignment = VCENTRO
        ws.cell(r, 4, i + 1).alignment = CENTRO
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
        for k in range(2, 11):
            c = ws.cell(r, k)
            c.font = F_TAB; c.border = BORDA
            if k >= 5:
                c.number_format = NUM_MI
    r_tot = r1 + 1 + n
    _linha_total(ws, r_tot, 2, 10)
    for col in "EFGHIJ":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        c.font = F_TAB_NEG; c.number_format = NUM_MI
    confere[f"Q7_SDA!H{r_tot}"] = float(q7["tec"].sum())
    confere[f"Q7_SDA!I{r_tot}"] = float(q7["dem"].sum())
    ws.freeze_panes = f"E{r1 + 1}"

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
