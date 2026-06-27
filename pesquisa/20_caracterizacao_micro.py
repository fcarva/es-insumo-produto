# -*- coding: utf-8 -*-
"""
20_caracterizacao_micro.py — C3: CARACTERIZAÇÃO TERRITORIAL do ES (microrregiões, 2015).
Mapa de VOCAÇÃO ECONÔMICA por microrregião: setor dominante (VBP), ESPECIALIZAÇÃO
(quociente locacional vs. o estado) e multiplicador de produção. Descritivo —
"qual a vocação de cada território capixaba".

Fonte: Microrregiões do ES (2015).xlsx, aba 'IIOS'. Layout (de _micro.md/script 15):
Z 350x350 = cols 3..352; R1..R10 em blocos de 35 setores (linhas 6..355); VBP lin 402.
Nomes S1..S35 = 35 atividades da MIP-ES 2015 (de ESPÍRITO SANTO (2015).xlsm, aba '13').
"""
import os, csv, sys, warnings
import numpy as np, openpyxl
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

P   = r"C:/Users/DELL/Downloads/Material IO/Microrregiões do ES (2015).xlsx"
OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
os.makedirs(OUT, exist_ok=True)

REG_NOME = {1:"Metropolitana",2:"Central Serrana",3:"Sudoeste Serrana",4:"Litoral Sul",
            5:"Central Sul",6:"Caparaó",7:"Rio Doce",8:"Centro-Oeste",9:"Nordeste",10:"Noroeste"}
SET35 = ["Agricultura","Pecuária","Florestal/pesca","Extr. carvão/não-met.","Extr. petróleo e gás",
"Extr. minério de ferro","Alimentos e bebidas","Têxtil/vestuário","Madeira e móveis","Celulose e papel",
"Refino de petróleo","Químicos/borracha/plást.","Minerais não-metálicos","Metalurgia","Prod. de metal/máq.",
"Automóveis/caminhões","Eletricidade e gás","Construção","Comércio","Transporte","Armaz./aux. transp.",
"Alojam./alimentação","Informação","Financeiro/seguros","Imobiliárias","Prof./cient./técn.",
"Administrativas","Administração pública","Educação pública","Educação privada","Saúde pública",
"Saúde privada","Artísticas/criativas","Associativas","Serviços domésticos"]

num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0
wb = openpyxl.load_workbook(P, read_only=True, data_only=True); ws = wb["IIOS"]
grid = [r for r in ws.iter_rows(values_only=True)]; wb.close()
cell = lambda r, c: num(grid[r-1][c-1]) if (r-1 < len(grid) and c-1 < len(grid[r-1])) else 0.0
NR, NS = 10, 35; N = NR*NS
Z = np.array([[cell(r, c) for c in range(3, 3+N)] for r in range(6, 6+N)])
x = np.array([cell(402, c) for c in range(3, 3+N)])
reg = lambda g: slice(NS*g, NS*g+NS)
xs = np.where(x == 0, 1.0, x); A = Z / xs[None, :]; B = np.linalg.inv(np.eye(N) - A)
mult = B.sum(0)

# VBP por (microrregiao, setor) e share/LQ
VBP = x.reshape(NR, NS)                      # 10 x 35
reg_tot = VBP.sum(1)                         # producao de cada microrregiao
es_tot  = VBP.sum(0)                         # producao do ES por setor
share_reg = VBP / reg_tot[:, None]           # composicao interna de cada microrregiao
es_share  = es_tot / es_tot.sum()            # composicao do ES
LQ = share_reg / es_share[None, :]           # quociente locacional (>1 => especializado)

print("="*86)
print("C3 — VOCAÇÃO ECONÔMICA DAS MICRORREGIÕES DO ES (2015)")
print("="*86)
print(f"{'microrregião':16s} {'%ES':>5s} | setor DOMINANTE (VBP)      | ESPECIALIZAÇÃO (top quoc. locacional)")
print("-"*86)
rows_csv = []
order = np.argsort(reg_tot)[::-1]
for g in order:
    dom = int(np.argmax(VBP[g]))
    lq_order = np.argsort(LQ[g])[::-1]
    # top especializacoes com peso minimo (share>2% para nao pegar setor irrelevante)
    spec = [s for s in lq_order if share_reg[g, s] > 0.02][:3]
    spec_str = " · ".join(f"{SET35[s]} (LQ{LQ[g,s]:.1f})" for s in spec)
    print(f"R{g+1} {REG_NOME[g+1]:12s} {reg_tot[g]/reg_tot.sum()*100:4.1f}% | "
          f"{SET35[dom][:24]:24s} | {spec_str}")
    rows_csv.append([f"R{g+1}", REG_NOME[g+1], f"{reg_tot[g]/reg_tot.sum()*100:.1f}",
                     SET35[dom], f"{share_reg[g,dom]*100:.1f}",
                     " | ".join(f"{SET35[s]}:LQ{LQ[g,s]:.2f}" for s in spec)])
print("="*86)
# S4 (parecer): padrao NAO-OBVIO — concentracao (HHI) da composicao setorial por microrregiao
# (LQ diz EM QUE cada uma se especializa; HHI diz QUAO concentrada => polarizacao nucleo-periferia)
hhi_comp = (share_reg**2).sum(1)            # 1 = monossetorial; baixo = diversificada
print("CONCENTRAÇÃO SETORIAL (HHI da composição de VBP) — núcleo diversificado × periferia concentrada:")
o2 = np.argsort(hhi_comp)
for g in o2:
    tag = "  <- metrópole (diversificada)" if g==int(np.argmax(reg_tot)) else ""
    print(f"   R{g+1} {REG_NOME[g+1]:16s} HHI={hhi_comp[g]:.3f}  (share ES {reg_tot[g]/reg_tot.sum()*100:4.1f}%){tag}")
corr_hhi_size = float(np.corrcoef(hhi_comp, np.log(reg_tot))[0,1])
print(f"   correlação HHI × log(porte) = {corr_hhi_size:.2f}  (≈0: concentração NÃO é efeito de porte;")
print("     os mais concentrados são os ENCLAVES extrativos — Litoral Sul/minério, Nordeste/petróleo —")
print("     reproduzindo no território o mesmo padrão-enclave da escala setorial)")
print("="*86)

# setores-chave do ES por multiplicador de producao (media entre microrregioes)
mult_setor = mult.reshape(NR, NS).mean(0)
top = np.argsort(mult_setor)[::-1][:6]
print("Setores de maior MULTIPLICADOR DE PRODUÇÃO (média das microrregiões):")
for s in top: print(f"   {SET35[s]:28s} {mult_setor[s]:.2f}")
print("="*86)

with open(os.path.join(OUT, "caracterizacao_micro.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["regiao","nome","share_ES_%","setor_dominante","dom_share_%","especializacao_LQ"])
    for r in rows_csv: wr.writerow(r)
# matriz LQ completa p/ a figura
with open(os.path.join(OUT, "micro_LQ.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["setor"] + [REG_NOME[g+1] for g in range(NR)])
    for s in range(NS): wr.writerow([SET35[s]] + [f"{LQ[g,s]:.3f}" for g in range(NR)])
print("salvos: caracterizacao_micro.csv, micro_LQ.csv")
