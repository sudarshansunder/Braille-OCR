import os

for i in range(8):
	name = str(i+1) + '.png'
	cmd = 'python find_roi.py ' + name
	os.system(cmd)
	print 'File ' + name + ' done'