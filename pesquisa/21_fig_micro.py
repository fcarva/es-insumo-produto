# -*- coding: utf-8 -*-
"""
21_fig_micro.py — figura C3: mapa de VOCAÇÃO das microrregiões do ES (2015).
Heatmap de quociente locacional (LQ): linhas = 10 microrregiões (por porte),
colunas = setores que definem vocação. LQ>1 (vermelho) = especializado.
Le: outputs/micro_LQ.csv.
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
sys.path.insert(0, os.path.dirname(__file__)); import estilo
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
FIG = r"C:/Users/DELL/Documents/es-insumo-produto/figuras"
estilo.apply()

lq = pd.read_csv(os.path.join(OUT, "micro_LQ.csv"), index_col=0)   # 35 setores x 10 micro
# ordem das microrregioes por porte (da caracterizacao_micro): R1,R7,R5,R9,R8,R4,R10,R6,R3,R2
ordem_reg = ["Metropolitana","Rio Doce","Central Sul","Nordeste","Centro-Oeste",
             "Litoral Sul","Noroeste","Caparaó","Sudoeste Serrana","Central Serrana"]
# setores que definem vocacao (colunas)
setores = ["Extr. petróleo e gás","Extr. minério de ferro","Celulose e papel","Metalurgia",
           "Minerais não-metálicos","Têxtil/vestuário","Alimentos e bebidas","Agricultura",
           "Pecuária","Comércio"]
M = lq.loc[setores, ordem_reg].T.values        # 10 micro x 10 setores
Mc = np.clip(M, 0, 6)                          # capa LQ em 6 p/ a escala de cor

cmap = LinearSegmentedColormap.from_list("flex", [estilo.WHITE, estilo.RED_P, estilo.RED])
fig, ax = plt.subplots(figsize=(11.2, 6.2))
fig.subplots_adjust(left=0.16, right=0.99, top=0.78, bottom=0.30)
im = ax.imshow(Mc, cmap=cmap, vmin=0, vmax=6, aspect="auto")
ax.set_xticks(range(len(setores))); ax.set_xticklabels(setores, rotation=40, ha="right", fontsize=8.5)
ax.set_yticks(range(len(ordem_reg))); ax.set_yticklabels(ordem_reg, fontsize=9)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        if v >= 1.3:
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=7.6,
                    color=estilo.PAPER if v > 3 else estilo.INK, fontweight="bold")
ax.set_xticks(np.arange(-.5, len(setores), 1), minor=True)
ax.set_yticks(np.arange(-.5, len(ordem_reg), 1), minor=True)
ax.grid(which="minor", color=estilo.WHITE, linewidth=2); ax.tick_params(which="minor", length=0)
ax.set_facecolor(estilo.WHITE)   # base branca p/ as células de LQ baixo (sem dado = branco)
cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("quociente locacional (LQ)", fontsize=8)
estilo.nexo(fig, "A vocação econômica das microrregiões do ES (2015)",
    "Quociente locacional por setor: vermelho = o território concentra aquele setor acima da média estadual. Cada microrregião tem sua especialidade.",
    "Fonte: sistema inter-regional das microrregiões do ES (2015), 20_caracterizacao_micro.py. LQ capado em 6 na escala de cor.")
fig.savefig(os.path.join(OUT, "fig_micro_vocacao.png"), dpi=160)
fig.savefig(os.path.join(FIG, "es_micro_vocacao.png"), dpi=160)
print("salvo: fig_micro_vocacao.png")
