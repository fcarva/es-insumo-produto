# -*- coding: utf-8 -*-
"""Figura para slides: o ES e as 'oncas brasileiras' (Apex Partners)."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "oncas_resumo.csv"), encoding="utf-8"))}
states = list(csv.DictReader(open(os.path.join(OUT, "oncas.csv"), encoding="utf-8")))

ONCAS = ["SC","PR","ES","MG","RS","GO","MT","MS"]; NUCLEO = ["SP","RJ"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
fig.suptitle('O Espírito Santo e as "onças brasileiras" (Apex Partners) — IO 2008',
             fontsize=13.5, fontweight="bold")

# painel 1 — destino do spillover do ES, reagrupado
labels = ["Núcleo\nSP+RJ\n(Faria Lima)", "Outras 7\nonças", "Resto\ndo Brasil"]
vals = [res["es_spill_nucleo"], res["es_spill_outras_oncas"], res["es_spill_resto"]]
cols = ["#c0392b", "#27ae60", "#95a5a6"]
bars = ax1.bar(labels, vals, color=cols, width=0.6)
for b, v in zip(bars, vals):
    ax1.text(b.get_x()+b.get_width()/2, v+1, f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold")
ax1.set_ylabel("% do spillover do ES")
ax1.set_title("Para onde escoa o encadeamento do ES", fontsize=11)
ax1.set_ylim(0, max(vals)*1.2)
ax1.spines[["top", "right"]].set_visible(False)
ax1.text(0.5, -0.34, "feedback de volta ao ES ≈ 0  →  encadeamento vai ao núcleo, valor não volta",
         transform=ax1.transAxes, ha="center", fontsize=8.5, color="#c0392b")

# painel 2 — abertura: oncas vs nucleo
rows = [(s["estado"], float(s["vazamento_%"])) for s in states
        if s["estado"] in ONCAS + NUCLEO]
rows.sort(key=lambda kv: kv[1])
ylab = [r[0] for r in rows]; yval = [r[1] for r in rows]
ycol = ["#c0392b" if r[0] in NUCLEO else "#27ae60" for r in rows]
ax2.barh(ylab, yval, color=ycol)
for i, v in enumerate(yval):
    ax2.text(v+0.3, i, f"{v:.1f}%", va="center", fontsize=8.5)
ax2.set_xlabel("vazamento médio do multiplicador (%)")
ax2.set_title("Abertura: onças (verde) vs núcleo SP/RJ (vermelho)", fontsize=10.5)
ax2.set_xlim(0, max(yval)*1.16)
ax2.spines[["top", "right"]].set_visible(False)

fig.text(0.5, 0.005,
         f"Onças = 33,9% do PIB em 2008 (Apex: 34%→39% 2002-2023) · bloco retém "
         f"{res['bloco_dentro']:.0f}% do próprio encadeamento · núcleo SP+RJ = 43,3% do PIB",
         ha="center", fontsize=8.5, color="#444")
fig.tight_layout(rect=[0, 0.05, 1, 0.94])
p = os.path.join(OUT, "es_oncas.png")
fig.savefig(p, dpi=150); print("figura salva:", p)
