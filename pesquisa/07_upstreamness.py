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
import os, csv, time, sys
import numpy as np
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows (cp1252) nao encoda alguns caracteres nos prints; forca UTF-8

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
mining = 4*56 + 3                                # mineracao do Brasil (setor B), idx global

# --- Tratamento de qualidade do dado (literatura) -------------------------------
# A demanda final implicita (X - soma de linha de Z) inclui variacao de estoques e
# discrepancia estatistica (OECD, 2019, Tab. 2.1): 49/2464 setores tem F<0 e a cauda
# de U e nao-economica (max ~15 mil; upstreamness teorica ~1-5). Entradas negativas
# devem ser reconciliadas, nao interpretadas como fluxo (Tukker & Dietzenbacher, 2013,
# p. 10 e 14). Logo, para a POSICAO global, excluem-se setores com F<=0 e a cauda
# implausivel (U>10) e reporta-se NIVEL + RANKING como estatistica primaria
# (Araujo Junior, 2018, p. 21); o percentil e descritor secundario sobre a base limpa.
fd_floor = 1e-6 * np.maximum(X, 1.0)
valid = np.isfinite(U) & (F_impl > fd_floor) & (U <= 10.0)
n_valid = int(valid.sum()); n_excl = N - n_valid

U_mining = float(U[mining])
pct_mining = (U[valid] < U_mining).mean()*100        # percentil sobre distribuicao LIMPA
pct_mining_raw = (U < U_mining).mean()*100           # bruta (contaminada), p/ contraste
rank_mining = int((U[valid] > U_mining).sum()) + 1   # 1 = mais a montante
avg_bra_out = float((U_bra * (X_bra/X_bra.sum())).sum())
avg_world_out = float((U * (X/ X.sum())).sum())       # ponderado pela producao (robusto a outliers)

print("="*64)
print("UPSTREAMNESS (Antras-Chor) — WIOD 2014, dado real")
print("="*64)
print(f"U global (bruto): min {U.min():.2f} | mediana {np.median(U):.2f} | max {U.max():.2f}")
print(f"Setores excluidos (F<=0 ou U>10 — estoques/discrepancia): {n_excl}/{N} | validos: {n_valid}")
print(f"Brasil — upstreamness media ponderada pela producao: {avg_bra_out:.2f}")
print(f"Mundo  — upstreamness media ponderada pela producao: {avg_world_out:.2f}")
print("-"*64)
print(f"MINERACAO do Brasil (setor B): U = {U_mining:.2f}")
print(f"  posicao GLOBAL (base limpa): {rank_mining}o de {n_valid}  | percentil {pct_mining:.1f}")
print(f"  [contraste] percentil sobre distribuicao BRUTA: {pct_mining_raw:.1f}")
print("-"*64)
print("Setores brasileiros mais a montante (maior U):")
for k in np.argsort(U_bra)[::-1][:6]:
    print(f"   {U_bra[k]:5.2f}  setor {k+1:2d} {nome.get(k,'')}")
print("="*64)

with open(os.path.join(OUT, "brasil_upstreamness.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh); wr.writerow(["setor_wiod_idx", "nome", "upstreamness", "output_US_mi", "percentil_global_limpo"])
    for k in range(56):
        gi = 4*56 + k
        wr.writerow([k+1, nome.get(k, ""), f"{U_bra[k]:.4f}", f"{X_bra[k]:.0f}",
                     f"{(U[valid] < U[gi]).mean()*100:.1f}"])
print("salvo: brasil_upstreamness.csv")

with open(os.path.join(OUT, "upstream_resumo.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh); wr.writerow(["metrica", "valor"])
    wr.writerow(["brasil_upstreamness", f"{avg_bra_out:.4f}"])
    wr.writerow(["mundo_upstreamness", f"{avg_world_out:.4f}"])
    wr.writerow(["mineracao_U", f"{U_mining:.4f}"])
    wr.writerow(["mineracao_rank_global", f"{rank_mining}"])
    wr.writerow(["mineracao_n_validos", f"{n_valid}"])
    wr.writerow(["setores_excluidos", f"{n_excl}"])
    wr.writerow(["mineracao_percentil_bruto", f"{pct_mining_raw:.1f}"])
    wr.writerow(["mineracao_percentil", f"{pct_mining:.1f}"])   # limpa (consumida por 09)
print("salvo: upstream_resumo.csv")
