.PHONY: paper paper-v1 figuras clean

# Artigo principal (v3 - caracterizacao da estrutura produtiva)
paper:
	cd paper && pdflatex es_estrutura_produtiva.tex && bibtex es_estrutura_produtiva || true && pdflatex es_estrutura_produtiva.tex && pdflatex es_estrutura_produtiva.tex

# Versao arquivada (v1 - economia-plataforma)
paper-v1:
	cd paper && pdflatex es_insumo_produto.tex && bibtex es_insumo_produto || true && pdflatex es_insumo_produto.tex && pdflatex es_insumo_produto.tex

figuras:
	python src/make_figuras.py

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg *.toc
