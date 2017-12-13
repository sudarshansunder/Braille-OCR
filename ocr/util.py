import numpy as np
from matplotlib import pyplot as plt
import cv2

def vertical_profile(img, thresh=25, debug=False):
	h, w = img.shape
	count = np.zeros(w)
	for i in range(w):
		for j in range(h):
			if img[j][i] == 255:
				count[i] += 1

	seg_pts = []
	i = 0
	
	#Get the initial point
	while i < len(count):
		if count[i] != 0:
			seg_pts.append(i)
			break
		i += 1
	i = 0
	while i < w and count[i] == 0:
		i += 1

	while i < w-1:
		if count[i] == 0:
			dist = 0
			start = i
			for j in range(i, w):
				if count[j] == 0:
					dist += 1
				else:
					break
			if j == w-1:
				dist = 0
			if dist > thresh:
				seg_pts.append(start)
				seg_pts.append(start + dist)
			if dist != 0:
				i = start + dist
			else:
				i += 1
		else:
			i += 1

	#Get the final point
	i = len(count) - 1
	while i > 0:
		if count[i] != 0:
			seg_pts.append(i)
			break
		i -= 1

	lines = []
	i = 0
	while i < len(seg_pts):
		cur_line = img[0:h, seg_pts[i]:seg_pts[i+1]]
		lines.append(cur_line)
		#cv2.imshow('line' + str(i+1), cur_line)
		i += 2

	if debug is True:
		yaxis = np.arange(w)
		for pt in seg_pts:
			plt.axvline(pt, color='r')
		plt.plot(yaxis, count)
		plt.show()

	return lines

def contains_white(img):
	h,w = img.shape
	for i in range(h):
		for j in range(w):
			if img[i][j] == 255:
				return True
	return False

def horizontal_profile(img, thresh=15, debug=False):
	h, w = img.shape
	count = np.zeros(h)
	for i in range(h):
		for j in range(w):
			if img[i][j] == 255:
				count[i] += 1

	seg_pts = []

	#Get the initial point
	i = 0
	for c in count:
		if c != 0:
			seg_pts.append(i)
			break
		i += 1

	i = 0

	#Get intermeditate points
	while i < h:
		if count[i] == 0:
			dist = 0
			start = i
			for j in range(i, h):
				if count[j] == 0:
					dist += 1
				else:
					break
			if dist > thresh:
				seg_pts.append(start)
				seg_pts.append(start + dist)
			if dist != 0:
				i = start + dist
			else:
				i += 1
		else:
			i += 1

	#Get the final point
	i = len(count) - 1
	while i > 0:
		if count[i] != 0:
			seg_pts.append(i)
			break
		i -= 1

	lines = []

	#Segment the image
	i = 0
	while i < len(seg_pts):
		cur_line = img[seg_pts[i]:seg_pts[i+1], 0:w]
		lines.append(cur_line)
		#cv2.imshow('line' + str(i+1), cur_line)
		i += 2

	if debug is True:	
		yaxis = np.arange(h)
		for pt in seg_pts:
			plt.axvline(pt, color='r')
		plt.plot(yaxis, count)
		plt.show()
	
	return lines