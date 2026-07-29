# -*- coding: utf-8 -*-
"""
27_tab_multiplicadores.py — emite a tabela LaTeX dos multiplicadores dos 26 setores
do ES a partir de outputs/es_caracterizacao_2008.csv (reprodutivel; o artigo faz
\\input dela). Colunas: setor, multiplicadores de producao, emprego e renda, cada
um nos tipos I e II. Ordena pelo multiplicador de producao de tipo I e fecha com a
media simples dos 26 setores.

O multiplicador de emprego vem do CSV por R$ 1 de demanda final; o artigo reporta
por R$ 1 milhao, dai a divisao por 1e6 em EMP_ESCALA.

Paths portaveis (ao contrario de 12_tab_setores.py, que fixa o diretorio da maquina
do autor): tudo relativo a este arquivo. Escreve nas duas copias do pacote, para
que overleaf/ e paper/ nao precisem ser espelhados a mao.
"""
import os, csv

AQUI  = os.path.dirname(os.path.abspath(__file__))
RAIZ  = os.path.dirname(AQUI)
OUT   = os.path.join(AQUI, "outputs")
DEST  = [os.path.join(RAIZ, "overleaf"), os.path.join(RAIZ, "paper")]

EMP_ESCALA = 1e6  # empregos por R$ 1 -> por R$ 1 milhao

SHORT = {
    "Agricultura, silvicultura, exploração florestal": "Agricultura/silvicultura",
    "Pecuária e pesca": "Pecuária e pesca", "Mineração": "Mineração",
    "Alimentos, bebidas e fumo": "Alimentos/bebidas/fumo",
    "Têxtil, vestuário e calçados": "Têxtil/vestuário",
    "Madeira, papel e impressão": "Madeira/papel",
    "Refino de petróleo, coque e álcool": "Refino/coque/álcool",
    "Outros produtos químicos e farmacêuticos": "Químicos/farmacêuticos",
    "Artigos de borracha e plástico": "Borracha/plástico",
    "Cimento e outros produtos de minerais não-metálicos": "Min. não-metálicos",
    "Metalurgia": "Metalurgia", "Máquinas e equipamentos": "Máquinas/equip.",
    "Material elétrico e eletrônicos": "Mat. elétrico/eletrônicos",
    "Material de transporte": "Material de transporte",
    "Indústrias diversas": "Indústrias diversas",
    "Eletricidade e gás, água, esgoto e limpeza urbana": "Eletricidade/gás/água",
    "Construção": "Construção", "Comércio": "Comércio",
    "Transporte, armazenagem e correio": "Transporte/armazenagem",
    "Serviços privados": "Serviços privados",
    "Intermediação financeira e seguros": "Financeiro/seguros",
    "Serviços imobiliários e aluguel": "Imobiliário/aluguel",
    "Serviços de alojamento e alimentação": "Alojamento/alimentação",
    "Educação mercantil e pública": "Educação", "Saúde mercantil e pública": "Saúde",
    "Administração pública e seguridade social": "Adm. pública",
}

rows = list(csv.DictReader(open(os.path.join(OUT, "es_caracterizacao_2008.csv"), encoding="utf-8")))
def f(r, c): return float(r[c])
rows.sort(key=lambda r: -f(r, "mult_prod_I"))

def br(x, d): return f"{x:.{d}f}".replace(".", ",")

# (coluna do csv, casas decimais, escala)
COLS = [("mult_prod_I", 2, 1.0), ("mult_prod_II", 2, 1.0),
        ("mult_emp_I",  1, EMP_ESCALA), ("mult_emp_II",  1, EMP_ESCALA),
        ("mult_renda_I", 3, 1.0), ("mult_renda_II", 3, 1.0)]

def celulas(r):
    return " & ".join(br(f(r, c) / s, d) for c, d, s in COLS)

L = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
     r"& \multicolumn{2}{c}{Produção} & \multicolumn{2}{c}{Emprego}"
     r" & \multicolumn{2}{c}{Renda}\\",
     r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}",
     r"Setor & Tipo I & Tipo II & Tipo I & Tipo II & Tipo I & Tipo II\\",
     r"\midrule"]
for r in rows:
    L.append(f"{SHORT.get(r['setor'], r['setor'])} & {celulas(r)}\\\\")
L.append(r"\midrule")
L.append(r"\textbf{Média (simples)} & " + " & ".join(
    br(sum(f(r, c) / s for r in rows) / len(rows), d) for c, d, s in COLS) + r"\\")
L.append(r"\bottomrule")
L.append(r"\end{tabular}")

for d in DEST:
    with open(os.path.join(d, "tab_multiplicadores.tex"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("salvo:", os.path.relpath(os.path.join(d, "tab_multiplicadores.tex"), RAIZ))

m = lambda c, s: sum(f(r, c) / s for r in rows) / len(rows)
print(f"media producao  I/II: {m('mult_prod_I',1):.2f} / {m('mult_prod_II',1):.2f}")
print(f"media emprego   I/II: {m('mult_emp_I',EMP_ESCALA):.1f} / {m('mult_emp_II',EMP_ESCALA):.1f}")
print(f"media renda     I/II: {m('mult_renda_I',1):.3f} / {m('mult_renda_II',1):.3f}")
