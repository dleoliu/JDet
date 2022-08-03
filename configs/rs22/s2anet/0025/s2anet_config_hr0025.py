_base_ = "s2anet_r50_fpn_1x_dota_rotate_balance_ms_fair.py"

dataset = dict(
    train=dict(
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed_1024_hr/trainval_1024_200_1.0",
        batch_size=8,
        num_workers=18,
    ),
    val=dict(
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed_1024_hr/trainval_1024_200_1.0",
        batch_size=8,
        num_workers=18,
    ),
    test=dict(
        images_dir="/scratch/acd13834xw/FAIR1M2/processed_1024_hr/test_1024_200_1.0/images/",
        batch_size=8,
        num_workers=18,
    ),
)

optimizer = dict(
    lr=0.0025,
)

max_epoch = 6
