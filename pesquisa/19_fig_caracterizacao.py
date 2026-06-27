# -*- coding: utf-8 -*-
"""
19_fig_caracterizacao.py — figuras da caracterização (estilo Flexoki/Nexo).
Fig 1 (mapa de ligações, ES 2008): para-trás x para-frente dos 26 setores; quadrante
       superior-direito = setores-chave. Fig 2 (trajetória, 2010-2021): ligação para
       trás dos setores-base do ES na estrutura nacional (Nível 68).
Le: outputs/es_caracterizacao_2008.csv, outputs/trajetoria_n68.csv.
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__)); import estilo
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
FIG = r"C:/Users/DELL/Documents/es-insumo-produto/figuras"
estilo.apply()

# ---------------- FIG 1: mapa de ligações ES 2008 ----------------
d = pd.read_csv(os.path.join(OUT, "es_caracterizacao_2008.csv"))
fig, ax = plt.subplots(figsize=(9.8, 6.2))
fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.10)
for _, r in d.iterrows():
    key = r.chave_RH == 1
    c = estilo.C_ES if key else estilo.C_RESTO
    ax.scatter(r.lig_tras, r.lig_frente, s=90 if key else 45, color=c, zorder=3,
               edgecolor=estilo.PAPER, linewidth=0.6)
ax.axhline(1, color=estilo.INK_SOFT, lw=0.9, ls="--"); ax.axvline(1, color=estilo.INK_SOFT, lw=0.9, ls="--")
# rotular setores-chave + alguns notáveis
notar = ["Mineração","Metalurgia","Refino de petróleo, coque e álcool","Madeira, papel e impressão",
         "Alimentos, bebidas e fumo","Cimento e outros produtos de minerais não-metálicos","Agricultura, silvicultura, exploração florestal"]
for _, r in d.iterrows():
    if r.setor in notar:
        nm = r.setor.split(",")[0].split(" e ")[0][:16]
        ax.annotate(nm, (r.lig_tras, r.lig_frente), fontsize=8, color=estilo.INK,
                    xytext=(4,3), textcoords="offset points", fontweight="bold")
ax.text(0.985, 0.97, "SETORES-CHAVE", transform=ax.transAxes, ha="right", va="top",
        fontsize=9, color=estilo.TXT["ES"], fontweight="bold")
ax.set_xlabel("ligação para trás (poder de dispersão)")
ax.set_ylabel("ligação para frente (sensibilidade de dispersão)")
estilo.nexo(fig, "Setores-chave da economia capixaba (2008)",
    "Cada ponto é um setor do ES. Acima de 1 nos dois eixos (vermelho) = setor-chave: puxa e é puxado acima da média.",
    "Fonte: MIP-ES-BR (2008), 17_caracterizacao_es_2008.py. Para-trás: inversa de Leontief; para-frente: inversa de Ghosh.")
fig.savefig(os.path.join(OUT, "fig_setores_chave.png"), dpi=160)
fig.savefig(os.path.join(FIG, "es_setores_chave.png"), dpi=160)
print("salvo: fig_setores_chave.png")

# ---------------- FIG 2: trajetória 2010-2021 ----------------
t = pd.read_csv(os.path.join(OUT, "trajetoria_n68.csv"))
fig2, ax2 = plt.subplots(figsize=(10.2, 5.6))
fig2.subplots_adjust(left=0.08, right=0.82, top=0.80, bottom=0.12)
cores = {"Celulose/papel":estilo.C_CLUSTER, "Metalurgia/sider.":estilo.C_ES,
         "Refino":estilo.YELLOW, "Petróleo/gás":estilo.C_NUCLEO, "Minério de ferro":estilo.CYAN}
for lab, g in t.groupby("setor"):
    g = g.sort_values("ano")
    ax2.plot(g.ano, g.ligacao_tras, "-o", ms=4, lw=1.8, color=cores.get(lab, estilo.GRAY), label=lab, zorder=3)
    ax2.annotate(lab, (g.ano.iloc[-1], g.ligacao_tras.iloc[-1]), fontsize=8.3,
                 color=cores.get(lab, estilo.GRAY), xytext=(6,0), textcoords="offset points", va="center", fontweight="bold")
ax2.axhline(1, color=estilo.INK_SOFT, lw=0.9, ls="--")
ax2.text(2010.05, 1.02, "limiar de setor-chave (=1)", fontsize=7.5, color=estilo.INK_SOFT)
for yr, lab in [(2015,"Fundão"), (2020,"COVID")]:
    ax2.axvline(yr, color=estilo.GRAY, lw=0.8, ls=":")
    ax2.text(yr, ax2.get_ylim()[0], f" {lab}", fontsize=7.5, color=estilo.INK_SOFT, rotation=90, va="bottom")
ax2.set_xlabel("ano"); ax2.set_ylabel("ligação para trás (Rasmussen-Hirschman)")
ax2.set_xticks(range(2010, 2022, 2))
estilo.nexo(fig2, "A base capixaba na estrutura nacional (2010–2021)",
    "Celulose e siderurgia são setores-chave (>1); a extração de petróleo e de minério é enclave de baixa ligação doméstica (<1).",
    "Fonte: série nacional Nível 68 (NEREUS/CECEG), 18_trajetoria_n68.py.")
fig2.savefig(os.path.join(OUT, "fig_trajetoria_n68.png"), dpi=160)
fig2.savefig(os.path.join(FIG, "es_trajetoria_n68.png"), dpi=160)
print("salvo: fig_trajetoria_n68.png")
