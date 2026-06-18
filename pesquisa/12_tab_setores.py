# -*- coding: utf-8 -*-
"""
12_tab_setores.py — emite a tabela LaTeX completa dos 26 setores do ES a partir
de outputs/es_setores_resultados.csv (reprodutivel; o artigo faz \\input dela).
Colunas: setor, multiplicador de producao, vazamento de producao e de emprego,
ligacoes de Rasmussen-Hirschman (tras/frente). Ordena por vazamento de producao
e adiciona medias simples e ponderada pela producao.
"""
import os, csv

OUT   = r"C:/Users/DELL/Documents/es-insumo-produto/pesquisa/outputs"
PAPER = r"C:/Users/DELL/Documents/es-insumo-produto/paper"

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

rows = list(csv.DictReader(open(os.path.join(OUT, "es_setores_resultados.csv"), encoding="utf-8")))
def f(r, c): return float(r[c])
rows.sort(key=lambda r: f(r, "vazamento_prod_%"))

cols = ["mult_producao", "vazamento_prod_%", "vazamento_emprego_%", "ligacao_tras", "ligacao_frente"]
vbp = [f(r, "VBP") for r in rows]; tot = sum(vbp)
def simples(c): return sum(f(r, c) for r in rows) / len(rows)
def pond(c):    return sum(f(r, c) * w for r, w in zip(rows, vbp)) / tot
def br(x, d):   return f"{x:.{d}f}".replace(".", ",")

L = [r"\begin{tabular}{lrrrrr}", r"\toprule",
     r"Setor & $O_j$ & Vaz.\ prod.\ (\%) & Vaz.\ empr.\ (\%) & Lig.\ trás & Lig.\ frente\\",
     r"\midrule"]
for r in rows:
    nm = SHORT.get(r["setor"], r["setor"])
    L.append(f"{nm} & {br(f(r,'mult_producao'),2)} & {br(f(r,'vazamento_prod_%'),1)} & "
             f"{br(f(r,'vazamento_emprego_%'),1)} & {br(f(r,'ligacao_tras'),2)} & "
             f"{br(f(r,'ligacao_frente'),2)}\\\\")
L.append(r"\midrule")
L.append(r"\textbf{Média (simples)} & " + " & ".join(
    br(simples(c), 2 if c in ("mult_producao","ligacao_tras","ligacao_frente") else 1) for c in cols) + r"\\")
L.append(r"\textbf{Média (ponderada)} & " + " & ".join(
    br(pond(c), 2 if c in ("mult_producao","ligacao_tras","ligacao_frente") else 1) for c in cols) + r"\\")
L.append(r"\bottomrule"); L.append(r"\end{tabular}")

with open(os.path.join(PAPER, "tab_setores.tex"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print(f"vazamento producao -> simples {simples('vazamento_prod_%'):.1f}% | ponderada {pond('vazamento_prod_%'):.1f}%")
print("salvo: paper/tab_setores.tex")
