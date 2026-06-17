# -*- coding: utf-8 -*-
"""Figura A2: o ES preso a montante da cadeia (upstreamness, WIOD 2014)."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
BRASIL, MUNDO = 1.91, 2.31
rows = [r for r in csv.DictReader(open(os.path.join(OUT, "es_upstreamness.csv"), encoding="utf-8"))
        if r["setor_BR"] != "ES_PAUTA"]
es_up = float([r for r in csv.DictReader(open(os.path.join(OUT, "es_upstreamness.csv"), encoding="utf-8"))
               if r["setor_BR"] == "ES_PAUTA"][0]["upstreamness"])

rows.sort(key=lambda r: float(r["share_export_%"]), reverse=True)
top = rows[:8][::-1]
labels = [f'{r["setor_BR"]}' for r in top]
ups    = [float(r["upstreamness"]) for r in top]
shares = [float(r["share_export_%"]) for r in top]

fig, ax = plt.subplots(figsize=(9.6, 4.8))
maxsh = max(shares)
colors = [plt.cm.Reds(0.35 + 0.6*s/maxsh) for s in shares]
ax.barh(labels, ups, color=colors)
for i, (u, s) in enumerate(zip(ups, shares)):
    ax.text(u+0.03, i, f"U={u:.2f}  ·  {s:.0f}% da pauta", va="center", fontsize=8.5)

n = len(labels)
for x, lab, col, ls, yo in [(BRASIL, f"Brasil {BRASIL:.2f}".replace(".", ","), "#555", "--", -1.05),
                            (MUNDO, f"Mundo {MUNDO:.2f}".replace(".", ","), "#2c7fb8", "--", -0.35),
                            (es_up, f"Pauta ES {es_up:.2f}".replace(".", ","), "#c0392b", "-", -0.35)]:
    ax.axvline(x, color=col, linestyle=ls, linewidth=1.6)
    ax.text(x, n+yo, lab, color=col, fontsize=8.6, ha="center",
            fontweight="bold", backgroundcolor="white")

ax.set_xlabel("upstreamness (Antràs-Chor) — distância ao consumo final →")
ax.set_title("O Espírito Santo está preso a montante da cadeia (WIOD 2014)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, max(ups)*1.32)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.5, 0.005, "Pauta exportadora do ES ponderando a upstreamness setorial do Brasil "
         "(WIOD 2014). ES = 3,12 vs Brasil 1,91 vs Mundo 2,31. Mineração no percentil ~98 global.",
         ha="center", fontsize=8, color="#444")
fig.tight_layout(rect=[0, 0.04, 1, 1])
p = os.path.join(OUT, "es_upstreamness.png")
fig.savefig(p, dpi=150); print("figura salva:", p)
