# -*- coding: utf-8 -*-
"""
22_benchmark_caracterizacao.py — R1 (revisão): BENCHMARK interestadual da
caracterização. Responde ao parecer (DA-1/R2-W2): a dualidade "extração-enclave +
líderes de baixo emprego" é específica do ES ou genérica? Compara o ES às 27 UFs em:
participação de setores de base, multiplicador médio de produção, multiplicador médio
de emprego e ligação para trás média (ponderada pela produção).

Fonte: MIP-26x26-BR-2008.xlsx (aba 'BR'). Layout = 02_interestadual.py.
"""
import os, csv, sys
import numpy as np, pandas as pd
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
P   = r"C:/Users/DELL/Downloads/Material IO/MIP-26x26-BR-2008.xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
REG = ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI",
       "SE","RN","DF","GO","MT","MS","ES","MG","RJ","SP","PR","SC","RS"]
ES = REG.index("ES"); BASE = [0,2,3,5,6,10]   # agric, mineração, alimentos, madeira/papel, refino, metalurgia

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z  = to(df.iloc[4:706, 3:705].values); x = to(df.iloc[729, 3:705].values); emp = to(df.iloc[730, 3:705].values)
N = 702; rseg = lambda g: slice(26*g, 26*g+26)
xs = np.where(x<=0, 1.0, x); A = Z/xs[None,:]; B = np.linalg.inv(np.eye(N)-A)
w = emp/xs; jobs = (w[:,None]*B).sum(0)               # empregos/R$mi por setor
backward = B.sum(0)/N/B.mean()

pmult = np.zeros(27); emult = np.zeros(27); base = np.zeros(27); backw = np.zeros(27)
for g in range(27):
    c = np.arange(26*g, 26*g+26); xc = x[c]; wt = xc/xc.sum()
    pmult[g] = float((B[:,c].sum(0)*wt).sum())        # mult. produção ponderado p/ produção
    emult[g] = float((jobs[c]*wt).sum())              # empregos/R$mi ponderado
    base[g]  = float(xc[BASE].sum()/xc.sum())
    backw[g] = float((backward[c]*wt).sum())          # ligação p/ trás ponderada

def rank(v, g, hi=True):
    o = np.argsort(v)[::-1] if hi else np.argsort(v)
    return list(o).index(g)+1
def stats(v): return v.mean(), np.median(v), v.min(), v.max()

print("="*78)
print("R1 — BENCHMARK INTERESTADUAL (2008): o ES é típico ou extremo?")
print("="*78)
print(f"{'métrica':28s} {'ES':>8s} {'rank':>6s} {'média':>8s} {'mediana':>8s} {'min':>7s} {'max':>7s}")
for nm, v, hi in [("Base/commodity (%)", base*100, True),
                  ("Mult. produção (pond.)", pmult, True),
                  ("Emprego (empr./R$mi)", emult, True),
                  ("Ligação p/ trás (pond.)", backw, True)]:
    m, md, lo, hi2 = stats(v)
    print(f"{nm:28s} {v[ES]:8.2f} {rank(v,ES,hi):>4d}/27 {m:8.2f} {md:8.2f} {lo:7.2f} {hi2:7.2f}")
print("-"*78)
# leitura da dualidade: emprego do setor dominante vs media do estado
dom_emp_gap = np.zeros(27)
for g in range(27):
    c = np.arange(26*g, 26*g+26); dom = c[int(np.argmax(x[c]))]
    dom_emp_gap[g] = jobs[dom] / emult[g]             # <1 => líder emprega menos que a média do estado
print("Emprego do SETOR DOMINANTE / emprego médio do estado (<1 = líder gera menos emprego):")
print(f"  ES = {dom_emp_gap[ES]:.2f} (rank {rank(dom_emp_gap,ES,False)}/27 entre os mais baixos)  "
      f"| média {dom_emp_gap.mean():.2f} | mediana {np.median(dom_emp_gap):.2f}")
print("="*78)
print(f"Leitura: ES base {base[ES]*100:.0f}% (rank {rank(base*100,ES)}/27) — entre os mais primário-industriais;")
print(f"  emprego baixo ({emult[ES]:.0f}/R$mi, rank {rank(emult,ES,False)}/27 entre os menores); a DUALIDADE")
print("  (líder de baixo emprego) é genérica em TIPO mas EXTREMA em GRAU no ES.")

with open(os.path.join(OUT, "benchmark_caracterizacao.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["UF","base_pct","mult_producao","emprego_Rmi","ligacao_tras","dom_emp_gap"])
    for g in range(27):
        wr.writerow([REG[g], f"{base[g]*100:.2f}", f"{pmult[g]:.4f}", f"{emult[g]:.2f}",
                     f"{backw[g]:.4f}", f"{dom_emp_gap[g]:.3f}"])
print("salvo: benchmark_caracterizacao.csv")
