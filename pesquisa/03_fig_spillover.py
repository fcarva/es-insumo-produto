# -*- coding: utf-8 -*-
"""Figura: destino do spillover do ES (estados + macrorregião) — tema Flexoki."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
rows = list(csv.DictReader(open(os.path.join(OUT, "es_spillover_destino.csv"), encoding="utf-8")))
spill = {r["regiao"]: float(r["spillover_RS_mi"]) for r in rows}
total = sum(spill.values())

NUCLEO = {"SP", "RJ"}; CLUSTER = {"MG", "SC", "PR", "RS", "GO", "MT", "MS"}
def cor(uf):
    if uf in NUCLEO: return st.C_NUCLEO
    if uf in CLUSTER: return st.C_CLUSTER
    return st.C_RESTO_P
MACRO = {"Norte": ["AC","AP","AM","PA","RO","RR","TO"],
         "Nordeste": ["AL","BA","CE","MA","PB","PE","PI","SE","RN"],
         "Centro-Oeste": ["DF","GO","MT","MS"], "Sudeste\n(ex-ES)": ["MG","RJ","SP"],
         "Sul": ["PR","SC","RS"]}

top = sorted(spill.items(), key=lambda kv: kv[1], reverse=True)[:10][::-1]
macro = sorted([(m, sum(spill[u] for u in ufs)) for m, ufs in MACRO.items()], key=lambda kv: kv[1])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
fig.suptitle("Para onde vaza o multiplicador do Espírito Santo (2008)", fontsize=14)

labels = [k for k, _ in top]; vals = [v/total*100 for _, v in top]
ax1.barh(labels, vals, color=[cor(k) for k in labels], height=0.74)
for i, v in enumerate(vals):
    ax1.text(v+0.4, i, f"{v:.1f}%", va="center", fontsize=8.5, color=st.INK_SOFT)
ax1.set_xlabel("% do spillover do ES"); ax1.set_title("Top destinos (estados)", fontsize=11)
ax1.set_xlim(0, max(vals)*1.16); ax1.grid(axis="y", visible=False)

ml = [m for m, _ in macro]; mv = [v/total*100 for _, v in macro]
mc = [st.C_NUCLEO if "Sudeste" in m else (st.C_CLUSTER if m == "Sul" else st.C_RESTO_P) for m in ml]
ax2.barh(ml, mv, color=mc, height=0.66)
for i, v in enumerate(mv):
    ax2.text(v+0.6, i, f"{v:.1f}%", va="center", fontsize=8.5, color=st.INK_SOFT)
ax2.set_xlabel("% do spillover do ES"); ax2.set_title("Por macrorregião", fontsize=11)
ax2.set_xlim(0, max(mv)*1.16); ax2.grid(axis="y", visible=False)

fig.text(0.5, 0.01, "Sudeste (ex-ES) absorve 65% do spillover · feedback de volta ao ES ≈ 0,3%",
         ha="center", fontsize=8.6, color=st.C_NUCLEO)
fig.tight_layout(rect=[0, 0.04, 1, 0.95])
fig.savefig(os.path.join(OUT, "es_spillover_destino.png"))
print("ok es_spillover_destino.png")
