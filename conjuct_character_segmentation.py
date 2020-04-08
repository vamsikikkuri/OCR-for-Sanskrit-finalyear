# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 21:41:48 2020

@author: vamsi
"""

import cv2
import matplotlib.pyplot as plt


test_chars_path = 'D:\\Academics\\OCR Final Year Project\\character segments\\'

img = cv2.imread(test_chars_path + '3.png', 0)
plt.imshow(img)

img = cv2.GaussianBlur(img, (3,3), 10) ##(3,3) is kernel size and 10 is sigma value
plt.imshow(img)

ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if(img[i][j] <= ret2):
            img[i][j] = 255
        elif (img[i][j] > ret2):
            img[i][j] = 0

plt.imshow(img)

def findVerticalBarPos(img, hPosLine, height, mid, right):
    vBar = []
    for i in range(mid, right):
        count = 0
        for j in range(hPosLine+1, img.shape[0]):
            if(img[j][i] == 255):
                count += 1
        
        if(count >= 0.8*height):
            vBar.append(i)
    
    return vBar
        
def findHeightOfCharacter(img, hPosLine):
    count = 0
    for i in range(hPosLine+1, img.shape[0]):
        #print(str(i) ,'th row', str(count))
        for j in range(img.shape[1]):
            if img[i][j] == 255:
                count += 1
                break
    
    return count


def findhPosLine(img):
    white_pixels = []
    #white_pixels_dup = []
    for i in range(img.shape[0]):
        count = 0
        for j in range(img.shape[1]):
            if img[i][j] == 255:
                count += 1
        white_pixels.append(count)
        #white_pixels_dup.append(count)
        
    #hLinePos = []
    #white_pixels_dup.sort() #changed this part for HLINEPOS .........
    hLinePos = -1
    flag = 0
    for i in range(len(white_pixels)):
        if(white_pixels[i] == max(white_pixels)):
            print("true", str(i+1))
            flag += 1
        if(flag > 0 and white_pixels[i] != max(white_pixels)):
            print("broken", str(i+1))
            hLinePos = i-1
            break
    
    return hLinePos

############### CONTINUED HORIZONTAL PROJECTION ############################
def findC1(conj_top, img, conj_right, c1):
    r1 = -1
    r2 = -1
    r3 = -1
    height_of_chp = 0
    hasDisc = True
    chp = []
    for c in range(conj_top+1, img.shape[0]):
        if(255 in img[c][c1:conj_right]):
            chp.append(1)
        else:
            chp.append(0)
     
        
    for k in range(len(chp)):
        if(chp[k] == 1 and r1 < 0):
            r1 = conj_top + k + 1
        elif(chp[k] == 1 and  r1 >0 and r2 > 0 and r3<0):
            r3 = conj_top + k + 1
        elif(chp[k] == 0 and r1 > 0 and r2 < 0 and r3 < 0):
            r2 = conj_top + k + 1
        
    if((r2 < 0 and r3 < 0) or (r2 > 0 and r3 < 0)):
        print('no discc....', str(c1))
        if(r2 < 0):
            r2 = len(chp)
        
        height_of_chp = r2 - r1
        hasDisc = False
    else:
        print('disc unduu', str(c1))
        hasDisc = True
    
    return height_of_chp, hasDisc

### UPDATED LOGIC FOR CONSIDERING HLINEPOS---------------------

############################ FINDING AND IGNORING VERTICAL BAR ###################
hLinePos = findhPosLine(img)
height = findHeightOfCharacter(img, hLinePos)

conj_top = hLinePos + 1
conj_btm = conj_top + height
conj_left = 0
conj_right = img.shape[1]

conj_mid = conj_left + (conj_right - conj_left) // 2
conj_left_onethird = conj_left + (conj_right - conj_left) // 3
conj_height = conj_btm - conj_top

vbar = findVerticalBarPos(img, conj_top, height, conj_mid, conj_right)

conj_right = vbar[0]

pen_width = 3
####################### FINDING C1, C2, C ############################

""" CHECK AND CHANGE hLinePos where ever written to conj_top  """

c1 = conj_right - pen_width + 1

hasDisc = True
while(hasDisc):
    c1 -= 1
    result_for_c1 = findC1(conj_top+1, img, conj_right, c1)
    hasDisc = result_for_c1[1]
    height_of_chp = result_for_c1[0]
    print(str(height_of_chp), 'for', str(c1))
    if(height_of_chp > (conj_height/3)):
        hasDisc = False
    else:
        hasDisc = True




#### C2 ######
## H1 OR H2
def findC2(conj_top, img, right):
    chp2 = []
    chp2_height = 0
    for con in range(conj_top+2, img.shape[0]):
        if(255 in img[con][:right]):
            chp2.append(1)
            chp2_height += 1
        else:
            chp2.append(0)
    
    return chp2_height




chp2_height = findC2(conj_top, img, conj_left_onethird)
if(chp2_height >= 0.8 * conj_height):
    print('h2')
    black_pixels_cols_for_c2 = []
    for cols in range(conj_left, conj_left_onethird):
        count = 0
        for rows in range(conj_top, img.shape[0]):
            if(img[rows][cols] == 255):
                count+=1
    
        black_pixels_cols_for_c2.append(count)
    
    for i in range(len(black_pixels_cols_for_c2)):
        if(black_pixels_cols_for_c2[i] == max(black_pixels_cols_for_c2)):
            c2 = i
    
    not_good_for_c2 = True
    while(c2 < conj_mid and not_good_for_c2):
        if(findC2(conj_top, img, c2) <= findC2(conj_top, img, c2+1)):
              c2 += 1  
              not_good_for_c2 = True
        else:
            not_good_for_c2 = False
    print(c2)
else:
    print('h1')
    c2 = conj_left_onethird
    not_good_for_c2 = True
    while(c2 < conj_mid and not_good_for_c2):
        if(findC2(conj_top, img, c2) < (conj_height/3)):
            if(findC2(conj_top, img, c2) <= findC2(conj_top, img, c2+1)):
              c2 += 1  
              not_good_for_c2 = True
        else:
            not_good_for_c2 = False
    print(c2)


if(c1 < c2):
    print('no segmentation needed')
elif (c1 == c2 or c1 - c2 <= pen_width):
    c1 = c1 - (c1 - c2)
    print('segement at ', str(c1))
elif (c1 - c2 > pen_width):
    print('segment at ', str(c1))
    print('send remaining image for furthur segmentation.... same alog runs again')


