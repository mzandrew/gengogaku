#!/usr/bin/env python3

# written 2023-04-14 by mza
# based on https://github.com/kerrickstaley/genanki
# last updated 2023-04-25 by mza

# "I'm-learning-Japanese-I-think-I'm-learning-Japanese-I-really-think-so"

# usage:
# ./日本語.py && pdflatex 日本語.tex

# ---------- user settings ----------

modes = [ "anki", "latex" ]

anki_output_file = "日本語.apkg"
latex_output_file = "日本語.tex"

#order = "natural"
order = "hiragana-alphabetical"
#order = "lesson"

FONT_SIZE = "12pt" # allowed values in extarticle are 8pt, 9pt, 10pt, 11pt, 12pt, 14pt, 17pt and 20pt
NUMBER_OF_LINES_PER_TABULAR = 46

# -----------------------------------

import re

entries = []
duplicate_entries = []

def parse_csv_file():
	global entries
	line_number = 0
	count = 0
	with open("日本語.csv") as my_file:
		for line in my_file:
			line = line.rstrip('\n')
			line_number += 1
			if 1==line_number:
				continue
			if ""==line:
				continue
			if '#'==line[0]:
				continue
			#print(line)
			items = re.split('、|,', line)
			#print(str(items))
			if 0==len(items):
				continue
			hiragana = ""
			english = ""
			kanji = ""
			kanji_furigana = ""
			lesson = ""
			part_of_speech = ""
			if 0<len(items):
				hiragana = items[0]
			if 1<len(items):
				english = items[1]
			if 2<len(items):
				kanji = items[2]
			if 3<len(items):
				kanji_furigana = items[3]
			if 4<len(items):
				lesson = items[4]
			if 5<len(items):
				part_of_speech = items[5]
			entries.append([hiragana, english, kanji, kanji_furigana, lesson, part_of_speech])
			count += 1
	print("found " + str(count) + " total entries")

def filter_lesson(lesson_strings):
	global entries
	temporary = []
	for entry in entries:
		for lesson_string in lesson_strings:
			match = re.search(lesson_string, entry[4])
			if match:
				temporary.append(entry)
	entries = temporary

def sort_by(order):
	global entries
	if "hiragana-alphabetical"==order:
		entries = sorted(entries)
		for entry in entries:
			print(str(entry[0]))
	elif "lesson"==order:
		entries = sorted(entries, key=lambda x: x[4])
		for entry in entries:
			print(str(entry[4]) + " " + str(entry[0]))
	else:
		for entry in entries:
			print(str(entry[0]))

def deduplicate():
	global entries
	global duplicate_entries
	new_entries = []
	hiragana = []
	for entry in entries:
		if entry[0] not in hiragana:
			hiragana.append(entry[0])
			new_entries.append(entry)
		else:
			print("duplicate!: " + str(entry[0]))
			duplicate_entries.append(entry)
	#uniq = set(entries)
	#entries = list(uniq)
	entries = new_entries

anki_style = """
.card {
	font-size: 48px;
	text-align: center;
	color: yellow;
	background-color: black;
}
"""

def do_anki():
	import genanki
	vocab_3way_deck = genanki.Deck(2342356, 'vocab 3-way')
	vocab_3way_fields = [
		{'name': 'kanji'},
		{'name': 'hiragana'},
		{'name': 'English'}
	]
	vocab_3way_cards = [
		{ 'name': 'kanji',    'qfmt': '{{kanji}}',    'afmt': '{{FrontSide}}<hr id="answer">{{hiragana}}<hr>{{English}}' },
		{ 'name': 'hiragana', 'qfmt': '{{hiragana}}', 'afmt': '{{FrontSide}}<hr id="answer">{{kanji}}   <hr>{{English}}' },
		{ 'name': 'English',  'qfmt': '{{English}}',  'afmt': '{{FrontSide}}<hr id="answer">{{kanji}}   <hr>{{hiragana}}' }
	]
	vocab_3way_model = genanki.Model(293487, '3-way vocab', fields=vocab_3way_fields, templates=vocab_3way_cards, css=anki_style)
	vocab_3way_count = 0
	vocab_3way_entries = []
	#print(str(vocab_3way_model))
	kanji_base_deck = genanki.Deck(6463537, 'kanji base')
	kanji_base_fields = [
		{'name': 'kanji'},
		{'name': 'hiragana'},
		{'name': 'English'}
	]
	kanji_base_cards = [
		{ 'name': 'kanji',    'qfmt': '{{kanji}}',    'afmt': '{{FrontSide}}<hr id="answer">{{hiragana}}<hr>{{English}}' },
		#{ 'name': 'hiragana', 'qfmt': '{{hiragana}}', 'afmt': '{{FrontSide}}<hr id="answer">{{kanji}}   <hr>{{English}}' },
		{ 'name': 'English',  'qfmt': '{{English}}',  'afmt': '{{FrontSide}}<hr id="answer">{{kanji}}   <hr>{{hiragana}}' }
	]
	kanji_base_model = genanki.Model(92929237, 'kanji base', fields=kanji_base_fields, templates=kanji_base_cards, css=anki_style)
	kanji_base_count = 0
	kanji_base_entries = []
	#print(str(kanji_base_model))
	vocab_deck = genanki.Deck(3563948, 'vocab')
	vocab_fields = [
		{'name': 'hiragana'},
		{'name': 'English'}
	]
	vocab_cards = [
		{ 'name': 'hiragana', 'qfmt': '{{hiragana}}', 'afmt': '{{FrontSide}}<hr id="answer">{{English}}' },
		{ 'name': 'English',  'qfmt': '{{English}}',  'afmt': '{{FrontSide}}<hr id="answer">{{hiragana}}' }
	]
	vocab_model = genanki.Model(487293, 'vocab', fields=vocab_fields, templates=vocab_cards, css=anki_style)
	vocab_count = 0
	vocab_entries = []
	for hiragana, english, kanji, kanji_furigana, lesson, part_of_speech in entries:
		my_fields = [ hiragana, english ]
		#print(str(my_fields))
		if not "kanji-base"==part_of_speech:
			vocab_entries.append(my_fields)
			vocab_count += 1
		if not ""==kanji:
			my_fields = [ kanji, hiragana, english ]
			#print(str(my_fields))
			if "kanji-base"==part_of_speech:
				kanji_base_entries.append(my_fields)
				kanji_base_count += 1
			else:
				vocab_3way_entries.append(my_fields)
				vocab_3way_count += 1
	for my_fields in vocab_entries:
		my_note = genanki.Note(model=vocab_model, fields=my_fields[0:2])
		vocab_deck.add_note(my_note)
	for my_fields in vocab_3way_entries:
		my_note = genanki.Note(model=vocab_3way_model, fields=my_fields[0:3])
		vocab_3way_deck.add_note(my_note)
	for my_fields in kanji_base_entries:
		my_note = genanki.Note(model=kanji_base_model, fields=my_fields[0:3])
		kanji_base_deck.add_note(my_note)
	decks = []
	if vocab_3way_count:
		print("found " + str(vocab_3way_count) + " 3-way vocab")
		decks.append(vocab_3way_deck)
	if kanji_base_count:
		print("found " + str(kanji_base_count) + " 3-way kanji")
		decks.append(kanji_base_deck)
	if vocab_count:
		print("found " + str(vocab_count) + " total vocab")
		decks.append(vocab_deck)
	genanki.Package(decks).write_to_file(anki_output_file)

latex_header = r"""\documentclass[""" + FONT_SIZE + r""",twocolumn]{extarticle}
\usepackage{CJKutf8}
\usepackage[overlap,CJK]{ruby}
\usepackage[table]{xcolor}
\renewcommand{\rubysep}{-0.2ex}
\renewcommand{\rubysize}{0.7}
\pagenumbering{gobble}
\usepackage[portrait,left=12mm,right=8mm,top=3mm,bottom=3mm]{geometry}
\definecolor{verylightgray}{rgb}{0.9, 0.9, 0.9}
\begin{document}
\begin{CJK}{UTF8}{min}
\rowcolors{1}{white}{verylightgray}
%\begin{tabular}{l|l}

"""
latex_footer = r"""
%\end{tabular}
\end{CJK}
\end{document}

"""

def latex_start_tabular():
	return "\n" + r"""\begin{tabular}{l|l}"""

def latex_end_tabular():
	return r"""\end{tabular}""" + "\n"

def tabular_break():
	return latex_end_tabular() + "\n" + latex_start_tabular() + "\n"

def show_hiragana_alphabetical_order():
	return "\nあかさたなはまやらわん\n"

def do_latex():
	latex_entries = []
	for hiragana, english, kanji, kanji_furigana, lesson, part_of_speech in entries:
		japanese = hiragana
		if not ""==kanji:
			japanese = kanji
		if not ""==kanji_furigana and not "\\ruby{}{}"==kanji_furigana:
			japanese = kanji_furigana
		my_fields = [ hiragana, japanese, english, lesson, part_of_speech ]
		if not "kanji-base"==part_of_speech:
			latex_entries.append(my_fields)
	latex_count = len(latex_entries)
	print("found " + str(latex_count) + " latex entries")
	line_count_so_far_for_this_tabular = 0
	with open(latex_output_file, "w") as my_file:
		my_file.write(latex_header)
		#my_file.write(show_hiragana_alphabetical_order())
		my_file.write(latex_start_tabular())
		for entry in latex_entries:
			line_count_so_far_for_this_tabular += 1
			#print(entry)
			#print(str(entry[1]) + " " + str(entry[2]))
			my_file.write("\ " + str(entry[1]) + "&\small{" + str(entry[2]) + "}\\\\\n")
			if NUMBER_OF_LINES_PER_TABULAR<=line_count_so_far_for_this_tabular:
				my_file.write(tabular_break())
				line_count_so_far_for_this_tabular = 0
		my_file.write(latex_end_tabular())
		my_file.write(latex_footer)

def summary():
	if len(duplicate_entries):
		print("duplicate entries:")
		for entry in duplicate_entries:
			print(str(entry))
	else:
		print("no duplicate entries!")

parse_csv_file()
deduplicate()
#filter_lesson(["lesson8.1", "lesson8.3"])
#filter_lesson(["lesson8"])
#filter_lesson(["lesson6"])
sort_by(order)
for mode in modes:
	if "anki"==mode:
		do_anki()
	if "latex"==mode:
		do_latex()
summary()

