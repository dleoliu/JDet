import logging
import jittor as jt
import os 
import cv2 

from jdet.config.config import get_cfg,write_cfg
from jdet.utils.registry import build_from_cfg,META_ARCHS,OPTIMS,DATASETS,HOOKS
from jdet.utils.checkpointer import Checkpointer


def draw_box(img,box,text,color):
    box = [int(x) for x in box]
    img = cv2.rectangle(img=img, pt1=tuple(box[0:2]), pt2=tuple(box[2:]), color=color, thickness=1)
    img = cv2.putText(img=img, text=text, org=(box[0],box[1]-5), fontFace=0, fontScale=0.5, color=color, thickness=1)
    return img 

def draw_boxes(img,boxes,cats):
    if isinstance(img,jt.Var):
        img = img.numpy()
    for box,cat in zip(boxes,cats):
        img = draw_box(img,box,cat,(255,0,0))
    cv2.imwrite("test.png",img)


class Runner:
    def __init__(self,mode="whole"):
        cfg = get_cfg()
        self.cfg = cfg
        self.work_dir = os.path.abspath(cfg.work_dir)
        self.max_epoch = cfg.epoch 
        self.max_iter = cfg.max_iter
        self.log_interval = cfg.log_interval
        self.save_interval = cfg.save_interval
        self.resume_path = cfg.resume

        os.makedirs(self.work_dir,exist_ok=True)
        save_config_file = os.path.join(self.work_dir,"config.yaml")
        write_cfg(save_config_file)

    
        self.model = build_from_cfg(cfg.model,META_ARCHS)
        self.optimizer = build_from_cfg(cfg.optim,OPTIMS,params=self.model.parameters())
        self.scheduler = build_from_cfg(cfg.solver,OPTIMS,optimizer=self.optimizer)
        self.train_dataset = build_from_cfg(cfg.dataset.train,DATASETS)
        self.val_dataset = build_from_cfg(cfg.dataset.val,DATASETS)
        self.test_dataset = build_from_cfg(cfg.dataset.test,DATASETS)
        
        self.logger = build_from_cfg(cfg.logger,HOOKS)
        self.checkpointer = Checkpointer(model=self.model,optimizer=self.optimizer,scheduler = self.scheduler)
        self.iter = 0
        self.epoch = 0
    

    def save(self):
        save_file = os.path.join(self.work_dir,f"/ckpt_{self.epoch}.pkl")
        self.checkpointer.save(save_file)
    
    def resume(self):
        self.iter,self.epoch = self.checkpointer.load(self.resume_path)
        
    def display(self,images,targets):
        for image,target in zip(images,targets):
            mean = target["mean"]
            std = target["std"]
            to_bgr = target["to_bgr"]
            if to_bgr:
                image = image[::-1]
            image *=255.
            image = image*std+mean
            image = image[::-1]
            image = image.transpose(1,2,0)
            
            classes = [target["classes"][i-1] for i in target["labels"]]
            draw_boxes(image,target["bboxes"],classes)
    
    def run(self):
        print("running") 
        while self.epoch < self.max_epoch:
            self.train()
            if self.epoch % self.save_interval == 0:
                self.save_checkpoint()
            if self.epoch % self.val_interval == 0:
                self.val()
            self.epoch +=1
        self.test()

    def train(self):
        self.model.train()
        for batch_idx,(images,targets) in enumerate(self.train_dataset):
            # self.display(images,targets)
            results,losses = self.model(images,targets)
            self.optimizer.step(losses)
            self.scheduler.step()
            self.logger.log({"losses":losses.item()})
   
    @jt.no_grad()
    def run_on_images(self,img_files,save_dir=None):
        self.model.val()
        dataset = build_from_cfg("ImageDataset",img_files=img_files)
        for i,(images,targets) in enumerate(dataset):
            results = self.model(images,targets)

    @jt.no_grad()
    def val(self):
        self.model.val() 
    
    @jt.no_grad()
    def test(self):
        self.model.val()
    

    