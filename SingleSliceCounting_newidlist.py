import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image
import os
import json
import cv2
from skimage.io import imread
#from libtiff import *
import xlrd
import csv
#from scipy import misc


def getgrayarea(img):
    gray2area = {}
    grays = np.unique(img)
    for gray in grays:
        if gray == 0:
            continue
        area = np.sum(img == gray)
        gray2area[gray] = area
    return gray2area


def getStatic(region2grayFile, brain3Dimg, labelcsv, outFolder, scale):
    if not os.path.exists(outFolder):
        os.mkdir(outFolder)
    print ('reading region2gray...')
    grays = []
    names = []

    with open(region2grayFile) as fin:
        for line in fin:
            temp = line.strip().split(';')
            ids = temp[2].split(',')
            grays.append(int(ids[0]))
            names.append(temp[1] + '_left')
            grays.append(int(ids[1]))
            names.append(temp[1] + '_right')
    names.append('others_left')
    grays.append(1300)
    names.append('others_right')
    grays.append(1400)

    print ('get statics...')

    img2detail = {}
    with open(labelcsv) as fin:
        for line in fin:
            temp = line.strip().split(',')
            # 
            z = temp[0]
            x = temp[1]
            y = temp[2]

            if not z in img2detail:
                img2detail[z] = []
            img2detail[z].append([x, y])
    for img in img2detail:
        print (img)
        imgname = brain3Dimg + ('%02d.tif' % int(img))
        #imgname = brain3Dimg + ('%d.tif' % int(img))
        print(imgname)
        #slice = cv2.imread(imgname, cv2.IMREAD_UNCHANGED)
        slice = imread(imgname)
        shape = slice.shape
        gray2area = getgrayarea(slice)
        graystat = np.zeros((len(grays)+1, 1), dtype=int)
        for pnt in img2detail[img]:
            x = int(float(pnt[0]) * scale)
            y = int(float(pnt[1]) * scale)
            if y >= shape[0] or x >= shape[1]:
                print('outliers')
                continue
            gray = slice[y, x]
            if gray == 0:
                ind = len(grays)
            else:
                #mask = np.zeros(slice.shape, dtype=np.uint8)
                #mask[slice == gray] = 255
                #cv2.imwrite('test.jpg', mask)
                if not gray in grays:
                    print ('error3')
                    print(gray)
                    return
                ind = grays.index(gray)
            graystat[ind] += 1
        print ('output the statistics...')
        #fout = open(outFolder + bytes(img, 'utf-8') + '.csv', 'w')
        fout = open(outFolder + str(img) + '.csv', 'w')
        fout.write('name,gray,cell,area\n')
        for i in range(len(grays)):
            fout.write('%s,%d,' % (names[i], grays[i]))
            gray = grays[i]
            if not gray in gray2area:
                fout.write('NaN,NaN\n')
            else:
                ind = grays.index(gray)
                fout.write('%d,%d\n' % (graystat[ind], gray2area[gray]))
        fout.close()


if __name__ == '__main__':
    brain2gray = 'newidlist_order.txt'
    template = 'ANOnew_order\\'
    pnts = 'pnt_correct_rotated_5-3.csv'
    outfolder = 'SSc\\'
    getStatic(brain2gray, template, pnts, outfolder, 0.25)
