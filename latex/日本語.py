#!/usr/bin/env python3

# written 2023-04-14 by mza
# based on https://github.com/kerrickstaley/genanki
# last updated 2023-05-10 by mza

# "I'm-learning-Japanese-I-think-I'm-learning-Japanese-I-really-think-so"

import re
import random
import genanki

def parse_csv_file():
	global entries
	entries = []
	duplicate_entries = []
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

def filter_include_lessons(lesson_strings):
	global entries
	temporary = []
	for entry in entries:
		for lesson_string in lesson_strings:
			match = re.search(lesson_string, entry[4])
			if match:
				temporary.append(entry)
	entries = temporary

def filter_include_parts_of_speech(parts_of_speech):
	global entries
	temporary = []
	for entry in entries:
		should_include = False
		for part_of_speech in parts_of_speech:
			match = re.search(part_of_speech, entry[5])
			if match:
				should_include = True
#			else:
#				print(entry[5])
		if should_include:
			temporary.append(entry)
#	print(str(len(temporary)))
	entries = temporary

def filter_exclude_parts_of_speech(parts_of_speech):
	global entries
	temporary = []
	for entry in entries:
		should_include = True
		for part_of_speech in parts_of_speech:
			match = re.search(part_of_speech, entry[5])
			if match:
				should_include = False
		if should_include:
			temporary.append(entry)
	entries = temporary

def sort_by(order):
	global entries
	if "hiragana-alphabetical"==order:
		entries = sorted(entries)
#		for entry in entries:
#			print(str(entry[0]))
	elif "lesson"==order:
		entries = sorted(entries, key=lambda x: x[4])
#		for entry in entries:
#			print(str(entry[4]) + " " + str(entry[0]))
	elif "shuffle"==order:
		random.shuffle(entries)
#	else:
#		for entry in entries:
#			print(str(entry[0]))

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

def summary():
	if len(duplicate_entries):
		print("found " + str(len(duplicate_entries)) + " duplicate entries:")
		for entry in duplicate_entries:
			print(str(entry))
	else:
		print("no duplicate entries!")

def anki_style():
	return """
.card {
	font-size: 48px;
	text-align: center;
	color: yellow;
	background-color: black;
}
"""

def setup_anki_decks():
	global vocab_3way_deck
	global vocab_3way_model
	global kanji_base_deck
	global kanji_base_model
	global vocab_deck
	global vocab_model
	vocab_3way_deck = genanki.Deck(random.randrange(1,12345678), 'vocab 3-way')
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
	vocab_3way_model = genanki.Model(random.randrange(1,12345678), '3-way vocab', fields=vocab_3way_fields, templates=vocab_3way_cards, css=anki_style())
	#print(str(vocab_3way_model))
	kanji_base_deck = genanki.Deck(random.randrange(1,12345678), 'kanji base')
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
	kanji_base_model = genanki.Model(random.randrange(1,12345678), 'kanji base', fields=kanji_base_fields, templates=kanji_base_cards, css=anki_style())
	#print(str(kanji_base_model))
	vocab_deck = genanki.Deck(random.randrange(1,12345678), 'vocab')
	vocab_fields = [
		{'name': 'hiragana'},
		{'name': 'English'}
	]
	vocab_cards = [
		{ 'name': 'hiragana', 'qfmt': '{{hiragana}}', 'afmt': '{{FrontSide}}<hr id="answer">{{English}}' },
		{ 'name': 'English',  'qfmt': '{{English}}',  'afmt': '{{FrontSide}}<hr id="answer">{{hiragana}}' }
	]
	vocab_model = genanki.Model(random.randrange(1,12345678), 'vocab', fields=vocab_fields, templates=vocab_cards, css=anki_style())

def latex_header(font_size):
	return r"""\documentclass[""" + font_size + r""",twocolumn]{extarticle}
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

def latex_footer():
	return r"""
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

def write_latex_file(filename, number_of_lines_per_tabular, font_size):
	latex_entries = []
	for hiragana, english, kanji, kanji_furigana, lesson, part_of_speech in entries:
		japanese = hiragana
		if not ""==kanji:
			japanese = kanji
		if not ""==kanji_furigana and not "\\ruby{}{}"==kanji_furigana:
			japanese = kanji_furigana
		my_fields = [ hiragana, japanese, english, lesson, part_of_speech ]
		#if not "kanji-base"==part_of_speech:
		latex_entries.append(my_fields)
	latex_count = len(latex_entries)
	print("found " + str(latex_count) + " latex entries")
	line_count_so_far_for_this_tabular = 0
	with open(filename, "w") as my_file:
		my_file.write(latex_header(font_size))
		#my_file.write(show_hiragana_alphabetical_order())
		my_file.write(latex_start_tabular())
		for entry in latex_entries:
			line_count_so_far_for_this_tabular += 1
			#print(entry)
			#print(str(entry[1]) + " " + str(entry[2]))
			my_file.write("\ " + str(entry[1]) + "&\small{" + str(entry[2]) + "}\\\\\n")
			if number_of_lines_per_tabular<=line_count_so_far_for_this_tabular:
				my_file.write(tabular_break())
				line_count_so_far_for_this_tabular = 0
		my_file.write(latex_end_tabular())
		my_file.write(latex_footer())

def do_latex():
	# allowed values of font_size in extarticle are 8pt, 9pt, 10pt, 11pt, 12pt, 14pt, 17pt and 20pt
	# order can be: "natural", "hiragana-alphabetical", "lesson" and "shuffle"
	lessons = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
	print("kanji-base:"); parse_csv_file(); filter_include_parts_of_speech(["kanji-base"]); sort_by("natural"); write_latex_file("日本語.kanji-base.tex", 32, "12pt")
	print("kanji-compound:"); parse_csv_file(); filter_include_parts_of_speech(["kanji-compound"]); sort_by("natural"); write_latex_file("日本語.kanji-compound.tex", 32, "12pt")
	print("vocab:"); parse_csv_file(); filter_exclude_parts_of_speech(["kanji-base", "expression", "title", "name", "place", "field_of_study"]); sort_by("hiragana-alphabetical"); write_latex_file("日本語.vocab.tex", 39, "12pt")
	print("verbs:"); parse_csv_file(); filter_include_parts_of_speech(["verb"]); sort_by("hiragana-alphabetical"); write_latex_file("日本語.verbs.tex", 39, "12pt")
	print("everything everywhere all at once:"); parse_csv_file(); sort_by("shuffle"); write_latex_file("日本語.everything.tex", 36, "12pt")
	if do_lesson_by_lesson:
		for lesson in lessons:
			lesson_string = "lesson" + str(lesson)
			parse_csv_file(); filter_include_lessons([lesson_string]); filter_include_parts_of_speech(["kanji-base"]); sort_by("natural"); write_latex_file("日本語." + lesson_string + ".kanji-base.tex", 32, "12pt")
			parse_csv_file(); filter_include_lessons([lesson_string]); filter_include_parts_of_speech(["kanji-compound"]); sort_by("natural"); write_latex_file("日本語." + lesson_string + ".kanji-compound.tex", 32, "12pt")
			parse_csv_file(); filter_include_lessons([lesson_string]); filter_exclude_parts_of_speech(["kanji-base", "expression", "title", "name", "place", "field_of_study"]); sort_by("hiragana-alphabetical"); write_latex_file("日本語." + lesson_string + ".vocab.tex", 39, "12pt")

def do_anki(anki_output_file):
	global vocab_3way_count
	global kanji_base_count
	global vocab_count
	vocab_3way_count = 0
	kanji_base_count = 0
	vocab_count = 0
	vocab_3way_entries = []
	kanji_base_entries = []
	vocab_entries = []
	print("anki:")
	setup_anki_decks()
	parse_csv_file()
	sort_by("shuffle")
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

modes = [ "anki", "latex" ]
do_lesson_by_lesson = False
for mode in modes:
	if "anki"==mode:
		do_anki("日本語.apkg")
	if "latex"==mode:
		do_latex()

#deduplicate()
#summary()

