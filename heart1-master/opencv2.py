import cv2
# đọc ảnh
img = cv2.imread("2.jpg",1)
# gan kich thuoc cho anh
#img = cv2.resize(img,(500,300)) #theo kíc thước tự đặt
img = cv2.resize(img,(0,0),fx=2/3,fy=2/3) # đặt theo tỷ lệ
# xuất ảnh
cv2.imshow("anh",img)
#delay
k = cv2.waitKey(0)