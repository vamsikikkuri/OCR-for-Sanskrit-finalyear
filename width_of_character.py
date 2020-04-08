# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:44:18 2020

@author: vamsi
"""
import cv2
import matplotlib.pyplot as plt
import os

test_chars_path = 'D:\\Academics\\OCR Final Year Project\\character segments\\'
letters_width = []
for i in range(len(os.listdir(test_chars_path))):
    letter = cv2.imread(test_chars_path + str(i+1) + '.png', 0)
    letters_width.append(letter.shape[1])

max_width = max(letters_width)

char_bin_1 = []
char_bin_2 = [] 
char_bin_3 = []
widths_bin_1 = []
widths_bin_2 = []
widths_bin_3 = []


for imgs in range(len(letters_width)):
    if(letters_width[imgs] >= 0.8*max_width):
        char_bin_1.append(str(imgs+1)+'.png')
        widths_bin_1.append(letters_width[imgs])
        print("bin 1", str(letters_width[imgs]))
    elif (letters_width[imgs] > 0.64*max_width and letters_width[imgs] < 0.8*max_width):
        char_bin_2.append(str(imgs+1)+'.png')
        widths_bin_2.append(letters_width[imgs])
        print("bin 2", str(letters_width[imgs]))
    else:
        char_bin_3.append(str(imgs+1)+'.png')
        widths_bin_3.append(letters_width[imgs])

countOf_bins_list = [len(char_bin_1), len(char_bin_2), len(char_bin_3)]
bins_list = [char_bin_1, char_bin_2, char_bin_3]
widths_list = [widths_bin_1, widths_bin_2, widths_bin_3]
bin_with_max_count = countOf_bins_list.index(max(countOf_bins_list))

threshold_width = sum(widths_list[bin_with_max_count])/len(widths_list[bin_with_max_count])

res = [i for i in os.listdir(test_chars_path) if i not in bins_list[bin_with_max_count]]

list_for_conjuct_char_seg = []
for imgs in range(len(res)):
    letter = cv2.imread(test_chars_path + res[imgs], 0)
    if(letter.shape[1] > threshold_width):
        list_for_conjuct_char_seg.append(res[imgs])


