import cv2
import matplotlib.pyplot as plt
import shutil
import os
from PIL import Image

word_segs_path = 'D:\\Academics\\OCR Final Year Project\\word segments\\'
char_segs_path = 'D:\\Academics\\OCR Final Year Project\\character segments\\'
temp = os.listdir(word_segs_path)
letter_count = 0
if(os.path.exists(char_segs_path) == False):
    os.mkdir(char_segs_path)
else:
    shutil.rmtree(char_segs_path)
    os.mkdir(char_segs_path)

for image_temp in range(len(temp)):
    image_name = str(image_temp+1) + '.png'
    print(image_temp)
    #image_name = str(7) + '.png'
    word = cv2.imread('D:\\Academics\\OCR Final Year Project\\word segments\\'+image_name, 0)
    plt.imshow(word)
    word = cv2.GaussianBlur(word, (3,3), 10) ##(3,3) is kernel size and 10 is sigma value
    plt.imshow(word)
    ret2,th2 = cv2.threshold(word,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #word_canny = cv2.Canny(word, ret2, ret2//2)
    for i in range(word.shape[0]):
        for j in range(word.shape[1]):
            if(word[i][j] <= ret2):
                word[i][j] = 255
            elif (word[i][j] > ret2):
                word[i][j] = 0

    plt.imshow(word)
    
###################################################
    
###################################################
    hist_values = []
    hist_values = cv2.calcHist([word], channels = [0], mask = None, histSize=[256], ranges=[0,256])
    plt.plot(hist_values)
    
    
    row_pixel = []
    for i in range(word.shape[0]):
        row_pixel.append(cv2.calcHist([word[i]], channels = [0], mask = None, histSize=[256], ranges=[0,256]))
    
    black_pixel = []
    dup_black_pixel = []
    for i in range(len(row_pixel)):
        black_pixel.append(row_pixel[i][255][0])
        dup_black_pixel.append(row_pixel[i][255][0])
        
    
    dup_black_pixel.sort()
    maxi1 = dup_black_pixel[len(dup_black_pixel)-1]
    maxi2 = dup_black_pixel[len(dup_black_pixel)-2]
    
    hLinePos = []
    if(maxi1 != maxi2):
        hLinePos = [black_pixel.index(maxi1), black_pixel.index(maxi2)]
    else:
        for i in range(len(black_pixel)):
            if(black_pixel[i] == maxi1):
                hLinePos.append(i)
   
    hLinePos.sort()
    #hLinePos1 = black_pixel.index(maxi1)
    #hLinePos2 = black_pixel.index(maxi2)
    
    for j in range(hLinePos[0]-2, hLinePos[1]+3):  ####### REMOVED -1 AND +1 FOR BOTH START_INDEX AND END_INDEX.
       for i in range(word.shape[1]):
            word[j][i] = 0

        
    plt.imshow(word)
    
    start_range = []
    end_range = []
    white = False
    for i in range(0, word.shape[1]):
        white_count = 0
        for j in range(0, word.shape[0]):
            if(word[j][i] == 255):  ##  word_canny[j][i] == 255 >>
                white_count += 1
        
        if(white_count > 0 and white == False):
            start_range.append(i)
            white = True
        elif(white_count == 0 and white == True):
            end_range.append(i)
            white = False
        elif(white_count > 0 and white == True and i == (word.shape[1]-1)):
            end_range.append(i)

    
#    if(len(end_range) == 0):
#        end_range.append(word_canny.shape[1])
    
    image_to_be_cropped = Image.open('D:\\Academics\\OCR Final Year Project\\word segments\\'+image_name)
        #image_to_be_cropped.show()
        
    width, height = image_to_be_cropped.size
        
    for x in range(len(start_range)):
        letter_count += 1
        char_segmented = image_to_be_cropped.crop((start_range[x], 0, end_range[x], height))
        char_segmented.save(char_segs_path + str(letter_count) + '.png')
        
           # char_segmented.show()
            
        
print(len(os.listdir(char_segs_path)))