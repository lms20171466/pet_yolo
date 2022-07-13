from pycocotools.coco import COCO
import os
import numpy as np
import skimage.io as io
from PIL import Image
import random
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
import threading
import parmap

def save_img_and_bbox(myIds, coco) -> None:
    img_number = myIds

    # Save Image
    img = coco.loadImgs(img_number)[0]
    I = io.imread(img['coco_url'])
    Im = Image.fromarray(I)
    Im.save('images/{}.jpg.'.format(img_number), "JPEG")
        
    # Save Bounding Box
    annIds = coco.getAnnIds(imgIds = img['id'])
    anns = coco.loadAnns(annIds)
        
    dw = 1./img['width']
    dh = 1./img['height']   
        
    with open('labels/{}.txt'.format(img_number), 'w') as f:
            
        for object_name in anns:
            if object_name['category_id'] == 1 or object_name['category_id'] == 17 or object_name['category_id'] == 18:
                
                # Convert coco bbox format to yolo bbox format
                x = (object_name['bbox'][0] + 0.5 * object_name['bbox'][2]) * dw
                y = (object_name['bbox'][1] + 0.5 * object_name['bbox'][3]) * dh
                w = object_name['bbox'][2] * dw
                h = object_name['bbox'][3] * dh
                
                if object_name['category_id'] == 17:
                    object_label = 1 # cat
                elif object_name['category_id'] == 18:
                    object_label = 2 # dog
                else:
                    object_label = 0

                bbox = "{} {} {} {} {}\n".format(object_label,x, y, w, h)
                
                f.writelines(bbox)
    f.close()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory." + directory)

if __name__ == '__main__':
    dataDir = 'C:/Users/user/Documents/GitHub/pet_yolo'

    # 주석 풀면서 사용(하나씩)
    # dataType = 'train2017'
    # dataType = 'val2017'
    # dataType = 'train2014'
    dataType = 'val2014'

    annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
    coco = COCO(annFile)

    createFolder("labels")
    createFolder("images")

    cats = coco.loadCats(coco.getCatIds())
    nms = [cat['name'] for cat in cats]

    nms = set([cat['supercategory'] for cat in cats])

    personIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['person'])) # 1
    catIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['cat'])) # 17
    dogIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['dog'])) # 18

    person_catIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['person', 'cat']))
    person_dogIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['person', 'dog']))
    cat_dogIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['cat', 'dog']))

    person_cat_dogIds = coco.getImgIds(catIds = coco.getCatIds(catNms = ['cat', 'dog', 'cat']))

    print("====================================================")
    print("Image include person :", len(personIds))
    print("Image include cat :", len(catIds))
    print("Image include dog :", len(dogIds))
    print("====================================================")

    print("====================================================")
    print("Image include person and cat :", len(person_catIds))
    print("Image include person and dog :", len(person_dogIds))
    print("Image include dog and  cat:", len(cat_dogIds))

    print("Image include person, cat and dog :", len(person_cat_dogIds))

    print("====================================================")

    print("====================================================")


    uni_personIds = list(set(personIds) - set(catIds) - set(dogIds))
    uni_catIds = list(set(catIds) - set(personIds) - set(dogIds))
    uni_dogIds = list(set(dogIds) - set(catIds) - set(personIds))

    print("Number of using person images(", len(uni_personIds), ") :", end = "")
    number_of_person = int(input())

    random.seed(100)
    uni_personIds = random.sample(uni_personIds, number_of_person)

    print("Number of using person images(", len(uni_catIds), ") :", end = "")
    number_of_cat = int(input())
    
    random.seed(100)
    uni_catIds = random.sample(uni_catIds, number_of_cat)

    print("Number of using person images(", len(uni_dogIds), ") :", end = "")
    number_of_dog = int(input())
    
    random.seed(100)
    uni_dogIds = random.sample(uni_dogIds, number_of_dog)
    print("====================================================")

    myIds = list(set(uni_personIds + uni_dogIds + uni_catIds + person_catIds + person_dogIds + cat_dogIds))
    print("Final image number :", len(myIds))

    parmap.map(save_img_and_bbox, myIds, coco, pm_pbar = True, pm_processes = 15) # 본인의 코어수에 맞게 수정해서 사용해야 합니다