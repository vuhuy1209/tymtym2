from random import randint, random
import cv2
jpg = cv2.imread("1.jpg",1)

print(jpg)
print(type(jpg))
print(jpg.shape)

#for i in range(200):
  #  for j in range(jpg.shape[1]):
 #       jpg[i][j]=[random.r(0,255),random(0,255),random(0,255)]
vung = jpg[300:600,250:500]
jpg[600:900,500:750] = vung
cv2.imshow("anh",jpg)
cv2.waitKey()
