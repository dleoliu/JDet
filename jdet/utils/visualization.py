import numpy as np
import jittor as jt
import cv2 
import os

def draw_box(img,box,text,color):
    box = [int(x) for x in box]
    img = cv2.rectangle(img=img, pt1=tuple(box[0:2]), pt2=tuple(box[2:]), color=color, thickness=1)
    img = cv2.putText(img=img, text=text, org=(box[0],box[1]-5), fontFace=0, fontScale=0.5, color=color, thickness=1)
    return img 

def draw_rbox(img,box,text,color):
    box = [int(x) for x in box]
    img = cv2.rectangle(img=img, pt1=tuple(box[0:2]), pt2=tuple(box[2:]), color=color, thickness=1)
    img = cv2.putText(img=img, text=text, org=(box[0],box[1]-5), fontFace=0, fontScale=0.5, color=color, thickness=1)
    return img 

def draw_mask(img,box,mask,text,color):
    pass

def draw_boxes(img,boxes,cats):
    if isinstance(img,jt.Var):
        img = img.numpy()
    for box,cat in zip(boxes,cats):
        img = draw_box(img,box,cat,(255,0,0))
    cv2.imwrite("test.png",img)

def visualize_results(detections,classes,files,save_dir):
    os.makedirs(save_dir,exist_ok=True)
    for (bboxes,scores,labels),img_f in zip(detections,files):
        if hasattr(bboxes,"numpy"):
            bboxes = bboxes.numpy()
        if hasattr(scores,"numpy"):
            scores = scores.numpy()
        if hasattr(labels,"numpy"):
            labels = labels.numpy()
        cats = [classes[l-1] for l in labels]
        img = cv2.imread(img_f)
        print(len(cats))
        for box,cate,score in zip(bboxes,cats,scores):
            text = f"{cate}:{score:.2f}"
            img = draw_box(img,box,text,(255,0,0))
        cv2.imwrite(os.path.join(save_dir,img_f.split("/")[-1]),img)

def visual_gts(targets,save_dir):
    for t in targets:
        bbox = t["bboxes"]
        labels = t["labels"]
        classes = t["classes"]
        ori_img_size = t["ori_img_size"]
        img_size = t["img_size"]
        bbox[:,0::2] *= (ori_img_size[0]/img_size[0])
        bbox[:,1::2] *= (ori_img_size[1]/img_size[1])
        img_f = t["img_file"]
        img = cv2.imread(img_f)
        for box,l in zip(bbox,labels):
            text = classes[l-1]
            img = draw_box(img,box,text,(255,0,0))
        cv2.imwrite(os.path.join(save_dir,"test.jpg"),img)
            
        

