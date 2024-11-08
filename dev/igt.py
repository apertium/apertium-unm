#!/usr/bin/env python3

import pandas as pd
import re

form = "new<v><tv><aa><dir><p3><sg><o_pl>"  # new<v><tv><aa><dir><p3><sg><o_pl>:wëneyook"
igtFile = "../apertium-unm.unm.igt"

#with open(igtFile, 'r') as igtF:
#	columns = csv.reader(igtF, delimiter="\t")

igtConv = pd.read_csv(igtFile, sep='\t')

#for line in igtF:
#	

#print(igtConv[igtConv['POS'] == 'v']['entryPOS'])
#print(igtConv.query('POS == "v"')['entryPOS'].item())

lemma = re.match('(.*?)<.*', form).groups()[0]
pos = re.match('.*?<(.*?)>.*', form).groups()[0]
gramtags = re.match('.*?<.*?><(.*)>$', form).groups()[0]
gramtags = re.sub('><', '.', gramtags)

#print(lemma, pos, gramtags)

entryPOS = ""
IGT = ""

if (len(igtConv.query('POS == "'+pos+'"')['entryPOS']) > 0):
	print(pos, igtConv.query('POS == "'+pos+'"')['entryPOS'].item())

accumulated_tag = ""
for tag in gramtags.split("."):
	#print(tag)
	if accumulated_tag == "":
		accumulated_tag = tag
	else:
		accumulated_tag += tag
	searchTags = '.'.join(accumulated_tag)
	
	#if accumulated_tag in 

