# -*- coding: utf-8 -*-
"""
mip_nereus.py — carga das matrizes nacionais "MIP-BR <ano> (Nível 68).xlsm"
(NEREUS/CECEG, pasta de trabalho estilo Guilhoto) para a Lista de Exercícios da
disciplina (Prof. Celso Bissoli Sessa, 2026/1).

Layout confirmado nos arquivos reais (2010 e 2020):
  aba '12' = ESTRUTURA DA MATRIZ INSUMO-PRODUTO, R$ milhões correntes:
    - linha 6: cabeçalho 'Código' (col B) / 'Atividades' (col C); col D = índice 1..68;
    - linhas 7-74: 68 atividades; cols E-BT (5-72) = consumo intermediário de
      origem NACIONAL (D.Un); cols BV-CA (74-79) = demanda final nacional
      (Exportação, Governo, ISFLSF, Famílias, FBCF, Var. estoque); col 80 = total;
    - abaixo do bloco: linhas 'Importação', 'Impostos', 'Margens' (com o
      desdobramento 'Comércio'/'Transporte'), bloco de VA ('B) Remunerações',
      'B.1) Salários', 'F) Valor Adicionado Bruto'), 'Valor Bruto da Produção'
      e 'Fator Trabalho (Ocupações)' — essas linhas cruzam TAMBÉM as colunas de
      demanda final (ex.: célula Importação×Famílias = consumo importado das
      famílias), o que alimenta a UPCF da Questão 3.
  aba '13' = matriz A dos insumos nacionais (usada só como conferência).

A carga é dirigida por rótulos: âncora 'Código/Atividades' quando existir,
heurística de bloco contíguo caso contrário; `--inspect` depura qualquer layout.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

import numpy as np
import openpyxl


# --------------------------------------------------------------------------- #
# utilidades
# --------------------------------------------------------------------------- #
def norm(s) -> str:
    """minúsculas, sem acento, espaços colapsados — para casar rótulos."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def num(v) -> float:
    return float(v) if isinstance(v, (int, float)) else 0.0


def grade(ws, max_row=None, max_col=None):
    """matriz de valores da planilha (lista de listas, indexada de 0)."""
    return [list(r) for r in ws.iter_rows(min_row=1, max_row=max_row,
                                          max_col=max_col, values_only=True)]


RE_CODIGO = re.compile(r"^\d{3,5}$")

COMPONENTES_DF = ["exportacao", "governo", "isflsf", "familias", "fbcf", "estoque"]

PADROES_DF = {
    "exportacao": ("exportacao",),
    "governo":    ("governo", "administracao publica"),
    "isflsf":     ("isflsf", "instituicoes sem fins"),
    "familias":   ("familias",),
    "fbcf":       ("formacao bruta", "fbcf"),
    "estoque":    ("variacao de estoque", "estoque"),
}

# linhas do bloco abaixo de Z (a ordem dos padrões evita capturas erradas:
# 'valor adicionado bruto' NÃO casa com 'A) Valor Adicionado a Custo de Fatores')
PADROES_LINHAS = {
    "importacao":  ("importacao",),
    "impostos":    ("impostos",),
    "margens":     ("margens",),
    "marg_com":    ("comercio",),
    "marg_transp": ("transporte",),
    "va":          ("valor adicionado bruto", "vab"),
    "rem":         ("remuneracoes",),
    "salarios":    ("salarios",),
    "vp":          ("valor bruto da producao", "valor da producao", "valor de producao"),
    "ocup":        ("fator trabalho", "ocupacoes", "pessoal ocupado"),
}


@dataclass
class MIPAno:
    ano: int
    nomes: list[str]
    cod: list[str]
    Z: np.ndarray                      # consumo intermediário NACIONAL (n x n)
    y: dict[str, np.ndarray]           # demanda final nacional por componente (n)
    x: np.ndarray                      # valor bruto da produção (n)
    rem: np.ndarray                    # remunerações (n)
    va: np.ndarray                     # valor adicionado bruto (n)
    ocup: np.ndarray                   # fator trabalho / ocupações (n)
    imp_int: np.ndarray                # importação intermediária por setor comprador (n)
    fd_fam: dict[str, float] = field(default_factory=dict)  # cesta das famílias fora
    # do vetor nacional: importacao, impostos, margens_comercio, margens_transporte
    proveniencia: dict = field(default_factory=dict)

    @property
    def n(self) -> int:
        return len(self.nomes)

    def y_total(self) -> np.ndarray:
        return np.sum([self.y[c] for c in COMPONENTES_DF], axis=0)

    def cesta_familias_total(self) -> float:
        """consumo das famílias a preço de consumidor = nacional básico + extras."""
        return float(self.y["familias"].sum() + sum(self.fd_fam.values()))

    def validar(self) -> list[str]:
        avisos = []
        x_row = self.Z.sum(1) + self.y_total()
        err = np.max(np.abs(self.x - x_row) / np.where(self.x == 0, 1, np.abs(self.x)))
        if err > 0.02:
            avisos.append(f"balanço de linha x = Z·1 + y com desvio máximo de {err:.1%}")
        A = self.Z / np.where(self.x == 0, 1, self.x)[None, :]
        if A.sum(0).max() >= 1:
            avisos.append(f"soma de coluna de A chega a {A.sum(0).max():.3f} (>=1)")
        for rot, v in [("rem", self.rem), ("va", self.va), ("ocup", self.ocup),
                       ("imp_int", self.imp_int)]:
            if not np.any(v):
                avisos.append(f"vetor {rot} zerado/ausente")
        return avisos


# --------------------------------------------------------------------------- #
# localização do bloco de setores
# --------------------------------------------------------------------------- #
def _ancora_codigo(G):
    """âncora 'Código'/'Atividades': devolve (linha_1o_setor, c_cod, c_nome) ou None."""
    for r in range(min(len(G), 20)):
        row = G[r]
        vals = [norm(v) for v in row[:8]]
        if "codigo" in vals:
            c_cod = vals.index("codigo")
            c_nome = next((i for i, v in enumerate(vals)
                           if v.startswith("atividade") or v.startswith("descricao")
                           or v.startswith("setor")), None)
            if c_nome is not None:
                return r + 1, c_cod, c_nome
    return None


def achar_bloco_setores(G, min_run=5):
    """Fallback heurístico: maior sequência contígua de textos que não sejam
    rótulos de total; entre finalistas, a que começa mais acima e, no empate,
    a de texto médio mais longo (nomes, não códigos). Índices base 0."""
    candidatas = []
    nlin = len(G)
    ncol = max(len(r) for r in G) if G else 0
    for c in range(min(ncol, 8)):
        r = 0
        while r < nlin:
            v = G[r][c] if c < len(G[r]) else None
            if isinstance(v, str) and norm(v) and not _eh_total(v):
                r0 = r
                textos = []
                while r < nlin:
                    v = G[r][c] if c < len(G[r]) else None
                    if isinstance(v, str) and norm(v) and not _eh_total(v):
                        textos.append(str(v)); r += 1
                    else:
                        break
                if len(textos) >= min_run:
                    media = sum(len(t) for t in textos) / len(textos)
                    candidatas.append((r0, r - 1, c, len(textos), media))
            else:
                r += 1
    if not candidatas:
        raise ValueError("não achei bloco contíguo de nomes de setor — use --inspect")
    run_max = max(c[3] for c in candidatas)
    finalistas = [c for c in candidatas if c[3] >= 0.9 * run_max]
    r0, r1, c, _, _ = min(finalistas, key=lambda t: (t[0], -t[4]))
    return r0, r1, c


def _eh_total(v) -> bool:
    s = norm(v)
    return s.startswith("total") or s in ("demanda final", "demanda total",
                                          "consumo intermediario", "usos")


def _bloco_numerico(G, r0, r1, col_ini, n):
    """primeiras n colunas densamente numéricas a partir de col_ini (pula colunas
    de índice sequencial 1..n, comuns nos arquivos do IBGE/NEREUS)."""
    ncol = max(len(r) for r in G)
    cols = []
    c = col_ini
    while c < ncol and len(cols) < n:
        vals = [G[r][c] if c < len(G[r]) else None for r in range(r0, r1 + 1)]
        dens = sum(isinstance(v, (int, float)) for v in vals) / (r1 - r0 + 1)
        eh_rampa = all(isinstance(v, (int, float)) and abs(v - (k + 1)) < 1e-9
                       for k, v in enumerate(vals))
        if dens >= 0.5 and not eh_rampa:
            cols.append(c)
        elif cols:
            break
        c += 1
    if len(cols) < n:
        raise ValueError(f"esperava {n} colunas numéricas a partir da coluna "
                         f"{col_ini + 1}; achei {len(cols)} — use --inspect")
    return cols


def _cabecalho(G, r0, cols_alvo, alcance=6):
    """cabeçalho por coluna: concatena até `alcance` linhas acima do bloco."""
    out = {}
    for c in cols_alvo:
        partes = []
        for r in range(max(0, r0 - alcance), r0):
            v = G[r][c] if c < len(G[r]) else None
            if isinstance(v, str) and v.strip():
                partes.append(v)
        out[c] = norm(" ".join(partes))
    return out


# --------------------------------------------------------------------------- #
# carga da aba de fluxos ('12' — estrutura da MIP)
# --------------------------------------------------------------------------- #
def _carregar_fluxos(ws, rotulo_aba):
    G = grade(ws)
    anc = _ancora_codigo(G)
    if anc:
        r_hdr, c_cod, c_nome = anc
        r0 = r_hdr
        r1 = r0
        while r1 < len(G):
            v = G[r1][c_cod] if c_cod < len(G[r1]) else None
            txt = str(v).strip() if v is not None else ""
            if RE_CODIGO.match(txt) or (isinstance(v, (int, float)) and float(v).is_integer()):
                r1 += 1
            else:
                break
        r1 -= 1
        if r1 - r0 + 1 < 5:
            anc = None
    if not anc:
        r0, r1, c_nome = achar_bloco_setores(G)
        c_cod = None
    n = r1 - r0 + 1

    nomes = [str(G[r][c_nome]).replace("\n", " ").strip() for r in range(r0, r1 + 1)]
    cods = []
    for r in range(r0, r1 + 1):
        cod = ""
        for c in range(c_nome):
            v = G[r][c] if c < len(G[r]) else None
            if v is not None and str(v).strip():
                cod = str(v).strip()
        cods.append(cod)

    cols_Z = _bloco_numerico(G, r0, r1, c_nome + 1, n)
    Z = np.array([[num(G[r][c] if c < len(G[r]) else None) for c in cols_Z]
                  for r in range(r0, r1 + 1)])

    # componentes de demanda final (colunas à direita de Z, casadas pelo cabeçalho)
    ncol = max(len(r) for r in G)
    cols_dir = list(range(cols_Z[-1] + 1, ncol))
    cab = _cabecalho(G, r0, cols_dir)
    col_df = {}
    for comp, padroes in PADROES_DF.items():
        for c in cols_dir:
            if any(p in cab[c] for p in padroes) and comp not in col_df:
                col_df[comp] = c
                break
    ycomp = {comp: np.array([num(G[r][c] if c < len(G[r]) else None)
                             for r in range(r0, r1 + 1)])
             for comp, c in col_df.items()}

    # linhas rotuladas abaixo do bloco (com densidade numérica mínima sobre Z)
    linhas, linhas_df = {}, {}
    for r in range(r1 + 1, len(G)):
        rot = ""
        for c in range(0, c_nome + 1):
            v = G[r][c] if c < len(G[r]) else None
            if isinstance(v, str) and v.strip():
                rot = norm(v)
        if not rot:
            continue
        vals = [G[r][c] if c < len(G[r]) else None for c in cols_Z]
        dens = sum(isinstance(v, (int, float)) for v in vals) / n
        if dens < 0.5:
            continue
        for chave, padroes in PADROES_LINHAS.items():
            if any(p in rot for p in padroes) and chave not in linhas:
                linhas[chave] = np.array([num(v) for v in vals])
                if col_df:
                    linhas_df[chave] = {comp: num(G[r][c] if c < len(G[r]) else None)
                                        for comp, c in col_df.items()}
                break

    prov = {"aba": rotulo_aba, "linhas_setores": (r0 + 1, r1 + 1),
            "col_nomes": c_nome + 1, "cols_Z": (cols_Z[0] + 1, cols_Z[-1] + 1),
            "df_encontrada": sorted(ycomp), "linhas_encontradas": sorted(linhas)}
    return nomes, cods, Z, ycomp, linhas, linhas_df, prov


def carregar_mip(caminho: str, ano: int) -> MIPAno:
    """Carrega um 'MIP-BR <ano> (Nível 68).xlsm/.xlsx' e devolve MIPAno."""
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    try:
        erros = {}
        candidatos = [s for s in ("12", "11", "03") if s in wb.sheetnames]
        candidatos += [s for s in wb.sheetnames if s not in candidatos]
        for aba in candidatos:
            try:
                nomes, cods, Z, ycomp, linhas, linhas_df, prov = \
                    _carregar_fluxos(wb[aba], aba)
            except ValueError as e:
                erros[aba] = str(e)
                continue
            faltam = [c for c in COMPONENTES_DF if c not in ycomp]
            essenciais = [k for k in ("rem", "va", "ocup") if k not in linhas]
            if faltam or essenciais:
                erros[aba] = f"faltam df={faltam} linhas={essenciais}"
                continue

            n = len(nomes)
            x = linhas.get("vp", np.zeros(n))
            if not np.any(x):
                x = Z.sum(1) + np.sum([ycomp[c] for c in COMPONENTES_DF], axis=0)
            fd_fam = {}
            for chave, alvo in (("importacao", "importacao"), ("impostos", "impostos"),
                                ("marg_com", "margens_comercio"),
                                ("marg_transp", "margens_transporte")):
                if chave in linhas_df:
                    fd_fam[alvo] = linhas_df[chave].get("familias", 0.0)
            return MIPAno(ano=ano, nomes=nomes, cod=cods, Z=Z, y=ycomp, x=x,
                          rem=linhas["rem"], va=linhas["va"], ocup=linhas["ocup"],
                          imp_int=linhas.get("importacao", np.zeros(n)),
                          fd_fam=fd_fam,
                          proveniencia={"arquivo": caminho, "nacional": prov})
        raise ValueError(f"nenhuma aba com a estrutura da MIP; tentativas: {erros}")
    finally:
        wb.close()


# --------------------------------------------------------------------------- #
# inspeção de layout
# --------------------------------------------------------------------------- #
def inspecionar(caminho: str) -> str:
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    saida = [f"arquivo: {caminho}", f"abas: {wb.sheetnames}"]
    for nome in wb.sheetnames:
        ws = wb[nome]
        G = grade(ws, max_row=min(ws.max_row or 0, 200), max_col=min(ws.max_column or 0, 130))
        saida.append(f"\n--- aba '{nome}' ({ws.max_row}x{ws.max_column}) ---")
        try:
            anc = _ancora_codigo(G)
            if anc:
                saida.append(f"  âncora Código/Atividades na linha {anc[0]}, "
                             f"cols {anc[1] + 1}/{anc[2] + 1}")
            r0, r1, c = achar_bloco_setores(G)
            saida.append(f"  bloco: linhas {r0 + 1}-{r1 + 1} ({r1 - r0 + 1} itens), "
                         f"nomes na coluna {c + 1}; 1º {G[r0][c]!r} último {G[r1][c]!r}")
            for r in range(r1 + 1, min(r1 + 30, len(G))):
                rot = next((str(G[r][cc]) for cc in range(0, c + 1)
                            if cc < len(G[r]) and isinstance(G[r][cc], str)
                            and G[r][cc].strip()), "")
                if rot:
                    saida.append(f"  linha {r + 1}: {rot[:80]!r}")
        except ValueError as e:
            saida.append(f"  (sem bloco de setores: {e})")
    wb.close()
    return "\n".join(saida)


# --------------------------------------------------------------------------- #
# gerador sintético (selftest): aba '12' em miniatura, no layout REAL
# --------------------------------------------------------------------------- #
def escrever_sintetico(caminho: str, ano: int, semente: int = 7, n: int = 8) -> None:
    """Economia sintética balanceada escrita no MESMO layout da aba '12' real
    (âncora Código/Atividades, DF por componente, bloco inferior com Importação/
    Margens/VA/VBP/Ocupações cruzando as colunas de demanda final)."""
    rng = np.random.default_rng(semente + ano)
    nomes = [f"Setor sintético {i + 1:02d}" for i in range(n)]
    nomes[n - 3] = "Comércio sintético por atacado e a varejo"
    nomes[n - 2] = "Transporte sintético terrestre"
    x = rng.uniform(1e5, 5e5, n)
    A = rng.uniform(0.01, 0.10, (n, n)); np.fill_diagonal(A, rng.uniform(0.04, 0.10, n))
    Z = A * x[None, :]
    while (x - Z.sum(1)).min() <= 0.05 * x.min():
        A *= 0.8
        Z = A * x[None, :]
    m_coef = rng.uniform(0.02, 0.08, n)
    imp_int = m_coef * x
    impostos = rng.uniform(0.01, 0.04, n) * x
    va = x - Z.sum(0) - imp_int - impostos
    rem = va * rng.uniform(0.35, 0.6, n)
    sal = rem * rng.uniform(0.6, 0.8, n)
    ocup = x * rng.uniform(5, 40, n) / 1e3
    resto = x - Z.sum(1)
    pesos = rng.dirichlet(np.ones(6), n)
    Ynac = pesos * resto[:, None]
    fd_imp = rng.uniform(0.03, 0.10, 6) * Ynac.sum(0)
    fd_impostos = rng.uniform(0.02, 0.08, 6) * Ynac.sum(0)
    fd_marg_c = np.array([0, 0, 0, 0.12 * Ynac.sum(0)[3], 0.05 * Ynac.sum(0)[4], 0])
    fd_marg_t = fd_marg_c * 0.06

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    ws = wb.create_sheet("12")
    ws.cell(2, 2, "ESTRUTURA DA MATRIZ INSUMO-PRODUTO (SINTÉTICA)")
    ws.cell(3, 2, "(valores correntes em R$ milhões)")
    cabec = ["Exportação", "Consumo \ndo Governo", "Consumo \ndas ISFLSF",
             "Consumo \ndas Famílias", "Formação Bruta de Capital Fixo",
             "Variação de Estoque"]
    ws.cell(4, 4 + n + 1, "Demanda Final")
    for k, h in enumerate(cabec):
        ws.cell(5, 5 + n + k, h)
    ws.cell(6, 2, "Código"); ws.cell(6, 3, "Atividades")
    for j in range(n):
        ws.cell(6, 5 + j, j + 1)
    for i in range(n):
        r = 7 + i
        ws.cell(r, 2, f"{(i + 1) * 100 + 91:04d}")
        ws.cell(r, 3, nomes[i])
        ws.cell(r, 4, i + 1)
        for j in range(n):
            ws.cell(r, 5 + j, float(Z[i, j]))
        for k in range(6):
            ws.cell(r, 5 + n + k, float(Ynac[i, k]))
    blocos = [
        ("Insumos Domésticos", Z.sum(0), Ynac.sum(0)),
        ("Importação", imp_int, fd_imp),
        ("Impostos", impostos, fd_impostos),
        ("Margens", np.zeros(n), fd_marg_c + fd_marg_t),
        ("Comércio", np.zeros(n), fd_marg_c),
        ("Transporte", np.zeros(n), fd_marg_t),
        ("B) Remunerações (= B.1+B.2+B.3)", rem, None),
        ("B.1)  Salários", sal, None),
        ("F) Valor Adicionado Bruto, VAB (=A+D+E)", va, None),
        ("Valor Bruto da Produção (VBP)", x, None),
        ("Fator Trabalho (Ocupações)", ocup, None),
    ]
    for b, (rot, vet, fd) in enumerate(blocos):
        r = 8 + n + b
        ws.cell(r, 2, rot)
        for j in range(n):
            ws.cell(r, 5 + j, float(vet[j]))
        if fd is not None:
            for k in range(6):
                ws.cell(r, 5 + n + k, float(fd[k]))

    ws13 = wb.create_sheet("13")
    ws13.cell(2, 2, "Matriz de coeficientes técnicos dos insumos nacionais (sintética)")
    ws13.cell(6, 2, "Código"); ws13.cell(6, 3, "Atividades")
    for i in range(n):
        ws13.cell(7 + i, 2, f"{(i + 1) * 100 + 91:04d}")
        ws13.cell(7 + i, 3, nomes[i])
        ws13.cell(7 + i, 4, i + 1)
        for j in range(n):
            ws13.cell(7 + i, 5 + j, float(A[i, j]))
    wb.save(caminho)


def carregar_A_conferencia(caminho: str):
    """Lê a matriz A da aba '13' (se existir) para conferência contra Z/x̂."""
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    try:
        if "13" not in wb.sheetnames:
            return None
        G = grade(wb["13"])
        anc = _ancora_codigo(G)
        if not anc:
            return None
        r0, c_cod, c_nome = anc
        r1 = r0
        while r1 < len(G):
            v = G[r1][c_cod] if c_cod < len(G[r1]) else None
            if v is not None and RE_CODIGO.match(str(v).strip()):
                r1 += 1
            else:
                break
        r1 -= 1
        n = r1 - r0 + 1
        cols = _bloco_numerico(G, r0, r1, c_nome + 1, n)
        return np.array([[num(G[r][c] if c < len(G[r]) else None) for c in cols]
                         for r in range(r0, r1 + 1)])
    finally:
        wb.close()
