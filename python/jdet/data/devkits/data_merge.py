import shutil
import jittor as jt 
from jdet.config.constant import DOTA1_CLASSES, DOTA1_5_CLASSES, DOTA2_CLASSES, FAIR_CLASSES_
from jdet.utils.general import check_dir
from jdet.models.boxes.box_ops import rotated_box_to_poly_single
from jdet.data.devkits.result_merge import mergebypoly
import os
import shutil
from tqdm import tqdm
import numpy as np
from jdet.data.devkits.dota_to_fair import dota_to_fair
from jdet.utils.general import is_win

def flip_box(box, target):
    ans = [box[i] for i in range(8)]
    if not "flip_mode" in target:
        return ans
    mode = target["flip_mode"]
    w = target['ori_img_size'][0]
    h = target['ori_img_size'][1]
    if ('H' in mode):
        for i in [0,2,4,6]:
            ans[i] = w - ans[i]
    if ('V' in mode):
        for i in [1,3,5,7]:
            ans[i] = h - ans[i]
    return ans

def prepare(result_pkl,save_path, classes):
    check_dir(save_path)
    results = jt.load(result_pkl)
    data = {}
    for result,target in tqdm(results):
        dets,labels = result
        img_name = os.path.splitext(os.path.split(target["img_file"])[-1])[0]
        for det,label in zip(dets,labels):
            bbox = det[:5]
            score = det[5]
            classname = classes[label]
            bbox = rotated_box_to_poly_single(bbox)
            bbox_ = flip_box(bbox, target)
            temp_txt = '{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n'.format(
                        img_name, score, 
                        bbox_[0], bbox_[1], bbox_[2], bbox_[3], 
                        bbox_[4], bbox_[5], bbox_[6], bbox_[7])
            if classname not in data:
                data[classname] = []
            data[classname].append(temp_txt)
    for classname,lines in data.items():
        f_out = open(os.path.join(save_path, classname + '.txt'), 'w')
        f_out.writelines(lines)
        f_out.close()

def prepare_gliding(result_pkl,save_path, classes):
    check_dir(save_path)
    results = jt.load(result_pkl)
    data = {}
    for result,target in tqdm(results):
        img_name = os.path.splitext(os.path.split(target["img_file"])[-1])[0]
        for bbox,score,label in zip(*result):
            classname = classes[label-1]
            bbox_ = flip_box(bbox, target)
            temp_txt = '{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n'.format(
                        img_name, score, 
                        bbox_[0], bbox_[1], bbox_[2], bbox_[3], 
                        bbox_[4], bbox_[5], bbox_[6], bbox_[7])
            if classname not in data:
                data[classname] = []
            data[classname].append(temp_txt)
    for classname,lines in data.items():
        f_out = open(os.path.join(save_path, classname + '.txt'), 'w')
        f_out.writelines(lines)
        f_out.close()

def prepare_fasterrcnn(result_pkl,save_path, classes):
    check_dir(save_path)
    results = jt.load(result_pkl)
    data = {}
    for result,target in tqdm(results):
        img_name = os.path.splitext(os.path.split(target['img_meta'][0]["img_file"])[-1])[0]
        for idx, res in enumerate(result):
            for i in range(res.shape[0]):
                bbox = res[i]
                classname = classes[idx]
                score = bbox[-1]
                bbox_ = [bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], bbox[5], bbox[6], bbox[7]]
                bbox_ = flip_box(bbox_, target)
                temp_txt = '{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n'.format(
                            img_name, score, 
                            bbox_[0], bbox_[1], bbox_[2], bbox_[3], 
                            bbox_[4], bbox_[5], bbox_[6], bbox_[7])
                if classname not in data:
                    data[classname] = []
                data[classname].append(temp_txt)
    for classname,lines in data.items():
        f_out = open(os.path.join(save_path, classname + '.txt'), 'w')
        f_out.writelines(lines)
        f_out.close()

def data_merge(result_pkl, save_path, final_path,dataset_type):
    if (dataset_type == 'DOTA'):
        classes = DOTA1_CLASSES
    elif (dataset_type == 'DOTA1_5'):
        classes = DOTA1_5_CLASSES
    elif (dataset_type == 'DOTA2'):
        classes = DOTA2_CLASSES
    elif (dataset_type == 'FAIR'):
        classes = FAIR_CLASSES_
    else:
        assert(False)
    if "gliding" in result_pkl:
        prepare_gliding(result_pkl,save_path, classes)
    elif "faster_rcnn" in result_pkl:
        prepare_fasterrcnn(result_pkl,save_path, classes)
    else:
        prepare(result_pkl,save_path, classes)
    check_dir(final_path)
    mergebypoly(save_path,final_path)

def data_merge_result(result_pkl,work_dir,epoch,name,dataset_type,images_dir=""):
    assert dataset_type in ["FAIR", "DOTA", "DOTA1_5", "DOTA2"], "need to set dataset.test.dataset_type in the config file. FAIR, DOTA, DOTA1_5 and DOTA2 are supported"
    print("Merge results...")
    save_path = os.path.join(work_dir, f"test/submit_{epoch}/before_nms")
    final_path = os.path.join(work_dir, f"test/submit_{epoch}/after_nms")
    if (os.path.exists(save_path)):
        shutil.rmtree(save_path)
    if (os.path.exists(final_path)):
        shutil.rmtree(final_path)
    if not os.path.exists("submit_zips"):
        os.makedirs("submit_zips")
    data_merge(result_pkl, save_path, final_path,dataset_type)
    if (dataset_type == 'FAIR'):
        print("converting to fair...")
        final_fair_path = os.path.join(work_dir, f"test/submit_{epoch}/final_fair/test")
        dota_to_fair(final_path, final_fair_path, images_dir)
        final_path = final_fair_path
    print("zip..")
    zip_path = os.path.join("submit_zips", name + ".zip")
    if (os.path.exists(zip_path)):
        os.remove(zip_path)
    if (dataset_type == 'FAIR'):
        if is_win():
            files = glob.glob(os.path.join(final_path,"*"))
            with zipfile.ZipFile(zip_path, 'w',zipfile.ZIP_DEFLATED) as t:
                for f in files:
                    t.write(f, os.path.join("test",os.path.split(f)[-1]))# TODO
        else:
            os.system(f"cd {os.path.join(final_path, '..')} && zip -r -q {name+'.zip'} 'test'")
            os.system(f"mv {os.path.join(final_path, '..', name+'.zip')} {zip_path}")
    else:
        if is_win():
            files = glob.glob(os.path.join(final_path,"*"))
            with zipfile.ZipFile(zip_path, 'w',zipfile.ZIP_DEFLATED) as t:
                for f in files:
                    t.write(f, os.path.split(f)[-1])
        else:
            os.system(f"zip -rj -q {zip_path} {os.path.join(final_path,'*')}")

if __name__ == "__main__":
    work_dir = "/mnt/disk/lxl/JDet/work_dirs/gliding_r101_fpn_1x_dota_bs2_tobgr_steplr_rotate_balance_ms"
    epoch = 12
    result_pkl = f"{work_dir}/test/test_{epoch}.pkl"
    save_path = f"{work_dir}/test/submit_{epoch}/before_nms"
    final_path = f"{work_dir}/test/submit_{epoch}/after_nms"
    data_merge(result_pkl, save_path, final_path, 'DOTADataset')