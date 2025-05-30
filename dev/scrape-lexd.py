#!/usr/bin/env python3

import os
import re

lang1="unm"
lang2="eng"
reGloss = re.compile("\"(.*)\"")
entryline = "<e><l>{}{}</l><r>{}{}</r></e>"
tagtemplate = "<s n=\"{}\"/>"

taglist = {
	"AdjMorph": (["adj"], ["adj"]),
	"Preverb-Lex": (["vaux"], ["vbmod"]),
	"NounRoot-Anim": (["n", "aa"], ["n"]),
	"NounRoot-Inan": (["n", "nn"], ["n"]),
	"NounRoot-Family(2)": (["n", "nn"], ["n"]),
	"VerbRootAI(2)": (["v", "iv", "aa"], ["vblex"]),
	"VerbRootTI(2)": (["v", "tv", "nn"], ["vblex"]),
	"VerbRootTA(2)": (["v", "tv", "aa"], ["vblex"]),
	"AdjLex": (["v", "iv", "nn"], ["vblex"]),
	"AdjLex-Cooking": (["v", "iv", "nn"], ["vblex"]),
	"Determiners(2)": (["det"], ["det"]),  # get subcat from second column
	"Pronouns(2)": (["prn"], ["prn"]),
	"AdvLex": (["adv"], ["adv"]),
	"CnjLex(2)": (),  # get cat from second column
	"Misc": (),
	"Prepositions": (["pr"], ["pr"]),
	"NumberLex": (["num"], ["num"]),
	"IjLex": (["ij"], ["ij"]),
}

with open(os.path.join("../", "apertium-"+lang1+"."+lang1+".lexd"), 'r') as lexd:
	tags = None
	for lexdline in lexd.readlines():
		if "Dir/LR" not in lexdline:
			line = lexdline.split("#")
			uncommentedline = line[0].strip()

			if "LEXICON" in uncommentedline:
				lexname = uncommentedline.split(" ")[1]
				if lexname in taglist:
					tags = taglist[lexname]
				else:
					tags = None

				#print(tags)
			elif "PATTERN" in uncommentedline and "PATTERNS" not in uncommentedline:
				tags = None
			else:
				if tags:
					lang1tags = ""
					lang2tags = ""
					for tag in tags[0]:
						lang1tags += tagtemplate.format((tag))
					for tag in tags[1]:
						lang2tags += tagtemplate.format((tag))
					if ":" in lexdline:
						lang1lemma = uncommentedline.split(':')[0]
						lang1lemma = lang1lemma.replace("\\ ", "<b/>")
						if len(line)>1:
							result = reGloss.search(line[1].strip())
							if result:
								lang2lemmas = result.group(1)
								for lemma in re.split("[,;]", lang2lemmas):
									lemma = re.sub("\(.*?\)", "", lemma)
									lemma = lemma.strip(' !')
									lang2lemma = lemma.replace(" ", "<b/>")
									line = entryline.format(lang1lemma, lang1tags, lang2lemma, lang2tags)
									print(line)

