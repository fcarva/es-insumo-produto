# -*- coding: utf-8 -*-
"""
estilo.py — paleta e tema das figuras (Flexoki/Kepano: papel quente, pastéis,
minimalista). Importado pelos scripts de figura. Cores de Steph Ango (Flexoki).
"""
import matplotlib.pyplot as plt

# tons base
PAPER    = "#FFFCF0"   # (legado) papel quente — não mais usado como fundo
WHITE    = "#FFFFFF"   # base neutra p/ colormaps (célula sem dado = branco)
INK      = "#100F0F"
INK_SOFT = "#575653"
GRID     = "#E7E7E7"   # grid neutro e leve (boas práticas: reduzir chart junk)

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

# paleta SUAVE (padrão editorial Nexo): nó / fluxo / texto, por papel
NODE = {"ES": "#D7A99D", "NUC": "#8AAAC8", "CLU": "#A9B873", "RES": "#C7C5B8"}
FLOW = {"ES": "#ECD2CB", "NUC": "#CFDCEA", "CLU": "#DEE3C7", "RES": "#E6E4DB"}
TXT  = {"ES": "#9E4A3C", "NUC": "#3F6B97", "CLU": "#5E6B2E", "RES": "#8A887C"}


def nexo(fig, title, dek="", source="", x=0.045):
    """Título + dek (subtítulo) à esquerda e nota de fonte ao rodapé (estilo Nexo)."""
    fig.text(x, 0.965, title, fontsize=15.5, fontweight="bold", color=INK, ha="left", va="top")
    if dek:
        fig.text(x, 0.912, dek, fontsize=9.8, color=INK_SOFT, ha="left", va="top")
    if source:
        fig.text(x, 0.022, source, fontsize=7.8, color=INK_SOFT, ha="left", va="bottom")


def apply():
    plt.rcParams.update({
        # fundo TRANSPARENTE (sem cor): a figura mescla com a página do documento
        "figure.facecolor": "none", "axes.facecolor": "none",
        "savefig.facecolor": "none", "savefig.edgecolor": "none", "savefig.transparent": True,
        "axes.edgecolor": INK_SOFT, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": INK_SOFT, "ytick.color": INK_SOFT,
        "axes.spines.top": False, "axes.spines.right": False,
        # grid leve só no eixo y (reduz chart junk); fica atrás dos dados
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 13, "axes.titleweight": "bold", "figure.dpi": 150,
    })
