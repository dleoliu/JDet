type='FAIR'
source_fair_dataset_path='/scratch/acd13834xw/FAIR1M2/origin_data_hr'
source_dataset_path='/scratch/acd13834xw/FAIR1M2/fair_DOTA_1024_hr'
target_dataset_path='/scratch/acd13834xw/FAIR1M2/processed_1024_hr'
convert_tasks=['train','val','test']

# available labels: train, val, test, trainval
tasks=[
    dict(
        label='trainval',
        config=dict(
            subimage_size=1024,
            overlap_size=200,
            multi_scale=[1.],
            horizontal_flip=False,
            vertical_flip=False,
            rotation_angles=[0.] 
        )
    ),
    dict(
        label='test',
        config=dict(
            subimage_size=1024,
            overlap_size=200,
            multi_scale=[1.],
            horizontal_flip=False,
            vertical_flip=False,
            rotation_angles=[0.] 
        )
    )
]
