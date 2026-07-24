.PHONY: paper paper-v1 figuras clean lista lista-selftest lista-auditoria

# Lista de exercícios (2026/1): requer as MIPs nacionais em dados/ (ver lista/README.md)
lista:
	python lista/resolver_lista.py --m2010 "dados/MIP-BR 2010 (Nível 68).xlsm" --m2020 "dados/MIP-BR 2020 (Nível 68).xlsm"

lista-selftest:
	python lista/resolver_lista.py --selftest

# Auditoria HARD da lista contra as abas de cálculo do professor (dentro dos .xlsm)
lista-auditoria:
	python lista/auditoria.py

# Artigo principal (v3 - caracterizacao da estrutura produtiva)
paper:
	cd paper && pdflatex es_estrutura_produtiva.tex && bibtex es_estrutura_produtiva || true && pdflatex es_estrutura_produtiva.tex && pdflatex es_estrutura_produtiva.tex

# Versao arquivada (v1 - economia-plataforma)
paper-v1:
	cd paper && pdflatex es_insumo_produto.tex && bibtex es_insumo_produto || true && pdflatex es_insumo_produto.tex && pdflatex es_insumo_produto.tex

# Figuras do artigo (v3): regeneradas dos CSVs versionados em pesquisa/outputs/
figuras:
	python pesquisa/09_fig_upstreamness.py
	python pesquisa/11_fig_sankey.py
	python pesquisa/16_fig_fractal.py
	python pesquisa/19_fig_caracterizacao.py
	python pesquisa/21_fig_micro.py

# Artes da v1/slides (fluxo spillover/feedback e smile curve, em figuras/)
figuras-v1:
	python src/make_figuras.py

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg *.toc
