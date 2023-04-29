Preparation for InOutDoor (from scratch, in case you need it)
1. split images and annotations into 4 sequences according to ImageSets/seq#.txt  # = sequence number
2. rename images and annotations to %6d 
3. create labels_with_ids directory and follow FairMOT directory structure 
4. in images/train/seq#/
    create det, gt, img1 directories, store images in img1
    create seqinfo.ini
        [Sequence]
        name=seq0
        imDir=img0
        frameRate=30
        seqLength=2334
        imWidth=1920
        imHeight=1080
        imExt=.png

(from here, the process can be simplified but this is what i did)
5. create gt2.txt for each sequence
   run InoutDoor/helpers/dataloader.py (takes in sequence number, 0~3) -> creates gt2.txt, this has wrong ID numbers and skips empty frames
6. run datasets/data_path/gen_labels_inout.py 
    - this creates text files for all images, saved in labels_with_ids
    - now since empty frames are skipped in gt2.txt, empty frames don't have the labels -> use this fact to remove empty frames in the images
7. run datasets/InOutDoor/helpers/check_files.py to remove emtpy frames 
    - run for both images and annotations
8. rename images and annoations to %6d (so no skipping between frames, not sure this is necessary)
9. rerun InOutDoor/helpers/dataloader.py to recreate gt.txt (here, make sure to change the output file name from gt2.txt to gt.txt)
10. clear labels_with_ids directory, and rerun gen_labels_inout.py 
    - double check number of files in labels_with_ids match with img1 for each sequence
11. the fun part begins. REASSIGNING IDs.
    - for gt.txt in InoutDoor/images/train/seq#/gt/gt.txt
    - go through all annotations and images and assign correct IDs (ID is second column)
    - use macros in vim to automate

12. in datasets/data_path/prepare.py
    Train set:
        line 80: if video_name != "seq3"
        line 116: save_path = './inout_seq02_new.train' #can be anything but that's what I used
    Test set:
        line 80: if video_name == "seq3"
        line 116: save_path = './inout_seq3_new.val' #can be anything but that's what I used
======================================================================================================
resnet50:
    in main.py line 66: '--backbone' is set to resnet50 (currently resnet18)
    in models/backbone.py: uncomment lines 76~78 and comment out lines 80~82
                          uncomment lines 85, 87 and comment out lines 86,88  
(the code is for resnet18 right now) 

======================================================================================================
<Results>
MOT15:
 In eval.py: change data path in lines 271 ~ 272, 348 (currently set to InOutDoor)
             uncomment lines 418 ~ 419 to label with correct sequence names

 In configs/r50_motr_eval.sh:
    --pretrained ${EXP_DIR}/model_motr_final.pth
    --resume ${EXP_DIR}/model_motr_final.pth

 Evaluation results in exps/e2e_motr_r50_joint

InOutDoor:
 To train:
    in configs/r50_motr_train.sh:
        * change EXP_DIR 
        PRETRAIN = exps/inout_train_3/r50_deformable_detr_plus_iterative_bbox_refinement.pth (this is pretrained on coco and crowdHuman)
        --datset_file e2e_mot (the repo uses e2e_joint which is for MOT17 and CrowdHuman; doesn't work for InOutDoor)
        --data_txt_path_train ./datasets/data_path/inout_seq02_new.train \ 
        --data_txt_path_val ./datasets/data_path/inout_seq3_new.val \
        
 To evaluate:
    in configs/r50_motr_eval.sh:
        --datset_file e2e_mot (the repo uses e2e_joint which is for MOT17 and CrowdHuman; doesn't work for InOutDoor)
        --pretrained ${EXP_DIR}/checkpoint.pth
        --resume ${EXP_DIR}/checkpoint.pth   
    
    in eval.py, make sure the data paths are set to InOutDoor and correct seq_nums (if you didn't switch to MOT15, they are all set to InOutDoor by default)

 Results: exps/inout_train_3
    weight: checkpoint.pth
    evalaution results: exps/inout_train_3/results

Distillation:
 change to resnet18 in main.py and modles/backbone.py
 To train:
    in configs/r50_mor_train.sh:
        PRETRAIN = exps/inout_train_3/checkpoint.pth (undistilled model)
        --datset_file e2e_mot (the repo uses e2e_joint which is for MOT17 and CrowdHuman; doesn't work for InOutDoor)
        --data_txt_path_train ./datasets/data_path/inout_seq02_new.train \ 
        --data_txt_path_val ./datasets/data_path/inout_seq3_new.val \

 To evaluate:
    in configs/r50_motr_eval.sh:
        --pretrained ${EXP_DIR}/checkpoint.pth (checkpoint from training)
        --resume ${EXP_DIR}/checkpoint.pth (checkpoint from training)
        --datset_file e2e_mot (the repo uses e2e_joint which is for MOT17 and CrowdHuman; doesn't work for InOutDoor)

 Results: exps/inout_kd
    weight: checkpoint.pth
    evaluation results: exps/inout_kd/results
