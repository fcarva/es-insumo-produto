# -*- coding: utf-8 -*-
"""Figura: o ES e o cluster de estados dinâmicos (ex-núcleo) — tema Flexoki."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "cluster_resumo.csv"), encoding="utf-8"))}
states = list(csv.DictReader(open(os.path.join(OUT, "cluster.csv"), encoding="utf-8")))
CLUSTER = ["SC","PR","ES","MG","RS","GO","MT","MS"]; NUCLEO = ["SP","RJ"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
fig.suptitle("O Espírito Santo num cluster de estados dinâmicos (ex-núcleo SP/RJ)", fontsize=13)

# painel 1 — destino do spillover do ES
labels = ["Núcleo\nSP+RJ", "Resto do\ncluster", "Resto\ndo Brasil"]
vals = [res["es_spill_nucleo"], res["es_spill_cluster"], res["es_spill_resto"]]
ax1.bar(labels, vals, color=[st.C_NUCLEO, st.C_CLUSTER, st.C_RESTO_P], width=0.62)
for i, v in enumerate(vals):
    ax1.text(i, v+1, f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold", color=st.INK)
ax1.set_ylabel("% do spillover do ES"); ax1.set_title("Para onde escoa o encadeamento do ES", fontsize=11)
ax1.set_ylim(0, max(vals)*1.2); ax1.grid(axis="x", visible=False)
ax1.text(0.5, -0.32, "feedback de volta ao ES ≈ 0  →  encadeamento vai ao núcleo, valor não volta",
         transform=ax1.transAxes, ha="center", fontsize=8.5, color=st.C_ES)

# painel 2 — abertura: cluster vs núcleo (ES destacado)
rows = sorted([(s["estado"], float(s["vazamento_%"])) for s in states
               if s["estado"] in CLUSTER + NUCLEO], key=lambda kv: kv[1])
ylab = [r[0] for r in rows]; yval = [r[1] for r in rows]
def cor(uf): return st.C_ES if uf == "ES" else (st.C_NUCLEO if uf in NUCLEO else st.C_CLUSTER)
ax2.barh(ylab, yval, color=[cor(u) for u in ylab], height=0.72)
for i, (lab, v) in enumerate(zip(ylab, yval)):
    ax2.text(v+0.3, i, f"{v:.1f}%", va="center", fontsize=8.5,
             color=(st.C_ES if lab == "ES" else st.INK_SOFT),
             fontweight=("bold" if lab == "ES" else "normal"))
for t in ax2.get_yticklabels():
    if t.get_text() == "ES": t.set_fontweight("bold"); t.set_color(st.C_ES)
ax2.set_xlabel("vazamento médio do multiplicador (%)")
ax2.set_title("Abertura: cluster (verde) vs núcleo (azul) — ES em destaque", fontsize=10.5)
ax2.set_xlim(0, max(yval)*1.16); ax2.grid(axis="y", visible=False)

fig.text(0.5, 0.01, "Cluster = 8 estados de crescimento sub-cobertos pelo mercado de capitais "
         "(leitura Apex Partners) · cluster = 33,9% do PIB 2008", ha="center", fontsize=8.2, color=st.INK_SOFT)
fig.tight_layout(rect=[0, 0.05, 1, 0.94])
fig.savefig(os.path.join(OUT, "es_cluster.png"))
print("ok es_cluster.png")
