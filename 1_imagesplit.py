from sklearn.model_selection import train_test_split
from glob import glob

# repository clone 후 yolov5 폴더 안에 위치한 requirements.txt 설치
!pip install -r "./yolov5/requirements.txt"

img_list = glob('./dataset/export/images/*.jpg')
train_img_list, val_img_list = train_test_split(img_list, test_size=0.2, random_state=2000)

with open('./dataset/train.txt', 'w') as f:
  f.write('\n'.join(train_img_list) + '\n')

with open('./dataset/val.txt', 'w') as f:
  f.write('\n'.join(val_img_list) + '\n')