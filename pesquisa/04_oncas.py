# -*- coding: utf-8 -*-
"""
04_oncas.py — lê o artigo da Apex Partners sobre as "oncas brasileiras" e testa,
no modelo interestadual, se o ES (e o bloco das oncas) escoa encadeamento para o
NUCLEO (SP+RJ, a Faria Lima) em vez de reter no proprio bloco.

Oncas (8): SC, PR, ES, MG, RS, GO, MT, MS  (excluem SP e RJ — o nucleo).
"""
import os, csv
import numpy as np
import pandas as pd

P   = r"C:/Users/DELL/Downloads/Material IO/MIP-26x26-BR-2008.xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"

REG = ["AC","AP","AM","PA","RO","RR","TO","AL","BA","CE","MA","PB","PE","PI",
       "SE","RN","DF","GO","MT","MS","ES","MG","RJ","SP","PR","SC","RS"]
idx = {r:i for i,r in enumerate(REG)}
ES = idx["ES"]
ONCAS = ["SC","PR","ES","MG","RS","GO","MT","MS"]
NUCLEO = ["SP","RJ"]
onca_i  = [idx[u] for u in ONCAS]
nucleo_i= [idx[u] for u in NUCLEO]

df = pd.read_excel(P, sheet_name="BR", header=None)
to = lambda a: np.nan_to_num(np.array(a, dtype=float))
Z  = to(df.iloc[4:706, 3:705].values)
x  = to(df.iloc[729, 3:705].values)         # VALOR DA PRODUCAO
VA = to(df.iloc[728, 3:705].values)         # Valor adicionado bruto (PIB)
FD = to(df.iloc[4:706, 706:868].values)
N = 702
def rseg(g):  return slice(26*g, 26*g+26)
def fdseg(g): return slice(6*g, 6*g+6)
xs = np.where(x==0,1.0,x); A = Z/xs[None,:]; B = np.linalg.inv(np.eye(N)-A)
def by_region(v): return np.array([v[rseg(g)].sum() for g in range(27)])

def spill_groups(region_list):
    """injeta demanda final do conjunto por produtos do conjunto; devolve
    producao por regiao."""
    f = np.zeros(N)
    for g in region_list:
        rr = np.arange(26*g, 26*g+26)
        f[rr] = FD[rr, fdseg(g)].sum(axis=1)
    xf = B @ f
    return by_region(xf), f.sum()

def grupos(prod, origem_i):
    """reparte producao em: dentro do bloco-origem / nucleo SP+RJ / resto."""
    dentro = sum(prod[g] for g in origem_i)
    nucleo = sum(prod[g] for g in nucleo_i if g not in origem_i)
    resto  = prod.sum() - dentro - nucleo
    return dentro, nucleo, resto

def br(v): return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

# (1) PIB share das oncas em 2008 (vs Apex: 39% em 2023)
pib_reg = by_region(VA); pib_tot = pib_reg.sum()
share_oncas = sum(pib_reg[g] for g in onca_i)/pib_tot
share_nucleo= sum(pib_reg[g] for g in nucleo_i)/pib_tot

# (2) ES: spillover para outras oncas vs nucleo vs resto
prodES, injES = spill_groups([ES])
spillES = prodES.copy(); spillES[ES]=0; tot_spES=spillES.sum()
es_outras_oncas = sum(prodES[g] for g in onca_i if g!=ES)
es_nucleo = sum(prodES[g] for g in nucleo_i)
es_resto  = tot_spES - es_outras_oncas - es_nucleo

# (3) bloco ONCAS: retem dentro do bloco ou escoa pro nucleo?
prodB, injB = spill_groups(onca_i)
dentro, nucleoB, restoB = grupos(prodB, onca_i)

# (4) abertura (vazamento medio do mult.) por onca
def leak_region(g):
    cols=np.arange(26*g,26*g+26); O=B[:,cols].sum(0); Oin=B[rseg(g)][:,cols].sum(0)
    lk=1-Oin/np.where(O==0,1,O); w=x[cols]/x[cols].sum(); return float((lk*w).sum())
leak_all = {r: leak_region(idx[r]) for r in REG}
rank = sorted(REG, key=lambda r: leak_all[r], reverse=True)

print("="*66)
print('AS "ONCAS BRASILEIRAS" (Apex Partners) NO MODELO INTERESTADUAL 2008')
print("="*66)
print(f"Oncas (8): {', '.join(ONCAS)}   | Nucleo: SP, RJ")
print("-"*66)
print(f"[1] Participacao no PIB (2008): oncas={share_oncas:.1%} | nucleo(SP+RJ)={share_nucleo:.1%}")
print(f"    (Apex cita oncas 34%->39% do PIB entre 2002 e 2023)")
print("-"*66)
print("[2] DESTINO DO SPILLOVER DO ES (R$ %s mi):" % br(tot_spES))
print(f"    -> outras 7 oncas : {es_outras_oncas/tot_spES:5.1%}")
print(f"    -> NUCLEO (SP+RJ) : {es_nucleo/tot_spES:5.1%}   <-- a Faria Lima")
print(f"    -> resto do Brasil: {es_resto/tot_spES:5.1%}")
print("-"*66)
print("[3] BLOCO DAS ONCAS — para onde escoa seu encadeamento:")
print(f"    retido DENTRO do bloco: {dentro/prodB.sum():5.1%}")
print(f"    escoa p/ NUCLEO SP+RJ : {nucleoB/prodB.sum():5.1%}")
print(f"    resto do Brasil       : {restoB/prodB.sum():5.1%}")
print("-"*66)
print("[4] ABERTURA (vazamento medio) — oncas em destaque:")
for r in REG:
    mark = " <ONCA" if r in ONCAS else ("  [nucleo]" if r in NUCLEO else "")
    if r in ONCAS or r in NUCLEO:
        print(f"    {rank.index(r)+1:2d}o {r}: {leak_all[r]:.1%}{mark}")
print("="*66)

with open(os.path.join(OUT,"oncas_resumo.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["metrica","valor_pct"])
    w.writerow(["es_spill_outras_oncas", f"{es_outras_oncas/tot_spES*100:.1f}"])
    w.writerow(["es_spill_nucleo",       f"{es_nucleo/tot_spES*100:.1f}"])
    w.writerow(["es_spill_resto",        f"{es_resto/tot_spES*100:.1f}"])
    w.writerow(["bloco_dentro",          f"{dentro/prodB.sum()*100:.1f}"])
    w.writerow(["bloco_nucleo",          f"{nucleoB/prodB.sum()*100:.1f}"])
    w.writerow(["bloco_resto",           f"{restoB/prodB.sum()*100:.1f}"])
    w.writerow(["pib_share_oncas_2008",  f"{share_oncas*100:.1f}"])
    w.writerow(["pib_share_nucleo_2008", f"{share_nucleo*100:.1f}"])

with open(os.path.join(OUT,"oncas.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["estado","onca","pib_share_2008_%","vazamento_%","rank_abertura","es_spillover_%"])
    for r in REG:
        g=idx[r]
        w.writerow([r, "sim" if r in ONCAS else "", f"{pib_reg[g]/pib_tot*100:.2f}",
                    f"{leak_all[r]*100:.2f}", rank.index(r)+1,
                    f"{spillES[g]/tot_spES*100:.2f}"])
print("salvo: oncas.csv")
