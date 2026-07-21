.PHONY: paper paper-v1 figuras clean

# Artigo principal (v3 - caracterizacao da estrutura produtiva)
paper:
	cd paper && pdflatex es_estrutura_produtiva.tex && bibtex es_estrutura_produtiva || true && pdflatex es_estrutura_produtiva.tex && pdflatex es_estrutura_produtiva.tex

# Versao arquivada (v1 - economia-plataforma)
paper-v1:
	cd paper && pdflatex es_insumo_produto.tex && bibtex es_insumo_produto || true && pdflatex es_insumo_produto.tex && pdflatex es_insumo_produto.tex

# Figuras e tabelas do artigo (v3): regeneradas dos CSVs versionados em pesquisa/outputs/
figuras:
	python pesquisa/11_fig_sankey.py
	python pesquisa/19_fig_caracterizacao.py
	python pesquisa/21_fig_micro.py
	python pesquisa/27_tab_multiplicadores.py

# Artes da v1/slides (fluxo spillover/feedback e smile curve, em figuras/)
figuras-v1:
	python src/make_figuras.py

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg *.toc
