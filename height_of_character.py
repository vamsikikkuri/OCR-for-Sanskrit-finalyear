import cv2
import matplotlib.pyplot as plt
import os


test_chars_path = 'D:\\Academics\\OCR Final Year Project\\character segments\\'

def letterToBinary(ret2, letter):
    for i in range(letter.shape[0]):
        for j in range(letter.shape[1]):
            if(letter[i][j] <= ret2):
                letter[i][j] = 255
            elif (letter[i][j] > ret2):
                letter[i][j] = 0
    
    return letter

def findHeightOfCharacter(hPosLine, letter):
    count = 0
    for i in range(hPosLine+1, letter.shape[0]):
        for j in range(letter.shape[1]):
            if letter[i][j] == 255:
                count += 1
                break
    
    return count


def findhPosLine(letter):
    white_pixels = []
    white_pixels_dup = []
    for i in range(letter.shape[0]):
        count = 0
        for j in range(letter.shape[1]):
            if letter[i][j] == 255:
                count += 1
        white_pixels.append(count)
        white_pixels_dup.append(count)
        
    hLinePos = []
    white_pixels_dup.sort()
    maxi1 = white_pixels_dup[len(white_pixels_dup)-1]
    maxi2 = white_pixels_dup[len(white_pixels_dup)-2]
    
    hLinePos = []
    if(maxi1 != maxi2):
        hLinePos = [white_pixels.index(maxi1), white_pixels.index(maxi2)]
    else:
        for i in range(len(white_pixels)):
            if(white_pixels[i] == maxi1):
                hLinePos.append(i)
   
    hLinePos.sort()
    return hLinePos

def findHeightList():
    height_list = []
    # Put the below line in a for loop where all test sample images come.........
    for test_chars in range(len(os.listdir(test_chars_path))):
        letter = cv2.imread(test_chars_path + str(test_chars+1) + '.png', 0)
        #plt.imshow(letter)
        ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
        letter = letterToBinary(ret2, letter)
        height_list.append(findHeightOfCharacter(findhPosLine(letter)[1], letter))
        
    
    return height_list
    


height_list = findHeightList() 
max_height = max(height_list)
print(max_height)
    

char_bin_1 = []
char_bin_2 = []
char_bin_3 = []

for imgs in range(len(height_list)):
    if(height_list[imgs] >= 0.8*max_height):
        char_bin_1.append(str(imgs+1)+'.png')
    elif (height_list[imgs] > 0.64*max_height and height_list[imgs] < 0.8*max_height):
        char_bin_2.append(str(imgs+1)+'.png')
    else:
        char_bin_3.append(str(imgs+1)+'.png')

countOf_bins_list = [len(char_bin_1), len(char_bin_2), len(char_bin_3)]
bins_list = [char_bin_1, char_bin_2, char_bin_3]
bin_with_max_count = countOf_bins_list.index(max(countOf_bins_list))


heights_of_max_bin = []
for img_bin in range(len(bins_list[bin_with_max_count])):
    letter = cv2.imread(test_chars_path + bins_list[bin_with_max_count][img_bin], 0)
    ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #letter = cv2.Canny(letter, ret2, ret2//2)
    letter = letterToBinary(ret2, letter)
    heights_of_max_bin.append(findHeightOfCharacter(findhPosLine(letter)[1], letter))
    print(bins_list[bin_with_max_count][img_bin])


threshold_char_height = sum(heights_of_max_bin)/len(heights_of_max_bin)
print(threshold_char_height)
                              
res = [i for i in os.listdir(test_chars_path) if i not in bins_list[bin_with_max_count]] 
#res is list of images that are to be sent for verification whether, 
#they have to be sent to furthur segmentation or not. Lower modifier is present.....

list_for_furthur_segmentation = []
for x in range(len(res)):
    letter = cv2.imread(test_chars_path + res[x], 0)
    ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #letter = cv2.Canny(letter, ret2, ret2//2)
    letter = letterToBinary(ret2, letter)
    if(findHeightOfCharacter(findhPosLine(letter)[1], letter) > threshold_char_height):
        list_for_furthur_segmentation.append(res[x])
        

print(list_for_furthur_segmentation)

######### LOWER MODIFIER SEGMENTATION ##########
for imgs in range(len(list_for_furthur_segmentation)):
    letter = cv2.imread(test_chars_path + list_for_furthur_segmentation[imgs], 0)
    #letter = cv2.imread(test_chars_path + '16.png', 0)
    ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #letter = cv2.Canny(letter, ret2, ret2//2)
    letter = letterToBinary(ret2, letter)
    plt.imshow(letter)
    lower_modifier_blacks = []
    for row_pixels in range(int(threshold_char_height)+1, letter.shape[0]):
        count = 0
        for col_pixels in range(0, letter.shape[1]):
            if(letter[row_pixels][col_pixels] == 255):
                count += 1
        lower_modifier_blacks.append(count)
    print("image", lower_modifier_blacks)
    break_point = lower_modifier_blacks.index(min(lower_modifier_blacks))
    height_of_char = findHeightOfCharacter(findhPosLine(letter)[1], letter)
    height_of_lower_modifier = findHeightOfCharacter(int(threshold_char_height)+break_point, letter)
    if(height_of_lower_modifier >= 0.2 * height_of_char):
        print('suitable for lower modifier segmentation', str(int(threshold_char_height)+break_point), 'is breaking point', list_for_furthur_segmentation[imgs])
   ### FINDING TOP STRIP CHARACTER ### CHECK IF REALLY NEEDED

def findTopCharSegmentation(letter, sirorekha):
    started = False
    #print('sirorekha',sirorekha)
    left_bound = -1
    right_bound = -1
    black_pixel_count_col = []
    for cols in range(letter.shape[1]):
        count = 0
        for rows in range(sirorekha):
            if(letter[rows][cols] == 255):
                count += 1
            
        black_pixel_count_col.append(count)
        if(count != 0 and started == False):
            #print('started', cols)
            left_bound = cols
            started = True
        elif (count == 0 and started == True):
            #print('ended', cols)
            right_bound = cols
            started = False
        elif (count != 0 and started == True and cols == letter.shape[1]-1):
            #print('reached', count)
            right_bound = cols
        
    return left_bound, right_bound
   

for i in range(len(os.listdir(test_chars_path))):
    letter = cv2.imread(test_chars_path + str(i+1) + '.png', 0)
    ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #letter = cv2.Canny(letter, ret2, ret2//2)
    letter = letterToBinary(ret2, letter)
    top_modifier_lr_boundaries = findTopCharSegmentation(letter, findhPosLine(letter)[0])
    if(top_modifier_lr_boundaries != (-1, -1)):
        print(str(top_modifier_lr_boundaries), 'for', str(i+1))

"""    
letter = cv2.imread(test_chars_path + str(50) + '.png', 0)
ret2,th2 = cv2.threshold(letter,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
letter = letterToBinary(ret2, letter)
"""