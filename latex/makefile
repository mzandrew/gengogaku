
%.pdf : %.tex
	pdflatex $<
	@mv $*.aux $*.log work/
	@mv $@ pdf/

default:
	@mkdir -p work pdf
	./日本語.py
	lf *.tex
	@mv *.apkg anki/
	$(MAKE) $(patsubst %.tex,%.pdf,$(wildcard *.tex))
	@mv 日本語*.tex work/
	@#mv *.aux *.log work/
	@#mv *.pdf pdf/

