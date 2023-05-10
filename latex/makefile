
default:
	@mkdir -p work pdf anki
	@./日本語.py
	$(MAKE) findtex
	$(MAKE) tidy

findtex:
	@#lf *.tex *.pdf
	@#$(MAKE) $(patsubst %.tex,%.pdf,$(wildcard *.tex))
	$(foreach item,$(wildcard *.tex),$(MAKE) $(patsubst %.tex,%.pdf,$(item));)
	@#lf *.tex *.pdf

tidy:
	$(foreach item,$(wildcard *.apkg),mv $(item) anki/;)
	@mv 日本語*.tex work/
	$(foreach item,$(wildcard *.aux *.log),mv $(item) work/;)
	$(foreach item,$(wildcard *.pdf),mv $(item) pdf/;)

clean:
	rm -rf anki work pdf

.PHONY: tidy default clean

%.pdf : %.tex
	pdflatex $<
	@#mv $*.aux $*.log work/
	@#mv $@ pdf/

