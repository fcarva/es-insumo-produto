# -*- coding: utf-8 -*-
"""
07_upstreamness.py — A2: upstreamness de Antras-Chor (2012) a partir do WIOD 2014.
Valida do dado real a posicao do Brasil em CGV (e da mineracao no ranking global).

WIOD 2014 (aba '2014'): 44 regioes (43 paises + ROW) x 56 setores = 2464.
Z = linhas 7-2470, cols 5-2468 ; output X = col 2690 ('Demanda Total').
Brasil = bloco 5 (idx 4): linhas excel 231-286 -> array 224:280. Mineracao = setor B (4o).

Upstreamness: U = (I - G)^-1 1, com G_ij = Z_ij / X_i (aloca producao de i; quanto
maior U_i, mais 'a montante' / longe do consumo final).
"""
import os, csv, time
import numpy as np
import openpyxl

P   = r"C:/Users/DELL/Downloads/Material IO/Matrizes/MIP-Mundo (2014).xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
N = 2464
R0, R1 = 7, 2470          # linhas de dados (excel)
C0, C1 = 5, 2468          # colunas Z (excel)
COL_X  = 2690             # 'Demanda Total' (output)

t0 = time.time()
wb = openpyxl.load_workbook(P, read_only=True, data_only=True); ws = wb["2014"]
Z = np.zeros((N, N), dtype=float); X = np.zeros(N, dtype=float)
def f(v): return float(v) if isinstance(v, (int, float)) else 0.0
for r, row in enumerate(ws.iter_rows(min_row=R0, max_row=R1, values_only=True)):
    Z[r, :] = [f(v) for v in row[C0-1:C1]]      # cols 5..2468
    X[r] = f(row[COL_X-1])                        # col 2690
wb.close()
print(f"WIOD carregado em {time.time()-t0:.0f}s  | Z{Z.shape}  X>0: {(X>0).sum()}/{N}")

Xs = np.where(X <= 0, 1.0, X)
G = Z / Xs[:, None]                              # G_ij = Z_ij / X_i
U = np.linalg.solve(np.eye(N) - G, np.ones(N))   # upstreamness

# checagem de identidade contabil (Antras-Chor pressupoe X_i = sum_j Z_ij + F_i)
F_impl = X - Z.sum(axis=1)
neg = int((F_impl < -1e-6 * np.maximum(X, 1.0)).sum())
print(f"[check WIOD] U finito={np.isfinite(U).all()}  U>=1={bool((U >= 1-1e-6).all())}  "
      f"demanda final implicita < 0 em {neg}/{N} setores")

# Brasil = bloco idx 4
BRA = slice(4*56, 5*56)
U_bra = U[BRA]; X_bra = X[BRA]
# setores WIOD (D=1..56): nomes-chave por indice (0-based)
nome = {0:"Agricultura (A01)",1:"Silvicultura (A02)",2:"Pesca (A03)",3:"Mineracao (B)",
        9:"Coque/refino (C19)",7:"Papel (C17)",14:"Metais basicos (C24)"}
mining = 4*56 + 3                                # mineracao global idx
pct_mining = (U < U[mining]).mean()*100
avg_bra_out = float((U_bra * (X_bra/X_bra.sum())).sum())
avg_world_out = float((U * (X/ X.sum())).sum())

print("="*64)
print("UPSTREAMNESS (Antras-Chor) — WIOD 2014, dado real")
print("="*64)
print(f"U global: min {U.min():.2f} | mediana {np.median(U):.2f} | max {U.max():.2f}")
print(f"Brasil — upstreamness media ponderada pela producao: {avg_bra_out:.2f}")
print(f"Mundo  — upstreamness media ponderada pela producao: {avg_world_out:.2f}")
print("-"*64)
print(f"MINERACAO do Brasil (setor B): U = {U[mining]:.2f}  -> percentil GLOBAL {pct_mining:.1f}")
print("-"*64)
print("Setores brasileiros mais a montante (maior U):")
for k in np.argsort(U_bra)[::-1][:6]:
    print(f"   {U_bra[k]:5.2f}  setor {k+1:2d} {nome.get(k,'')}")
print("="*64)

with open(os.path.join(OUT, "brasil_upstreamness.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh); wr.writerow(["setor_wiod_idx", "nome", "upstreamness", "output_US_mi", "percentil_global"])
    for k in range(56):
        gi = 4*56 + k
        wr.writerow([k+1, nome.get(k, ""), f"{U_bra[k]:.4f}", f"{X_bra[k]:.0f}",
                     f"{(U < U[gi]).mean()*100:.1f}"])
print("salvo: brasil_upstreamness.csv")

with open(os.path.join(OUT, "upstream_resumo.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh); wr.writerow(["metrica", "valor"])
    wr.writerow(["brasil_upstreamness", f"{avg_bra_out:.4f}"])
    wr.writerow(["mundo_upstreamness", f"{avg_world_out:.4f}"])
    wr.writerow(["mineracao_percentil", f"{pct_mining:.1f}"])
print("salvo: upstream_resumo.csv")
