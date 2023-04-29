# ------------------------------------------------------------------------
# Copyright (c) 2021 megvii-model. All Rights Reserved.
# ------------------------------------------------------------------------
# Modified from Deformable DETR (https://github.com/fundamentalvision/Deformable-DETR)
# Copyright (c) 2020 SenseTime. All Rights Reserved.
# ------------------------------------------------------------------------

# for MOT17

EXP_DIR=exps/inout_kd
python3 eval.py \
    --meta_arch motr \
    --dataset_file e2e_mot \
    --epoch 200 \
    --with_box_refine \
    --lr_drop 100 \
    --lr 1e-4 \
    --lr_backbone 2e-5 \
   --pretrained ${EXP_DIR}/checkpoint.pth \
    --output_dir ${EXP_DIR} \
    --batch_size 1 \
    --sample_mode 'random_interval' \
    --sample_interval 10 \
    --sampler_steps 50 90 120 \
    --sampler_lengths 2 3 4 5 \
    --update_query_pos \
    --merger_dropout 0 \
    --dropout 0 \
    --random_drop 0.1 \
    --fp_ratio 0.3 \
    --query_interaction_layer 'QIM' \
    --extra_track_attn \
    --resume ${EXP_DIR}/checkpoint.pth \
