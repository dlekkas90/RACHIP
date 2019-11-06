#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:42:57 2019

@author: dlekkas
"""
import os
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from glob import glob

#PIXEL COLOR VALUES
#YELLOW = [191 191   0 255]
#WHITE = [255 255 255 255]
#BLACK = [0 0 0 255]
#PURPLE= [<200 <200 <200 255]   


print '\n', 'P R O G R A M  I N I T I A L I Z E D', '\n'

print '+----------------------------- RACHIP v1.2 -------------------------------+'
print '|                                                                         |'
print '|         RADIAL ALVEOLAR COUNTER for HISTOLOGICAL IMAGE PROCESSING       |'
print '|             [ Conceived and Coded by Damien Lekkas (c) 2019 ]           |'
print '|                                                                         |'
print '+-------------------------------------------------------------------------+', '\n'

if not os.path.exists('./lung_images'):
    os.mkdir('./lung_images')

if not os.path.exists('./lung_images/input_images/'):
    os.mkdir('./lung_images/input_images/')
    print '> CREATED NEW SUBDIRECTORY FOR INPUT IMAGES IN YOUR CURRENT WORKING DIRECTORY.'
    print '> ADD IMAGES TO PROCESS IN THE ./lung_images/input_images DIRECTORY AND RESTART PROGRAM.'
    print '\n'*2
    print 'P R O G R A M  T E R M I N A T E D', '\n'
    exit()

RAC_out = open('RAC_data_out.txt', 'w+')
RAC_out.write('IMAGE_TITLE' + '\t' + 'ROW_COORD' + '\t' + 'COL_COORD' + '\t' + 'ANGLE' + '\t' + 'RAC' + '\n')

read_dir = './lung_images/input_images/*'
image_files = []

for f in glob(read_dir):
    f = f.split('/')[-1]
    image_files.append(f)

read_dir = read_dir[0:-1]    

write_dir = './lung_images/output_images/'

if not os.path.exists(write_dir):
    os.mkdir(write_dir)

os.chdir('./lung_images/')

for i_f in range(len(image_files)):
    x1s = []
    y1s = []
    x2s = []
    y2s = []
    
    os.chdir('./input_images')
    img = mpimg.imread(image_files[i_f])
    
    os.chdir('../')  
    os.chdir('./output_images')
    
    num_rows = len(img)
    num_cols = len(img[0])

    plt.ion()
    
    RACs = []
    measure = 'y'
    first_flag = True
    while measure == 'y':
        print '\n', '+---------------------- IMAGE ' + str(i_f + 1) + ' ----------------------+'

        accept_flag = ''
        while accept_flag != 'y':
            accept_flag = ''
            if first_flag == True:
                plt.yticks([y for y in range(0, num_rows, 50)])
                imgplot = plt.imshow(img)
           
                plt.show(block=False)
            
            else:
                plt.yticks([y for y in range(0, num_rows, 50)])
                
                imgplot = plt.imshow(img)
                
                for coord in range(len(x1s)):
                    plt.scatter([x1s[coord]],[y1s[coord]], c='k', s=5)
                    plt.plot([x1s[coord], x2s[coord]], [y1s[coord], y2s[coord]], 'y-') 
                
                plt.show(block=False)
                
            user_point_coord_col = -1
            while user_point_coord_col not in range(0, num_cols+1):
                user_point_coord_col = input('> SELECT COLUMN COORDINATE (FROM 0 to ' + str(num_cols) + '): ')
    
                if user_point_coord_col not in range(0, num_cols+1):
                    print '> INVALID VALUE. PLEASE RE-ENTER A VALID COLUMN COORDINATE.'    
            
            user_point_coord_row = -1
            while user_point_coord_row not in range(0, num_rows+1):
                user_point_coord_row = input('> SELECT ROW COORDINATE (FROM 0 to ' + str(num_rows) + '): ')
    
                if type(user_point_coord_row) != int:
                    print '> NOT A NUMBER. PLEASE RE-ENTER A VALID ROW COORDINATE.'
    
                if user_point_coord_row not in range(0, num_rows+1):
                    print '> INVALID VALUE. PLEASE RE-ENTER A VALID ROW COORDINATE.'

            plt.scatter([user_point_coord_col],[user_point_coord_row], c='k', s=5)
            
            user_angle = -1
            while user_angle < 0 or user_angle > 359:
                user_angle = input('> SPECIFY ANGLE OF LINE (IN DEGREES) DRAWN FROM SPECIFIED COORDINATES (0 - 359): ')
                if user_angle < 0 or user_angle > 359:
                    print '> INVALID ANGLE DESIGNATION. ANGLES MUST RANGE FROM 0 TO 359 DEGREES.'
            
            user_angle_copy = user_angle
            x = user_point_coord_col 
            y = user_point_coord_row
            slope = 0
            intercept = 0
            
            if user_angle < 90:
                leg_1 = y
                R_triangle_leg_1 = num_cols - x
                R_triangle_angle = 90 - user_angle
                R_triangle_angle = math.radians(R_triangle_angle)
                line_length =  R_triangle_leg_1/(math.cos(R_triangle_angle))
    
                second_coord_x = num_cols
                second_coord_y = math.sin(R_triangle_angle)*line_length  
                second_coord_y = y - second_coord_y    
                slope = (second_coord_y - y)/(second_coord_x - x)
                intercept = y - slope*x
                
                if second_coord_y < 0:
                    intercept = y - slope*x
                    second_coord_y = 0
                    second_coord_x = (second_coord_y - intercept)/slope
                
            elif user_angle > 90 and user_angle < 180:
                user_angle = user_angle - 90
                leg_1 = num_cols - x
                R_triangle_leg_1 = num_rows - y
                R_triangle_angle = 90 - user_angle
                R_triangle_angle = math.radians(R_triangle_angle)
                line_length =  R_triangle_leg_1/(math.cos(R_triangle_angle))
    
                second_coord_y = num_rows
                second_coord_x = math.sin(R_triangle_angle)*line_length
                second_coord_x = second_coord_x + x
    
                slope = (second_coord_y - y)/(second_coord_x - x)
                intercept = y - slope*x
                
                if second_coord_x > num_cols:
                    second_coord_x = num_cols
                    second_coord_y = slope*second_coord_x + intercept 
    
            elif user_angle > 180 and user_angle < 270:
                user_angle = user_angle - 180
                leg_1 = num_rows - y
                R_triangle_leg_1 = x
                R_triangle_angle = 90 - user_angle
                R_triangle_angle = math.radians(R_triangle_angle)
                line_length = R_triangle_leg_1/(math.cos(R_triangle_angle))
    
                second_coord_x = 0
                second_coord_y = math.sin(R_triangle_angle)*line_length
                second_coord_y = second_coord_y + y
                slope = (second_coord_y - y)/(second_coord_x - x)
                intercept = y - slope*x
                
                if second_coord_y > num_rows:
                    second_coord_y = num_rows
                    second_coord_x = (second_coord_y - intercept)/slope
   
            elif user_angle > 270 and user_angle < 360:
                user_angle = user_angle - 270
                leg_1 = x
                R_triangle_leg_1 = y
                R_triangle_angle = 90 - user_angle
                R_triangle_angle = math.radians(R_triangle_angle)
                line_length =  R_triangle_leg_1/(math.cos(R_triangle_angle))

                second_coord_y = 0
                second_coord_x = math.sin(R_triangle_angle)*line_length
                second_coord_x = x - second_coord_x   

                slope = (second_coord_y - y)/(second_coord_x - x)
                intercept = y - slope*x
                
                if second_coord_x < 0:    
                    second_coord_x = 0
                    second_coord_y = slope*second_coord_x + intercept    

            elif user_angle == 0:
                second_coord_y = 0
                second_coord_x = x

            elif user_angle == 90:
                second_coord_y = y
                second_coord_x = num_cols
                
            elif user_angle == 180:
                second_coord_y = num_rows
                second_coord_x = x

            elif user_angle == 270:
                second_coord_y = y
                second_coord_x = 0
            
            x1s.append(x)
            x2s.append(second_coord_x)
            y1s.append(y)
            y2s.append(second_coord_y)
            
            imgplot = plt.imshow(img)
          
            for coord in range(len(x1s)):
                plt.scatter([x1s[coord]],[y1s[coord]], c='k', s=5)  
                plt.plot([x1s[coord], x2s[coord]], [y1s[coord], y2s[coord]], 'y-')
            
            plt.show(block=False)
        
            print '\n', '> REVIEW IMAGE FOR DESIRED DEMARKATION.'

            while accept_flag != 'y' and accept_flag != 'n':
                accept_flag = raw_input('\t' + '> PROCEED WITH IMAGE PROCESSING (y/n)? ')
            
            if accept_flag == 'n':
                x1s = x1s[0:-1]
                y1s = y1s[0:-1]
                x2s = x2s[0:-1]
                y2s = y2s[0:-1]
                print '\n'
                
            plt.close()
    
        print '\n', '> IMAGE PROCESSING IN PROGRESS. PLEASE WAIT . . .', '\n'
        
        if user_angle_copy == 0:
            y_points = [coord for coord in range(int(y), int(second_coord_y), -1)]
            x_points = [user_point_coord_col for y_point in range(len(y_points))]
           
        elif user_angle_copy < 90:
            if user_angle_copy >= 20:
                x_points = [coord for coord in range(int(x), int(second_coord_x))]
                y_points = []    
                for x_point in x_points:
                    y_points.append(slope*x_point+intercept)
            else:
                y_points = [coord for coord in range(int(y), int(second_coord_y), -1)]
                x_points = []
                for y_point in y_points:
                    x_points.append((y_point - intercept) / slope)
                
        elif user_angle_copy == 90:
            x_points = [coord for coord in range(int(x), int(second_coord_x))]
            y_points = []
            for x_point in x_points:
                y_points = [user_point_coord_row for x_point in range(len(x_points))]
      
        elif user_angle_copy > 90 and user_angle_copy < 180:
            if user_angle_copy < 160:
                x_points = [coord for coord in range(int(x), int(second_coord_x))]
                y_points = []
                for x_point in x_points:
                    y_points.append(slope*x_point+intercept)
            else:
                y_points = [coord for coord in range(int(y), int(second_coord_y))]
                x_points = []
                for y_point in y_points:
                    x_points.append((y_point - intercept)/slope)
        
        elif user_angle_copy == 180:
            y_points = [coord for coord in range(int(y), int(second_coord_y))]
            x_points = [user_point_coord_col for y_point in range(len(y_points))]
       
        elif user_angle_copy > 180 and user_angle_copy < 270:
            if user_angle_copy > 200:
                x_points = [coord for coord in range(int(x), int(second_coord_x), -1)]
                y_points = []
                for x_point in x_points:
                    y_points.append(slope*x_point+intercept)    
            else:
                y_points = [coord for coord in range(int(y), int(second_coord_y))]
                x_points = []
                for y_point in y_points:
                    x_points.append((y_point - intercept)/slope)
                
        elif user_angle_copy == 270:
            x_points = [coord for coord in range(int(x), int(second_coord_x), -1)]
            y_points = [user_point_coord_row for x_point in range(len(x_points))]
       
        elif user_angle_copy > 270 and user_angle_copy < 360:
            if user_angle_copy < 340: 
                x_points = [coord for coord in range(int(x), int(second_coord_x), -1)]
                y_points = []
                for x_point in x_points:
                    y_points.append(slope*x_point+intercept) 
            else:
                y_points = [coord for coord in range(int(y), int(second_coord_y), -1)]
                x_points = []
                for y_point in y_points:
                    x_points.append((y_point - intercept)/slope)
                

        pixel_list = []
        pixel_colors = []
        for coord in range(len(x_points)):
            pixel_list.append(img[int(y_points[coord])][int(x_points[coord])])    
        
        for pixel in pixel_list:
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
                pixel_colors.append('W')
            elif pixel[0] < 200 and pixel[1] < 200 and pixel[2] < 200:
                pixel_colors.append('R')
            else:
                pixel_colors.append('?')
                
        print '> IMAGE PROCESSING COMPLETE!', '\n'

        RAC_count = 0
        for color in range(len(pixel_colors)):
            if pixel_colors[color] == '?':
                pixel_colors[color] = pixel_colors[color-1]

        for color in range(len(pixel_colors)):    
            if pixel_colors[color] != pixel_colors[color-1]:
                RAC_count += 1         

        if RAC_count % 2 == 0:
            RAC_count = RAC_count/2
        else:
            RAC_count = RAC_count/2 + 1
        RACs.append(RAC_count)
        
        print '\t' + '> RAC COUNT FOR ' + image_files[i_f][0:-4] + '_X' + str(user_point_coord_col) + '_Y' + str(user_point_coord_row) + '_angle_' + str(user_angle_copy) + ' = ' + str(RAC_count) + '\n'
    
        print '> NOW WRITING DATA TO .TXT OUTPUT IN WORKING DIRECTORY . . . ', '\n' 
        
        RAC_out.write(image_files[i_f] + '\t' + str(user_point_coord_row) + '\t' + str(user_point_coord_col) + '\t' + str(user_angle_copy) + '\t' + str(RAC_count) + '\n')
    
        measure = raw_input('> WOULD YOU LIKE TO PERFORM ANOTHER MEASUREMENT ON THIS IMAGE (y/n)? ')
        first_flag = False    
        
    imgplot = plt.imshow(img)
    
    for coord in range(len(x1s)):
        plt.scatter([x1s[coord]],[y1s[coord]], c='k', s=5)
        plt.plot([x1s[coord], x2s[coord]], [y1s[coord], y2s[coord]], 'y-')     
    
    print '\n', '> SAVING CUMULATIVE MARKUP IMAGE FOR REFERENCE IN OUTPUT_IMAGES DIRECTORY . . .'
    plt.savefig(image_files[i_f][0:-4] + '_labeled.tif', dpi=1000)  
    plt.close()
    
    RAC_average = 0
    RAC_average = sum(RACs)/float(len(RACs))
    RAC_out.write('RAC AVERAGE = ' + str(RAC_average) + '\n')
    
    if i_f + 1 != len(image_files):
        raw_input('> PRESS ENTER TO CONTINUE WITH NEXT IMAGE: ')
        os.chdir('../')
    else:
        print '\n'*3, '> ALL FILES IN THE INPUT_IMAGES DIRECTORY HAVE BEEN PROCESSED!', '\n'*2
        RAC_out.close()
        plt.close()
        print 'P R O G R A M  T E R M I N A T E D', '\n'