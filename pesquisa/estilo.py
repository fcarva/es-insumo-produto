# -*- coding: utf-8 -*-
"""
estilo.py — paleta e tema das figuras (Flexoki/Kepano: papel quente, pastéis,
minimalista). Importado pelos scripts de figura. Cores de Steph Ango (Flexoki).
"""
import matplotlib.pyplot as plt

# tons base
PAPER    = "#FFFCF0"   # papel quente
INK      = "#100F0F"
INK_SOFT = "#575653"
GRID     = "#E6E4D9"

# acentos (saturado / pastel)
RED,    RED_P    = "#AF3029", "#E3A99F"   # ES (protagonista)
BLUE,   BLUE_P   = "#4385BE", "#AEC8E0"   # núcleo SP/RJ
GREEN,  GREEN_P  = "#879A39", "#C9D2A1"   # cluster (pares)
YELLOW, YELLOW_P = "#D0A215", "#E8CF93"
CYAN,   CYAN_P   = "#3AA99F", "#AFD7D2"
GRAY,   GRAY_P   = "#B7B5AC", "#D6D4CA"   # resto

# papéis (consistência entre figuras)
C_ES, C_NUCLEO, C_CLUSTER, C_RESTO = RED, BLUE, GREEN, GRAY
C_ES_P, C_NUCLEO_P, C_CLUSTER_P, C_RESTO_P = RED_P, BLUE_P, GREEN_P, GRAY_P


def apply():
    plt.rcParams.update({
        "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
        "axes.edgecolor": INK_SOFT, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": INK_SOFT, "ytick.color": INK_SOFT,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 13, "axes.titleweight": "bold", "figure.dpi": 150,
    })
