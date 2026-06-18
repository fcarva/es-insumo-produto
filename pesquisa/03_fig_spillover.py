# -*- coding: utf-8 -*-
"""Figura: destino do spillover do ES (estados + macrorregião) — padrão Nexo suave."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import estilo as st; st.apply()

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
spill = {r["regiao"]: float(r["spillover_RS_mi"]) for r in
         csv.DictReader(open(os.path.join(OUT, "es_spillover_destino.csv"), encoding="utf-8"))}
total = sum(spill.values())
NUCLEO = {"SP", "RJ"}; CLUSTER = {"MG", "SC", "PR", "RS", "GO", "MT", "MS"}
def role(uf): return "NUC" if uf in NUCLEO else ("CLU" if uf in CLUSTER else "RES")
MACRO = {"Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
         "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "SE", "RN"],
         "Centro-Oeste": ["DF", "GO", "MT", "MS"], "Sudeste (ex-ES)": ["MG", "RJ", "SP"],
         "Sul": ["PR", "SC", "RS"]}
MROLE = {"Sudeste (ex-ES)": "NUC", "Sul": "CLU", "Nordeste": "RES", "Centro-Oeste": "RES", "Norte": "RES"}

top = sorted(spill.items(), key=lambda kv: kv[1], reverse=True)[:10][::-1]
macro = sorted([(m, sum(spill[u] for u in ufs)) for m, ufs in MACRO.items()], key=lambda kv: kv[1])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2))
labels = [k for k, _ in top]; vals = [v/total*100 for _, v in top]
ax1.barh(labels, vals, color=[st.NODE[role(k)] for k in labels], height=0.72)
for i, (k, v) in enumerate(zip(labels, vals)):
    ax1.text(v+0.5, i, f"{v:.0f}%", va="center", fontsize=8.6, color=st.TXT[role(k)])
ax1.set_title("Por estado", loc="left", fontsize=10.5, color=st.INK)
ax1.set_xlabel("% do spillover do ES"); ax1.set_xlim(0, max(vals)*1.16); ax1.grid(axis="y", visible=False)

ml = [m for m, _ in macro]; mv = [v/total*100 for _, v in macro]
ax2.barh(ml, mv, color=[st.NODE[MROLE[m]] for m in ml], height=0.6)
for i, (m, v) in enumerate(zip(ml, mv)):
    ax2.text(v+0.7, i, f"{v:.0f}%", va="center", fontsize=8.6, color=st.TXT[MROLE[m]])
ax2.set_title("Por macrorregião", loc="left", fontsize=10.5, color=st.INK)
ax2.set_xlabel("% do spillover do ES"); ax2.set_xlim(0, max(mv)*1.16); ax2.grid(axis="y", visible=False)

st.nexo(fig, "O Sudeste absorve dois terços do que vaza do Espírito Santo",
        "Destino do spillover de produção do ES, por estado e macrorregião · MIP inter-regional 2008",
        "Fonte: MIP inter-regional ES × Brasil (2008), modelo de Isard · elaboração própria. "
        "Azul = núcleo SP/RJ · verde = cluster · cinza = resto.")
fig.tight_layout(rect=[0, 0.06, 1, 0.84])
fig.savefig(os.path.join(OUT, "es_spillover_destino.png"))
print("ok es_spillover_destino.png")
