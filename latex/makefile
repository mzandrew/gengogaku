list = jpn101-jpn102-kanji.tex jpn102-grammar-notes.tex jpn102-verbs-table.tex

%.pdf : %.tex
	pdflatex $<

%.tex : %.csv %.py
	./日本語.py

default:
	$(MAKE) $(patsubst %.tex,%.pdf,$(list))
	$(MAKE) 日本語.pdf

