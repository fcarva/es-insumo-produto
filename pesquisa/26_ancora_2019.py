# -*- coding: utf-8 -*-
"""
26_ancora_2019.py — P6: a SEGUNDA ANCORA (2019). Reestima a bateria central do artigo
na matriz interestadual de Haddad et al. (2025) — 27 UFs x 68 setores, ano-base 2019,
com conta-satelite de ocupacoes — e compara com a ancora de 2008, transformando o
retrato "2008 + pano de fundo 2010-2021" em DUAS fotografias comparadas.

INTEGRIDADE PRIMEIRO (mesmo padrao do 23_carbono_plataforma.py): este script NAO
produz numero sem dado real. Ele exige a matriz em dados/MIP_2019/ e PARA se ela
nao existir. Nenhum resultado 2019 e reportado ate o dado estar presente.

ONDE OBTER O DADO (1 passo, na maquina com internet aberta):
  1. Pagina do artigo na RBERU: revistaaber.org.br/rberu/article/view/1225
     (Haddad, Araujo, Rocha & Vale, 2025, RBERU 19(4):607-638) — dados suplementares; OU
  2. Portal NEREUS/USP (usp.br/nereus), aba "Dados" — Matriz Interestadual 2019.
  Salvar o(s) .xlsx em dados/MIP_2019/. O satelite de CO2 do MESMO pacote alimenta
  o 23_carbono_plataforma.py (agregado aos 26 setores em dados/co2_intensidade.csv).

FLUXO EM DOIS MODOS:
  Modo 1 (LAYOUT vazio): INSPECIONA os arquivos (abas e dimensoes), imprime o mapa
    e para — preencha LAYOUT abaixo com o que a inspecao mostrar.
  Modo 2 (LAYOUT preenchido): computa a bateria por UF (vazamento ponderado do
    multiplicador, razao de feedback pela inversa particionada, destino do spillover
    ao nucleo SP+RJ, multiplicador de emprego se houver satelite), checa identidades
    contabeis, salva outputs/ancora_2019.csv e imprime a comparacao ES 2008 x 2019
    (2008 lido de outputs/benchmark_ufs.csv, ja versionado).
"""
import os, sys, csv, glob

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(BASE), "dados", "MIP_2019")
OUT  = os.path.join(BASE, "outputs")
os.makedirs(OUT, exist_ok=True)
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

UFS = ["RO","AC","AM","RR","PA","AP","TO","MA","PI","CE","RN","PB","PE","AL","SE","BA",
       "MG","ES","RJ","SP","PR","SC","RS","MS","MT","GO","DF"]  # ordem IBGE; conferir na inspecao
NR, NS = 27, 68

# ----------------------------------------------------------------------------
# LAYOUT: preencher APOS a inspecao (modo 1). Deixado vazio de proposito —
# nenhum intervalo e assumido sem ver o arquivo real.
# ----------------------------------------------------------------------------
LAYOUT = {
    # "arquivo":   "nome-do-arquivo.xlsx",
    # "aba_Z":     "nome da aba com a matriz de consumo intermediario 1836x1836",
    # "Z_r0": 0, "Z_c0": 0,        # linha/coluna (1-based) do primeiro elemento de Z
    # "aba_x":     "aba do VBP", "x_row": 0, "x_c0": 0,
    # "aba_fd":    "aba da demanda final", ...   (colunas por UF e componente)
    # "aba_emp":   "aba do satelite de ocupacoes (se houver)", ...
}

files = sorted(glob.glob(os.path.join(DATA, "*.xls*")))
if not files:
    print("=" * 76)
    print("[DADO AUSENTE] dados/MIP_2019/ nao contem a matriz interestadual de 2019.")
    print("=" * 76)
    print(__doc__.split("ONDE OBTER O DADO")[1].split("FLUXO")[0])
    print("Nada foi computado (nenhum numero e inventado sem o dado).")
    sys.exit(1)

import numpy as np
import openpyxl
print("=" * 76)
print("INSPECAO — arquivos em dados/MIP_2019/")
print("=" * 76)
for f in files:
    print(f"\n{os.path.basename(f)}")
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    for ws in wb.worksheets:
        print(f"   aba '{ws.title}': {ws.max_row} linhas x {ws.max_column} colunas")
    wb.close()

if not LAYOUT:
    print("\n[MODO 1] LAYOUT vazio: preencha o dicionario LAYOUT no topo deste script")
    print("com base na inspecao acima (aba e celula inicial de Z, VBP, demanda final,")
    print("ocupacoes) e rode novamente para computar a bateria 2019.")
    sys.exit(0)

# ----------------------------------------------------------------------------
# Modo 2 — computo (so executa com LAYOUT confirmado)
# ----------------------------------------------------------------------------
num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0
N = NR * NS
f = os.path.join(DATA, LAYOUT["arquivo"])
wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
ws = wb[LAYOUT["aba_Z"]]
grid = [r for r in ws.iter_rows(values_only=True)]
cell = lambda r, c: num(grid[r-1][c-1]) if (r-1 < len(grid) and c-1 < len(grid[r-1])) else 0.0
r0, c0 = LAYOUT["Z_r0"], LAYOUT["Z_c0"]
Z = np.array([[cell(r0 + i, c0 + j) for j in range(N)] for i in range(N)])
wsx = wb[LAYOUT["aba_x"]]
gx = [r for r in wsx.iter_rows(values_only=True)]
cx = lambda r, c: num(gx[r-1][c-1]) if (r-1 < len(gx) and c-1 < len(gx[r-1])) else 0.0
x = np.array([cx(LAYOUT["x_row"], LAYOUT["x_c0"] + j) for j in range(N)])
wb.close()

xs = np.where(x == 0, 1.0, x)
A = Z / xs[None, :]
assert A.sum(0).max() < 1.0 + 1e-6, f"SigmaA>=1 (max {A.sum(0).max():.3f}) — conferir LAYOUT"
B = np.linalg.inv(np.eye(N) - A)
assert (B >= -1e-9).all(), "B com entradas negativas — conferir LAYOUT"
reg = lambda g: slice(NS * g, NS * g + NS)
NUCLEO = [UFS.index("SP"), UFS.index("RJ")]

rows = []
for g in range(NR):
    Lc = np.arange(NS * g, NS * g + NS)
    Mc = np.array([i for i in range(N) if i // NS != g])
    O = B[:, Lc].sum(0); O_in = B[np.ix_(Lc, Lc)].sum(0)
    w = x[Lc] / x[Lc].sum()
    leak = float((w * (1 - O_in / np.where(O == 0, 1, O))).sum())
    A_LL = A[np.ix_(Lc, Lc)]; A_LM = A[np.ix_(Lc, Mc)]
    A_ML = A[np.ix_(Mc, Lc)]; A_MM = A[np.ix_(Mc, Mc)]
    iMM = np.linalg.inv(np.eye(Mc.size) - A_MM)
    iLL = np.linalg.inv(np.eye(NS) - A_LL)
    ifd = np.linalg.inv(np.eye(NS) - A_LL - A_LM @ iMM @ A_ML)
    # injecao-proxy: producao propria como escala (sem FD desagregada no LAYOUT minimo)
    yL = x[Lc] - (Z[Lc, :].sum(1))          # demanda final total por produto da UF
    yL = np.clip(yL, 0, None)
    inj = float(yL.sum())
    feed = float((ifd @ yL).sum() - (iLL @ yL).sum()) / inj if inj else 0.0
    xM = iMM @ A_ML @ (ifd @ yL)
    sb = np.zeros(NR); pos = 0
    for h in range(NR):
        if h == g: continue
        sb[h] = xM[pos:pos + NS].sum(); pos += NS
    dest_nucleo = float(sb[NUCLEO].sum() / sb.sum() * 100) if sb.sum() else 0.0
    rows.append([UFS[g], f"{x[Lc].sum():.1f}", f"{leak:.4f}", f"{feed:.5f}", f"{dest_nucleo:.1f}"])

with open(os.path.join(OUT, "ancora_2019.csv"), "w", newline="", encoding="utf-8") as fo:
    wr = csv.writer(fo)
    wr.writerow(["UF", "producao", "vazamento", "feedback_razao", "dest_nucleo_pct"])
    wr.writerows(rows)
print("salvo: ancora_2019.csv")

# comparacao ES 2008 x 2019
b08 = {r["UF"]: r for r in csv.DictReader(open(os.path.join(OUT, "benchmark_ufs.csv")))}
es19 = next(r for r in rows if r[0] == "ES")
print("-" * 76)
print("ES — 2008 (benchmark_ufs.csv) vs 2019 (esta matriz):")
print(f"  vazamento : {float(b08['ES']['vazamento'])*100:.1f}%  ->  {float(es19[2])*100:.1f}%")
print(f"  feedback  : {float(b08['ES']['feedback_razao'])*100:.2f}% ->  {float(es19[3])*100:.2f}%")
print(f"  ->nucleo  : {b08['ES']['dest_nucleo_pct']}%  ->  {es19[4]}%")
print("(interpretar com a ressalva de safra/agregacao: 2008/26 setores vs 2019/68)")
