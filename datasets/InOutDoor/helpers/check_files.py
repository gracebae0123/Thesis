import os
import sys
seq_num = sys.argv[1]

# uncomment these to remove empty images 
#seq_root = f"../images/train/seq{seq_num}/img1"
#lab_root = f"../labels_with_ids/train/seq{seq_num}/img1"

#img_files = os.listdir(seq_root)
#img_files = [img.replace('.png','') for img in img_files]
#lab_files = os.listdir(lab_root)
#lab_files = [lab.replace('.txt','') for lab in lab_files]

img_root = f"../Annotations/seq{seq_num}"
lab_root = f"../images/train/seq{seq_num}/img1"

img_files = os.listdir(img_root)
img_files = [img.replace('.yml','') for img in img_files]
lab_files = os.listdir(lab_root)
lab_files = [lab.replace('.png','') for lab in lab_files]


for imge in img_files:
    if imge not in lab_files and imge != '.DS_Store':
        path = os.path.join(img_root,imge+'.yml')
        print(path)
        os.remove(path)


img_files = os.listdir(img_root)
print(len(img_files))
print(len(lab_files))
