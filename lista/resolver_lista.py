# -*- coding: utf-8 -*-
"""
resolver_lista.py — Lista de Exercícios (Prof. Celso Bissoli Sessa, entrega 24/07/2026)
resolvida com o arcabouço insumo-produto do repositório (src/io_core.py + convenções
de pesquisa/01, 17, 25). Entrada: MIP-BR 2010 e 2020 (Nível 68, NEREUS/CECEG).
Saída: pasta de trabalho Excel com uma aba por questão, formulada sobre as abas de
dados (as inversas 68x68 entram como valores documentados; todo o resto recalcula).

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
        n, B, B2n = self.n, self.B, self.B2[:self.n, :self.n]
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
# 2. GERADOR DO EXCEL
# =========================================================================== #
ARIAL = "Arial"
F_TIT = Font(name=ARIAL, size=13, bold=True, color="1F3864")
F_SUB = Font(name=ARIAL, size=10, italic=True, color="404040")
F_CAB = Font(name=ARIAL, size=9, bold=True, color="FFFFFF")
F_TXT = Font(name=ARIAL, size=10)
F_NEG = Font(name=ARIAL, size=10, bold=True)
F_IN = Font(name=ARIAL, size=10, color="0000FF", bold=True)     # entradas editáveis
FILL_CAB = PatternFill("solid", fgColor="1F3864")
FILL_IN = PatternFill("solid", fgColor="FFFF00")                # premissas-chave
FILL_ZEB = PatternFill("solid", fgColor="F2F2F2")
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
QUEBRA = Alignment(wrap_text=True, vertical="top")

NUM_MULT = "0.0000"
NUM_MI = "#,##0"
NUM_PCT = "0.00%"
NUM_IDX = "0.000"


def _cab_tabela(ws, linha, col0, rotulos, larguras=None):
    for k, r in enumerate(rotulos):
        c = ws.cell(linha, col0 + k, r)
        c.font = F_CAB; c.fill = FILL_CAB; c.border = BORDA
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        if larguras:
            ws.column_dimensions[CL(col0 + k)].width = larguras[k]


def _titulo(ws, titulo, enunciado, ncols=10):
    ws.cell(1, 1, titulo).font = F_TIT
    ws.merge_cells(start_row=2, start_column=1, end_row=3, end_column=ncols)
    c = ws.cell(2, 1, enunciado)
    c.font = F_SUB; c.alignment = QUEBRA
    ws.row_dimensions[2].height = 26


def _resposta(ws, linha0, linhas_texto, ncols=10):
    ws.cell(linha0, 1, "Resposta / leitura dos resultados:").font = F_NEG
    r = linha0 + 1
    for t in linhas_texto:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
        c = ws.cell(r, 1, "•  " + t)
        c.font = F_TXT; c.alignment = QUEBRA
        ws.row_dimensions[r].height = max(13, 13 * (1 + len(t) // 130))
        r += 1
    return r + 1


def _matriz(ws, M, nomes, cods, titulo, nota, fmt=NUM_MULT, extra_rotulo=None):
    """Escreve matriz com rótulos: dados em C4:.., códigos na linha 3/coluna A."""
    ws.cell(1, 1, titulo).font = F_TIT
    ws.cell(2, 1, nota).font = F_SUB
    nlin, ncol = M.shape
    ws.column_dimensions["A"].width = 7
    ws.column_dimensions["B"].width = 34
    for j in range(ncol):
        rot = cods[j] if j < len(cods) else (extra_rotulo or "+")
        c = ws.cell(3, 3 + j, rot)
        c.font = F_CAB; c.fill = FILL_CAB
        ws.column_dimensions[CL(3 + j)].width = 9
    for i in range(nlin):
        ws.cell(4 + i, 1, cods[i] if i < len(cods) else (extra_rotulo or "+")).font = F_TXT
        ws.cell(4 + i, 2, nomes[i] if i < len(nomes) else (extra_rotulo or "Famílias")).font = F_TXT
        for j in range(ncol):
            c = ws.cell(4 + i, 3 + j, float(M[i, j]))
            c.font = F_TXT; c.number_format = fmt
    ws.freeze_panes = "C4"


def _ref_mat(aba, i=None, j=None, n=68):
    """referência a uma linha (i) ou coluna (j) da matriz da aba (dados em C4)."""
    if i is not None:
        return f"{aba}!C{4 + i}:{CL(2 + n)}{4 + i}"
    return f"{aba}!{CL(3 + j)}4:{CL(3 + j)}{3 + n}"


COL_DADOS = {"x": "C", "rem": "D", "va": "E", "ocup": "F", "imp": "G",
             "exportacao": "H", "governo": "I", "isflsf": "J", "familias": "K",
             "fbcf": "L", "estoque": "M", "ytot": "N",
             "w_emp": "O", "v_renda": "P", "v_va": "Q", "m_coef": "R"}


def _aba_dados(wb, tag, mip: MIPAno):
    """Tabela vertical (setores nas linhas) com vetores e coeficientes (fórmulas)."""
    ws = wb.create_sheet(f"Dados_{tag}")
    _titulo(ws, f"Dados — MIP Brasil {tag} (R$ milhões correntes; ocupações em pessoas)",
            "Vetores extraídos da MIP; coeficientes por unidade de produção calculados "
            "por fórmula (colunas P a S). Fonte: MIP-BR (Nível 68), NEREUS/CECEG.")
    rot = ["Código", "Setor", "VBP (x)", "Remunerações", "VA (PIB)", "Ocupações",
           "Import. intermediária", "Exportações", "Governo", "ISFLSF",
           "Cons. famílias (nac.)", "FBCF", "Var. estoques", "Demanda final total",
           "w = ocup/x", "v_renda = rem/x", "v_va = VA/x", "m = imp/x"]
    _cab_tabela(ws, 5, 1, rot, larguras=[7, 36] + [13] * (len(rot) - 2))
    n = mip.n
    for i in range(n):
        r = 6 + i
        ws.cell(r, 1, mip.cod[i]).font = F_TXT
        ws.cell(r, 2, mip.nomes[i]).font = F_TXT
        vals = [mip.x[i], mip.rem[i], mip.va[i], mip.ocup[i], mip.imp_int[i],
                mip.y["exportacao"][i], mip.y["governo"][i], mip.y["isflsf"][i],
                mip.y["familias"][i], mip.y["fbcf"][i], mip.y["estoque"][i]]
        for k, v in enumerate(vals):
            c = ws.cell(r, 3 + k, float(v))
            c.font = F_TXT; c.number_format = NUM_MI; c.border = BORDA
        ws.cell(r, 14, f"=SUM(H{r}:M{r})").number_format = NUM_MI
        for col, expr in (("O", f"=IF(C{r}=0,0,F{r}/C{r})"),
                          ("P", f"=IF(C{r}=0,0,D{r}/C{r})"),
                          ("Q", f"=IF(C{r}=0,0,E{r}/C{r})"),
                          ("R", f"=IF(C{r}=0,0,G{r}/C{r})")):
            c = ws[f"{col}{r}"]
            c.value = expr; c.font = F_TXT
            c.number_format = NUM_MULT if col == "O" else "0.000000"
        ws[f"N{r}"].font = F_TXT
        if i % 2:
            for k in range(1, 19):
                ws.cell(r, k).fill = FILL_ZEB
    r_tot = 6 + n
    ws.cell(r_tot, 2, "TOTAL").font = F_NEG
    for col in "CDEFGHIJKLMN":
        ws[f"{col}{r_tot}"] = f"=SUM({col}6:{col}{5 + n})"
        ws[f"{col}{r_tot}"].font = F_NEG
        ws[f"{col}{r_tot}"].number_format = NUM_MI
    ws.freeze_panes = "C6"
    return ws


def _celula_dado(tag, col, i):
    return f"Dados_{tag}!${COL_DADOS[col]}${6 + i}"


def _faixa_dado(tag, col, n):
    c = COL_DADOS[col]
    return f"Dados_{tag}!${c}$6:${c}${5 + n}"


def _linha_transposta(ws, linha, col0, tag, col_dado, n, fmt="0.000000"):
    """linha auxiliar horizontal: cada célula referencia o vetor vertical de Dados_."""
    for j in range(n):
        c = ws.cell(linha, col0 + j, f"={_celula_dado(tag, col_dado, j)}")
        c.font = F_TXT; c.number_format = fmt


def gerar_excel(saida: str, m10: MIPAno, m20: MIPAno, s10: Sistema, s20: Sistema,
                i_agro: int, i_q6: int, sintetico: bool = False) -> dict:
    """Escreve a pasta de trabalho completa; devolve dicionário de conferência
    {celula: valor_python} para validação pós-recálculo."""
    n = m20.n
    confere: dict[str, float] = {}
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # ---------------- Capa e Metodologia ---------------- #
    ws = wb.create_sheet("Capa")
    ws.column_dimensions["A"].width = 110
    linhas_capa = [
        ("Lista de Exercícios — Análise de Insumo-Produto", F_TIT),
        ("PPGEco/UFES · Prof. Dr. Celso Bissoli Sessa · 2026/1", F_TXT),
        ("Aluno: Felipe Carvalho de Souza Santos", F_TXT),
        ("Entrega: 24/07/2026 · Dados: Matrizes de Insumo-Produto do Brasil, 2010 e 2020 "
         "(Nível 68, NEREUS/CECEG; R$ milhões correntes)", F_TXT),
        ("", F_TXT),
        ("Resolução com o arcabouço do repositório fcarva/es-insumo-produto "
         "(src/io_core.py — Leontief, Ghosh, Rasmussen-Hirschman; convenções de "
         "pesquisa/01, 17 e 25), gerada por lista/resolver_lista.py.", F_SUB),
        ("", F_TXT),
        ("Abas: Q1_Multiplicadores · Q2_Choques · Q3_UPCF · Q4_RH · Q5_CampoInfluencia · "
         "Q6_Extracao · Q7_SDA · Dados_2010/2020 · matrizes A, B (Leontief), G (Ghosh), "
         "B2 (modelo fechado).", F_TXT),
    ]
    if sintetico:
        linhas_capa.insert(4, ("*** ARQUIVO DE VALIDAÇÃO (selftest): economia SINTÉTICA de "
                               f"{n} setores — NÃO usa dados reais ***", F_NEG))
    for k, (t, f) in enumerate(linhas_capa, start=2):
        ws.cell(k, 1, t).font = f
        ws.cell(k, 1).alignment = QUEBRA

    ws = wb.create_sheet("Metodologia")
    ws.column_dimensions["A"].width = 118
    met = [
        "NOTAS METODOLÓGICAS E PREMISSAS (todas as hipóteses assumidas estão listadas aqui)",
        "1. Modelo aberto: A = Z·x̂⁻¹ sobre os fluxos NACIONAIS; B = (I−A)⁻¹ (Leontief). "
        "Ghosh: G = (I−x̂⁻¹Z)⁻¹. As matrizes B, G e B2 estão coladas como VALORES "
        "(inversão 68×68 feita externamente em NumPy — conferível por MINVERSE); "
        "todas as demais células derivam delas por fórmula e recalculam.",
        "2. Tipo II: modelo fechado para as famílias — coluna adicional = consumo das famílias "
        "por unidade de massa de remunerações; linha adicional = remunerações por unidade de "
        "produção (convenção Miller & Blair, cap. 6; idêntica a pesquisa/17 do repositório).",
        "3. Multiplicador de emprego em OCUPAÇÕES por R$ 1 milhão de demanda final; renda e VA "
        "em R$ por R$ de demanda final.",
        "4. Q2: choque de R$ 10 bi = 10.000 (R$ milhões). Cenário (a): tudo na linha de "
        "exportações do setor Agricultura. Cenário (b): distribuído pela estrutura observada "
        "da coluna FBCF (produtos nacionais). Premissa: o choque recai sobre produtos "
        "nacionais nos dois cenários (célula de entrada azul/amarela pode ser alterada).",
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
        "y0* = y(2010)·fator IPCA. O deflator único (IPCA acumulado dez/2010→dez/2020, tabela "
        "na aba Q7 com as variações anuais do IBGE) não altera A nem B de 2010 — coeficientes "
        "são razões —, agindo apenas sobre os níveis. Limitação declarada: o ideal seriam "
        "deflatores setoriais (duplo deflacionamento); o enunciado pede IPCA.",
        "10. Unidades: R$ milhões correntes do ano de cada matriz (Q7 em preços de 2020).",
        "",
        f"Proveniência 2020: {m20.proveniencia.get('nacional')}",
        f"Proveniência 2010: {m10.proveniencia.get('nacional')}",
        f"Arquivo 2020: {m20.proveniencia.get('arquivo')}",
        f"Arquivo 2010: {m10.proveniencia.get('arquivo')}",
    ]
    for k, t in enumerate(met, start=1):
        c = ws.cell(k, 1, t)
        c.font = F_NEG if k == 1 else F_TXT
        c.alignment = QUEBRA
        ws.row_dimensions[k].height = max(13, 13 * (1 + len(t) // 115))

    # ---------------- Setores ---------------- #
    ws = wb.create_sheet("Setores")
    _titulo(ws, "Classificação setorial (comum a 2010 e 2020)", "Nível 68 — NEREUS/CECEG.")
    _cab_tabela(ws, 5, 1, ["Código", "Setor"], larguras=[10, 70])
    for i in range(n):
        ws.cell(6 + i, 1, m20.cod[i]).font = F_TXT
        ws.cell(6 + i, 2, m20.nomes[i]).font = F_TXT

    # ---------------- Dados e matrizes ---------------- #
    _aba_dados(wb, "2020", m20)
    _aba_dados(wb, "2010", m10)
    for tag, s, mip in (("2020", s20, m20), ("2010", s10, m10)):
        _matriz(wb.create_sheet(f"A_{tag}"), s.A, mip.nomes, mip.cod,
                f"A_{tag} — coeficientes técnicos nacionais",
                "a(i,j) = Z(i,j)/x(j); valores da MIP (aba 13 reproduzida do arquivo-fonte).")
        _matriz(wb.create_sheet(f"B_{tag}"), s.B, mip.nomes, mip.cod,
                f"B_{tag} — inversa de Leontief (I−A)⁻¹",
                "VALORES (inversão externa NumPy; confira com MINVERSE). Base das fórmulas das questões.")
        _matriz(wb.create_sheet(f"G_{tag}"), s.G, mip.nomes, mip.cod,
                f"G_{tag} — inversa de Ghosh (I−x̂⁻¹Z)⁻¹",
                "VALORES; usada na ligação para frente de Rasmussen-Hirschman (Q4).")
    _matriz(wb.create_sheet("B2_2020"), s20.B2, m20.nomes, m20.cod,
            "B2_2020 — inversa do modelo FECHADO para as famílias (tipo II)",
            "VALORES; última linha/coluna = famílias (renda ↔ consumo).",
            extra_rotulo="FAM")

    # ================= Q1 — multiplicadores ================= #
    mult = s20.multiplicadores()
    ws = wb.create_sheet("Q1_Multiplicadores")
    _titulo(ws, "Questão 1 — Multiplicadores de produção, emprego, renda e VA (2020), tipos I e II",
            "Tipo I: modelo aberto (B_2020). Tipo II: modelo fechado para as famílias (B2_2020). "
            "Emprego em ocupações por R$ 1 milhão; renda e VA em R$ por R$ 1 de demanda final.",
            ncols=12)
    o_emp = np.argsort(mult["emp_II"])[::-1]
    o_ren = np.argsort(mult["renda_II"])[::-1]
    resp = [
        f"Multiplicador de produção médio (2020): {mult['prod_I'].mean():.3f} (tipo I) e "
        f"{mult['prod_II'].mean():.3f} (tipo II) — o efeito induzido pelo consumo das famílias "
        f"amplia o encadeamento médio em {(mult['prod_II'].mean()/mult['prod_I'].mean()-1)*100:.1f}%.",
        f"Maior capacidade de GERAÇÃO DE EMPREGO (tipo II): {m20.nomes[o_emp[0]]} "
        f"({mult['emp_II'][o_emp[0]]:.1f} ocup./R$ mi), seguido de {m20.nomes[o_emp[1]]} e "
        f"{m20.nomes[o_emp[2]]} — setores trabalho-intensivos lideram.",
        f"Maior capacidade de GERAÇÃO DE RENDA (tipo II): {m20.nomes[o_ren[0]]} "
        f"(R$ {mult['renda_II'][o_ren[0]]:.3f} por R$ 1,00), seguido de {m20.nomes[o_ren[1]]} e "
        f"{m20.nomes[o_ren[2]]}.",
        "Rankings completos nas duas tabelas à direita; a tabela principal traz os oito "
        "multiplicadores por setor, com posição no ranking de emprego e de renda.",
    ]
    r0 = _resposta(ws, 5, resp, ncols=12)
    cab = ["Código", "Setor", "Produção I", "Produção II", "Emprego I (ocup/R$ mi)",
           "Emprego II (ocup/R$ mi)", "Renda I", "Renda II", "VA I", "VA II",
           "Rank emprego II", "Rank renda II"]
    _cab_tabela(ws, r0, 1, cab, larguras=[8, 36] + [12] * 10)
    r_ini, r_fim = r0 + 1, r0 + n
    for i in range(n):
        r = r0 + 1 + i
        L = CL(3 + i)                             # coluna do setor i nas matrizes
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        formulas = [
            f"=SUM(B_2020!{L}4:{L}{3 + n})",
            f"=SUM(B2_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'w_emp', n)},B_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'w_emp', n)},B2_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_renda', n)},B_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_renda', n)},B2_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_va', n)},B_2020!{L}4:{L}{3 + n})",
            f"=SUMPRODUCT({_faixa_dado('2020', 'v_va', n)},B2_2020!{L}4:{L}{3 + n})",
        ]
        for k, f in enumerate(formulas):
            c = ws.cell(r, 3 + k, f)
            c.font = F_TXT; c.number_format = NUM_MULT; c.border = BORDA
        ws.cell(r, 11, f"=RANK(F{r},$F${r_ini}:$F${r_fim},0)").font = F_TXT
        ws.cell(r, 12, f"=RANK(H{r},$H${r_ini}:$H${r_fim},0)").font = F_TXT
    confere[f"Q1_Multiplicadores!C{r_ini}"] = float(mult["prod_I"][0])
    confere[f"Q1_Multiplicadores!D{r_ini}"] = float(mult["prod_II"][0])
    confere[f"Q1_Multiplicadores!E{r_ini}"] = float(mult["emp_I"][0])
    confere[f"Q1_Multiplicadores!H{r_ini}"] = float(mult["renda_II"][0])
    # rankings (top-10) — referências vivas às linhas da tabela principal
    topk = min(10, n)
    for bloco, (rot, ordem, col_val) in enumerate(
            [("RANKING — geração de EMPREGO (tipo II)", o_emp, "F"),
             ("RANKING — geração de RENDA (tipo II)", o_ren, "H")]):
        c0 = 14 + bloco * 4
        ws.cell(r0 - 1, c0, rot).font = F_NEG
        _cab_tabela(ws, r0, c0, ["#", "Setor", "Multiplicador"], larguras=[4, 34, 12])
        for k in range(topk):
            r = r0 + 1 + k
            i = int(ordem[k])
            ws.cell(r, c0, k + 1).font = F_TXT
            ws.cell(r, c0 + 1, f"=B{r0 + 1 + i}").font = F_TXT
            v = ws.cell(r, c0 + 2, f"={col_val}{r0 + 1 + i}")
            v.font = F_TXT; v.number_format = NUM_MULT
    ws.freeze_panes = f"C{r0 + 1}"

    # ================= Q2 — choques ================= #
    q2 = q2_cenarios(s20, 10_000.0, i_agro)
    ws = wb.create_sheet("Q2_Choques")
    _titulo(ws, "Questão 2 — Choques de R$ 10 bilhões (2020): exportações da agricultura × FBCF",
            "Δx = B·Δy. Cenário (a): +R$ 10 bi nas exportações da Agricultura. Cenário (b): "
            "+R$ 10 bi na FBCF, distribuídos pela estrutura observada da coluna de investimento.",
            ncols=12)
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
        "empregos urbanos. A comparação numérica acima diz qual efeito de CURTO PRAZO domina; "
        "a escolha de modelo de desenvolvimento envolve também a dinâmica de longo prazo.",
    ]
    r0 = _resposta(ws, 5, resp, ncols=12)
    ws.cell(r0, 1, "Choque (R$ milhões):").font = F_NEG
    ce_choque = ws.cell(r0, 3, 10_000.0)
    ce_choque.font = F_IN; ce_choque.fill = FILL_IN; ce_choque.number_format = NUM_MI
    ws.cell(r0, 4, f"Setor do cenário (a): {m20.nomes[i_agro]}").font = F_SUB
    lin_dya, lin_dyb = r0 + 2, r0 + 3
    ws.cell(lin_dya, 2, "Δy (a) — linha auxiliar").font = F_SUB
    ws.cell(lin_dyb, 2, "Δy (b) — linha auxiliar").font = F_SUB
    Lch = f"$C${r0}"
    for j in range(n):
        ca = ws.cell(lin_dya, 3 + j, f"={Lch}" if j == i_agro else 0)
        cb = ws.cell(lin_dyb, 3 + j,
                     f"={Lch}*{_celula_dado('2020', 'fbcf', j)}/SUM({_faixa_dado('2020', 'fbcf', n)})")
        for c in (ca, cb):
            c.font = F_TXT; c.number_format = NUM_MI
    r1 = lin_dyb + 2
    _cab_tabela(ws, r1, 1, ["Código", "Setor", "Δx (a)", "ΔVA (a)", "Δocup (a)",
                            "Δx (b)", "ΔVA (b)", "Δocup (b)"],
                larguras=[8, 36] + [13] * 6)
    fim = CL(2 + n)
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        bfila = _ref_mat("B_2020", i=i, n=n)
        ws.cell(r, 3, f"=SUMPRODUCT({bfila},$C${lin_dya}:${fim}${lin_dya})")
        ws.cell(r, 4, f"=C{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 5, f"=C{r}*{_celula_dado('2020', 'w_emp', i)}")
        ws.cell(r, 6, f"=SUMPRODUCT({bfila},$C${lin_dyb}:${fim}${lin_dyb})")
        ws.cell(r, 7, f"=F{r}*{_celula_dado('2020', 'v_va', i)}")
        ws.cell(r, 8, f"=F{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(3, 9):
            ws.cell(r, k).font = F_TXT
            ws.cell(r, k).number_format = NUM_MI if k in (3, 4, 6, 7) else "#,##0.0"
    r_tot = r1 + 1 + n
    ws.cell(r_tot, 2, "TOTAL").font = F_NEG
    for col in "CDEFGH":
        c = ws[f"{col}{r_tot}"]
        c.value = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        c.font = F_NEG; c.number_format = NUM_MI
    confere[f"Q2_Choques!C{r_tot}"] = q2["a_agro_export"]["dprod"]
    confere[f"Q2_Choques!F{r_tot}"] = q2["b_fbcf"]["dprod"]
    confere[f"Q2_Choques!D{r_tot}"] = q2["a_agro_export"]["dva"]
    confere[f"Q2_Choques!G{r_tot}"] = q2["b_fbcf"]["dva"]
    ws.freeze_panes = f"C{r1 + 1}"

    # ================= Q3 — UPCF ================= #
    q3 = q3_upcf(s20, 120_000.0)
    ws = wb.create_sheet("Q3_UPCF")
    _titulo(ws, "Questão 3 — Reajuste do salário mínimo: +R$ 120 bi de consumo das famílias (2020)",
            "Choque repartido pela UPCF — a cesta observada a preço de consumidor: produtos "
            "nacionais + importados + impostos + margens (aba 12 da MIP, coluna Famílias). "
            "Margens voltam como demanda de comércio/transporte; impostos não geram produção.",
            ncols=12)
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
    r0 = _resposta(ws, 5, resp, ncols=12)
    ws.cell(r0, 1, "Choque (R$ milhões):").font = F_NEG
    c = ws.cell(r0, 3, 120_000.0)
    c.font = F_IN; c.fill = FILL_IN; c.number_format = NUM_MI
    Lch = f"$C${r0}"
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
        ws.cell(r0 + 1 + k, 2, rot).font = F_TXT
        cc = ws.cell(r0 + 1 + k, 3, float(v))
        cc.font = F_TXT; cc.number_format = NUM_MI
    r_den = r0 + 5
    ws.cell(r_den, 2, "Cesta total das famílias (denominador da UPCF)").font = F_NEG
    ws.cell(r_den, 3, f"=SUM({_faixa_dado('2020', 'familias', n)})"
                      f"+SUM(C{r0 + 1}:C{r0 + 4})").font = F_NEG
    ws[f"C{r_den}"].number_format = NUM_MI
    DEN = f"$C${r_den}"
    C_IMP, C_TAX, C_MGC, C_MGT = (f"$C${r0 + 1}", f"$C${r0 + 2}",
                                  f"$C${r0 + 3}", f"$C${r0 + 4}")
    soma_xc = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_c"]) or "1"
    soma_xt = "+".join(_celula_dado("2020", "x", i) for i in q3["idx_t"]) or "1"
    lin_dy = r_den + 2
    ws.cell(lin_dy, 2, "Δy (UPCF: nacional + margens realocadas) — linha auxiliar").font = F_SUB
    for j in range(n):
        termo = f"{_celula_dado('2020', 'familias', j)}"
        if j in q3["idx_c"]:
            termo += f"+{C_MGC}*{_celula_dado('2020', 'x', j)}/({soma_xc})"
        if j in q3["idx_t"]:
            termo += f"+{C_MGT}*{_celula_dado('2020', 'x', j)}/({soma_xt})"
        c = ws.cell(lin_dy, 3 + j, f"={Lch}*({termo})/{DEN}")
        c.font = F_TXT; c.number_format = NUM_MI
    r1 = lin_dy + 2
    _cab_tabela(ws, r1, 1, ["Código", "Setor", "Δ demanda (UPCF)", "Δx induzido",
                            "Δ importação induzida", "Δ ocupações"],
                larguras=[8, 36, 15, 13, 15, 13])
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        ws.cell(r, 3, f"={CL(3 + i)}{lin_dy}")
        ws.cell(r, 4, f"=SUMPRODUCT({_ref_mat('B_2020', i=i, n=n)},"
                      f"$C${lin_dy}:${CL(2 + n)}${lin_dy})")
        ws.cell(r, 5, f"=D{r}*{_celula_dado('2020', 'm_coef', i)}")
        ws.cell(r, 6, f"=D{r}*{_celula_dado('2020', 'w_emp', i)}")
        for k in range(3, 7):
            ws.cell(r, k).font = F_TXT
            ws.cell(r, k).number_format = NUM_MI if k < 6 else "#,##0.0"
    r_tot = r1 + 1 + n
    ws.cell(r_tot, 2, "TOTAL").font = F_NEG
    for col in "CDEF":
        ws[f"{col}{r_tot}"] = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        ws[f"{col}{r_tot}"].font = F_NEG
        ws[f"{col}{r_tot}"].number_format = NUM_MI
    r2 = r_tot + 2
    linhas_sint = [
        ("Importação direta (cesta importada da UPCF)",
         f"={Lch}*{C_IMP}/{DEN}", q3["dimp_direta"]),
        ("Importação induzida (insumos da produção)", f"=E{r_tot}", q3["dimp_induzida"]),
        ("IMPORTAÇÕES — TOTAL", None, q3["dimp_total"]),
        ("Impostos sobre produtos (vazamento fiscal, memo)",
         f"={Lch}*{C_TAX}/{DEN}", q3["dimposto"]),
        ("Ocupações geradas — TOTAL", f"=F{r_tot}", q3["demp"]),
    ]
    for k, (rot, formula, valor) in enumerate(linhas_sint):
        ws.cell(r2 + k, 2, rot).font = F_NEG
        cc = ws.cell(r2 + k, 5)
        cc.value = formula if formula else f"=E{r2}+E{r2 + 1}"
        cc.font = F_NEG; cc.number_format = NUM_MI
        confere[f"Q3_UPCF!E{r2 + k}"] = valor
    ws.freeze_panes = f"C{r1 + 1}"

    # ================= Q4 — Rasmussen-Hirschman ================= #
    bl10, fl10 = s10.rasmussen()
    bl20, fl20 = s20.rasmussen()
    chave10 = (bl10 > 1) & (fl10 > 1)
    chave20 = (bl20 > 1) & (fl20 > 1)
    ws = wb.create_sheet("Q4_RH")
    _titulo(ws, "Questão 4 — Índices de Rasmussen-Hirschman e setores-chave: 2010 × 2020",
            "Para trás: soma de coluna de B normalizada pela média geral (U_j). Para frente: "
            "soma de linha da inversa de GHOSH normalizada (U_i). Setor-chave: ambos > 1.",
            ncols=12)
    novos = [m20.nomes[i] for i in range(n) if chave20[i] and not chave10[i]]
    perdidos = [m20.nomes[i] for i in range(n) if chave10[i] and not chave20[i]]
    resp = [
        f"Setores-chave em 2010: {int(chave10.sum())}; em 2020: {int(chave20.sum())} "
        f"(critério RH estrito: U_para_trás > 1 e U_para_frente > 1).",
        ("Entraram no grupo-chave até 2020: " + "; ".join(novos)) if novos
        else "Nenhum setor entrou no grupo-chave entre 2010 e 2020.",
        ("Saíram do grupo-chave: " + "; ".join(perdidos)) if perdidos
        else "Nenhum setor saiu do grupo-chave entre 2010 e 2020.",
        "Transformações estruturais: as colunas Δ mostram onde o encadeamento para trás "
        "e para frente mudou na década — leia em conjunto com a Q7 (SDA): quedas difusas de "
        "ligação para trás indicam substituição de insumos domésticos (por importados ou por "
        "serviços), enquanto ganhos concentrados sinalizam adensamento de cadeia.",
    ]
    r0 = _resposta(ws, 5, resp, ncols=12)
    cab = ["Código", "Setor", "U trás 2010", "U frente 2010", "Chave 2010",
           "U trás 2020", "U frente 2020", "Chave 2020", "Δ trás", "Δ frente", "Mudança"]
    _cab_tabela(ws, r0, 1, cab, larguras=[8, 36] + [11] * 9)
    for i in range(n):
        r = r0 + 1 + i
        L = CL(3 + i)
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        for k, (aba_b, aba_g) in enumerate((("B_2010", "G_2010"), ("B_2020", "G_2020"))):
            cb = 3 + k * 3
            ws.cell(r, cb, f"=SUM({aba_b}!{L}4:{L}{3 + n})*{n}"
                           f"/SUM({aba_b}!$C$4:${CL(2 + n)}${3 + n})")
            ws.cell(r, cb + 1, f"=SUM({_ref_mat(aba_g, i=i, n=n)})*{n}"
                               f"/SUM({aba_g}!$C$4:${CL(2 + n)}${3 + n})")
            ws.cell(r, cb + 2, f'=IF(AND({CL(cb)}{r}>1,{CL(cb + 1)}{r}>1),"CHAVE","")')
        ws.cell(r, 9, f"=F{r}-C{r}")
        ws.cell(r, 10, f"=G{r}-D{r}")
        ws.cell(r, 11, f'=IF(E{r}=H{r},"",IF(H{r}="CHAVE","entrou","saiu"))')
        for k in (3, 4, 6, 7, 9, 10):
            ws.cell(r, k).number_format = NUM_IDX
        for k in range(3, 12):
            ws.cell(r, k).font = F_TXT
    confere[f"Q4_RH!C{r0 + 1}"] = float(bl10[0])
    confere[f"Q4_RH!G{r0 + 1}"] = float(fl20[0])
    ws.freeze_panes = f"C{r0 + 1}"

    # ================= Q5 — campo de influência (2010) ================= #
    S = q5_campo_influencia(s10)
    ws = wb.create_sheet("Q5_CampoInfluencia")
    _titulo(ws, "Questão 5 — Campos de influência dos setores (Brasil, 2010)",
            f"Sonis & Hewings; ε = {EPS_CAMPO}. S(i,j) mede o quanto uma variação no "
            "coeficiente a(i,j) se propaga pela economia (Σ dos quadrados de [B(ε)−B]/ε). "
            "Equivalente exato do laço em R do material de apoio (Vale & Perobelli), via "
            "Sherman-Morrison. Matriz S como VALOR; médias e destaques por fórmula.",
            ncols=12)
    Srow = S.mean(1); Scol = S.mean(0)
    o_link = np.dstack(np.unravel_index(np.argsort(S, axis=None)[::-1], S.shape))[0]
    resp = [
        f"Elo de maior campo de influência: a({m10.nomes[o_link[0][0]]} → "
        f"{m10.nomes[o_link[0][1]]}), S = {S[o_link[0][0], o_link[0][1]]:,.1f}.",
        f"Setores cujas LINHAS mais influenciam (vendedores estratégicos): "
        + "; ".join(m10.nomes[i] for i in np.argsort(Srow)[::-1][:3]) + ".",
        f"Setores cujas COLUNAS mais influenciam (compradores estratégicos): "
        + "; ".join(m10.nomes[j] for j in np.argsort(Scol)[::-1][:3]) + ".",
        "Interpretação: elos com S alto são os pontos onde mudanças tecnológicas (variações "
        "de coeficiente) mais alteram a inversa de Leontief — candidatos naturais a política "
        "industrial; coincidem majoritariamente com os setores-chave da Q4.",
    ]
    r0 = _resposta(ws, 5, resp, ncols=12)
    topk = min(20, n * n)
    ws.cell(r0 - 1, 14, "TOP elos a(i,j) por campo de influência").font = F_NEG
    _cab_tabela(ws, r0, 14, ["#", "Vendedor (i)", "Comprador (j)", "S(i,j)"],
                larguras=[4, 30, 30, 12])
    r_mat0 = r0 + topk + 3
    for k in range(topk):
        i, j = int(o_link[k][0]), int(o_link[k][1])
        ws.cell(r0 + 1 + k, 14, k + 1).font = F_TXT
        ws.cell(r0 + 1 + k, 15, m10.nomes[i]).font = F_TXT
        ws.cell(r0 + 1 + k, 16, m10.nomes[j]).font = F_TXT
        v = ws.cell(r0 + 1 + k, 17, f"={CL(3 + j)}{r_mat0 + 1 + i}")
        v.font = F_TXT; v.number_format = "#,##0.00"
    ws.cell(r_mat0 - 1, 1, "Matriz S (valores; linhas = vendedor i, colunas = comprador j) "
                           "— médias por fórmula nas bordas").font = F_NEG
    for j in range(n):
        c = ws.cell(r_mat0, 3 + j, m10.cod[j]); c.font = F_CAB; c.fill = FILL_CAB
    for i in range(n):
        r = r_mat0 + 1 + i
        ws.cell(r, 1, m10.cod[i]).font = F_TXT
        ws.cell(r, 2, m10.nomes[i]).font = F_TXT
        for j in range(n):
            c = ws.cell(r, 3 + j, float(S[i, j]))
            c.font = F_TXT; c.number_format = "#,##0.00"
        c = ws.cell(r, 3 + n, f"=AVERAGE(C{r}:{CL(2 + n)}{r})")
        c.font = F_NEG; c.number_format = "#,##0.00"
    ws.cell(r_mat0, 3 + n, "média linha").font = F_NEG
    r_med = r_mat0 + 1 + n
    ws.cell(r_med, 2, "média coluna").font = F_NEG
    for j in range(n):
        c = ws.cell(r_med, 3 + j, f"=AVERAGE({CL(3 + j)}{r_mat0 + 1}:{CL(3 + j)}{r_med - 1})")
        c.font = F_NEG; c.number_format = "#,##0.00"
    confere[f"Q5_CampoInfluencia!C{r_mat0 + 1}"] = float(S[0, 0])
    ws.freeze_panes = f"C{r0 + 1}"

    # ================= Q6 — extração hipotética ================= #
    q6 = q6_extracao(s20, i_q6)
    ws = wb.create_sheet("Q6_Extracao")
    _titulo(ws, f"Questão 6 — Extração hipotética TOTAL (2020): {m20.nomes[i_q6]}",
            "Zera-se a linha e a coluna do setor em A e sua demanda final; a perda é a "
            "diferença entre a produção do sistema completo (x = B·y) e a do sistema reduzido. "
            "Coluna 'x reduzido' colada como VALOR (nova inversão); demais colunas por fórmula.",
            ncols=12)
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
    r0 = _resposta(ws, 5, resp, ncols=12)
    _cab_tabela(ws, r0, 1, ["Código", "Setor", "x baseline (B·y)", "x reduzido (valor)",
                            "Perda", "Perda (% do setor)"],
                larguras=[8, 36, 15, 15, 15, 13])
    for i in range(n):
        r = r0 + 1 + i
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        ws.cell(r, 3, float(q6["x_base"][i])).number_format = NUM_MI
        ws.cell(r, 4, float(q6["x_ex"][i])).number_format = NUM_MI
        ws.cell(r, 5, f"=C{r}-D{r}").number_format = NUM_MI
        ws.cell(r, 6, f"=IF(C{r}=0,0,E{r}/C{r})").number_format = NUM_PCT
        for k in range(3, 7):
            ws.cell(r, k).font = F_TXT
    r_tot = r0 + 1 + n
    ws.cell(r_tot, 2, "TOTAL").font = F_NEG
    for col, fmt in (("C", NUM_MI), ("D", NUM_MI), ("E", NUM_MI)):
        ws[f"{col}{r_tot}"] = f"=SUM({col}{r0 + 1}:{col}{r_tot - 1})"
        ws[f"{col}{r_tot}"].font = F_NEG; ws[f"{col}{r_tot}"].number_format = fmt
    ws[f"F{r_tot}"] = f"=E{r_tot}/C{r_tot}"
    ws[f"F{r_tot}"].font = F_NEG; ws[f"F{r_tot}"].number_format = NUM_PCT
    confere[f"Q6_Extracao!E{r_tot}"] = q6["perda_total"]
    ws.freeze_panes = f"C{r0 + 1}"

    # ================= Q7 — SDA ================= #
    fator = float(np.prod([1 + v / 100 for v in IPCA_ANUAL.values()]))
    q7 = q7_sda(s10, s20, fator)
    ws = wb.create_sheet("Q7_SDA")
    _titulo(ws, "Questão 7 — Decomposição estrutural 2010→2020 (matriz de 2010 atualizada pelo IPCA)",
            "SDA bipolar média: Δx = ½ΔB·(y0*+y1) + ½(B0+B1)·Δy, com y0* = y2010 × fator IPCA. "
            "O deflator único não altera A/B de 2010 (coeficientes são razões) — atualiza níveis.",
            ncols=12)
    dtec, ddem, ddx = q7["tec"].sum(), q7["dem"].sum(), q7["dx"].sum()
    resp = [
        f"Fator IPCA acumulado dez/2010→dez/2020: {fator:.4f} (tabela de variações anuais "
        "abaixo, células azuis editáveis).",
        f"Δx total (preços de 2020): R$ {ddx:,.0f} mi — decomposto em EFEITO TECNOLOGIA "
        f"(mudança de coeficientes, ΔB): R$ {dtec:,.0f} mi ({dtec / ddx:.1%}) e EFEITO "
        f"DEMANDA FINAL (Δy): R$ {ddem:,.0f} mi ({ddem / ddx:.1%}).",
        "Leitura: efeito-demanda dominante com efeito-tecnologia negativo/difuso é o padrão "
        "de uma década de crescimento extensivo com desadensamento de cadeias (consistente "
        "com as mudanças de ligação da Q4); a coluna 'checagem' comprova a aditividade exata "
        "da decomposição em cada setor.",
    ]
    r0 = _resposta(ws, 5, resp, ncols=12)
    ws.cell(r0, 1, "IPCA % a.a. (IBGE):").font = F_NEG
    for k, (ano, v) in enumerate(sorted(IPCA_ANUAL.items())):
        ws.cell(r0 + 1, 2 + k, str(ano)).font = F_SUB
        c = ws.cell(r0 + 2, 2 + k, v)
        c.font = F_IN; c.number_format = "0.00"
    fator_expr = "=" + "*".join(f"(1+{CL(2 + k)}{r0 + 2}/100)"
                                for k in range(len(IPCA_ANUAL)))
    c_fat = ws.cell(r0 + 2, 3 + len(IPCA_ANUAL), fator_expr)
    c_fat.font = F_NEG; c_fat.number_format = "0.0000"
    ws.cell(r0 + 1, 3 + len(IPCA_ANUAL), "fator acumulado").font = F_SUB
    FAT = f"${CL(3 + len(IPCA_ANUAL))}${r0 + 2}"
    lin_ysum, lin_ydel = r0 + 4, r0 + 5
    ws.cell(lin_ysum, 2, "y0*+y1 — linha auxiliar").font = F_SUB
    ws.cell(lin_ydel, 2, "y1−y0* — linha auxiliar").font = F_SUB
    for j in range(n):
        y0 = f"{_celula_dado('2010', 'ytot', j)}*{FAT}"
        y1 = f"{_celula_dado('2020', 'ytot', j)}"
        ws.cell(lin_ysum, 3 + j, f"={y0}+{y1}").number_format = NUM_MI
        ws.cell(lin_ydel, 3 + j, f"={y1}-{y0}").number_format = NUM_MI
        ws.cell(lin_ysum, 3 + j).font = F_TXT
        ws.cell(lin_ydel, 3 + j).font = F_TXT
    r1 = lin_ydel + 2
    _cab_tabela(ws, r1, 1, ["Código", "Setor", "x 2010 a preços 2020", "x 2020", "Δx",
                            "Efeito tecnologia (ΔB)", "Efeito demanda (Δy)",
                            "Checagem (tec+dem−Δx)"],
                larguras=[8, 36, 16, 14, 14, 16, 16, 14])
    fim = CL(2 + n)
    for i in range(n):
        r = r1 + 1 + i
        ws.cell(r, 1, m20.cod[i]).font = F_TXT
        ws.cell(r, 2, m20.nomes[i]).font = F_TXT
        b0 = _ref_mat("B_2010", i=i, n=n)
        b1 = _ref_mat("B_2020", i=i, n=n)
        ws.cell(r, 3, f"={_celula_dado('2010', 'x', i)}*{FAT}")
        ws.cell(r, 4, f"={_celula_dado('2020', 'x', i)}")
        ws.cell(r, 5, f"=D{r}-C{r}")
        ws.cell(r, 6, f"=0.5*(SUMPRODUCT({b1},$C${lin_ysum}:${fim}${lin_ysum})"
                      f"-SUMPRODUCT({b0},$C${lin_ysum}:${fim}${lin_ysum}))")
        ws.cell(r, 7, f"=0.5*(SUMPRODUCT({b1},$C${lin_ydel}:${fim}${lin_ydel})"
                      f"+SUMPRODUCT({b0},$C${lin_ydel}:${fim}${lin_ydel}))")
        ws.cell(r, 8, f"=F{r}+G{r}-E{r}")
        for k in range(3, 9):
            ws.cell(r, k).font = F_TXT
            ws.cell(r, k).number_format = NUM_MI
    r_tot = r1 + 1 + n
    ws.cell(r_tot, 2, "TOTAL").font = F_NEG
    for col in "CDEFGH":
        ws[f"{col}{r_tot}"] = f"=SUM({col}{r1 + 1}:{col}{r_tot - 1})"
        ws[f"{col}{r_tot}"].font = F_NEG
        ws[f"{col}{r_tot}"].number_format = NUM_MI
    confere[f"Q7_SDA!F{r_tot}"] = float(q7["tec"].sum())
    confere[f"Q7_SDA!G{r_tot}"] = float(q7["dem"].sum())
    ws.freeze_panes = f"C{r1 + 1}"

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
        assert not any("dimensão" in a for a in avisos), avisos
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
    import json
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
    import json
    with open(Path(args.out).with_suffix(".confere.json"), "w", encoding="utf-8") as fh:
        json.dump(confere, fh, ensure_ascii=False, indent=1)
    print(f"[ok] planilha gerada: {args.out}")
    print("=> recalcule as fórmulas (abrir no Excel/LibreOffice ou scripts/recalc) e rode "
          "verificar_recalculo() com o .confere.json para a prova final.")


if __name__ == "__main__":
    main()
