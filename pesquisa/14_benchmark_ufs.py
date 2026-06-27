# -*- coding: utf-8 -*-
"""
14_benchmark_ufs.py — RQ-B: MODELO NULO / BENCHMARK das 27 UFs (2008).
Responde ao parecer (R1/DA-1): "feedback~0 e vazamento alto sao especificos do ES
ou genericos de regiao pequena-aberta?".

Para cada UF computa: vazamento medio do mult. de producao; razao de FEEDBACK
(inversa particionada de Miller-Blair, UF=L vs resto=M); CONCENTRACAO de destino do
spillover (HHI sobre as outras 26 UFs); porte (log da producao). Depois ajusta um
MODELO NULO (cada metrica ~ porte) e le o RESIDUO do ES — separa o generico (nivel de
feedback/vazamento, explicado por porte) do especifico-ES (concentracao de destino).

Fonte: Material IO/MIP-26x26-BR-2008.xlsx (aba 'BR'). Mesmo layout de 02_interestadual.py.
"""
import os, csv, sys
import numpy as np
import pandas as pd
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

P   = r"C:/Users/DELL/Downloads/Material IO/MIP-26x26-BR-2008.xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
os.makedirs(OUT, exist_ok=True)

REG = ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI",
       "SE","RN","DF","GO","MT","MS","ES","MG","RJ","SP","PR","SC","RS"]
ES = REG.index("ES")
CLUSTER = ["SC","PR","ES","MG","RS","GO","MT","MS"]   # leitura Apex (estados dinamicos)
NUCLEO  = ["SP","RJ"]

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z  = to(df.iloc[4:706, 3:705].values)       # 702 x 702
x  = to(df.iloc[729, 3:705].values)         # VALOR DA PRODUCAO
FD = to(df.iloc[4:706, 706:868].values)     # 702 x 162 (27 x 6)
N = 702
rseg  = lambda g: slice(26*g, 26*g+26)
fdseg = lambda g: slice(6*g, 6*g+6)

xs = np.where(x == 0, 1.0, x)
A = Z / xs[None, :]
B = np.linalg.inv(np.eye(N) - A)
assert A.sum(0).max() < 1, "coef tecnico >=1"

prod_uf = np.array([x[rseg(g)].sum() for g in range(27)])
share   = prod_uf / prod_uf.sum()

# --- por UF: vazamento, feedback (particionado), HHI de destino do spillover ---
leak = np.zeros(27); feed = np.zeros(27); hhi = np.zeros(27)
dest_nucleo = np.zeros(27)  # % do spillover que vai ao nucleo SP+RJ
idx = {r:i for i,r in enumerate(REG)}

for g in range(27):
    Lc = np.arange(26*g, 26*g+26)
    Mc = np.array([i for i in range(N) if i not in set(Lc.tolist())])
    # vazamento medio (ponderado pela producao) do multiplicador de producao
    O    = B[:, Lc].sum(axis=0)
    O_in = B[np.ix_(Lc, Lc)].sum(axis=0)
    lk = 1 - O_in / np.where(O == 0, 1, O)
    w  = x[Lc] / x[Lc].sum()
    leak[g] = float((lk * w).sum())
    # feedback de Miller-Blair (inversa particionada), UF=L vs resto=M
    A_LL = A[np.ix_(Lc, Lc)]; A_LM = A[np.ix_(Lc, Mc)]
    A_ML = A[np.ix_(Mc, Lc)]; A_MM = A[np.ix_(Mc, Mc)]
    inv_MM   = np.linalg.inv(np.eye(Mc.size) - A_MM)
    inv_LL   = np.linalg.inv(np.eye(26) - A_LL)
    inv_feed = np.linalg.inv(np.eye(26) - A_LL - A_LM @ inv_MM @ A_ML)
    yL = FD[Lc, fdseg(g)].sum(axis=1)          # demanda final da UF por seus produtos
    xL_closed = inv_LL @ yL; xL_full = inv_feed @ yL
    inj = float(yL.sum())
    feed[g] = (float(xL_full.sum() - xL_closed.sum()) / inj) if inj else 0.0
    # destino do spillover -> agregacao por UF -> HHI
    xM = inv_MM @ A_ML @ xL_full
    spill_by_reg = np.zeros(27)
    pos = 0
    for h in range(27):
        if h == g: continue
        spill_by_reg[h] = xM[pos:pos+26].sum(); pos += 26
    tot = spill_by_reg.sum()
    sh = spill_by_reg / (tot if tot else 1)
    hhi[g] = float((sh**2).sum())              # HHI da concentracao de destino
    dest_nucleo[g] = float(sum(sh[idx[u]] for u in NUCLEO))

# ----------------------------- MODELO NULO ---------------------------------- #
logsz = np.log(prod_uf)
def nullfit(y):
    X = np.column_stack([np.ones(27), logsz])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    ss_res = (resid**2).sum(); ss_tot = ((y - y.mean())**2).sum()
    r2 = 1 - ss_res/ss_tot
    return beta, yhat, resid, r2

bl, lhat, lres, lr2 = nullfit(leak)
bf, fhat, fres, fr2 = nullfit(feed)
bh, hhat, hres, hr2 = nullfit(hhi)

def br(v): return f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".")
print("="*72)
print("RQ-B — BENCHMARK 27 UFs (2008): especifico-ES x generico (regiao peq-aberta)")
print("="*72)
print(f"dim={N}  SigmaA max={A.sum(0).max():.3f}")
print("-"*72)
print("MODELO NULO  metrica ~ a + b*log(producao)   [R2 = quanto o PORTE explica]")
print(f"  vazamento         : b={bl[1]:+.4f}  R2={lr2:.2f}   (porte MAIOR -> {'menos' if bl[1]<0 else 'mais'} vazamento)")
print(f"  feedback (razao)  : b={bf[1]:+.5f}  R2={fr2:.2f}   (porte MAIOR -> {'mais' if bf[1]>0 else 'menos'} feedback)")
print(f"  HHI de destino    : b={bh[1]:+.5f}  R2={hr2:.2f}   (porte explica a concentracao? )")
print("-"*72)
print("ONDE O ES CAI (residuo = observado - previsto pelo porte):")
print(f"  vazamento : obs {leak[ES]:.1%}  prev {lhat[ES]:.1%}  resid {lres[ES]:+.1%}   -> {'GENERICO' if abs(lres[ES])<lres.std() else 'ESPECIFICO'}")
print(f"  feedback  : obs {feed[ES]:.2%}  prev {fhat[ES]:.2%}  resid {fres[ES]:+.2%}   -> {'GENERICO' if abs(fres[ES])<fres.std() else 'ESPECIFICO'}")
print(f"  HHI dest. : obs {hhi[ES]:.3f}  prev {hhat[ES]:.3f}  resid {hres[ES]:+.3f}  -> {'GENERICO' if abs(hres[ES])<hres.std() else 'ESPECIFICO'}")
print(f"  (destino ao nucleo SP+RJ: ES = {dest_nucleo[ES]:.1%})")
print("-"*72)
# z-scores do ES em cada dimensao
for nm, v in [("vazamento",leak),("feedback",feed),("HHI_destino",hhi)]:
    z = (v[ES]-v.mean())/v.std()
    print(f"  z-score ES em {nm:12s}: {z:+.2f}  (rank {sorted(v,reverse=True).index(v[ES])+1}/27)")
print("-"*72)
print("CLUSTER (estados dinamicos) x NUCLEO — assinatura media:")
ci = [idx[u] for u in CLUSTER]; ni = [idx[u] for u in NUCLEO]
print(f"  cluster: vaz {leak[ci].mean():.1%}  feed {feed[ci].mean():.2%}  HHI {hhi[ci].mean():.3f}")
print(f"  nucleo : vaz {leak[ni].mean():.1%}  feed {feed[ni].mean():.2%}  HHI {hhi[ni].mean():.3f}")
print("="*72)

with open(os.path.join(OUT, "benchmark_ufs.csv"), "w", newline="", encoding="utf-8") as fcsv:
    wr = csv.writer(fcsv)
    wr.writerow(["UF","producao_mi","share_pct","vazamento","feedback_razao","HHI_destino",
                 "dest_nucleo_pct","resid_vazamento","resid_feedback","resid_HHI"])
    for g in range(27):
        wr.writerow([REG[g], f"{prod_uf[g]:.1f}", f"{share[g]*100:.2f}", f"{leak[g]:.4f}",
                     f"{feed[g]:.5f}", f"{hhi[g]:.4f}", f"{dest_nucleo[g]*100:.1f}",
                     f"{lres[g]:.4f}", f"{fres[g]:.5f}", f"{hres[g]:.4f}"])
print("salvo: benchmark_ufs.csv")
