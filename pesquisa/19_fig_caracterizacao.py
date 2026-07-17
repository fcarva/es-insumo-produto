# -*- coding: utf-8 -*-
"""
19_fig_caracterizacao.py — figuras da caracterização (padrão editorial: sem título
embutido — a legenda LaTeX assume; vírgula decimal; PNG 300 dpi + PDF vetorial).
Fig 1 (mapa de ligações, ES 2008): para-trás x para-frente dos 26 setores; quadrante
       superior-direito = setores-chave (todos rotulados). Fig 2 (trajetória,
       2010-2021): ligação para trás dos setores-base do ES na estrutura nacional.
Le: outputs/es_caracterizacao_2008.csv, outputs/trajetoria_n68.csv.
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import estilo
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
estilo.apply()

# ---------------- FIG 1: mapa de ligações ES 2008 ----------------
d = pd.read_csv(os.path.join(OUT, "es_caracterizacao_2008.csv"))
fig, ax = plt.subplots(figsize=(9.8, 6.4))
fig.subplots_adjust(left=0.085, right=0.965, top=0.96, bottom=0.10)
for _, r in d.iterrows():
    key = r.chave_RH == 1
    c = estilo.C_ES if key else estilo.C_RESTO
    ax.scatter(r.lig_tras, r.lig_frente, s=90 if key else 45, color=c, zorder=3,
               edgecolor=estilo.WHITE, linewidth=0.6)
ax.axhline(1, color=estilo.INK_SOFT, lw=0.9, ls="--"); ax.axvline(1, color=estilo.INK_SOFT, lw=0.9, ls="--")

# rótulos: TODOS os setores-chave + notáveis; offsets manuais anti-colisão
rotulos = {  # setor -> (nome curto, dx pt, dy pt, ha)
    "Refino de petróleo, coque e álcool":                    ("Refino",          6,  2, "left"),
    "Outros produtos químicos e farmacêuticos":              ("Químicos",        6,  0, "left"),
    "Artigos de borracha e plástico":                        ("Borracha/plást.", 6,  0, "left"),
    "Cimento e outros produtos de minerais não-metálicos":   ("Cimento",         0,-12, "center"),
    "Metalurgia":                                            ("Metalurgia",     -6,  2, "right"),
    "Material elétrico e eletrônicos":                       ("Mat. elétrico",  -4,  7, "right"),
    "Material de transporte":                                ("Mat. transporte", 6, -7, "left"),
    "Eletricidade e gás, água, esgoto e limpeza urbana":     ("Eletricidade",    6,  2, "left"),
    "Mineração":                                             ("Mineração",       0,  8, "center"),
    "Agricultura, silvicultura, exploração florestal":       ("Agricultura",     4,-10, "left"),
    "Alimentos, bebidas e fumo":                             ("Alimentos",      -7, -1, "right"),
    "Madeira, papel e impressão":                            ("Madeira/papel",   6, -2, "left"),
}
for _, r in d.iterrows():
    if r.setor in rotulos:
        nm, dx, dy, ha = rotulos[r.setor]
        ax.annotate(nm, (r.lig_tras, r.lig_frente), fontsize=8, color=estilo.INK,
                    xytext=(dx, dy), ha=ha, textcoords="offset points", fontweight="bold")

# rótulos de quadrante (cantos, discretos)
ax.text(0.985, 0.975, "setores-chave", transform=ax.transAxes, ha="right", va="top",
        fontsize=9, color=estilo.TXT["ES"], fontweight="bold")
ax.text(0.015, 0.975, "fornecedores (fortes para a frente)", transform=ax.transAxes,
        ha="left", va="top", fontsize=8, color=estilo.INK_SOFT, style="italic")
ax.text(0.985, 0.025, "demandantes (fortes para trás)", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8, color=estilo.INK_SOFT, style="italic")
ax.text(0.015, 0.025, "ligações fracas", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=8, color=estilo.INK_SOFT, style="italic")

ax.set_xlim(0.60, 1.36)
ax.xaxis.set_major_formatter(estilo.eixo_virgula(1))
ax.yaxis.set_major_formatter(estilo.eixo_virgula(1))
ax.set_xlabel("ligação para trás (poder de dispersão)")
ax.set_ylabel("ligação para frente (sensibilidade de dispersão)")
estilo.salvar(fig, OUT, "fig_setores_chave")

# ---------------- FIG 2: trajetória 2010-2021 ----------------
t = pd.read_csv(os.path.join(OUT, "trajetoria_n68.csv"))
fig2, ax2 = plt.subplots(figsize=(10.2, 5.6))
fig2.subplots_adjust(left=0.075, right=0.82, top=0.96, bottom=0.09)
cores = {"Celulose/papel":estilo.C_CLUSTER, "Metalurgia/sider.":estilo.C_ES,
         "Refino":estilo.YELLOW, "Petróleo/gás":estilo.C_NUCLEO, "Minério de ferro":estilo.CYAN}
# offsets verticais dos rótulos de fim de linha (pt), anti-colisão Minério x Petróleo
off_fim = {"Celulose/papel": 0, "Refino": 2, "Metalurgia/sider.": -2,
           "Minério de ferro": 6, "Petróleo/gás": -6}
for lab, g in t.groupby("setor"):
    g = g.sort_values("ano")
    ax2.plot(g.ano, g.ligacao_tras, "-o", ms=4, lw=1.8, color=cores.get(lab, estilo.GRAY), label=lab, zorder=3)
    ax2.annotate(lab, (g.ano.iloc[-1], g.ligacao_tras.iloc[-1]), fontsize=8.3,
                 color=cores.get(lab, estilo.GRAY), xytext=(6, off_fim.get(lab, 0)),
                 textcoords="offset points", va="center", fontweight="bold")
ax2.axhline(1, color=estilo.INK_SOFT, lw=0.9, ls="--")
ax2.text(2010.05, 1.02, "limiar de setor-chave (=1)", fontsize=7.5, color=estilo.INK_SOFT)
for yr, lab in [(2015,"Fundão"), (2020,"COVID")]:
    ax2.axvline(yr, color=estilo.GRAY, lw=0.8, ls=":")
    ax2.text(yr, ax2.get_ylim()[0]+0.005, f" {lab}", fontsize=7.5, color=estilo.INK_SOFT,
             rotation=90, va="bottom")
ax2.set_ylabel("ligação para trás (Rasmussen-Hirschman)")
ax2.set_xticks(range(2010, 2022, 2))
ax2.yaxis.set_major_formatter(estilo.eixo_virgula(1))
estilo.salvar(fig2, OUT, "fig_trajetoria_n68")
