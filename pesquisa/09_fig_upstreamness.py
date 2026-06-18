# -*- coding: utf-8 -*-
"""Figura: o ES preso a montante da cadeia (upstreamness, WIOD 2014) — padrão Nexo suave."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
_res = {r["metrica"]: float(r["valor"]) for r in
        csv.DictReader(open(os.path.join(OUT, "upstream_resumo.csv"), encoding="utf-8"))}
BRASIL, MUNDO, PCT = _res["brasil_upstreamness"], _res["mundo_upstreamness"], _res["mineracao_percentil"]
allrows = list(csv.DictReader(open(os.path.join(OUT, "es_upstreamness.csv"), encoding="utf-8")))
rows = [r for r in allrows if r["setor_BR"] != "ES_PAUTA"]
es_up = float([r for r in allrows if r["setor_BR"] == "ES_PAUTA"][0]["upstreamness"])

rows.sort(key=lambda r: float(r["share_export_%"]), reverse=True)
top = rows[:8][::-1]
labels = [r["setor_BR"] for r in top]
ups = [float(r["upstreamness"]) for r in top]
shares = [float(r["share_export_%"]) for r in top]

cmap = LinearSegmentedColormap.from_list("es_soft", ["#EDD9D3", st.NODE["ES"]])
maxsh = max(shares)
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.barh(labels, ups, color=[cmap(0.3 + 0.7*s/maxsh) for s in shares], height=0.72)
for i, (u, s) in enumerate(zip(ups, shares)):
    ax.text(u+0.03, i, f"U={u:.2f} · {s:.0f}% da pauta".replace(".", ","), va="center",
            fontsize=8.4, color=st.INK_SOFT)

n = len(labels)
for x, lab, col, ls, yo in [(BRASIL, f"Brasil {BRASIL:.2f}".replace(".", ","), st.TXT["RES"], "--", -1.05),
                            (MUNDO, f"Mundo {MUNDO:.2f}".replace(".", ","), st.TXT["NUC"], "--", -0.35),
                            (es_up, f"Pauta ES {es_up:.2f}".replace(".", ","), st.TXT["ES"], "-", -0.35)]:
    ax.axvline(x, color=col, linestyle=ls, linewidth=1.7)
    ax.text(x, n+yo, lab, color=col, fontsize=8.6, ha="center", fontweight="bold", backgroundcolor=st.PAPER)

ax.set_xlabel("upstreamness (Antràs-Chor) — distância ao consumo final →")
ax.set_xlim(0, max(ups)*1.32); ax.grid(axis="y", visible=False)
st.nexo(fig, "O Espírito Santo está preso a montante da cadeia de valor",
        f"Upstreamness da pauta exportadora capixaba ({es_up:.2f}) ante Brasil ({BRASIL:.2f}) e mundo ({MUNDO:.2f}) · WIOD 2014".replace(".", ","),
        f"Fonte: WIOD 2014 (índice de Antràs-Chor), ponderado pela pauta de exportação do ES · mineração no percentil ~{PCT:.0f} global · elaboração própria.")
fig.tight_layout(rect=[0, 0.06, 1, 0.84])
fig.savefig(os.path.join(OUT, "es_upstreamness.png"))
print("ok es_upstreamness.png")
