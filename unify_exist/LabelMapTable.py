

def get_label_mappings(lan) -> dict:
	if 'zh' in lan:
		label_map = {'ROOT': 'ROOT', 'TOP': 'TOP', 'NP': 'NP', 'CLP': 'NP', 'LCP': 'NP', 'QP': 'NP', 'VCD': 'VP', 'VCP': 'VP',
					 'VNV': 'VP',
					 'VP': 'VP', 'VPT': 'VP', 'VRD': 'VP', 'VSB': 'VP', 'ADJP': 'AJP', 'DNP': 'AJP', 'DP': 'AJP',
					 'ADVP': 'AVP',
					 'DVP': 'AVP', 'PP': 'PP', 'CP': 'S', 'FRAG': 'S', 'IP': 'S', 'PRN': 'S', 'INTJ': 'X', 'LST': 'X',
					 'UCP': 'X'}
		tag_map = {'AD': 'ADV', 'AS': 'PRT', 'BA': 'X', 'CC': 'CONJ', 'CD': 'NUM', 'CS': 'CONJ', 'DEC': 'PRT',
				   'DEG': 'PRT',
				   'DER': 'PRT', 'DEV': 'PRT', 'DT': 'DET', 'ETC': 'PRT', 'FW': 'X', 'IJ': 'X', 'JJ': 'ADJ', 'LB': 'X',
				   'LC': 'PRT',
				   'M': 'NUM', 'MSP': 'PRT', 'NN': 'NOUN', 'NR': 'NOUN', 'NT': 'NOUN', 'OD': 'NUM', 'ON': 'X',
				   'P': 'ADP',
				   'PN': 'PRON', 'PU': '.', 'SB': 'X', 'SP': 'PRT', 'VA': 'VERB', 'VC': 'VERB', 'VE': 'VERB',
				   'VV': 'VERB', 'X': 'X'}
	
	elif 'en' in lan:
		label_map = {'ROOT': 'ROOT', 'TOP': 'TOP', 'NP': 'NP', 'NAC': 'NP', 'QP': 'NP', 'WHNP': 'NP', 'NX': 'NP', 'VP': 'VP',
					 'ADJP': 'AJP', 'WHADJP': 'AJP',
					 'ADVP': 'AVP', 'WHADVP': 'AVP', 'PRT': 'AVP', 'PP': 'PP', 'WHPP': 'PP', 'S': 'S', 'SBAR': 'S',
					 'SBARQ': 'S', 'SINV': 'S',
					 'SQ': 'S', 'PRN': 'S', 'FRAG': 'S', 'RRC': 'S', 'CONJP': 'CONJP', 'X': 'X', 'INTJ': 'X',
					 'LST': 'X', 'UCP': 'X'}
		tag_map = {'!': '.', '#': '.', '$': '.', "''": '.', '(': '.', ')': '.', ',': '.', '-LRB-': '.', '-RRB-': '.',
				   '.': '.', ':': '.', '?': '.',
				   'CC': 'CONJ', 'CD': 'NUM', 'CD|RB': 'X', 'DT': 'DET', 'EX': 'DET', 'FW': 'X', 'IN': 'ADP',
				   'IN|RP': 'ADP', 'JJ': 'ADJ', 'JJR': 'ADJ',
				   'JJRJR': 'ADJ', 'JJS': 'ADJ', 'JJ|RB': 'ADJ', 'JJ|VBG': 'ADJ', 'LS': 'X', 'MD': 'VERB', 'NN': 'NOUN',
				   'NNP': 'NOUN', 'NNPS': 'NOUN', 'NNS':
					   'NOUN', 'NN|NNS': 'NOUN', 'NN|SYM': 'NOUN', 'NN|VBG': 'NOUN', 'NP': 'NOUN', 'PDT': 'DET',
				   'POS': 'PRT', 'PRP': 'PRON', 'PRP$': 'PRON',
				   'PRP|VBP': 'PRON', 'PRT': 'PRT', 'RB': 'ADV', 'RBR': 'ADV', 'RBS': 'ADV', 'RB|RP': 'ADV',
				   'RB|VBG': 'ADV', 'RN': 'X', 'RP': 'PRT', 'SYM': 'X',
				   'TO': 'PRT', 'UH': 'X', 'VB': 'VERB', 'VBD': 'VERB', 'VBD|VBN': 'VERB', 'VBG': 'VERB',
				   'VBG|NN': 'VERB', 'VBN': 'VERB', 'VBP': 'VERB', 'VBP|TO': 'VERB',
				   'VBZ': 'VERB', 'VP': 'VERB', 'WDT': 'DET', 'WH': 'X', 'WP': 'PRON', 'WP$': 'PRON', 'WRB': 'ADV',
				   '``': '.'}
		
	elif 'de' in lan:
		label_map = {'ROOT': 'ROOT', 'TOP': 'TOP', 'PN':'NP', 'NP': 'NP', 'CNP': 'NP', 'MPN': 'NP', 'NM': 'NP', 'VP': 'VP', 'CVP': 'VP',
					 'VZ': 'VP', 'CVZ': 'VP', 'AP': 'AJP', 'AA': 'AJP', 'CAP': 'AJP', 'MTA': 'AJP', 'AVP': 'AVP',
					 'CAVP': 'AVP', 'PP': 'PP', 'CAC': 'PP', 'CPP': 'PP', 'CCP': 'PP', 'S': 'S', 'CS': 'S', 'CH': 'S',
					 'DL': 'S', 'PSEUDO': 'S', 'CO': 'COP', 'ISU': 'X', 'QL': 'X'}
		tag_map = 	{'$LRB': '.', '$,': '.', '$.': '.', 'ADJA': 'ADJ', 'ADJD': 'ADJ', 'ADV': 'ADV', 'APPO': 'ADP',
					 'APPR': 'ADP', 'APPRART': 'ADP', 'APZR': 'ADP', 'ART': 'DET', 'CARD': 'NUM', 'FM': 'X', 'ITJ': 'X',
					 'KOKOM': 'CONJ', 'KON': 'CONJ', 'KOUI': 'CONJ', 'KOUS': 'CONJ', 'NE': 'NOUN', 'NN': 'NOUN',
					 'NNE': 'NOUN', 'PDAT': 'PRON', 'PDS': 'PRON', 'PIAT': 'PRON', 'PIS': 'PRON', 'PPER': 'PRON',
					 'PPOSAT': 'PRON', 'PPOSS': 'PRON', 'PRELAT': 'PRON', 'PRELS': 'PRON', 'PRF': 'PRON', 'PROAV': 'PRON',
					 'PTKA': 'PRT', 'PTKANT': 'PRT', 'PTKNEG': 'PRT', 'PTKVZ': 'PRT', 'PTKZU': 'PRT', 'PWAT': 'PRON',
					 'PWAV': 'PRON', 'PWS': 'PRON', 'TRUNC': 'X', 'VAFIN': 'VERB', 'VAIMP': 'VERB', 'VAINF': 'VERB',
					 'VAPP': 'VERB', 'VMFIN': 'VERB', 'VMINF': 'VERB', 'VMPP': 'VERB', 'VVFIN': 'VERB', 'VVIMP': 'VERB',
					 'VVINF': 'VERB', 'VVIZU': 'VERB', 'VVPP': 'VERB', 'XY': 'X'}
	
	elif 'fr' in lan:
		label_map = {'ROOT': 'ROOT', 'TOP': 'TOP', 'NP': 'NP', 'VN': 'VP', 'VP': 'VP', 'VPpart': 'VP', 'VPinf': 'VP', 'AP': 'AJP',
					'AdP': 'AVP', 'PP': 'PP', 'SENT': 'S', 'Ssub': 'S', 'Sint': 'S', 'Srel': 'S', 'S': 'S',
					'COORD': 'COP'}
		compound_map = {'CLS': 'NP',
						'PROREL+': 'NP', 'DET+': 'NP', 
				  		'VPR+': 'VP', 'VS+': 'VP', 'VINF+': 'VP', 'V+': 'VP', 'VPP+': 'VP',
						'ET+': 'NP', 'NC+': 'NP', 'PRO+': 'NP', 'NPP+': 'NP',
						'ADJ+': 'AJP',
						'ADVWH+': 'AVP', 'ADV+': 'AVP',
						'P+': 'PP', 'P+D+': 'PP',
						'I+': 'X',
						'CC+': 'COP', 'CS+': 'CONJP'}

		label_map.update(compound_map)
		tag_map = {'ADJ': 'ADJ', 'ADJWH': 'ADJ', 'ADV': 'ADV', 'ADVWH': 'ADV', 'CC': 'CONJ', 'CLO': 'PRON', 'CLR': 'PRON',
				   'CLS': 'PRON', 'CS': 'CONJ', 'DET': 'DET', 'DETWH': 'DET', 'ET': 'X', 'I': 'X', 'NC': 'NOUN', 'NPP': 'NOUN',
				   'P': 'ADP', 'P+D': 'ADP', 'P+PRO': 'ADP', 'PONCT': '.', 'PREF': 'PRT', 'PRO': 'PRON', 'PROREL': 'PRON',
				   'PROWH': 'PRON', 'V': 'VERB', 'VIMP': 'VERB', 'VINF': 'VERB', 'VPP': 'VERB', 'VPR': 'VERB', 'VS': 'VERB'}

	elif 'ko' in lan:
		label_map = {'ROOT': 'ROOT', 'TOP': 'TOP', 'NP': 'NP', 'VP': 'VP', 'ADJP': 'AJP', 'DANP': 'AJP', 'ADVP': 'AVP', 'ADCP': 'AVP',
					 'S': 'S', 'INTJ': 'X', 'PRN': 'X', 'X': 'X', 'LST': 'X', 'XP': 'X', 'MODP':'AJP', 'AUXP':'VP', 'IP':'AJP'}
		tag_map = {}
	
	elif 'he' in lan:
		label_map = {'ADJP': 'AJP', 'ADJX': 'AJP', 'ADVO': 'AVP', 'ADVOP': 'AVP', 'ADVP': 'AVP', 'CC': 'X', 'CDP': 'NP', 'CDTP': 'NP',
					'FRAG': 'S', 'FRAGQ': 'S', 'INP': 'X', 'INTJ': 'X', 'NNPP': 'NP', 'NP': 'NP', 'NPP': 'NP', 'NX': 'NP', 'PP': 'PP',
					'PREDP': 'X', 'PRN': 'X', 'S': 'S', 'SBAR': 'S', 'SQ': 'S', 'SQBAR': 'S', 'ROOT': 'ROOT', 'TOP': 'TOP', 'VP': 'VP', 'ZVLP': 'X'}
		
		# tag_set = ['??', 'ADVERB', 'AT', 'BN', 'BNT', 'CC', 'CD', 'CDT', 'CONJ', 'COP', 'COP_TOINFINITIVE', 'DEF', 'DT', 'DTT',
		#  'DUMMY_AT', 'EX', 'IN', 'INTJ', 'JJ', 'JJT', 'MD', 'NCD', 'NN', 'NNP', 'NNT', 'NN_S_PP', 'P', 'POS',
		#  'PREPOSITION', 'PRP', 'QW', 'RB', 'REL', 'S_ANP', 'S_PRN', 'TEMP', 'VB', 'VB_TOINFINITIVE', 'ZVL', 'yyCLN',
		#  'yyCM', 'yyDASH', 'yyDOT', 'yyELPS', 'yyEXCL', 'yyLRB', 'yyQM', 'yyQUOT', 'yyRRB', 'yySCLN']
		tag_map = {}
		
	elif 'hu' in lan:
		label_map = {'ADJP': 'AJP', 'ADVP': 'AVP', 'C0': 'CONJP', 'CP': 'COP', 'INF': 'VP', 'INF0': 'VP', 'NEG': 'AVP',
					 'NP': 'NP', 'PA': 'AVP', 'PA0': 'AVP', 'PP': 'PP', 'PREVERB': 'AVP', 'ROOT': 'ROOT', 'TOP': 'TOP', 'V0': 'VP', 'XP': 'X'}
		
		# tag_set = ['A', 'C', 'I', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z']
		tag_map = {}
	
	elif 'ja' in lan:
		label_map = {'ADVP': 'AVP', 'CONJP': "CONJP", 'CP': 'CONJP', 'FRAG': 'S', 'FS': 'NP', 'INTJP': 'X', 'IP': 'S', 'LS': 'NP', 'LST': 'NP', 'META': 'NP', 'NML': 'NP', 'NP': 'NP', 'NUMCLP': 'NP', 'PNLP': 'AJP', 'PP':'PP', 'PRN': 'S', 'ROOT': 'ROOT', 'TOP': 'TOP', 'multi': 'S'}
		# tag_set = ['ADJI', 'ADJN', 'ADV', 'AX', 'AXD', 'CL', 'CONJ', 'D', 'FN',
		# 			'FW', 'INTJ', 'MD', 'N', 'NEG', 'NPR', 'NUM',
		# 			'P', 'PASS', 'PASS2', 'PNL', 'PRO', 'PU', 'PUL', 'PUR', 'Q',
		# 			'SYM', 'VB', 'VB0', 'VB2', 'WADV', 'WD', 'WNUM', 'WPRO']
		tag_map = {}
	
	elif 'sv' in lan:
		label_map = {'AP': 'AJP', 'AVP': 'AVP', 'NP': 'NP', 'PP':'PP', 'PSEUDO':'S',
					 'S':'S', 'TOP':'TOP', 'VP':'VP', 'XP':'X'}
		# tag_set = ['AB', 'DT', 'HA', 'HD', 'HP', 'HS', 'IE', 'IN', 'JJ', 'KN', 'MAD', 'MID', 'NN', 'P', 'PAD', 'PC',
		# 	'PL', 'PM', 'PN', 'PS', 'RG', 'RO', 'SN', 'UO', 'VB']
		tag_map = {}
		
	return label_map, tag_map

if __name__ == '__main__':
	for lan in ['en', 'de', 'fr', 'he', 'hu', 'ko', 'ja', 'sv', 'zh']:
		labelmap, tag_map = get_label_mappings(lan)
		print(lan, len(labelmap))
