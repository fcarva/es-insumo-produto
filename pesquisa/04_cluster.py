# -*- coding: utf-8 -*-
"""
04_cluster.py — testa, no modelo interestadual, se o Espirito Santo escoa
encadeamento para o NUCLEO (SP+RJ) em vez de reter, e situa o ES num CLUSTER de
estados dinamicos (ex-nucleo).

Cluster (8 estados, ex-SP/RJ): SC, PR, ES, MG, RS, GO, MT, MS.
Criterio (leitura da Apex Partners, Brazil Journal/NeoFeed jun-2026): crescimento
acima da media, contas organizadas, economia real sub-coberta pelo mercado de
capitais. Aqui o cluster e um GRUPO DE COMPARACAO; o foco do artigo segue no ES.
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
idx = {r:i for i,r in enumerate(REG)}
ES = idx["ES"]
CLUSTER  = ["SC","PR","ES","MG","RS","GO","MT","MS"]   # estados dinamicos (ex-nucleo)
NUCLEO   = ["SP","RJ"]
cluster_i = [idx[u] for u in CLUSTER]
nucleo_i  = [idx[u] for u in NUCLEO]

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z  = to(df.iloc[4:706, 3:705].values)
x  = to(df.iloc[729, 3:705].values)         # VALOR DA PRODUCAO
VA = to(df.iloc[728, 3:705].values)         # Valor adicionado bruto (PIB)
FD = to(df.iloc[4:706, 706:868].values)
N = 702
def rseg(g):  return slice(26*g, 26*g+26)
def fdseg(g): return slice(6*g, 6*g+6)
xs = np.where(x<=0,1.0,x); A = Z/xs[None,:]; B = np.linalg.inv(np.eye(N)-A)
assert A.sum(0).max() < 1, "coeficiente tecnico >= 1 (matriz desbalanceada?)"
def by_region(v): return np.array([v[rseg(g)].sum() for g in range(27)])

def spill_groups(region_list):
    f = np.zeros(N)
    for g in region_list:
        rr = np.arange(26*g, 26*g+26)
        f[rr] = FD[rr, fdseg(g)].sum(axis=1)
    return by_region(B @ f), f.sum()

def br(v): return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

# (1) participacao no PIB (2008)
pib_reg = by_region(VA); pib_tot = pib_reg.sum()
share_cluster = sum(pib_reg[g] for g in cluster_i)/pib_tot
share_nucleo  = sum(pib_reg[g] for g in nucleo_i)/pib_tot

# (2) ES: spillover para o resto do cluster vs nucleo vs resto do pais
prodES, injES = spill_groups([ES])
spillES = prodES.copy(); spillES[ES]=0; tot_spES=spillES.sum()
es_cluster = sum(prodES[g] for g in cluster_i if g!=ES)
es_nucleo  = sum(prodES[g] for g in nucleo_i)
es_resto   = tot_spES - es_cluster - es_nucleo

# (3) bloco CLUSTER: retem dentro ou escoa pro nucleo?
prodB, injB = spill_groups(cluster_i)
dentro = sum(prodB[g] for g in cluster_i)
nucleoB= sum(prodB[g] for g in nucleo_i if g not in cluster_i)
restoB = prodB.sum() - dentro - nucleoB

# (4) abertura por estado
def leak_region(g):
    cols=np.arange(26*g,26*g+26); O=B[:,cols].sum(0); Oin=B[rseg(g)][:,cols].sum(0)
    lk=1-Oin/np.where(O==0,1,O); w=x[cols]/x[cols].sum(); return float((lk*w).sum())
leak_all = {r: leak_region(idx[r]) for r in REG}
rank = sorted(REG, key=lambda r: leak_all[r], reverse=True)

print("="*66)
print("ES NO CLUSTER DE ESTADOS DINAMICOS (ex-nucleo SP/RJ) — INTEREST. 2008")
print("="*66)
print(f"Cluster (8): {', '.join(CLUSTER)}   | Nucleo: SP, RJ")
print(f"[1] PIB 2008: cluster={share_cluster:.1%} | nucleo(SP+RJ)={share_nucleo:.1%}")
print(f"    (leitura Apex: o grupo foi de 34% (2002) a 39% (2023) do PIB)")
print("-"*66)
print(f"[2] DESTINO DO SPILLOVER DO ES (R$ {br(tot_spES)} mi):")
print(f"    -> resto do cluster: {es_cluster/tot_spES:5.1%}")
print(f"    -> NUCLEO (SP+RJ)  : {es_nucleo/tot_spES:5.1%}   <-- mercado de capitais")
print(f"    -> resto do pais   : {es_resto/tot_spES:5.1%}")
print("-"*66)
print("[3] BLOCO CLUSTER — para onde escoa seu encadeamento:")
print(f"    retido DENTRO do cluster: {dentro/prodB.sum():5.1%}")
print(f"    escoa p/ NUCLEO SP+RJ   : {nucleoB/prodB.sum():5.1%}")
print(f"    resto do pais           : {restoB/prodB.sum():5.1%}")
print("-"*66)
print("[4] ABERTURA (vazamento medio) — cluster vs nucleo:")
for r in REG:
    if r in CLUSTER or r in NUCLEO:
        mark = " <cluster" if r in CLUSTER else "  [nucleo]"
        print(f"    {rank.index(r)+1:2d}o {r}: {leak_all[r]:.1%}{mark}")
print("="*66)

with open(os.path.join(OUT,"cluster_resumo.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["metrica","valor_pct"])
    for k,v in [("es_spill_cluster",es_cluster/tot_spES*100),("es_spill_nucleo",es_nucleo/tot_spES*100),
                ("es_spill_resto",es_resto/tot_spES*100),("bloco_dentro",dentro/prodB.sum()*100),
                ("bloco_nucleo",nucleoB/prodB.sum()*100),("bloco_resto",restoB/prodB.sum()*100),
                ("pib_share_cluster_2008",share_cluster*100),("pib_share_nucleo_2008",share_nucleo*100),
                ("es_spill_total_mi",tot_spES),("es_retido_mi",prodES[ES])]:
        w.writerow([k, f"{v:.1f}"])
with open(os.path.join(OUT,"cluster.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["estado","cluster","pib_share_2008_%","vazamento_%","rank_abertura","es_spillover_%"])
    for r in REG:
        g=idx[r]
        w.writerow([r, "sim" if r in CLUSTER else "", f"{pib_reg[g]/pib_tot*100:.2f}",
                    f"{leak_all[r]*100:.2f}", rank.index(r)+1, f"{spillES[g]/tot_spES*100:.2f}"])
print("salvos: cluster.csv, cluster_resumo.csv")
