import os
import glob
import re
import sys
# Read annotations from folder and convert to MOT format and save to txt file
num = sys.argv[1] # sequence number 
input_path = f"../Annotations/seq{num}/"
#output_path = f"../images/train/seq{num}/gt/gt.txt"
output_path = f"../images/train/seq{num}/gt/gt2.txt"
files = sorted(glob.glob(os.path.join(input_path,"0*")))
frame_num = 0
xmax,xmin,ymax,ymin,category = None,None,None,None,None

i = 0
for file in files:
    frame_num+=1
    annotations = []
    with open(file) as f:
        lines = f.readlines()
        with open(output_path, 'a') as f:
            count = 0
            for obj_line in lines:
                print(obj_line)
                if "bndbox" in obj_line:
                    extraction = re.findall(r'\d+\.\d+|\d+', obj_line)
                    xmax, xmin, ymax, ymin = list(map(float,extraction))
                if "name" in obj_line and not ".jpg" in obj_line:
                    category = count +1
                    count += 1

                if (xmax and xmin and ymax and ymin and category) != None:
                    #if frame_num == frame_ids[i][0]:
                    #    #print(frame_num,frame_ids[i])
                    #    category = frame_ids[i][1]
                    # MOT: <frame>,<ID>,<left>,<top>,<width>,<height>,<conf>,<x>,<y>,<z>
                    annotations+=[f"{frame_num},{category},{xmin},{ymin},{xmax-xmin},{ymax-ymin},1,-1,-1,-1"]
                    print(annotations)
                    xmax,xmin,ymax,ymin,category = None,None,None,None,None
                   # i+=1
    # save the annotations
    with open(output_path, 'a') as f:
        for line in annotations:
            f.write(f"{line}\n")
