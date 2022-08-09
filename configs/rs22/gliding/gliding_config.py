_base_ = "gliding_r50_fpn_1x_dota_with_flip_rotate_balance_cate.py"

model = dict(
    bbox_head=dict(
        num_classes=37,
    )
)

dataset = dict(
    train=dict(
        type="FAIRDataset",
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed_1024/trainval_1024_200_1.0",
        batch_size=8,
        num_workers=18,
    ),
    val=dict(
        type="FAIRDataset",
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed_1024/trainval_1024_200_1.0",
        batch_size=8,
        num_workers=18,
    ),
    test=dict(
        dataset_type="FAIR",
        images_dir="/scratch/acd13834xw/FAIR1M2/processed_1024/test_1024_200_1.0/images/",
        batch_size=8,
        num_workers=18,
    ),
)

max_epoch = 12
