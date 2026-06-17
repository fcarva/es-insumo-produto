#!/usr/bin/env python3
# Figuras do deck: (1) fluxo spillover/feedback  (2) smile curve de CGV
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# Paleta
TEAL_D = "#0F3540"   # petróleo profundo
TEAL   = "#1C6E7E"   # teal médio
RUST   = "#C75B39"   # minério / spillover
INK    = "#1E2B30"
MUTE   = "#5B6B70"
PAPER  = "#FFFFFF"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "text.color": INK,
    "axes.edgecolor": MUTE,
})

# ---------------------------------------------------------------------------
# FIGURA 1 — Fluxo spillover / feedback (assimetria extrema)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")

def box(cx, cy, w, h, label, sub, facecolor, textcolor):
    b = FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.12",
                       linewidth=0, facecolor=facecolor, zorder=3)
    ax.add_patch(b)
    ax.text(cx, cy+0.32, label, ha="center", va="center",
            fontsize=20, fontweight="bold", color=textcolor, zorder=4)
    ax.text(cx, cy-0.42, sub, ha="center", va="center",
            fontsize=12.5, color=textcolor, zorder=4)

# Caixas
box(2.05, 2.6, 3.0, 1.7, "ESPÍRITO SANTO", "injeção na demanda final\nR$ 60,6 bi", TEAL_D, "#EAF3F4")
box(7.95, 2.6, 3.0, 1.7, "RESTANTE DO BRASIL", "produção puxada", "#21505C", "#EAF3F4")

# Seta spillover (grossa) ES -> BR
ax.annotate("", xy=(6.4, 3.3), xytext=(3.6, 3.3),
            arrowprops=dict(arrowstyle="-|>,head_width=1.25,head_length=1.05",
                            lw=33, color=RUST, shrinkA=0, shrinkB=0,
                            joinstyle="miter"), zorder=2)
ax.text(4.35, 4.32, "SPILLOVER", ha="center", fontsize=14.5,
        fontweight="bold", color=RUST, fontfamily="monospace")
ax.text(4.35, 3.92, "R$ 22,4 bi", ha="center", fontsize=17.5,
        fontweight="bold", color=RUST)

# Seta feedback (fininha) BR -> ES
ax.annotate("", xy=(3.7, 1.95), xytext=(6.3, 1.95),
            arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6",
                            lw=2.0, color=TEAL, shrinkA=0, shrinkB=0), zorder=2)
ax.text(5.0, 1.50, "feedback   R$ 199 mi  (0,26%)", ha="center",
        fontsize=12.5, color=TEAL)

ax.text(5.0, 0.52, "O estado puxa o país; o país quase não o puxa de volta.",
        ha="center", fontsize=13.5, style="italic", color=MUTE)

fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("figuras/spillover_feedback.png", dpi=200,
            facecolor=PAPER, bbox_inches="tight", pad_inches=0.12)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIGURA 2 — Smile curve (curva do sorriso) de valor agregado x estágio
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=200)
x = np.linspace(0, 10, 400)
# U suave (sorriso)
y = 0.045*(x-5)**2 + 1.9
ax.plot(x, y, color=TEAL_D, lw=4, zorder=2, solid_capstyle="round")

ax.set_xlim(-0.2, 10.2); ax.set_ylim(0.8, 5.4)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right", "left", "bottom"]:
    ax.spines[s].set_visible(False)

# Eixos rotulados
ax.annotate("", xy=(10.2, 1.0), xytext=(-0.2, 1.0),
            arrowprops=dict(arrowstyle="-|>", lw=1.6, color=MUTE))
ax.annotate("", xy=(-0.05, 5.3), xytext=(-0.05, 1.0),
            arrowprops=dict(arrowstyle="-|>", lw=1.6, color=MUTE))
ax.text(5.0, 0.55, "estágio na cadeia de valor  →", ha="center",
        fontsize=12.5, color=MUTE)
ax.text(-0.35, 3.15, "valor agregado", rotation=90, va="center",
        ha="center", fontsize=12.5, color=MUTE)

# Estágios
for xx, lab in [(0.7, "P&D · insumos\nprimários"),
                (5.0, "manufatura\n(montagem)"),
                (9.3, "marca · serviços\ndistribuição")]:
    ax.text(xx, 1.18, lab, ha="center", va="bottom",
            fontsize=11, color=MUTE)

# Posição do ES (upstream, alto upstreamness)
xe = 1.15
ye = 0.045*(xe-5)**2 + 1.9
ax.scatter([xe], [ye], s=320, color=RUST, zorder=5, edgecolor="white", linewidth=2)
ax.annotate("ES",
            xy=(xe, ye), xytext=(xe+0.15, ye+0.9),
            fontsize=15, fontweight="bold", color=RUST,
            arrowprops=dict(arrowstyle="-", color=RUST, lw=1.4))
ax.text(xe+0.15, ye+1.32, "upstreamness 3,19", fontsize=12, color=RUST, fontweight="bold")
ax.text(xe+0.15, ye+1.02, "mineração no percentil 98 global", fontsize=10.5, color=MUTE)

# Captura de valor a jusante
ax.scatter([9.3], [0.045*(9.3-5)**2 + 1.9], s=120, color=TEAL, zorder=5,
           edgecolor="white", linewidth=1.5)
ax.text(9.3, 0.045*(9.3-5)**2 + 1.9 + 0.45, "captura de valor\nocorre fora do estado",
        ha="center", fontsize=10.5, color=TEAL, style="italic")

# média Brasil de referência
ax.text(5.0, 4.9, "pauta capixaba 3,19   vs.   média Brasil 1,97",
        ha="center", fontsize=12.5, color=INK,
        bbox=dict(boxstyle="round,pad=0.4", fc="#EAF1F2", ec="none"))

fig.subplots_adjust(left=0.04, right=0.99, top=0.99, bottom=0.04)
fig.savefig("figuras/cgv_smile_curve.png", dpi=200,
            facecolor=PAPER, bbox_inches="tight", pad_inches=0.12)
plt.close(fig)

print("figuras geradas em figuras/")
