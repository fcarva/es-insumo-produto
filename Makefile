.PHONY: paper figuras clean

paper:
	cd paper && pdflatex es_insumo_produto.tex && bibtex es_insumo_produto || true && pdflatex es_insumo_produto.tex && pdflatex es_insumo_produto.tex

figuras:
	python src/make_figuras.py

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg *.toc
