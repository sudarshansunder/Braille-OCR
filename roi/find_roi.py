import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

#Gets the area of the rectangle using two points
def area_rect(p1, p2):
	l = p1[0] - p2[0]
	b = p1[1] - p2[1]
	return l*b

#Gets the rectangular portion using the contour points
def get_rectangle(cont, crop):
	max_x = -1
	max_y = -1
	min_x = np.inf
	min_y = np.inf
	for c in cont:
		c = c[0]
		if c[0] > max_x:
			max_x = c[0]
		elif c[0] < min_x:
			min_x = c[0]
		if c[1] > max_y:
			max_y = c[1]
		elif c[1] < min_y:
			min_y = c[1]
	max_x -= crop
	max_y -= crop
	min_x += crop
	min_y += crop
	return [(max_x, max_y), (min_x, min_y)]

name = './images/' + sys.argv[1]
img = cv2.imread(name)
img_cont = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((5,5),np.uint8)
img = cv2.dilate(img,kernel,iterations=2)
ret, img = cv2.threshold(img, 165, 255, cv2.THRESH_BINARY)
img = cv2.GaussianBlur(img, (5, 5), 0)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=23,param2=23,minRadius=12,maxRadius=16)
circles = np.uint16(np.around(circles))

final_img = np.zeros(img.shape, np.uint8)

for i in circles[0,:]:
	cv2.circle(final_img,(i[0],i[1]),i[2],255,-1)

final_img = cv2.dilate(final_img, kernel, iterations=50)
final_img, contours, hierarchy = cv2.findContours(final_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
regions = []
max_area = -1

for cont in contours:
	rect = get_rectangle(cont, crop=40)
	area = area_rect(rect[0], rect[1])
	if area >= max_area:
		max_area = area
		regions.append(rect)

for rect in regions:
	cv2.rectangle(img_cont, rect[0], rect[1], (0,255,0), 3)

file_name = 'out' + sys.argv[1]
cv2.imwrite(file_name, img_cont)