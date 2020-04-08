import cv2
import matplotlib.pyplot as plt
import shutil

image_name = 'test font 3.png'
img = cv2.imread('D:\\Academics\\OCR Final Year Project\\'+image_name, 0)
#plt.imshow(img)
img = cv2.GaussianBlur(img, (3,3), 10) ##(3,3) is kernel size and 10 is sigma value
plt.imshow(img)
ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#tight = cv2.Canny(img, ret2, ret2//2)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if(img[i][j] <= ret2):
            img[i][j] = 255
        elif (img[i][j] > ret2):
            img[i][j] = 0

plt.imshow(img)
############### ADDED HERE MORPHOLOGICAL OPERATORS###########################
"""
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if(img[i][j] == 255):
            img[i][j] = 1

plt.imshow(img)

img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
plt.imshow(img)
"""
##############################################################################
hist_values = cv2.calcHist([img], channels = [0], mask = None, histSize=[256], ranges=[0,256])
plt.plot(hist_values)

line_segs = []
for i in range(img.shape[0]):
    line_segs.append(cv2.calcHist([img[i]], channels = [0], mask = None, histSize=[256], ranges=[0,256]))


white = True
start_ranges=[]
end_ranges = []
for i in range(len(line_segs)):
    if (line_segs[i][0] != img.shape[1]) and (white == True):
        start_ranges.append(i)
        white = False
    
    elif (line_segs[i][0] == img.shape[1]) and (white == False):
        end_ranges.append(i-1)
        white = True
        
        
from PIL import Image
image_to_be_cropped = Image.open('D:\\Academics\\OCR Final Year Project\\'+image_name)
#image_to_be_cropped.show()

width, height = image_to_be_cropped.size

import os
line_segs_path = 'D:\\Academics\\OCR Final Year Project\\line segments'
if(os.path.exists(line_segs_path) == False):
    os.mkdir(line_segs_path)
else:
    shutil.rmtree(line_segs_path)
    os.mkdir(line_segs_path)
    

for i in range(len(start_ranges)):
    line_segmented = image_to_be_cropped.crop((0, start_ranges[i], width, end_ranges[i]))
    line_segmented.save('D:\\Academics\\OCR Final Year Project\\line segments\\' + str(i+1) + '.png')
    #line_segmented.show()
    
    
    
print(len(os.listdir(line_segs_path)))