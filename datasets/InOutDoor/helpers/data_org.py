# to split images and annoations according to sequence lists in ImageSets
import shutil
import sys

seq_num = sys.argv[1]
source = '../Images'
dest = f'../Images/seq{seq_num}'

#source = '../Annotations'
#dest = f'../Annotations/seq{seq_num}'

with open(f'../ImageSets/seq{seq_num}.txt','r') as filelist:
    for line in filelist:
        filename = line.strip()
        source_file = f"{source}/{filename}.png"
        dest_file = f"{dest}/{filename}"
        shutil.move(source_file, dest_file)

