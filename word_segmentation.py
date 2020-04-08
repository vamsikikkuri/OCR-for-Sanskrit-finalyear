import cv2
import matplotlib.pyplot as plt
import shutil
import os
from PIL import Image


line_segs_path = 'D:\\Academics\\OCR Final Year Project\\line segments'
temp = os.listdir(line_segs_path)
word_count = 0
#word_segs_path = 'D:\\Academics\\OCR Final Year Project\\word segments\\'
word_segs_path = 'D:\\Academics\\OCR Final Year Project\\OCR Dataset fonts\\test fonts3\\'
if(os.path.exists(word_segs_path) == False):
    os.mkdir(word_segs_path)
else:
    shutil.rmtree(word_segs_path)
    os.mkdir(word_segs_path)
        
for i in range(len(temp)):
    image_name = str(i+1) + '.png'
    line  = cv2.imread('D:\\Academics\\OCR Final Year Project\\line segments\\'+image_name, 0)
    plt.imshow(line)
    line = cv2.GaussianBlur(line, (3,3), 10) ##(3,3) is kernel size and 10 is sigma value
    plt.imshow(line)
    ret2,th2 = cv2.threshold(line,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #line = cv2.Canny(line, ret2, ret2//2)
    for i in range(line.shape[0]):
        for j in range(line.shape[1]):
            if(line[i][j] <= ret2):
                line[i][j] = 255
            elif (line[i][j] > ret2):
                line[i][j] = 0

    plt.imshow(line)
    ############################################################
    ############################################################
    start_ranges = []
    end_ranges = []
    white = False
    for i in range(0, line.shape[1]):
        white_count = 0
        for j in range(0, line.shape[0]):
            if(line[j][i] == 255):  ## line[j][i] == 255 >>
                white_count += 1
        
        if(white_count > 0 and white == False):
            start_ranges.append(i)
            white = True
        elif(white_count == 0 and white == True):
            end_ranges.append(i)
            white = False
        elif(white_count > 0 and white == True and i == (line.shape[1]-1)):
            end_ranges.append(i)
            
            
    
    image_to_be_cropped = Image.open('D:\\Academics\\OCR Final Year Project\\line segments\\'+image_name)
    #image_to_be_cropped.show()
    
    width, height = image_to_be_cropped.size
    
    for k in range(len(start_ranges)):
        word_count += 1
        word_segmented = image_to_be_cropped.crop((start_ranges[k], 0, end_ranges[k], height))
        word_segmented.save(word_segs_path + str(word_count) + '.png')
        #word_segmented.show()
        
        
print(len(os.listdir(word_segs_path)))