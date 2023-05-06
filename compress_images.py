# compresses each prediction image for display in dash app using PIL library

import os
from PIL import Image

rootdir = 'Finished'
count = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:     
        if file.endswith('.jpg'):
            picture = Image.open(subdir + '/' + file)
            picture.save(str(count) + '.jpg', 
                 "JPEG", 
                 optimize = True, 
                 quality = 5)
            count = count + 1