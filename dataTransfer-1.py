import nrrd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import os
#
# Read image volume with NRRD reader
# Note that reader swaps the order of the first two axes
#
# AVGT = 3-D matrix of average_template
# NISSL = 3-D matrix of ara_nissl
# ANO = 3-D matrix of ccf_2015/annotation
#


#AVGT, metaAVGT = nrrd.read('average_template_25.nrrd')
#NISSL, metaNISSL = nrrd.read('ara_nissl_25.nrrd')
ANO, metaANO = nrrd.read('annotation_25.nrrd')
id2name = {}
id2newid = {}
with open('structurelite.txt') as fin:
    for line in fin:
        line = line.strip()
        ind = line.index(',')
        id2name[int(line[0:ind])] = line[ind+1:]

def saveANOorg(outpath):
    shape = ANO.shape
    for i in range(shape[0]):
        print('save image: %d' % i + 1)
        slice = ANO[i, :, :].astype(float)
        slice /= 2000
        if np.max(slice) > 1:
            print(i + 1)
        im = Image.fromarray(np.uint8(plt.cm.jet(slice) * 255))
        im.save(outpath + '/ano_coronal_' + str(i+1) + '.bmp')

def saveANOnew(inpath, outpath):
    newmask = np.load(inpath)
    maxvalue = np.max(newmask)
    shape = newmask.shape
    for i in range(shape[0]):
        print('save new image: %d' % i + 1)
        slice = newmask[i, :, :].astype(float)
        slice /= maxvalue
        im = Image.fromarray(np.uint8(plt.cm.jet(slice) * 255))
        im.save(outpath + '/ano_coronal_' + str(i+1) + '.bmp')

def getNewID(outfile):
    print('get new id and save to ' + outfile)
    ids = np.unique(ANO)
    for id in ids:
        if not id in id2name:
            id2name[id] = str(id)
    print('number of ids: %d', len(ids)-1)
    k = 0
    for id in ids:
        if id == 0:
            continue
        k += 1
        id2newid[id] = str(k) + ',' + str(k + len(ids)-1)
    fout = open(outfile, 'w')
    for id in ids:
        if id == 0:
            continue
        fout.write('%d' % id)
        fout.write(';' + id2name[id] + ';' + id2newid[id] + '\n')
    fout.close()

def getNewMask(outfile, saveImage):
    print('get new mask for data and save to ' + outfile)
    if saveImage == 1:
        if not os.path.exists(outfile):
            os.mkdir(outfile)
    newmask = np.zeros(ANO.shape, np.uint32)
    shape = ANO.shape
    middle = int(shape[2] / 2)
    for i in range(shape[0]):
        print('generate new mask %d' % i)
        slice = ANO[i, :, :]
        ids = np.unique(slice)
        for id in ids:
            if id == 0:
                continue
            if not id in id2newid:
                newids = ['1300', '1400']
                print('\tother cells exist!')
            else:
                newids = id2newid[id].split(',')
            maskleft = np.zeros(slice.shape, np.uint32)
            maskright = np.zeros(slice.shape, np.uint32)
            maskleft[slice == id] = int(newids[0])
            maskright[slice == id] = int(newids[1])
            newmask[i,:,0:middle] += maskleft[:,0:middle]
            newmask[i, :, middle:] += maskright[:, middle:]
        if saveImage == 1:
            im = Image.fromarray(newmask[i, :, :])
            im.save(os.path.join(outfile, str(i+1)+'.tif'))
    np.save(outfile + '.npy', newmask)

def checkmaskID(maskid, outcheck):
    print('check id for mask number %d' % maskid)
    k = 0
    slice = ANO[maskid-1, :, :]
    grays = np.unique(slice)
    for id in grays:
        if id == 0:
            continue
        k += 1
        temp = np.zeros(slice.shape)
        temp[slice == id] = 255
        cv2.imwrite(outcheck + '/' + str(maskid) + '_' + str(k) + '_' + id2name[id] + '.bmp', temp)
def checkcellID(cellid, outcheck):
    print('check id for cell id %d' % cellid)
    shape = ANO.shape
    for i in range(shape[0]):
        slice = ANO[i, :, :]
        if cellid in slice:
            temp = np.zeros(slice.shape)
            temp[slice == cellid] = 255
            cv2.imwrite(outcheck + '/mask' + str(i+1) + '_' + id2name[cellid] + '.bmp', temp)

def readNewID(infile):
    id2newid.clear()
    id2name.clear()
    with open(infile) as fin:
        for line in fin:
            line = line.strip()
            temp = line.split(';')
            id2name[int(temp[0])] = temp[1]
            id2newid[int(temp[0])] = temp[2]

if __name__ == '__main__':
    #save the original mask images
    #saveANOorg('output')

    #generate new ids
    #getNewID('newidlist.txt')

    #read the updated new id list
    readNewID('newidlist_order.txt')

    #generate all the masks of the cell ids in a give slice
    #checkmaskID(100, 'outcheck')

    #generate all the masks of a given cell id in all the slices
    #checkcellID(606826663, 'outcheck')

    #generate new mask file
    getNewMask('ANOnew_order', 1)

    #save the new mask images
    #saveANOnew('ANOnew.npy', 'outnew')



