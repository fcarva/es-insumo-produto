# -*- coding: utf-8 -*-
"""
02_interestadual.py — matriz INTERESTADUAL (27 UFs x 26 setores, 2008).
Responde: para ONDE vaza o multiplicador/encadeamento do ES (por estado e
macrorregiao) e como o ES se compara aos demais estados em abertura.

Fonte: Material IO/MIP-26x26-BR-2008.xlsx (aba 'BR', R$ milhoes)
Layout: Z linhas/cols (excel) 5-706 (702=27x26); demanda final cols 707-868
(27 reg x 6 cat); VALOR DA PRODUCAO = linha 730; Pessoal Ocupado = linha 731.
Ordem das regioes (linhas e colunas), ES = indice 20:
"""
import os, csv
import numpy as np
import pandas as pd

P   = r"C:/Users/DELL/Downloads/Material IO/MIP-26x26-BR-2008.xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
os.makedirs(OUT, exist_ok=True)

REG = ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI",
       "SE","RN","DF","GO","MT","MS","ES","MG","RJ","SP","PR","SC","RS"]
ES = REG.index("ES")  # 20
MACRO = {
 "Norte":["AC","AP","AM","PA","RO","RR","TO"],
 "Nordeste":["AL","BA","CE","MA","PB","PE","PI","SE","RN"],
 "Centro-Oeste":["DF","GO","MT","MS"],
 "Sudeste":["MG","RJ","SP"],            # Sudeste exceto ES
 "Sul":["PR","SC","RS"]}

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z   = to(df.iloc[4:706, 3:705].values)      # 702 x 702
x   = to(df.iloc[729, 3:705].values)        # VALOR DA PRODUCAO
emp = to(df.iloc[730, 3:705].values)        # Pessoal Ocupado
FD  = to(df.iloc[4:706, 706:868].values)    # 702 x 162 (27 x 6)
N = 702

def rseg(g):  return slice(26*g, 26*g+26)   # linhas/cols do estado g
def fdseg(g): return slice(6*g, 6*g+6)      # colunas de demanda final do estado g

xs = np.where(x == 0, 1.0, x)
A = Z / xs[None, :]
B = np.linalg.inv(np.eye(N) - A)
assert A.sum(0).max() < 1, "coef. tecnico >=1"

def by_region(vec):
    return np.array([vec[rseg(g)].sum() for g in range(27)])

# --------------------------------------------------------------------------- #
# (a) DESTINO DO SPILLOVER do ES (Miller-Blair: demanda final do ES por ES)
# --------------------------------------------------------------------------- #
f = np.zeros(N)
esr = np.arange(26*ES, 26*ES+26)
f[esr] = FD[esr, fdseg(ES)].sum(axis=1)     # demanda final do ES por produtos do ES
xf = B @ f
prod_reg = by_region(xf)
inj = f.sum()
retido = prod_reg[ES]
spill = prod_reg.copy(); spill[ES] = 0.0
spill_total = spill.sum()

# (b) PEGADA TOTAL: demanda final TOTAL do ES (todas as origens)
f2 = FD[:, fdseg(ES)].sum(axis=1)
xf2 = B @ f2
prod_reg2 = by_region(xf2)

# --------------------------------------------------------------------------- #
# (c) ABERTURA por estado: vazamento medio do multiplicador de producao
# --------------------------------------------------------------------------- #
leak_state = np.zeros(27)
for g in range(27):
    cols = np.arange(26*g, 26*g+26)
    O = B[:, cols].sum(axis=0)
    O_in = B[rseg(g), :][:, cols].sum(axis=0)
    lk = 1 - O_in / np.where(O == 0, 1, O)
    wts = x[cols] / x[cols].sum()
    leak_state[g] = float((lk * wts).sum())   # ponderado pela producao

# --------------------------------------------------------------------------- #
def br(v): return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
print("="*68)
print("MATRIZ INTERESTADUAL 27-UF (2008) — PARA ONDE VAZA O ES")
print("="*68)
print(f"dim={N}  ΣA max={A.sum(0).max():.3f}  B>=0:{bool((B>=-1e-9).all())}")
print("-"*68)
print("[a] DESTINO DO SPILLOVER  (injecao demanda final ES->produtos ES)")
print(f"    Injecao f^ES                : R$ {br(inj)} mi")
print(f"    Retido+feedback no ES       : R$ {br(retido)} mi ({retido/xf.sum():.1%} da prod. total)")
print(f"    Spillover (fora do ES)      : R$ {br(spill_total)} mi")
print("    Top destinos do spillover:")
for g in np.argsort(spill)[::-1][:8]:
    print(f"      {REG[g]:3s}  R$ {br(spill[g]):>10s} mi  ({spill[g]/spill_total:5.1%} do spillover)")
print("    Por macrorregiao (exclui ES):")
idx = {r:i for i,r in enumerate(REG)}
for mr, ufs in MACRO.items():
    s = sum(spill[idx[u]] for u in ufs)
    print(f"      {mr:13s} R$ {br(s):>10s} mi  ({s/spill_total:5.1%})")
print("-"*68)
print("[b] PEGADA DA DEMANDA FINAL TOTAL DO ES (todas as origens)")
print(f"    Injecao total ES            : R$ {br(f2.sum())} mi")
print(f"    Producao no ES              : {prod_reg2[ES]/xf2.sum():.1%} | fora do ES: {1-prod_reg2[ES]/xf2.sum():.1%}")
print("-"*68)
print("[c] ABERTURA (vazamento medio do mult. de producao) — ranking")
order = np.argsort(leak_state)[::-1]
rank_es = list(order).index(ES) + 1
for k,g in enumerate(order[:6],1):
    print(f"      {k:2d}. {REG[g]:3s} {leak_state[g]:5.1%}")
print(f"      ... ES em {rank_es}o/27  ({leak_state[ES]:.1%})  | menos aberto: {REG[order[-1]]} {leak_state[order[-1]]:.1%}")
print("="*68)

# --------------------------------------------------------------------------- #
with open(os.path.join(OUT, "es_spillover_destino.csv"), "w", newline="", encoding="utf-8") as fcsv:
    wr = csv.writer(fcsv); wr.writerow(["regiao","spillover_RS_mi","pct_spillover","pegada_total_RS_mi"])
    for g in range(27):
        if g == ES: continue
        wr.writerow([REG[g], f"{spill[g]:.1f}", f"{spill[g]/spill_total*100:.2f}", f"{prod_reg2[g]:.1f}"])
with open(os.path.join(OUT, "estados_abertura.csv"), "w", newline="", encoding="utf-8") as fcsv:
    wr = csv.writer(fcsv); wr.writerow(["regiao","vazamento_medio_pct","rank"])
    for k,g in enumerate(order,1):
        wr.writerow([REG[g], f"{leak_state[g]*100:.2f}", k])
print("salvos: es_spillover_destino.csv, estados_abertura.csv")
