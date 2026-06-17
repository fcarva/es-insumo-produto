# -*- coding: utf-8 -*-
"""Figura para slides: o Espirito Santo e o cluster de estados dinamicos (ex-nucleo)."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "cluster_resumo.csv"), encoding="utf-8"))}
states = list(csv.DictReader(open(os.path.join(OUT, "cluster.csv"), encoding="utf-8")))

CLUSTER = ["SC","PR","ES","MG","RS","GO","MT","MS"]; NUCLEO = ["SP","RJ"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
fig.suptitle("O Espírito Santo num cluster de estados dinâmicos (ex-núcleo SP/RJ) — IO 2008",
             fontsize=13, fontweight="bold")

# painel 1 — destino do spillover do ES
labels = ["Núcleo\nSP+RJ", "Resto do\ncluster", "Resto\ndo Brasil"]
vals = [res["es_spill_nucleo"], res["es_spill_cluster"], res["es_spill_resto"]]
cols = ["#c0392b", "#27ae60", "#95a5a6"]
bars = ax1.bar(labels, vals, color=cols, width=0.6)
for b, v in zip(bars, vals):
    ax1.text(b.get_x()+b.get_width()/2, v+1, f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold")
ax1.set_ylabel("% do spillover do ES")
ax1.set_title("Para onde escoa o encadeamento do ES", fontsize=11)
ax1.set_ylim(0, max(vals)*1.2)
ax1.spines[["top", "right"]].set_visible(False)
ax1.text(0.5, -0.34, "feedback de volta ao ES ≈ 0  →  o encadeamento vai ao núcleo, o valor não volta",
         transform=ax1.transAxes, ha="center", fontsize=8.5, color="#c0392b")

# painel 2 — abertura: cluster vs nucleo (ES em destaque)
rows = [(s["estado"], float(s["vazamento_%"])) for s in states
        if s["estado"] in CLUSTER + NUCLEO]
rows.sort(key=lambda kv: kv[1])
ylab = [r[0] for r in rows]; yval = [r[1] for r in rows]
def color(r):
    if r == "ES": return "#145a32"          # ES destacado (verde escuro)
    return "#c0392b" if r in NUCLEO else "#27ae60"
ycol = [color(r) for r in ylab]
ax2.barh(ylab, yval, color=ycol)
for i, (lab, v) in enumerate(zip(ylab, yval)):
    ax2.text(v+0.3, i, f"{v:.1f}%", va="center",
             fontsize=8.5, fontweight=("bold" if lab == "ES" else "normal"))
for t in ax2.get_yticklabels():
    if t.get_text() == "ES": t.set_fontweight("bold")
ax2.set_xlabel("vazamento médio do multiplicador (%)")
ax2.set_title("Abertura: cluster (verde, ES escuro) vs núcleo (vermelho)", fontsize=10)
ax2.set_xlim(0, max(yval)*1.16)
ax2.spines[["top", "right"]].set_visible(False)

fig.text(0.5, 0.005,
         f"Cluster = 8 estados de crescimento acima da média e sub-cobertos pelo mercado de "
         f"capitais (leitura da Apex Partners) · cluster=33,9% do PIB 2008 · núcleo SP+RJ=43,3%",
         ha="center", fontsize=8.3, color="#444")
fig.tight_layout(rect=[0, 0.05, 1, 0.94])
p = os.path.join(OUT, "es_cluster.png")
fig.savefig(p, dpi=150); print("figura salva:", p)
