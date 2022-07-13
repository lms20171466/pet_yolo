# pet_yolo
1. repository를 clone 합니다.

2. 드롭박스 링크에 있는 export.zip을 다운받은 뒤, 압축을 해제하고, export 폴더를 클론받은 dataset 폴더로 이동합니다.

3. 1_imagesplit.py를 열고 5, 7, 10, 13 line에 기재된 Path를 자신의 경우에 맞게 수정합니다. (clone한 pet_yolo 폴더를 working directory로 설정하면 수정하지 않아도 됩니다.)
   이후, 1_imagesplit.py를 실행합니다.
   
4. 3번을 수행하면, dataset폴더에 train.txt파일과 val.txt.파일이 생성됩니다. dataset폴더안에 위치한 data.yaml 파일을 열어, 1, 2 line의 경로를 각각 train.txt, val.txt의 경로로 수정합니다.

5. 터미널 / cmd / powershell 에서 

!python ./pet_yolo/yolov5/train.py --img 640 --batch 32 --epochs 50 --data ./pet_yolo/dataset/data.yaml --cfg ./pet_yolo/yolov5/models/yolov5s.yaml --weights ./pet_yolo/yolov5/yolov5s.pt --name yolov5_sample

위 코드를 실행하여, yolo 모델을 학습시킬 수 있습니다.
