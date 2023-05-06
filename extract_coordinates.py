# extracts coordinates from downloaded USGS text files 
# for each image and saves them to numbered text file

import os

rootdir = 'Finished'
count = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:    
        if file.endswith('.txt'):
            with open(subdir + '/' + file) as geodata:
                for line in geodata:
                    if line.strip().startswith("West_Bounding_Coordinate: "):
                        #print(float(line.split(':')[1].strip()))
                        west = line.split(':')[1].strip()
                    if line.strip().startswith("East_Bounding_Coordinate: "):
                        east = line.split(':')[1].strip()
                    if line.strip().startswith("South_Bounding_Coordinate: "):
                        south = line.split(':')[1].strip()
                    if line.strip().startswith("North_Bounding_Coordinate: "):
                        north = line.split(':')[1].strip()
                data = south + ',' + west + ',' + north + ',' + east
                with open(str(count) + '.txt', 'w') as f:
                    f.write(data)
                count = count + 1

#[[S, W], [N, E]]