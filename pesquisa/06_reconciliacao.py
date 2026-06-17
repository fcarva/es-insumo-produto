# -*- coding: utf-8 -*-
"""
06_reconciliacao.py — A1: identifica a CONVENCAO de injecao/decomposicao que
reproduz os numeros de spillover/feedback do artigo (alvos: injecao 60.600,
spillover 22.400, feedback 199, R$ mi). Varre variantes sobre a MIP-ES-BR real.

A base ja esta validada (vazamento 24,9% e emprego batem exatos em 01_..), entao
qualquer diferenca aqui e puramente de DEFINICAO. Objetivo: travar a definicao.
"""
import numpy as np, openpyxl

DATA = r"C:/Users/DELL/Downloads/Material IO/Matrizes/MIP-ES-BR (2008).xlsx"
TGT  = dict(inj=60600.0, spill=22400.0, feedback=199.0)

def num(v): return float(v) if isinstance(v,(int,float)) else 0.0
wb = openpyxl.load_workbook(DATA, data_only=True); ws = wb["ES-BR"]
Z  = np.array([[num(ws.cell(r,c).value) for c in range(5,57)] for r in range(7,59)])
FD = np.array([[num(ws.cell(r,c).value) for c in range(58,70)] for r in range(7,59)])
vbp= np.array([num(ws.cell(80,c).value) for c in range(5,57)]); wb.close()

L = np.arange(0,26); M = np.arange(26,52)
x = np.where(vbp==0,1.0,vbp); A = Z/x[None,:]; B = np.linalg.inv(np.eye(52)-A)
A_LL=A[np.ix_(L,L)]; A_LM=A[np.ix_(L,M)]; A_ML=A[np.ix_(M,L)]; A_MM=A[np.ix_(M,M)]
I=np.eye(26); inv_LL=np.linalg.inv(I-A_LL); inv_MM=np.linalg.inv(I-A_MM)
inv_feed=np.linalg.inv(I-A_LL-A_LM@inv_MM@A_ML)

# categorias de demanda final do ES: 0=Export,1=Gov,2=ISFLSF,3=Familias,4=FBCF,5=VarEst
cats_nome = ["Export","Gov","ISFLSF","Familias","FBCF","VarEst"]
tot = FD[:,0:6].sum()
print("Demanda final do ES por categoria (R$ mi):")
for i,nm in enumerate(cats_nome):
    print(f"   {nm:10s}: {FD[:,i].sum():10,.0f}")
fam = FD[:,3].sum()
print(f"   TOTAL     : {tot:10,.0f}")
print(f"   -> total - Familias (injecao exogena no modelo FECHADO): {tot-fam:,.0f}  (alvo 60.600)")
print("="*92)
print(f"{'variante (vetor de injecao y, 52)':46s}{'inj':>10s}{'spill_full':>12s}{'spill_MB':>11s}{'feedb':>9s}")
print("-"*92)

def metrics(y):
    inj = y.sum()
    xf  = B@y; spill_full = xf[M].sum()
    yL  = y[L]
    xL_full = inv_feed@yL
    spill_MB = (inv_MM@A_ML@xL_full).sum()
    feedback = xL_full.sum() - (inv_LL@yL).sum()
    return inj, spill_full, spill_MB, feedback

def y_allorig(cats):           # demanda final do ES por TODAS as origens
    v=np.zeros(52); v[:]=FD[:,cats].sum(1); return v
def y_esprod(cats):            # demanda final do ES so por produtos do ES
    v=np.zeros(52); v[L]=FD[np.ix_(L,cats)].sum(1); return v

variantes = {
 "V1 FD total ES (todas origens, c/ export)": y_allorig(range(0,6)),
 "V2 FD ES excl. export (todas origens)":     y_allorig(range(1,6)),
 "V3 FD ES p/ produtos ES (c/ export)":       y_esprod(range(0,6)),
 "V4 FD ES p/ produtos ES (excl. export)":    y_esprod(range(1,6)),
}
def mark(v,t): return "*" if abs(v-t)/t < 0.03 else " "
for nome,y in variantes.items():
    inj,sf,smb,fb = metrics(y)
    print(f"{nome:46s}{inj:10,.0f}{mark(inj,TGT['inj'])}{sf:11,.0f}{smb:10,.0f}"
          f"{mark(smb,TGT['spill'])}{fb:8,.0f}{mark(fb,TGT['feedback'])}")
print("-"*92)
print(f"{'ALVO (artigo)':46s}{TGT['inj']:10,.0f} {'':11s}{TGT['spill']:10,.0f} {TGT['feedback']:8,.0f}")
print("="*92)
print("* = a <3% do alvo.  spill_full = By no bloco M;  spill_MB = (I-A_MM)^-1 A_ML xL (Miller-Blair).")
print()
print("CONCLUSAO DE AUDITORIA:")
print("- Nenhuma convencao-padrao (modelo aberto) reproduz 60.600/22.400/199 nesta matriz.")
print("- MAS a tese 'feedback ~ 0' e ROBUSTA: feedback/injecao por variante --")
for nome,y in variantes.items():
    inj,sf,smb,fb = metrics(y)
    print(f"    {nome[:38]:38s} feedback/injecao = {fb/inj:5.2%}")
print("- Recomendacao: adotar a convencao Miller-Blair limpa (V3: injeta demanda final do ES")
print("  por produtos do ES) como numeros PUBLICAVEIS e reprodutiveis -> inj 51.483, spill 18.163,")
print("  feedback 164 (0,32%); ou confirmar o metodo do artigo original. A assimetria nao muda.")
