import numpy as np
import cv2
from matplotlib import pyplot as plt
import mapping
import util
import sys

#Change this code
def get_final_image(image_name):
	img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
	img = 255 - img
	ret, img = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
	#resized_image = cv2.resize(img, (614L, 365L)) 
	return img

def translate_letter(img, max_width):
	h,w = img.shape
	#Some words only have their right side.
	#This is to adjust the size of those words
	if w < max_width:
		diff = max_width - w
		add = np.zeros((h, diff))
		img = np.concatenate((img, add), axis=1)
	img_seg = []
	h,w = img.shape

	#Find a better way to do this. Shit method
	img_seg.append(img[0:h/3, 0:w/2])
	img_seg.append(img[0:h/3, w/2:w])
	img_seg.append(img[h/3:(2*h)/3, 0:w/2])
	img_seg.append(img[h/3:(2*h)/3, w/2:w])
	img_seg.append(img[(2*h)/3:h, 0:w/2])
	img_seg.append(img[(2*h)/3:h, w/2:w])

	index = [1, 4, 2, 5, 3, 6]
	braille = []
	i = 0

	for seg in img_seg:
		if util.contains_white(seg):
			braille.append(str(index[i]))
		i += 1

	return tuple(sorted(braille))

def segment_word(word):
	return util.vertical_profile(word, LETTER_THRESH)

def segment_line(line):
	return util.vertical_profile(line, WORD_THRESH)

def get_max_width(letters):
	max_width = letters[0].shape[1]
	for letter in letters:
		h,w = letter.shape
		if w > max_width:
			max_width = w
	return max_width

if len(sys.argv) != 2:
	print 'Name of file must be given as an argument'
	exit()

img = get_final_image(sys.argv[1])
LINE_THRESH = 30 * (img.shape[0]/365L)
WORD_THRESH = 80 * (img.shape[1]/614L) * 0.7
LETTER_THRESH = 20 * (img.shape[1]/614L) * 0.7

braille = []
#cv2.imshow('image', img)
lines = util.horizontal_profile(img, LINE_THRESH)
#print 'There are', len(lines), 'lines'

for line in lines:
	words = segment_line(line)
	for word in words:
		braille_word = []
		letters = segment_word(word)
		max_width = get_max_width(letters)
		for letter in letters:
			braille_word.append(translate_letter(letter, max_width))
		braille.append(braille_word)

print braille

print mapping.getAlpha(braille)

cv2.waitKey(0)
cv2.destroyAllWindows()