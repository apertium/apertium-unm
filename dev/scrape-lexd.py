#!/usr/bin/env python3

import os

lang1="unm"
lang2="eng"

taglist = {
	"AdjMorph": (["adj"], ["adj"]),
	"Preverb-Lex": (["vaux"], ["vaux"]),
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
	for lexdline in lexd.readlines():
		line = lexdline.split("#")[0].strip()
		if "LEXICON" in line:
			lexname = line.split(" ")[1]
			if lexname in taglist:
				tags = taglist[lexname]
			else:
				print(lexname)
			
