# Imports model that has been created and outputs a prediction image for each aerial image

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import earthpy.plot as ep
import cv2

from tensorflow.keras.layers import Input, Conv3D, Flatten, Dense, Dropout
from tensorflow.keras import Model

# createImageCubes and padWithZeros borrowed code from 
# https://github.com/mahmad00/A-Fast-and-Compact-3-D-CNN-for-HSIC/blob/master/A_Fast_3D_CNN_for_HSIC_v2.ipynb
# and https://gist.github.com/syamkakarla98/c76733c48d739a17c1d638450be06f4e

def padWithZeros(X, margin=2):
    newX = np.zeros((X.shape[0] + 2 * margin, X.shape[1] + 2* margin, X.shape[2]))
    x_offset = margin
    y_offset = margin
    newX[x_offset:X.shape[0] + x_offset, y_offset:X.shape[1] + y_offset, :] = X
    return newX

def createImageCubesX(X, windowSize=5, removeZeroLabels = False):
    margin = int((windowSize - 1) / 2)
    zeroPaddedX = padWithZeros(X, margin=margin)
    # split patches
    patchesData = np.zeros((X.shape[0] * X.shape[1], windowSize, windowSize, X.shape[2]), dtype = 'uint8')
    patchIndex = 0
    for r in range(margin, zeroPaddedX.shape[0] - margin):
        for c in range(margin, zeroPaddedX.shape[1] - margin):
            patch = zeroPaddedX[r - margin:r + margin + 1, c - margin:c + margin + 1]   
            patchesData[patchIndex, :, :, :] = patch
            patchIndex = patchIndex + 1
    if removeZeroLabels:
        patchesData = patchesData[patchesLabels>0,:,:,:]
        patchesLabels -= 1
    return patchesData

def seg_save(y_data, filename):
    gt = np.zeros((y_data.shape[0], y_data.shape[1], 3), dtype = 'uint8')
    gt[y_data == 0] = [0,0,255] # Red for Maple
    gt[y_data == 1] = [0,255,255] # Yellow for Aspen
    gt[y_data == 2] = [0,165,255] # Orange for Oak
    gt[y_data == 3] = [0,100,0] # Dark green for Fir
    gt[y_data == 4] = [50,205,50] # Lime green for Other
    gt[y_data == 5] = [220,245,245] # Beige for None

    cv2.imwrite(filename, gt)

windowSize = 7
K = 4

output_units = 6

input_layer = Input((windowSize, windowSize, K, 1))

x = Conv3D(filters=16, kernel_size=(3, 3, 2), activation='relu')(input_layer)
x = Conv3D(filters=32, kernel_size=(3, 3, 2), activation='relu')(x)
x = Conv3D(filters=64, kernel_size=(2, 2, 2), activation='relu')(x)
x = Conv3D(filters=64, kernel_size=(2, 2, 1), activation='relu')(x)

x = Flatten()(x)

x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
output_layer = Dense(units=output_units, activation='softmax')(x)

model = Model(name = 'Wasatch_Model' , inputs=input_layer, outputs=output_layer)

model.load_weights('Wasatch_Model.h5')

rootdir = 'wasatch_images'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))
        print(subdir + subdir.lstrip(rootdir) + '.jpg')      
        if file.endswith('.tif'):
            im = plt.imread(os.path.join(subdir, file))
            # Create 3D Patches
            X = createImageCubesX(im, windowSize=windowSize)
            pred_t = model.predict(X.reshape(-1, windowSize, windowSize, K, 1),
                       batch_size=10000, verbose=1)
            pred_data = np.argmax(pred_t, axis=1).reshape(im.shape[0], im.shape[1])
            seg_save(pred_data, subdir + subdir.lstrip(rootdir) + '.jpg')