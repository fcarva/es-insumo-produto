# -*- coding: utf-8 -*-
"""
15_intra_es_fractal.py — RQ-A: a economia-plataforma e FRACTAL?
Testa se o padrao metropole-retem / periferia-vaza se reproduz DENTRO do ES, entre
as 10 microrregioes de planejamento (sistema inter-regional 2015, R1-R10 x S1-S35).

Para cada microrregiao: vazamento medio do mult. de producao (para OUTRAS microrregioes
do ES), razao de FEEDBACK (inversa particionada), destino do spillover intra-ES e HHI;
extracao hipotetica da metropole; e um MODELO NULO intra-ES (metrica ~ porte) para ver
se a MESMA regularidade size-driven do nivel 27-UF vale uma escala abaixo.

Fonte: Material IO/Microrregioes do ES (2015).xlsx (aba 'IIOS', R$ mi).
Layout (de _micro.md + inspecao): Z 350x350 = cols 3..352, regioes R1..R10 em blocos de
35 setores (linhas 6..355); VBP (GO) = linha 402; demanda final cols 353..395
(353-362 fam | 363-372 FBCF | 373-382 adm | 383-392 ISFLSF | 393 ERB|394 ERM|395 STOCK).
RESSALVAS: 2015!=2008; 35!=26 setores; SEM emprego (so Remuneracoes); chave R1-R10->nome
oficial PENDENTE (regioes identificadas por indice/porte).
"""
import os, csv, sys
import numpy as np
import openpyxl
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

P   = r"C:/Users/DELL/Downloads/Material IO/Microrregiões do ES (2015).xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
os.makedirs(OUT, exist_ok=True)

wb = openpyxl.load_workbook(P, read_only=True, data_only=True)
ws = wb["IIOS"]
grid = [row for row in ws.iter_rows(values_only=True)]
wb.close()
num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0
def cell(r, c):
    row = grid[r-1]; return num(row[c-1]) if c-1 < len(row) else 0.0

NR, NS = 10, 35
N = NR*NS                                    # 350
# Z (350x350): linhas 6..355, cols 3..352
Z = np.array([[cell(r, c) for c in range(3, 3+N)] for r in range(6, 6+N)])
# VBP (GO) linha 402, cols 3..352
x = np.array([cell(402, c) for c in range(3, 3+N)])
# demanda final intra-ES de cada regiao por seus produtos (4 categorias domesticas)
def fd_own(g):  # g=0..9 -> cols (1-based) 353+g,363+g,373+g,383+g
    cols = [353+g, 363+g, 373+g, 383+g]
    return np.array([sum(cell(r, c) for c in cols) for r in range(6, 6+N)])

# chave R1-R10 -> nome (ordem da Lei 9.768/2011, corroborada por porte/geografia
# economica: R1 Metropolitana=62% (Grande Vitoria); R4 Litoral Sul=Anchieta/Samarco tem
# o maior vazamento; R7 Rio Doce=Linhares/Aracruz 2o maior). Confirmacao fina via .xlsb pendente.
REG_NOME = {1:"Metropolitana",2:"Central Serrana",3:"Sudoeste Serrana",4:"Litoral Sul",
            5:"Central Sul",6:"Caparaó",7:"Rio Doce",8:"Centro-Oeste",9:"Nordeste",10:"Noroeste"}

reg = lambda g: slice(NS*g, NS*g+NS)
xs = np.where(x == 0, 1.0, x)
A = Z / xs[None, :]
colsumA = A.sum(0)
B = np.linalg.inv(np.eye(N) - A)

prod_reg = np.array([x[reg(g)].sum() for g in range(NR)])
share = prod_reg / prod_reg.sum()
METRO = int(np.argmax(prod_reg))             # metropole = maior producao (esperado R1)

# por regiao: vazamento (p/ outras microrregioes), feedback, HHI de destino, % p/ metropole
leak = np.zeros(NR); feed = np.zeros(NR); hhi = np.zeros(NR); to_metro = np.zeros(NR)
for g in range(NR):
    Lc = np.arange(NS*g, NS*g+NS)
    Mc = np.array([i for i in range(N) if i//NS != g])
    O = B[:, Lc].sum(0); O_in = B[np.ix_(Lc, Lc)].sum(0)
    lk = 1 - O_in/np.where(O == 0, 1, O)
    w = x[Lc]/x[Lc].sum(); leak[g] = float((lk*w).sum())
    A_LL=A[np.ix_(Lc,Lc)]; A_LM=A[np.ix_(Lc,Mc)]; A_ML=A[np.ix_(Mc,Lc)]; A_MM=A[np.ix_(Mc,Mc)]
    inv_MM=np.linalg.inv(np.eye(Mc.size)-A_MM)
    inv_LL=np.linalg.inv(np.eye(NS)-A_LL)
    inv_fd=np.linalg.inv(np.eye(NS)-A_LL-A_LM@inv_MM@A_ML)
    yL=fd_own(g)[Lc]; inj=float(yL.sum())
    xLc=inv_LL@yL; xLf=inv_fd@yL
    feed[g]=(float(xLf.sum()-xLc.sum())/inj) if inj else 0.0
    xM=inv_MM@A_ML@xLf
    sb=np.zeros(NR); pos=0
    for h in range(NR):
        if h==g: continue
        sb[h]=xM[pos:pos+NS].sum(); pos+=NS
    tot=sb.sum(); shh=sb/(tot if tot else 1)
    hhi[g]=float((shh**2).sum()); to_metro[g]=float(shh[METRO]) if g!=METRO else np.nan

# extracao hipotetica da metropole: quanto da producao do ES some se R(metro) "sai"
keep = np.array([i for i in range(N) if i//NS != METRO])
A_kk = A[np.ix_(keep, keep)]
B_kk = np.linalg.inv(np.eye(keep.size) - A_kk)
y_all = sum(fd_own(g) for g in range(NR))     # demanda final intra-ES total
x_full = B @ y_all
x_ext  = B_kk @ y_all[keep]
loss = 1 - x_ext.sum()/x_full[keep].sum()     # queda na producao das demais regioes

# modelo nulo intra-ES (n=10): metrica ~ a + b log(porte)
logsz = np.log(prod_reg)
def fit(y):
    m = ~np.isnan(y); X = np.column_stack([np.ones(m.sum()), logsz[m]])
    b,*_ = np.linalg.lstsq(X, y[m], rcond=None); yh = X@b
    r2 = 1-((y[m]-yh)**2).sum()/((y[m]-y[m].mean())**2).sum()
    return b, r2
bl, lr2 = fit(leak); bf, fr2 = fit(feed)

print("="*72)
print("RQ-A — A PLATAFORMA E FRACTAL? Intra-ES: 10 microrregioes (2015)")
print("="*72)
print(f"dim={N} (10x35)  SigmaA max={colsumA.max():.3f}  cols com SigmaA>=1: {(colsumA>=1).sum()}")
if (colsumA>=1).any():
    bad=np.where(colsumA>=1)[0]
    print(f"  [ALERTA] colunas desbalanceadas (SigmaA>=1): {[f'R{c//NS+1}S{c%NS+1}={colsumA[c]:.2f}' for c in bad]}")
print(f"  B>=0? {bool((B>=-1e-9).all())}   metropole (maior producao) = R{METRO+1} ({share[METRO]:.1%} da prod. do ES)")
print("-"*72)
print(f"{'reg':16s} {'share':>7s} {'vazam.':>7s} {'feedb.':>7s} {'HHIdest':>7s} {'%->metro':>8s}")
for g in np.argsort(prod_reg)[::-1]:
    tm = "  (metro)" if g==METRO else f"{to_metro[g]:8.1%}"
    lab = f"R{g+1} {REG_NOME[g+1]}"
    print(f"{lab:16s} {share[g]:7.1%} {leak[g]:7.1%} {feed[g]:7.2%} {hhi[g]:7.3f} {tm}")
print("-"*72)
print("INVARIANCIA DE ESCALA (modelo nulo intra-ES, n=10):")
print(f"  vazamento ~ log(porte): b={bl[1]:+.4f}  R2={lr2:.2f}  (metropole grande -> {'menos' if bl[1]<0 else 'mais'} vazamento)")
print(f"  feedback  ~ log(porte): b={bf[1]:+.5f}  R2={fr2:.2f}  (porte maior -> {'mais' if bf[1]>0 else 'menos'} feedback)")
print(f"  -> compare com 27-UF (script 14): vazamento decresce no porte; feedback CRESCE no porte (R2~0.6)")
print("-"*72)
print(f"EXTRACAO HIPOTETICA DA METROPOLE (R{METRO+1}={REG_NOME[METRO+1]}): producao das demais microrregioes")
print(f"  cairia {loss:.1%} se a metropole 'saisse' do sistema -> dependencia da periferia do nucleo capixaba")
print("-"*72)
# ---- SENSIBILIDADE: dropar S23 (col-sum>=1 em todas as regioes) ----
S23 = 22  # 0-based
keepS = np.array([i for i in range(N) if i % NS != S23])
Zs = Z[np.ix_(keepS, keepS)]; xss = xs[keepS]
As = Zs / xss[None, :]; Bs = np.linalg.inv(np.eye(keepS.size) - As)
NSs = NS - 1
leak_s = np.zeros(NR); feed_s = np.zeros(NR)
for g in range(NR):
    Lc = np.arange(NSs*g, NSs*g+NSs); Mc = np.array([i for i in range(keepS.size) if i//NSs != g])
    O = Bs[:, Lc].sum(0); O_in = Bs[np.ix_(Lc, Lc)].sum(0)
    lk = 1 - O_in/np.where(O==0,1,O); w = xss[Lc]/xss[Lc].sum(); leak_s[g] = float((lk*w).sum())
    A_LL=As[np.ix_(Lc,Lc)]; A_LM=As[np.ix_(Lc,Mc)]; A_ML=As[np.ix_(Mc,Lc)]; A_MM=As[np.ix_(Mc,Mc)]
    iMM=np.linalg.inv(np.eye(Mc.size)-A_MM); iLL=np.linalg.inv(np.eye(NSs)-A_LL)
    ifd=np.linalg.inv(np.eye(NSs)-A_LL-A_LM@iMM@A_ML)
    yL=fd_own(g)[keepS][Lc]; inj=float(yL.sum())
    feed_s[g]=(float((ifd@yL).sum()-(iLL@yL).sum())/inj) if inj else 0.0
bf_s, fr2_s = fit(feed_s)
print("SENSIBILIDADE (dropando S23, col-sum>=1 nas 10 regioes):")
print(f"  metropole R{METRO+1}: vazamento {leak[METRO]:.1%} -> {leak_s[METRO]:.1%}  (delta {leak_s[METRO]-leak[METRO]:+.1%})")
print(f"  feedback ~ porte: R2 {fr2:.2f} -> {fr2_s:.2f}  -> o padrao fractal {'SOBREVIVE' if fr2_s>0.5 else 'MUDA'}")
print("="*72)

with open(os.path.join(OUT, "intra_es_fractal.csv"), "w", newline="", encoding="utf-8") as f:
    wr=csv.writer(f); wr.writerow(["regiao","nome","share_prod_pct","vazamento","feedback_razao","HHI_destino","pct_para_metropole","is_metropole"])
    for g in range(NR):
        wr.writerow([f"R{g+1}", REG_NOME[g+1], f"{share[g]*100:.2f}", f"{leak[g]:.4f}", f"{feed[g]:.5f}",
                     f"{hhi[g]:.4f}", "" if g==METRO else f"{to_metro[g]*100:.1f}", int(g==METRO)])
print("salvo: intra_es_fractal.csv")
