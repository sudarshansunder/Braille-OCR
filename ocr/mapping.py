'''
Standard braille matrix

1 2
3 4
5 6

'''

alpha_map = {
	
	'1' : 'a',
	'12'  : 'b',
	'14'  : 'c',
	'145'  : 'd',
	'15'  : 'e',
	'124'  : 'f',
	'1245'  : 'g',
	'125'  : 'h',
	'24'  : 'i',
	'245'  : 'j',
	'13'  : 'k',
	'123'  : 'l',
	'134'  : 'm',
	'1345'  : 'n',
	'135'  : 'o',
	'1234'  : 'p',
	'12345'  : 'q',
	'1235'  : 'r',
	'234'  : 's',
	'2345'  : 't',
	'136'  : 'u',
	'1236'  : 'v',
	'2456'  : 'w',
	'1346'  : 'x',
	'13456'  : 'y',
	'1356'  : 'z',
	'6' : 'caps',
	'3456' : 'num'
}

num_map = {
	'1' : '1',
	'12'  : '2',
	'14'  : '3',
	'145'  : '4',
	'15'  : '5',
	'124'  : '6',
	'1245'  : '7',
	'125'  : '8',
	'24'  : '9',
	'245'  : '0'
}


def brlmap(brl, mode):
	if mode is 2:
		return num_map[brl]
	elif mode is 1:
		return upper(alpha_map[brl])
	else:
		return alpha_map[brl]

def getAlpha(document):
	mode = 0
	string = ''
	for word in document:
		mode = 0
		for letter in word:
			alpha = brlmap(''.join(letter), mode)
			if alpha is 'num':
				mode = 2
				continue
			if alpha is not None:
				string += alpha
		string += ' '
	return string