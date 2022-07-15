_base_ = 'retinanet_r50v1d_fpn_fair.py'

dataset = dict(
    val=dict(
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed/trainval_600_150_1.0"
    ),
    train=dict(
        dataset_dir="/scratch/acd13834xw/FAIR1M2/processed/trainval_600_150_1.0"
    ),
    test=dict(
        images_dir="/scratch/acd13834xw/FAIR1M2/processed/test_600_150_1.0/images/"
    )
)
