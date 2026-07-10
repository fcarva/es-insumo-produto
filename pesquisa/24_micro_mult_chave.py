# -*- coding: utf-8 -*-
"""
24_micro_mult_chave.py — C3b: MULTIPLICADORES E RETENCAO TERRITORIAL por microrregiao
(sistema inter-regional das 10 microrregioes do ES, 2015, 350x350) — base da Tabela
`tab:micro` do artigo. Para cada microrregiao:

  - multiplicador de producao SIMPLES (media) e PONDERADO pelo VBP setorial
  - RETENCAO intra-territorial do multiplicador ponderado:
        retencao_g = sum_j(w_j * O_intra_j) / sum_j(w_j * O_j),  w_j = VBP setorial
  - multiplicador de RENDA tipo I (remuneracoes), ponderado
  - checagem: ligacoes RH quase INVARIANTES no espaco (setor-chave = tecnologia)

Fonte: Microrregiões do ES (2015).xlsx, aba 'IIOS'. Layout (de 15/20):
Z 350x350 = linhas 6..355 x cols 3..352; VBP (GO) linha 402; blocos R1..R10 de 35
setores; linha de REMUNERACOES localizada por rotulo (varredura das linhas 356..401).

NOTA DE PROVENIENCIA: reconstrucao fiel do script local original (nao versionado a
tempo), nas convencoes de 15/20. AUTOVERIFICACAO ao final contra a Tabela publicada
(Metropolitana 62,3/1,64/90,9/0,37 ... Litoral Sul 4,1/1,76/66,2/0,34). Se a sua
versao original existir, prefira-a e compare as saidas.
"""
import os, csv, sys, re, warnings
import numpy as np, openpyxl
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

P   = r"C:/Users/DELL/Downloads/Material IO/Microrregiões do ES (2015).xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
os.makedirs(OUT, exist_ok=True)

REG_NOME = {1:"Metropolitana",2:"Central Serrana",3:"Sudoeste Serrana",4:"Litoral Sul",
            5:"Central Sul",6:"Caparaó",7:"Rio Doce",8:"Centro-Oeste",9:"Nordeste",10:"Noroeste"}

num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0
wb = openpyxl.load_workbook(P, read_only=True, data_only=True); ws = wb["IIOS"]
grid = [r for r in ws.iter_rows(values_only=True)]; wb.close()
cell = lambda r, c: num(grid[r-1][c-1]) if (r-1 < len(grid) and c-1 < len(grid[r-1])) else 0.0
def label(r):
    row = grid[r-1] if r-1 < len(grid) else ()
    return " ".join(str(v) for v in row[:3] if isinstance(v, str))

NR, NS = 10, 35; N = NR*NS
Z = np.array([[cell(r, c) for c in range(3, 3+N)] for r in range(6, 6+N)])
x = np.array([cell(402, c) for c in range(3, 3+N)])

# localiza a linha de Remuneracoes no bloco de valor adicionado (356..401) pelo rotulo
rem_row = None
for r in range(356, 402):
    if re.search(r"remunera", label(r), re.I):
        rem_row = r; break
if rem_row is None:
    sys.exit("[ERRO] linha de Remuneracoes nao encontrada (rotulo 'Remunera*' em 356..401); "
             "confira o layout da aba IIOS.")
rem = np.array([cell(rem_row, c) for c in range(3, 3+N)])
print(f"linha de Remuneracoes detectada: {rem_row} ('{label(rem_row).strip()[:40]}')")

xs = np.where(x == 0, 1.0, x)
A = Z / xs[None, :]
B = np.linalg.inv(np.eye(N) - A)
v_inc = rem / xs                                  # renda (remuneracoes) por R$ de producao

O = B.sum(0)                                      # multiplicador de producao (350 colunas)
R = (v_inc[:, None] * B).sum(0)                   # multiplicador de renda tipo I
# RH no sistema completo (p/ checagem de invariancia espacial)
Ahat = Z / xs[:, None]; G = np.linalg.inv(np.eye(N) - Ahat)
bl = B.sum(0) / N / B.mean(); fl = G.sum(1) / N / G.mean()

share = np.zeros(NR); mult_s = np.zeros(NR); mult_w = np.zeros(NR)
ret_w = np.zeros(NR); renda_w = np.zeros(NR)
for g in range(NR):
    Lc = np.arange(NS*g, NS*g+NS)
    w = x[Lc] / x[Lc].sum()
    O_in = B[np.ix_(Lc, Lc)].sum(0)               # parcela do multiplicador DENTRO de g
    share[g]  = x[Lc].sum() / x.sum() * 100
    mult_s[g] = float(O[Lc].mean())
    mult_w[g] = float((w * O[Lc]).sum())
    ret_w[g]  = float((w * O_in).sum() / (w * O[Lc]).sum() * 100)
    renda_w[g]= float((w * R[Lc]).sum())

# invariancia espacial das ligacoes RH: amplitude entre regioes, por setor
bl35 = bl.reshape(NR, NS); fl35 = fl.reshape(NR, NS)
amp_bl = (bl35.max(0) - bl35.min(0)).mean(); amp_fl = (fl35.max(0) - fl35.min(0)).mean()

print("=" * 80)
print("C3b — MULTIPLICADORES E RETENCAO TERRITORIAL (10 microrregioes, 2015)")
print("=" * 80)
print(f"SigmaA max={A.sum(0).max():.3f}  B>=0: {bool((B >= -1e-9).all())}  "
      f"mult. simples medio (10 regioes): {mult_s.mean():.3f} (min {mult_s.min():.3f} max {mult_s.max():.3f})")
print(f"ligacoes RH quase invariantes no espaco: amplitude media entre regioes "
      f"p/tras {amp_bl:.3f} · p/frente {amp_fl:.3f}  -> setor-chave e atributo da TECNOLOGIA")
print("-" * 80)
print(f"{'microrregiao':18s} {'%VBP':>6s} {'mult(pond)':>10s} {'retencao%':>10s} {'mult renda':>10s}")
for g in np.argsort(share)[::-1]:
    print(f"R{g+1} {REG_NOME[g+1]:15s} {share[g]:6.1f} {mult_w[g]:10.2f} {ret_w[g]:10.1f} {renda_w[g]:10.2f}")
print("=" * 80)

# ------------------- AUTOVERIFICACAO contra a Tabela publicada -------------------
ALVO = {  # nome: (%VBP, mult pond, retencao %, mult renda) — Tabela `tab:micro`
    "Metropolitana":    (62.3, 1.64, 90.9, 0.37), "Rio Doce":        (10.6, 1.64, 74.3, 0.31),
    "Central Sul":      (6.2, 1.60, 79.4, 0.38),  "Nordeste":        (4.9, 1.50, 85.3, 0.32),
    "Centro-Oeste":     (4.4, 1.53, 85.6, 0.38),  "Litoral Sul":     (4.1, 1.76, 66.2, 0.34),
    "Noroeste":         (2.1, 1.50, 87.3, 0.36),  "Caparaó":         (1.9, 1.42, 88.2, 0.39),
    "Sudoeste Serrana": (1.9, 1.48, 80.6, 0.37),  "Central Serrana": (1.5, 1.43, 82.3, 0.31),
}
fails = []
def chk(rot, got, alvo, tol):
    ok = abs(got - alvo) <= tol
    if not ok: fails.append(f"{rot}: obtido {got:.2f} vs publicado {alvo:.2f}")
    return "OK " if ok else "FAIL"
print("AUTOVERIFICACAO (tolerancias: 0,2 pp share · 0,02 mult · 0,5 pp retencao · 0,01 renda):")
for g in range(NR):
    nome = REG_NOME[g+1]; a = ALVO[nome]
    s = (chk(f"{nome} share", share[g], a[0], 0.2), chk(f"{nome} mult", mult_w[g], a[1], 0.02),
         chk(f"{nome} ret", ret_w[g], a[2], 0.5),   chk(f"{nome} renda", renda_w[g], a[3], 0.01))
    print(f"  [{''.join(s)}] R{g+1} {nome}")
if fails:
    print("\n[FAIL] a reconstrucao NAO reproduz a tabela publicada nos itens:")
    for f_ in fails: print("   -", f_)
    print("=> hipoteses: agregacao da retencao (razao-de-somas vs media-de-razoes), linha de")
    print("   Remuneracoes, ou tratamento de S23. Compare com o script original, se existir.")
else:
    print("\n[OK] todos os numeros publicados reproduzidos.")

with open(os.path.join(OUT, "micro_multiplicadores.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["regiao", "nome", "share_VBP_pct", "mult_prod_simples",
                 "mult_prod_pond", "retencao_intra_pct", "mult_renda_pond"])
    for g in range(NR):
        wr.writerow([f"R{g+1}", REG_NOME[g+1], f"{share[g]:.2f}", f"{mult_s[g]:.4f}",
                     f"{mult_w[g]:.4f}", f"{ret_w[g]:.2f}", f"{renda_w[g]:.4f}"])
print("salvo: micro_multiplicadores.csv")
sys.exit(1 if fails else 0)
