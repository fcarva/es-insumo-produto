# -*- coding: utf-8 -*-
"""
10_cluster_setorial.py — A3: tabela comparativa do cluster (ES vs os 7 pares),
a partir da matriz interestadual 2008. Posiciona o ES entre os estados dinamicos.
Indicadores: PIB share, abertura (vazamento), multiplicador medio de producao,
setor dominante e participacao de setores de base/commodity (perfil-plataforma).
"""
import os, csv, sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows (cp1252) nao encoda alguns caracteres nos prints; forca UTF-8

P   = r"C:/Users/DELL/Downloads/Material IO/MIP-26x26-BR-2008.xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"

REG = ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI",
       "SE","RN","DF","GO","MT","MS","ES","MG","RJ","SP","PR","SC","RS"]
idx = {r: i for i, r in enumerate(REG)}
CLUSTER = ["ES","MG","SC","PR","RS","GO","MT","MS"]   # ES primeiro (protagonista)
NUCLEO  = ["SP","RJ"]
SET = ["Agricultura","Pecuária/pesca","Mineração","Alimentos","Têxtil","Madeira/papel",
       "Refino","Químicos","Borracha/plástico","Cimento/min.","Metalurgia","Máquinas",
       "Mat. elétrico","Mat. transporte","Ind. diversas","Eletric./gás/água","Construção",
       "Comércio","Transporte","Serv. privados","Financeiro","Imobiliário","Aloj./alim.",
       "Educação","Saúde","Adm. pública"]
BASE = [0, 2, 3, 5, 6, 10]   # agric, mineração, alimentos, madeira/papel, refino, metalurgia

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z  = to(df.iloc[4:706, 3:705].values)
x  = to(df.iloc[729, 3:705].values)
VA = to(df.iloc[728, 3:705].values)
N = 702
def rseg(g): return slice(26*g, 26*g+26)
xs = np.where(x <= 0, 1.0, x); A = Z/xs[None, :]; B = np.linalg.inv(np.eye(N)-A)
pib_tot = VA.sum()

def metrics(state):
    g = idx[state]; cols = np.arange(26*g, 26*g+26)
    xg = x[cols]
    O = B[:, cols].sum(0)
    Oin = B[rseg(g)][:, cols].sum(0)
    leak = float((( 1 - Oin/np.where(O==0,1,O)) * (xg/xg.sum())).sum())
    return dict(estado=state, pib=VA[cols].sum()/pib_tot, vaz=leak, mult=float(O.mean()),
                dom=SET[int(np.argmax(xg))], base=float(xg[BASE].sum()/xg.sum()))

rows = [metrics(s) for s in CLUSTER] + [metrics(s) for s in NUCLEO]

print("="*86)
print("A3 — CLUSTER DE ESTADOS DINÂMICOS: ES vs PARES  (interestadual 2008)")
print("="*86)
print(f"{'Estado':7s}{'PIB%':>7s}{'Vazam.':>8s}{'Mult.méd':>9s}{'Base/commodity':>16s}  Setor dominante")
print("-"*86)
for r in rows:
    tag = "" if r["estado"] in CLUSTER else " (núcleo)"
    print(f"{r['estado']:7s}{r['pib']*100:6.1f}%{r['vaz']*100:7.1f}%{r['mult']:9.3f}"
          f"{r['base']*100:14.1f}%   {r['dom']}{tag}")
print("="*86)
# medias do cluster (ex-ES) para contraste
cl = [r for r in rows if r["estado"] in CLUSTER and r["estado"] != "ES"]
print(f"Média dos 7 pares: vazamento {np.mean([r['vaz'] for r in cl])*100:.1f}% · "
      f"base/commodity {np.mean([r['base'] for r in cl])*100:.1f}%")
es = [r for r in rows if r["estado"]=="ES"][0]
print(f"ES               : vazamento {es['vaz']*100:.1f}% · base/commodity {es['base']*100:.1f}% "
      f"(setor dominante {es['dom']})")

with open(os.path.join(OUT, "cluster_setorial.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["estado","grupo","pib_share_%","vazamento_%","mult_medio","base_commodity_%","setor_dominante"])
    for r in rows:
        w.writerow([r["estado"], "cluster" if r["estado"] in CLUSTER else "nucleo",
                    f"{r['pib']*100:.2f}", f"{r['vaz']*100:.2f}", f"{r['mult']:.4f}",
                    f"{r['base']*100:.2f}", r["dom"]])
print("salvo: cluster_setorial.csv")
