
import os 
from PIL import Image
import numpy as np 

from jdet.utils.registry import DATASETS
from .transforms import Compose

from jittor.dataset import Dataset 

@DATASETS.register_module()
class ImageDataset(Dataset):

    def __init__(self,img_files,
                      transforms=[
                          dict(
                              type="Resize",
                              min_size=[800],
                              max_size=1333
                          ),
                          dict(
                              type="Pad",
                              size_divisor=32
                          ),
                          dict(
                              type="Normalize",
                              mean=[123.675, 116.28, 103.53],
                              std = [58.395, 57.12, 57.375],
                          )
                      ],
                      batch_size=1,
                      num_workers=0,
                      shuffle=False):
        super(ImageDataset,self).__init__(batch_size=batch_size,num_workers=num_workers,shuffle=shuffle)
        self.img_files = img_files
        self.total_len = len(img_files)
        if isinstance(transforms,list):
            transforms = Compose(transforms)
        if transforms is not None and not callable(transforms):
            raise TypeError("transforms must be list or callable")
        self.transforms = transforms
    
    def __getitem__(self,index):
        img = Image.open(self.img_files[index]).convert("RGB")
        targets = dict(
            ori_img_size=img.size,
            img_file = self.img_files[index]
        )

        if self.transforms:
            img,targets = self.transforms(img,targets)
        return img,targets 
    
    def collate_batch(self,batch):
        imgs = []
        anns = []
        max_width = 0
        max_height = 0
        for image,ann in batch:
            height,width = image.shape[-2],image.shape[-1]
            max_width = max(max_width,width)
            max_height = max(max_height,height)
            imgs.append(image)
            anns.append(ann)
        N = len(imgs)
        batch_imgs = np.zeros((N,3,max_height,max_width),dtype=np.float32)
        for i,image in enumerate(imgs):
            batch_imgs[i,:,:image.shape[-2],:image.shape[-1]] = image
        
        return batch_imgs,anns 
        