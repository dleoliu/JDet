_base_ = 's2anet_r50_fpn_1x_dota.py'

dataset = dict(
    _cover_ = True,
    val=dict(
        type="FAIRDataset",
        dataset_dir='/scratch/acd13834xw/FAIR1M2/processed_1024/trainval_1024_200_1.0',
        transforms=[
            dict(
                type="RotatedResize",
                min_size=1024,
                max_size=1024
            ),
            dict(
                type = "Pad",
                size_divisor=32),
            dict(
                type = "Normalize",
                mean =  [123.675, 116.28, 103.53],
                std = [58.395, 57.12, 57.375],
                to_bgr=False,)
        ],
        batch_size=2,
        num_workers=18,
        shuffle=True
    ),
    train=dict(
        type="FAIRDataset",
        dataset_dir='/scratch/acd13834xw/FAIR1M2/processed_1024/trainval_1024_200_1.0',
        transforms=[
            dict(
                type="RotatedResize",
                min_size=1024,
                max_size=1024
            ),
            dict(
                type='RotatedRandomFlip',
                prob=0.5),
            dict(
                type = "Pad",
                size_divisor=32),
            dict(
                type = "Normalize",
                mean =  [123.675, 116.28, 103.53],
                std = [58.395, 57.12, 57.375],
                to_bgr=False,)
        ],
        batch_size=2, 
        num_workers=18,
        shuffle=True
    ),
    test = dict(
        type= "ImageDataset",
        dataset_type="FAIR",
        images_dir= "/scratch/acd13834xw/FAIR1M2/processed_1024/test_1024_200_1.0/images/",
        transforms= [
        dict(
            type= "RotatedResize",
            min_size= 1024,
            max_size= 1024),
        dict(
                type = "Pad",
                size_divisor=32),
        dict(
            type= "Normalize",
            mean=  [123.675, 116.28, 103.53],
            std= [58.395, 57.12, 57.375],
            to_bgr= False)
        ],
        num_workers= 18,
        batch_size= 1)
)

max_epoch = 6
