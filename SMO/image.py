from PIL import Image
import random

x = 14
y = 10

feature = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
		   1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0,
		   0, 1, 0, 1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
		   0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 1, 26]

img = Image.new("RGB",(x*10,y*10))

for i in xrange(0,x):
	for j in xrange(0,y):
		# s = random.randint(0,255)
		# t = random.randint(0,255)
		# k = random.randint(0,255)
		for u in xrange(0,10):
			for v in xrange(0,10):
				s = feature[i*10+j]
				if s<5:
					img.putpixel([u+i*10,v+j*10],(64+s*48,64,64))
				else:
					img.putpixel([u + i * 10, v + j * 10], (s*256/27, s*256/27, s*256/27))

img.show()
img.save("img.png")
