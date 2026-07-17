# -*- coding: utf-8 -*-
"""Figura: upstreamness da pauta do ES (WIOD 2014). Padrão editorial: sem título
embutido (legenda LaTeX assume), rótulos acentuados, vírgula decimal, PNG+PDF.
Barras ordenadas pelo peso na pauta exportadora do ES."""
import os, sys, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.colors import LinearSegmentedColormap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as st; st.apply()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
_res = {r["metrica"]: float(r["valor"]) for r in
        csv.DictReader(open(os.path.join(OUT, "upstream_resumo.csv"), encoding="utf-8"))}
BRASIL, MUNDO = _res["brasil_upstreamness"], _res["mundo_upstreamness"]
allrows = list(csv.DictReader(open(os.path.join(OUT, "es_upstreamness.csv"), encoding="utf-8")))
rows = [r for r in allrows if r["setor_BR"] != "ES_PAUTA"]
es_up = float([r for r in allrows if r["setor_BR"] == "ES_PAUTA"][0]["upstreamness"])

# nomes de exibição (o CSV guarda rótulos ASCII)
NOME = {"Mineracao": "Mineração", "Metalurgia": "Metalurgia", "Madeira/papel": "Madeira/papel",
        "Transp/armaz": "Transp./armaz.", "Comercio": "Comércio", "Agric/silvic": "Agric./silvic.",
        "Min nao-metal": "Min. não-metálicos", "Alimentos": "Alimentos",
        "Pecuaria/pesca": "Pecuária/pesca", "Quimicos": "Químicos", "Textil": "Têxtil"}

rows.sort(key=lambda r: float(r["share_export_%"]), reverse=True)
top = rows[:8][::-1]
labels = [NOME.get(r["setor_BR"], r["setor_BR"]) for r in top]
ups = [float(r["upstreamness"]) for r in top]
shares = [float(r["share_export_%"]) for r in top]

cmap = LinearSegmentedColormap.from_list("es_soft", ["#EDD9D3", st.NODE["ES"]])
maxsh = max(shares)
fig, ax = plt.subplots(figsize=(10, 5.2))
fig.subplots_adjust(left=0.155, right=0.975, top=0.90, bottom=0.11)
ax.barh(labels, ups, color=[cmap(0.3 + 0.7*s/maxsh) for s in shares], height=0.72, zorder=3)
for i, (u, s) in enumerate(zip(ups, shares)):
    ax.text(u+0.05, i, f"U={st.br(u, 2)} · {s:.0f}% da pauta", va="center", fontsize=8.4,
            color=st.INK_SOFT, zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.2))

# linhas de referência com rótulos ACIMA do quadro (não cruzam as anotações);
# Brasil à esquerda e Mundo à direita das respectivas linhas, p/ não colidirem
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
for x, lab, col, ls, ha, dx in [(BRASIL, f"Brasil {st.br(BRASIL, 2)}", st.TXT["RES"], "--", "right", -0.04),
                                (MUNDO,  f"Mundo {st.br(MUNDO, 2)}",  st.TXT["NUC"], "--", "left",  0.04),
                                (es_up,  f"Pauta ES {st.br(es_up, 2)}", st.TXT["ES"], "-", "left",  0.04)]:
    ax.axvline(x, color=col, linestyle=ls, linewidth=1.5, zorder=2)
    ax.text(x+dx, 1.025, lab, transform=trans, color=col, fontsize=8.6, ha=ha,
            va="bottom", fontweight="bold")

ax.set_xlabel("upstreamness (Antràs-Chor) — distância ao consumo final →")
ax.set_xlim(0, max(ups)*1.32)
ax.grid(axis="y", visible=False)
st.salvar(fig, OUT, "es_upstreamness")
