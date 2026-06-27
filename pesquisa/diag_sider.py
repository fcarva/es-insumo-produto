# -*- coding: utf-8 -*-
"""Diagnose the 2021 siderurgia drop: classification break vs real shift."""
import sys, warnings, numpy as np, openpyxl
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DIR = r"C:/Users/DELL/Downloads/Material IO/Matrizes/Nível 68/Nível 68"
num = lambda v: float(v) if isinstance(v,(int,float)) else 0.0

def load(yr):
    wb = openpyxl.load_workbook(f"{DIR}/MIP-BR {yr} (Nível 68).xlsm", read_only=True, data_only=True)
    ws = wb["13"]; rows = list(ws.iter_rows(min_row=7, max_row=74, max_col=72, values_only=True))
    wb.close()
    names = [str(r[2]).replace("\n"," ").strip() for r in rows]
    codes = [str(r[1]).strip() for r in rows]
    A = np.array([[num(r[c]) for c in range(4,72)] for r in rows])
    return codes, names, A

for yr in (2019, 2020, 2021):
    codes, names, A = load(yr)
    n = A.shape[0]; B = np.linalg.inv(np.eye(n)-A)
    back = B.sum(0)/n/B.mean()
    i = 26  # 0-based index 27 = siderurgia (per script 18)
    print(f"\n=== {yr} === n={n}  ΣA_max={A.sum(0).max():.3f}  ΣA_mean={A.sum(0).mean():.3f}")
    for k in range(24, 30):
        tag = " <-- [27] usado p/ siderurgia" if k==i else ""
        print(f"  idx{k+1:2d} cod={codes[k]:6s} ΣAcol={A.sum(0)[k]:.3f} mult={B.sum(0)[k]:.2f} back={back[k]:.2f}  {names[k][:46]}{tag}")
# checar se a lista de codigos é idêntica entre 2020 e 2021
c19,_,_=load(2019); c20,_,_=load(2020); c21,_,_=load(2021)
print("\ncódigos idênticos 2019==2020?", c19==c20, " | 2020==2021?", c20==c21)
if c20!=c21:
    diff=[(k,c20[k],c21[k]) for k in range(len(c20)) if c20[k]!=c21[k]]
    print("  diferenças 2020->2021:", diff[:10])
