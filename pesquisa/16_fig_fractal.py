# -*- coding: utf-8 -*-
"""
16_fig_fractal.py — figuras do flagship RQ-A+RQ-B (estilo Flexoki/Nexo).
Fig 1 (fractal): razao de feedback ~ porte em DUAS escalas (27 UFs | 10 microrregioes ES)
                 -> mesma inclinacao = invariancia de escala.
Fig 2 (periferia->metropole): vazamento por microrregiao do ES + % do spillover que vai a R1.
Le: outputs/benchmark_ufs.csv, outputs/intra_es_fractal.csv.
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import estilo
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
FIG = r"C:/Users/DELL/Documents/es-insumo-produto/figuras"
estilo.apply()

uf = pd.read_csv(os.path.join(OUT, "benchmark_ufs.csv"))
mi = pd.read_csv(os.path.join(OUT, "intra_es_fractal.csv"))
NUCLEO = {"SP","RJ"}; CLUSTER = {"SC","PR","ES","MG","RS","GO","MT","MS"}

def fitline(x, y):
    b = np.polyfit(x, y, 1); xs = np.linspace(x.min(), x.max(), 50)
    r2 = 1 - ((y-np.polyval(b,x))**2).sum()/((y-y.mean())**2).sum()
    return xs, np.polyval(b, xs), r2

# ----------------------------- FIG 1: FRACTAL ------------------------------- #
fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5.2))
fig.subplots_adjust(left=0.065, right=0.975, top=0.80, bottom=0.13, wspace=0.22)

# painel esquerdo: 27 UFs
x1 = np.log(uf["producao_mi"].values); y1 = uf["feedback_razao"].values*100
for _, r in uf.iterrows():
    # boas práticas: destacar só a história (ES vermelho, núcleo azul) e acinzentar o resto
    c = estilo.C_NUCLEO if r.UF in NUCLEO else (estilo.C_ES if r.UF=="ES" else estilo.C_RESTO)
    sz = 90 if r.UF=="ES" else (60 if r.UF in NUCLEO else 34)
    axL.scatter(np.log(r.producao_mi), r.feedback_razao*100, s=sz, color=c,
                zorder=3, edgecolor=estilo.PAPER, linewidth=0.6)
xs, ys, r2 = fitline(x1, y1); axL.plot(xs, ys, color=estilo.INK_SOFT, lw=1.3, ls="--", zorder=2)
_off = {"ES":(5,5), "SP":(-6,3), "RJ":(5,-2), "MT":(2,-12)}
_ha  = {"ES":"left","SP":"right","RJ":"left","MT":"left"}
for lab in ("ES","SP","RJ","MT"):
    r = uf[uf.UF==lab].iloc[0]
    axL.annotate(lab, (np.log(r.producao_mi), r.feedback_razao*100), fontsize=8.5,
                 color=estilo.INK, xytext=_off[lab], ha=_ha[lab], textcoords="offset points", fontweight="bold")
axL.set_title(f"Escala nacional · 27 UFs (2008)", fontsize=11)
axL.set_xlabel("log da produção do estado"); axL.set_ylabel("razão de feedback  (%)")
axL.text(0.97, 0.05, f"R²={r2:.2f}", transform=axL.transAxes, ha="right", color=estilo.INK_SOFT, fontsize=9)

# painel direito: 10 microrregioes ES
mi2 = mi.copy()
# reconstruir producao absoluta a partir do share (so para o eixo log)
x2 = np.log(mi2["share_prod_pct"].values); y2 = mi2["feedback_razao"].values*100
for _, r in mi2.iterrows():
    metro = bool(r.is_metropole)
    c = estilo.C_NUCLEO if metro else (estilo.C_ES if r.nome=="Litoral Sul" else estilo.C_RESTO)
    sz = 90 if metro else (70 if r.nome in ("Litoral Sul","Rio Doce") else 38)
    axR.scatter(np.log(r.share_prod_pct), r.feedback_razao*100, s=sz, color=c,
                zorder=3, edgecolor=estilo.PAPER, linewidth=0.6)
xs, ys, r2b = fitline(x2, y2); axR.plot(xs, ys, color=estilo.INK_SOFT, lw=1.3, ls="--", zorder=2)
_offR = {"Metropolitana":(-6,3,"right"), "Rio Doce":(5,3,"left"), "Litoral Sul":(5,4,"left")}
for nm in ("Metropolitana","Rio Doce","Litoral Sul"):
    r = mi2[mi2.nome==nm].iloc[0]; dx,dy,ha = _offR[nm]
    axR.annotate(nm.split()[0], (np.log(r.share_prod_pct), r.feedback_razao*100), fontsize=8.5,
                 color=estilo.INK, xytext=(dx,dy), ha=ha, textcoords="offset points", fontweight="bold")
axR.set_xlim(axR.get_xlim()[0], axR.get_xlim()[1]+0.35)
axR.set_title("Escala intra-ES · 10 microrregiões (2015)", fontsize=11)
axR.set_xlabel("log do share de produção na microrregião"); axR.set_ylabel("razão de feedback  (%)")
axR.text(0.97, 0.05, f"R²={r2b:.2f}", transform=axR.transAxes, ha="right", color=estilo.INK_SOFT, fontsize=9)

estilo.nexo(fig, "A economia-plataforma em escalas aninhadas",
    "O feedback inter-regional cresce com o porte da unidade — a MESMA regularidade governa estados dentro do Brasil e microrregiões dentro do ES.",
    "Fonte: MIP interestadual 27-UF (2008) e sistema inter-regional das microrregiões do ES (2015). Razão de feedback = retorno/injeção (Miller-Blair, inversa particionada).")
fig.savefig(os.path.join(OUT, "fig_fractal.png"), dpi=160)
fig.savefig(os.path.join(FIG, "fractal_duas_escalas.png"), dpi=160)
print("salvo: fig_fractal.png  (R2 nac.={:.2f} / intra-ES={:.2f})".format(r2, r2b))

# ------------------ FIG 2: PERIFERIA -> METROPOLE (intra-ES) ----------------- #
fig2, ax = plt.subplots(figsize=(9.6, 5.4))
fig2.subplots_adjust(left=0.30, right=0.93, top=0.80, bottom=0.12)
d = mi2[mi2.is_metropole==0].copy().sort_values("vazamento")
labels = [f"R{int(r.regiao[1:])} {r.nome}" for _, r in d.iterrows()]
ypos = np.arange(len(d))
cols = [estilo.C_ES if n=="Litoral Sul" else (estilo.C_CLUSTER if n=="Rio Doce" else estilo.C_RESTO)
        for n in d.nome]
ax.barh(ypos, d.vazamento.values*100, color=cols, edgecolor=estilo.PAPER, height=0.7, zorder=3)
ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=9)
for i, (_, r) in enumerate(d.iterrows()):
    ax.text(r.vazamento*100+0.4, i, f"{r.vazamento*100:.0f}%  →metrópole {r.pct_para_metropole:.0f}%",
            va="center", fontsize=8.2, color=estilo.INK_SOFT)
ax.set_xlabel("vazamento do multiplicador de produção  (%)")
ax.set_xlim(0, 42); ax.set_yticks(ypos)
estilo.nexo(fig2, "A periferia capixaba é a “plataforma” do ES",
    "Cada microrregião vaza encadeamento, e o destino é a Metropolitana (Grande Vitória) — o “núcleo” do ES.",
    "Fonte: sistema inter-regional das microrregiões do ES (2015). Vazamento = parcela do multiplicador realizada fora da própria microrregião.")
fig2.savefig(os.path.join(OUT, "fig_periferia_metropole.png"), dpi=160)
print("salvo: fig_periferia_metropole.png")
