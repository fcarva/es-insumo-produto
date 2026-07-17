# -*- coding: utf-8 -*-
"""
11_fig_sankey.py — Sankey ESTRATIFICADO do destino do spillover do ES, por
macrorregião e estado, com rótulos coloridos por papel (núcleo SP/RJ=azul,
cluster=verde, resto=cinza). Padrão editorial: sem título/contexto embutidos —
a legenda LaTeX assume (injeção/spillover/feedback na convenção fechada).
Todos os "$" são escapados (\\$) para evitar o modo matemático do matplotlib.
"""
import os, sys, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as st; st.apply()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
spill = {r["regiao"]: float(r["spillover_RS_mi"]) for r in
         csv.DictReader(open(os.path.join(OUT, "es_spillover_destino.csv"), encoding="utf-8"))}
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "cluster_resumo.csv"), encoding="utf-8"))}
RETIDO, SPILL_TOT = res["es_retido_mi"], res["es_spill_total_mi"]
TOTAL = RETIDO + SPILL_TOT

MACROS = {"Sudeste": ["MG", "RJ", "SP"], "Sul": ["PR", "SC", "RS"],
          "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "SE", "RN"],
          "Centro-Oeste": ["DF", "GO", "MT", "MS"], "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"]}
mtot = {m: sum(spill[u] for u in ufs) for m, ufs in MACROS.items()}

# paleta Flexoki suave (nó / fluxo / texto) por papel
NODE = {"ES": "#D7A99D", "NUC": "#8AAAC8", "CLU": "#A9B873", "RES": "#C7C5B8"}
FLOW = {"ES": "#ECD2CB", "NUC": "#CFDCEA", "CLU": "#DEE3C7", "RES": "#E6E4DB"}
TXT  = {"ES": "#9E4A3C", "NUC": "#3F6B97", "CLU": "#5E6B2E", "RES": "#8A887C"}
MROLE = {"Sudeste": "NUC", "Sul": "CLU", "Nordeste": "RES", "Centro-Oeste": "RES", "Norte": "RES"}

def money(v): return "R\\$ " + f"{v/1000:.1f}".replace(".", ",") + " bi"

L1 = [(m, mtot[m], MROLE[m]) for m in ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]]
children = {
 "Sudeste": [("SP", spill["SP"], "NUC"), ("RJ", spill["RJ"], "NUC"), ("MG", spill["MG"], "CLU")],
 "Sul": [("PR", spill["PR"], "CLU"), ("RS", spill["RS"], "CLU"), ("SC", spill["SC"], "CLU")],
 "Nordeste": [("BA", spill["BA"], "RES"), ("demais NE", mtot["Nordeste"]-spill["BA"], "RES")],
 "Centro-Oeste": [("GO", spill["GO"], "CLU"), ("demais CO", mtot["Centro-Oeste"]-spill["GO"], "RES")],
 "Norte": [("Norte (7 UFs)", mtot["Norte"], "RES")]}

fig, axm = plt.subplots(figsize=(11.5, 7.0))
fig.subplots_adjust(left=0.045, right=0.86, top=0.98, bottom=0.02)

# ---- Sankey do spillover ----
T = SPILL_TOT
g1, g2 = 0.050 * T, 0.016 * T   # respiro entre macrorregiões e entre estados
xS, xL1, xL2 = (0.0, 0.035), (0.30, 0.335), (0.64, 0.675)

def ribbon(x0, x1, sa, sb, ta, tb, color, alpha=0.85):
    xm = (x0 + x1) / 2
    v = [(x0, sa), (xm, sa), (xm, ta), (x1, ta), (x1, tb), (xm, tb), (xm, sb), (x0, sb), (x0, sa)]
    c = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.LINETO,
         Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    axm.add_patch(patches.PathPatch(Path(v, c), facecolor=color, edgecolor="none", alpha=alpha))

y = T; L1pos = {}; SRC = {}
for nm, val, r in L1: L1pos[nm] = (y, y - val); y -= val + g1
y = T
for nm, val, r in L1: SRC[nm] = (y, y - val); y -= val
y = T; L2pos = {}
for nm, val, r in L1:
    chs = children[nm]
    for i, (cn, cv, cr) in enumerate(chs):
        L2pos[cn] = (y, y - cv); y -= cv + (g2 if i < len(chs)-1 else 0)
    y -= g1

for nm, val, r in L1:
    ribbon(xS[1], xL1[0], *SRC[nm], *L1pos[nm], FLOW[r])
for nm, val, r in L1:
    top = L1pos[nm][0]
    for cn, cv, cr in children[nm]:
        ribbon(xL1[1], xL2[0], top, top - cv, *L2pos[cn], FLOW[cr]); top -= cv

axm.add_patch(patches.Rectangle((xS[0], 0), xS[1]-xS[0], T, color=st.INK_SOFT))
axm.text(xS[0]-0.01, T/2, f"Spillover\ndo ES\n{money(T)}", va="center", ha="right",
         fontsize=10, color=st.INK, fontweight="bold")
for nm, val, r in L1:
    a, b = L1pos[nm]
    axm.add_patch(patches.Rectangle((xL1[0], b), xL1[1]-xL1[0], a-b, color=NODE[r]))
    axm.text(xL1[0]-0.01, (a+b)/2, f"{nm}\n{money(val)} · {val/T*100:.0f}%",
             ha="right", va="center", fontsize=8.6, color=TXT[r], linespacing=1.3)
for nm, val, r in L1:
    for cn, cv, cr in children[nm]:
        a, b = L2pos[cn]
        axm.add_patch(patches.Rectangle((xL2[0], b), xL2[1]-xL2[0], a-b, color=NODE[cr]))
        axm.text(xL2[1]+0.014, (a+b)/2, f"{cn}   {money(cv)} · {cv/T*100:.0f}%",
                 va="center", fontsize=8.8, color=TXT[cr])

axm.set_xlim(-0.16, 1.02)
axm.set_ylim(min(b for a, b in L2pos.values()) - 0.04*T, T + 0.04*T)
axm.axis("off")
st.salvar(fig, OUT, "es_sankey")
