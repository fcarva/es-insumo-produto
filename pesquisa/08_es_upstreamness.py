# -*- coding: utf-8 -*-
"""
08_es_upstreamness.py — A2 (headline): upstreamness da PAUTA EXPORTADORA do ES,
ponderando a upstreamness setorial do Brasil (WIOD 2014) pela composicao das
exportacoes capixabas (coluna Export da MIP-ES-BR). Alvo do paper: ~3,19.

LIMITE (B3): o ES nao tem assento no WIOD. Aproximamos via tecnologia do Brasil +
peso da pauta do ES. A concordancia 26 setores (BR-IO) -> 56 (WIOD) e aproximada
(setor primario representativo por setor); declarar no paper.
"""
import os, csv, sys
import numpy as np
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows (cp1252) nao encoda alguns caracteres nos prints; forca UTF-8

OUT = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
MIP = r"C:/Users/DELL/Downloads/Material IO/Matrizes/MIP-ES-BR (2008).xlsx"

# upstreamness setorial do Brasil (D=1..56) ja calculada em 07
ub = {}
for row in csv.DictReader(open(os.path.join(OUT, "brasil_upstreamness.csv"), encoding="utf-8")):
    ub[int(row["setor_wiod_idx"])] = float(row["upstreamness"])

# concordancia 26 setores BR-IO -> setor WIOD representativo (D, 1..56)
CONC = {1:1, 2:1, 3:4, 4:5, 5:6, 6:8, 7:10, 8:11, 9:13, 10:14, 11:15, 12:19,
        13:17, 14:20, 15:22, 16:24, 17:27, 18:29, 19:31, 20:45, 21:41, 22:44,
        23:36, 24:52, 25:53, 26:51}
SET_BR = ["Agric/silvic","Pecuaria/pesca","Mineracao","Alimentos","Textil",
          "Madeira/papel","Refino","Quimicos","Borracha/plast","Min nao-metal",
          "Metalurgia","Maquinas","Eletro","Transporte(mat)","Ind diversas",
          "Eletric/gas/agua","Construcao","Comercio","Transp/armaz","Serv privados",
          "Interm financeira","Imobiliario","Aloj/alim","Educacao","Saude","Adm publica"]

# pauta exportadora do ES: coluna 58 (Export) da MIP-ES-BR, linhas 7-32 (26 setores ES)
wb = openpyxl.load_workbook(MIP, data_only=True); ws = wb["ES-BR"]
def num(v): return float(v) if isinstance(v, (int, float)) else 0.0
es_exp = np.array([num(ws.cell(r, 58).value) for r in range(7, 33)]); wb.close()
share = es_exp / es_exp.sum()

# upstreamness de cada setor BR-IO via concordancia
u_set = np.array([ub[CONC[s+1]] for s in range(26)])
es_up = float((share * u_set).sum())

print("="*62)
print("UPSTREAMNESS DA PAUTA EXPORTADORA DO ES (via WIOD 2014 / Brasil)")
print("="*62)
print(f"  ES (ponderado pela pauta de exportacao): {es_up:.2f}   (paper: 3,12)")
print(f"  Brasil (media ponderada producao)      : 1,91")
print(f"  Mundo                                  : 2,31")
print("-"*62)
print("  Top setores da pauta do ES (peso na exportacao x upstreamness):")
for k in np.argsort(share)[::-1][:8]:
    print(f"    {share[k]:5.1%}  U={u_set[k]:4.2f}  {SET_BR[k]}")
print("="*62)

with open(os.path.join(OUT, "es_upstreamness.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh); wr.writerow(["setor_BR", "share_export_%", "wiod_D", "upstreamness"])
    for s in range(26):
        wr.writerow([SET_BR[s], f"{share[s]*100:.2f}", CONC[s+1], f"{u_set[s]:.3f}"])
    wr.writerow(["ES_PAUTA", "100.00", "", f"{es_up:.3f}"])
print("salvo: es_upstreamness.csv")
