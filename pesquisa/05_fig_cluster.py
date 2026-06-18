# -*- coding: utf-8 -*-
"""Figura: o ES no cluster de estados dinâmicos — padrão Nexo suave."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
res = {r["metrica"]: float(r["valor_pct"]) for r in
       csv.DictReader(open(os.path.join(OUT, "cluster_resumo.csv"), encoding="utf-8"))}
states = list(csv.DictReader(open(os.path.join(OUT, "cluster.csv"), encoding="utf-8")))
CLUSTER = ["SC", "PR", "ES", "MG", "RS", "GO", "MT", "MS"]; NUCLEO = ["SP", "RJ"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2))

# painel 1 — destino do spillover do ES
labels = ["Núcleo\nSP+RJ", "Resto do\ncluster", "Resto\ndo Brasil"]
vals = [res["es_spill_nucleo"], res["es_spill_cluster"], res["es_spill_resto"]]
ax1.bar(labels, vals, color=[st.NODE["NUC"], st.NODE["CLU"], st.NODE["RES"]], width=0.6)
for i, v in enumerate(vals):
    ax1.text(i, v+1, f"{v:.0f}%", ha="center", fontsize=11, fontweight="bold", color=st.INK)
ax1.set_title("Para onde escoa o encadeamento do ES", loc="left", fontsize=10.5, color=st.INK)
ax1.set_ylabel("% do spillover do ES"); ax1.set_ylim(0, max(vals)*1.2); ax1.grid(axis="x", visible=False)

# painel 2 — abertura: cluster vs núcleo (ES em destaque)
rows = sorted([(s["estado"], float(s["vazamento_%"])) for s in states
               if s["estado"] in CLUSTER + NUCLEO], key=lambda kv: kv[1])
ylab = [r[0] for r in rows]; yval = [r[1] for r in rows]
def papel(uf): return "ES" if uf == "ES" else ("NUC" if uf in NUCLEO else "CLU")
ax2.barh(ylab, yval, color=[st.NODE[papel(u)] for u in ylab], height=0.72)
for i, (lab, v) in enumerate(zip(ylab, yval)):
    ax2.text(v+0.3, i, f"{v:.1f}%", va="center", fontsize=8.4, color=st.TXT[papel(lab)],
             fontweight=("bold" if lab == "ES" else "normal"))
for t in ax2.get_yticklabels():
    if t.get_text() == "ES": t.set_fontweight("bold"); t.set_color(st.TXT["ES"])
ax2.set_title("Abertura: vazamento médio do multiplicador", loc="left", fontsize=10.5, color=st.INK)
ax2.set_xlabel("%"); ax2.set_xlim(0, max(yval)*1.16); ax2.grid(axis="y", visible=False)

st.nexo(fig, "No cluster de estados dinâmicos, o ES escoa metade ao núcleo SP/RJ",
        "Destino do spillover do ES e abertura comparada dos 8 estados do cluster · MIP inter-regional 2008",
        "Fonte: MIP inter-regional ES × Brasil (2008) · cluster = leitura de mercado da Apex Partners (33,9% do PIB) · "
        "vermelho = ES · azul = núcleo · verde = cluster · elaboração própria.")
fig.tight_layout(rect=[0, 0.06, 1, 0.84])
fig.savefig(os.path.join(OUT, "es_cluster.png"))
print("ok es_cluster.png")
