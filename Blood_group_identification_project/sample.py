import cv2
import numpy as np
print(cv2.__version__)

# img=cv2.imread('C:/Users/babit/OneDrive/Desktop/Django_Infosys/Blood_group_identification_project/133617083388862763.jpg',cv2.IMREAD_GRAYSCALE)

# cv2.imshow("Read Image",img)

# How to save an image in openCV
# img1=cv2.imread('C:/Users/babit/OneDrive/Desktop/Django_Infosys/Blood_group_identification_project/133617083388862763.jpg',cv2.IMREAD_GRAYSCALE)

imagename = 'grayscale_converted.jpg'

# cv2.imwrite(imagename,img1)
# img1 = cv2.imread(imagename)
# cv2.imshow("Read Image",img1)

#How to resize the images which we read

# img2 = cv2.resize(img1,(0,0),fx=0.5,fy=0.5)
# cv2.imshow("Resize Image",img2)


# steps to follow to find the blood group type of the given blood cell Image

# get the Image
abo_image = cv2.imread('Blood_group_identification_project/blood_cell_images/Humanrbc1000x-cr-primary.jpg')
# cv2.imshow('Original Image',abo_image)

# Convert the image from color to grayscale
gray = cv2.cvtColor(abo_image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray Scale image',gray)

# blur the image using Gaussian Blur (smoothning the image for more accurate blood cell Image)
blur = cv2.GaussianBlur(gray,(5,5),0)
# cv2.imshow('Blurred Image',blur)

# blurred to threshold to calculate the threshold values for the given images and will return the image and its value
val,threshold = cv2.threshold(blur,120,255,cv2.THRESH_BINARY) # sets pixels to either black or white
cv2.imshow('Treshold Image',threshold)

# finding the contours(continuous curve along the boundary) to find the curved edges of the blood cells in the image
contour, val2 = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # 2nd parameter is for considering only the outer contour and not any of its inside child contour

# print(contour)
# counting the number of contours found in the given Image
contour_length = len(contour)
print(contour_length)

if contour_length <50:
    print('O')
elif contour_length >=50 and contour_length<100:
    print('A')
elif contour_length>=100 and contour_length<150:
    print('B')
else:
    print('AB')            

cv2.waitKey(0)
cv2.destroyAllWindows()

