# -*- coding: utf-8 -*-
"""
27_tab_multiplicadores.py — emite a tabela LaTeX completa de multiplicadores dos
26 setores do ES a partir de outputs/es_caracterizacao_2008.csv (reprodutivel; o
artigo faz \\input dela). Colunas: setor, multiplicadores de producao (I/II), de
emprego (I/II, empregos por R$ 1 milhao) e de renda (I/II, R$ por R$ 1). Ordena
pelo multiplicador de producao de tipo I e adiciona medias simples e ponderada
pelo VBP (VBP de outputs/es_setores_resultados.csv).
"""
import os, csv

BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT   = os.path.join(BASE, "pesquisa", "outputs")
PAPER = os.path.join(BASE, "paper")

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
vbp_by_setor = {r["setor"]: float(r["VBP"]) for r in
                csv.DictReader(open(os.path.join(OUT, "es_setores_resultados.csv"), encoding="utf-8"))}

def f(r, c): return float(r[c])
def emp(r, c): return f(r, c) / 1e6  # empregos por R$ 1 milhao de demanda final
rows.sort(key=lambda r: -f(r, "mult_prod_I"))

vbp = [vbp_by_setor[r["setor"]] for r in rows]; tot = sum(vbp)
def br(x, d): return f"{x:.{d}f}".replace(".", ",")

def vals(r):
    return [f(r, "mult_prod_I"), f(r, "mult_prod_II"),
            emp(r, "mult_emp_I"), emp(r, "mult_emp_II"),
            f(r, "mult_renda_I"), f(r, "mult_renda_II")]
DEC = [2, 2, 1, 1, 2, 2]

L = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
     r" & \multicolumn{2}{c}{Produção} & \multicolumn{2}{c}{Emprego} & \multicolumn{2}{c}{Renda}\\",
     r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}",
     r"Setor & I & II & I & II & I & II\\",
     r"\midrule"]
for r in rows:
    nm = SHORT.get(r["setor"], r["setor"])
    L.append(nm + " & " + " & ".join(br(v, d) for v, d in zip(vals(r), DEC)) + r"\\")
L.append(r"\midrule")
n = len(rows)
simples = [sum(vals(r)[i] for r in rows) / n for i in range(6)]
pond    = [sum(vals(r)[i] * w for r, w in zip(rows, vbp)) / tot for i in range(6)]
L.append(r"\textbf{Média (simples)} & " + " & ".join(br(v, d) for v, d in zip(simples, DEC)) + r"\\")
L.append(r"\textbf{Média (ponderada)} & " + " & ".join(br(v, d) for v, d in zip(pond, DEC)) + r"\\")
L.append(r"\bottomrule"); L.append(r"\end{tabular}")

with open(os.path.join(PAPER, "tab_multiplicadores.tex"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print(f"medias simples: prod I {simples[0]:.2f} | II {simples[1]:.2f} | "
      f"emp I {simples[2]:.1f} | II {simples[3]:.1f} | renda I {simples[4]:.2f} | II {simples[5]:.2f}")
print("salvo: paper/tab_multiplicadores.tex")
