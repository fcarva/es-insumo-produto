# -*- coding: utf-8 -*-
"""
11_fig_sankey.py — Sankey (custom matplotlib, tema Flexoki) do encadeamento que
a demanda final do ES coloca em movimento: retido no ES vs vazado para o núcleo
SP+RJ, resto do cluster e resto do Brasil. Feedback de volta ≈ 0.
"""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "cluster_resumo.csv"), encoding="utf-8"))}
SPILL, RETIDO = res["es_spill_total_mi"], res["es_retido_mi"]   # R$ mi, lidos do CSV
nuc = SPILL*res["es_spill_nucleo"]/100
clu = SPILL*res["es_spill_cluster"]/100
rst = SPILL*res["es_spill_resto"]/100
items = [("Retido no ES", RETIDO, st.C_ES, st.RED_P),
         ("Núcleo SP+RJ", nuc, st.C_NUCLEO, st.BLUE_P),
         ("Resto do cluster", clu, st.C_CLUSTER, st.GREEN_P),
         ("Resto do Brasil", rst, st.C_RESTO, st.GRAY_P)]
T = sum(v for _, v, _, _ in items)
gap = 0.035*T
x0a, x0b, x1a, x1b = 0.03, 0.11, 0.78, 0.86

def ribbon(ax, s_top, s_bot, t_top, t_bot, color, alpha=0.55):
    xm = (x0b+x1a)/2
    verts = [(x0b, s_top), (xm, s_top), (xm, t_top), (x1a, t_top),
             (x1a, t_bot), (xm, t_bot), (xm, s_bot), (x0b, s_bot), (x0b, s_top)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    ax.add_patch(patches.PathPatch(Path(verts, codes), facecolor=color, edgecolor="none", alpha=alpha))

fig, ax = plt.subplots(figsize=(9.8, 5.4))
s_top = T; src = []
for _, v, _, _ in items:
    src.append((s_top, s_top-v)); s_top -= v
t_top = T; tgt = []
for _, v, _, _ in items:
    tgt.append((t_top, t_top-v)); t_top -= v + gap

for (name, v, c, cp), (sa, sb), (ta, tb) in zip(items, src, tgt):
    ribbon(ax, sa, sb, ta, tb, cp)
    ax.add_patch(patches.Rectangle((x1a, tb), x1b-x1a, ta-tb, color=c))      # nó destino
    ax.text(x1b+0.015, (ta+tb)/2, f"{name}\nR$ {v/1000:.1f} bi · {v/T*100:.0f}%",
            va="center", fontsize=9, color=st.INK)
# nó fonte
ax.add_patch(patches.Rectangle((x0a, 0), x0b-x0a, T, color=st.INK_SOFT))
ax.text(x0a-0.01, T/2, f"Produção puxada\npela demanda\nfinal do ES\n(R$ {T/1000:.1f} bi)".replace(".", ","),
        va="center", ha="right", fontsize=9.5, color=st.INK, fontweight="bold")

# feedback ~ 0
ax.annotate("feedback de volta ao ES ≈ 0,3%", xy=(x0b+0.02, T*0.02), xytext=(0.40, -gap*2.1),
            fontsize=9, color=st.C_ES, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=st.C_ES, lw=1.4,
                            connectionstyle="arc3,rad=0.35"))

ax.set_title("O encadeamento do ES vai ao núcleo — e o valor não volta (MIP inter-regional 2008)",
             fontsize=12.5)
ax.set_xlim(-0.12, 1.18); ax.set_ylim(tgt[-1][1]-0.04*T, T*1.04); ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "es_sankey.png"))
print("ok es_sankey.png")
