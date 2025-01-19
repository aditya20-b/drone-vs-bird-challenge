#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
from collections import defaultdict
                
          
if __name__ == '__main__':
    OUT_PATH = 'output_json'
    PATH_TO_GT_FILES = 'annotations' 
    # CURRENT_IMAGE_NAME =  lambda img_id, video_name: f"{video_name}_{img_id}.jpg"
    def format_image_name(img_id, video_name):
        return f"extracted_frames/{video_name}_{img_id:04d}.jpg"

    CURRENT_IMAGE_NAME = format_image_name
    
    gt_dir = PATH_TO_GT_FILES #has to be adapted
    gt_list = os.listdir(gt_dir)
    
    out_dir = OUT_PATH #has to be adapted
    
    for gt in gt_list:
        if gt.endswith('.txt'):
            gt_file = os.path.join(gt_dir, gt)
            
            out_name = gt.replace('.txt','.json')
            out_file = os.path.join(out_dir, out_name)
            
            out_data = {'categories': [],
                        'images': [],
                        'annotations': []}
            
            cat = dict(id=1, name='drone')
            out_data['categories'].append(cat)
            
            width = 1920
            height = 1080
            if 'C000' in gt:
                height = 3840
                width = 1920
            elif 'two_distant' in gt:
                height = 1280
                width = 720
            elif 'custom' in gt or 'swarm' in gt or 'matrice_600' in gt or 'two_parrot' in gt:
                height = 720
                width = 576  
                
            ann_cnt = 1         
                        
            with open(gt_file, 'r') as ann:
                line = ann.readline()  
                while line:
                    params = line.split(' ')
                    img_id = int(params[0]) + 1
                    obj_cnt = int(params[1])

                    img_info = dict()
                    img_info['id'] = img_id
                    img_info['width'] = width
                    img_info['height'] = height
                    img_info['file_name'] = CURRENT_IMAGE_NAME(img_id, gt.split('.')[0]) #has to be adapted for instance for img_id = 0 image_name = 0.jpg
                    out_data['images'].append(img_info)
                
                    for idx in range(obj_cnt):
                        x_left = int(params[idx*5 + 2])
                        y_top = int(params[idx*5 + 3])
                        w = int(params[idx*5 + 4])
                        h = int(params[idx*5 + 5])
                        cls = params[idx*5 +6]

                        ann_info = dict()
                        ann_info['id'] = ann_cnt
                        ann_info['iscrowd'] = 0
                        ann_info['image_id'] = img_id
                        ann_info['bbox'] = [x_left, y_top, w, h]
                        ann_info['area'] = w*h
                        ann_info['category_id'] = 1
                        out_data['annotations'].append(ann_info)
                
                        ann_cnt += 1
                
                    line = ann.readline()
                            
                                     
            #save out json 
            with open(out_file, 'w') as outfile:
                json.dump(out_data, outfile, indent=4)




