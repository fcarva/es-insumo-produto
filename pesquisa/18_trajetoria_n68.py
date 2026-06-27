# -*- coding: utf-8 -*-
"""
18_trajetoria_n68.py — C2: PANORAMA TEMPORAL (2010-2021) dos setores-base do ES na
estrutura NACIONAL (série Nível 68, NEREUS/CECEG). Para os setores que definem a
economia capixaba (petróleo/gás, minério de ferro, metalurgia, celulose/papel,
refino), acompanha a evolução do MULTIPLICADOR DE PRODUÇÃO e da LIGAÇÃO PARA TRÁS
(Rasmussen-Hirschman) ao longo de 12 anos — atravessando Fundão (2015), a recessão
2014-16 e a COVID (2020).

Fonte: MIP-BR <ano> (Nível 68).xlsm, aba '13' = matriz A (coef. técnicos, 68x68),
linhas 7-74, código col 2, índice col 4, coeficientes cols 5-72.
"""
import os, csv, sys, glob, re, warnings
import numpy as np, openpyxl
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

DIR = r"C:/Users/DELL/Downloads/Material IO/Matrizes/Nível 68/Nível 68"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0

# setores-base do ES (palavras-chave no nome do Nível 68)
BASE_KEYS = {
    "Petróleo/gás":      ["extração de petró"],
    "Minério de ferro":  ["minério de ferro", "minerais metál"],
    "Refino":            ["refino de petró", "coque"],
    "Metalurgia/sider.": ["siderurg", "metalurgia", "fabricação de aço"],
    "Celulose/papel":    ["celulose", "papel"],
}

def load_A(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["13"]
    rows = list(ws.iter_rows(min_row=7, max_row=74, max_col=72, values_only=True))
    wb.close()
    names = [str(r[2]).replace("\n", " ").strip() for r in rows]   # col C (idx 2)
    A = np.array([[num(r[c]) for c in range(4, 72)] for r in rows]) # cols 5-72 -> idx 4..71
    return names, A

def match_base(names):
    out = {}
    low = [nm.lower() for nm in names]
    for lab, keys in BASE_KEYS.items():
        for i, nm in enumerate(low):
            if any(k in nm for k in keys):
                out.setdefault(lab, i); break
    return out

files = sorted(glob.glob(os.path.join(DIR, "MIP-BR *.xlsm")))
years = [int(re.search(r"(20\d\d)", os.path.basename(f)).group(1)) for f in files]
traj = {}   # (lab) -> list of (year, mult_prod, backward)
base_map = None
for f, yr in zip(files, years):
    names, A = load_A(f)
    n = A.shape[0]
    if A.sum(0).max() >= 1:
        # raros coef>1 (ex. setores com forte importação) — Leontief ainda finita se raio espectral<1
        pass
    B = np.linalg.inv(np.eye(n) - A)
    mult = B.sum(0)
    backward = B.sum(0) / n / B.mean()
    if base_map is None:
        base_map = match_base(names)
        print("setores-base mapeados:")
        for lab, i in base_map.items(): print(f"  {lab:18s} -> [{i+1:2d}] {names[i]}")
        print("-"*72)
    for lab, i in base_map.items():
        traj.setdefault(lab, []).append((yr, mult[i], backward[i]))

print(f"{'setor':18s} | " + " ".join(f"{y:>6d}" for y in years))
print("MULTIPLICADOR DE PRODUÇÃO:")
for lab in BASE_KEYS:
    if lab in traj:
        vals = [m for _, m, _ in traj[lab]]
        print(f"  {lab:16s} | " + " ".join(f"{v:6.2f}" for v in vals))
print("LIGAÇÃO PARA TRÁS (Rasmussen-Hirschman):")
for lab in BASE_KEYS:
    if lab in traj:
        vals = [b for _, _, b in traj[lab]]
        print(f"  {lab:16s} | " + " ".join(f"{v:6.2f}" for v in vals))

with open(os.path.join(OUT, "trajetoria_n68.csv"), "w", newline="", encoding="utf-8") as fc:
    wr = csv.writer(fc); wr.writerow(["setor","ano","mult_producao","ligacao_tras"])
    for lab in traj:
        for yr, m, b in traj[lab]:
            wr.writerow([lab, yr, f"{m:.4f}", f"{b:.4f}"])
print("\nsalvo: trajetoria_n68.csv")
