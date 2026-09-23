report.pdf: main.tex figures/result.pdf
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	xelatex -interaction=nonstopmode -halt-on-error main.tex

clean:
	del /Q *.aux *.log *.out *.toc *.synctex.gz 2>NUL
