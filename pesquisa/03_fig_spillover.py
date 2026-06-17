# -*- coding: utf-8 -*-
"""Figura para slides: destino do spillover do ES (estados + macrorregiao)."""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
rows = list(csv.DictReader(open(os.path.join(OUT, "es_spillover_destino.csv"), encoding="utf-8")))
spill = {r["regiao"]: float(r["spillover_RS_mi"]) for r in rows}
total = sum(spill.values())

MACRO = {"Norte":["AC","AP","AM","PA","RO","RR","TO"],
         "Nordeste":["AL","BA","CE","MA","PB","PE","PI","SE","RN"],
         "Centro-Oeste":["DF","GO","MT","MS"],
         "Sudeste\n(ex-ES)":["MG","RJ","SP"], "Sul":["PR","SC","RS"]}
SUD = {"MG","RJ","SP"}

top = sorted(spill.items(), key=lambda kv: kv[1], reverse=True)[:10][::-1]
macro = [(m, sum(spill[u] for u in ufs)) for m, ufs in MACRO.items()]
macro.sort(key=lambda kv: kv[1])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
fig.suptitle("Para onde vaza o multiplicador do Espírito Santo (2008)",
             fontsize=14, fontweight="bold")

# painel 1 — estados
labels = [k for k, _ in top]
vals = [v/total*100 for _, v in top]
colors = ["#c0392b" if k in SUD else "#5d8aa8" for k in labels]
ax1.barh(labels, vals, color=colors)
for i, v in enumerate(vals):
    ax1.text(v+0.4, i, f"{v:.1f}%", va="center", fontsize=9)
ax1.set_xlabel("% do spillover total do ES")
ax1.set_title("Top destinos (estados)", fontsize=11)
ax1.set_xlim(0, max(vals)*1.18)
ax1.spines[["top", "right"]].set_visible(False)
ax1.text(0.98, 0.05, "vermelho = resto do Sudeste", transform=ax1.transAxes,
         ha="right", fontsize=8, color="#c0392b")

# painel 2 — macrorregiao
ml = [m for m, _ in macro]
mv = [v/total*100 for _, v in macro]
mc = ["#c0392b" if "Sudeste" in m else "#5d8aa8" for m in ml]
ax2.barh(ml, mv, color=mc)
for i, v in enumerate(mv):
    ax2.text(v+0.6, i, f"{v:.1f}%", va="center", fontsize=9)
ax2.set_xlabel("% do spillover total do ES")
ax2.set_title("Por macrorregião", fontsize=11)
ax2.set_xlim(0, max(mv)*1.18)
ax2.spines[["top", "right"]].set_visible(False)

fig.text(0.5, 0.005,
         "Injeção f(ES)=R\\$51,5 bi · spillover=R\\$18,1 bi (Sudeste ex-ES=65%) · "
         "retido+feedback no ES=77,9% · feedback de volta ≈0,3%",
         ha="center", fontsize=8.5, color="#444")
fig.tight_layout(rect=[0, 0.04, 1, 0.95])
p = os.path.join(OUT, "es_spillover_destino.png")
fig.savefig(p, dpi=150)
print("figura salva:", p)
