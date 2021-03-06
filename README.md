# YOLOv5 사용법

## 1. COCO API 사용하기

[https://github.com/cocodataset/cocoapi](https://github.com/cocodataset/cocoapi)

1. 윈도우이용자의 경우 다음 링크를 참고하셔서 실행하셔야 합니다
    
    [https://jjeamin.github.io/posts/coco_api/](https://jjeamin.github.io/posts/coco_api/)
    
     * 저는 visual studio 2015를 설치하지 않았습니다만, 작동이 되지 않는다면 링크 그대로 따라하시는 것을 권장합니다
    
2. [cocodataset.org](http://cocodataset.org) 에서 Dataset → Download로 간 이후 Annotations에서 다음과 같은 항목을 받아줍니다
    
    ![coco.png](img/coco.png)
    
3. 압축을 풀게 되면 다음과 같이 이미지가 있습니다, 저희는 instance_가 있는 json파일을 제외하고 사용하지 않기 때문에 삭제하셔도 됩니다
    
    ![json.png](img/json.png)
    
4. Download_COCO(YOLO_format).py의 다음과 같은 부분을 사용하실 폴더에 맞게 수정해 주시면 됩니다
    
    ![code.png](img/code.png)
    
5. 병렬 처리를 활용해 진행하였기 때문에 마지막에 있는 parmap.map에서 pm_processes를 본인의 컴퓨터에 맞게 수정하셔서 사용하셔야 합니다
    
    단일로 할 경우 오래걸린다는 단점이 있습니다
    

## 2. 압축파일 다운로드 이후 사용하기(권장)

[https://www.dropbox.com/sh/ptgh2hix1pfgywz/AABxzIT8ZcfvxlYKoCJXm0Qga?dl=0](https://www.dropbox.com/sh/ptgh2hix1pfgywz/AABxzIT8ZcfvxlYKoCJXm0Qga?dl=0)

1. 위의 Dropbox링크에 가시면 다음과 같이 구성되어 있습니다.
    
    ![dropbox.png](img/dropbox.png)
    
2. 여기서 압축파일들을 다운로드 받아서 압축을 해제하면 됩니다(이 경우 z01 ~ z04파일을 다 받아야 압축이 정상적으로 작동합니다)

## YOLOv5 학습 시작

1. repository를 clone합니다
2. 앞에서 다운로드 받은 파일을 dataset폴더로 이동시킵니다
3. 1_imagesplit.py를 열고 5, 7, 10, 13 line에 기재된 Path를 자신의 경우에 맞게 수정합니다. (Clone한 pet_yolo 폴더를 working directory로 설정하면 수정하지 않아도 됩니다)
   이후 1_imagesplit.py를 실행합니다. (해당 파일 내부에 필요한 패키지를 설치하는 코드가 첨부되어있습니다. 종속성 문제를 해결하기위해 반드시 해당 코드가 실행되어야 합니다. pip을 최신버전으로 수행하는것을 권장합니다.)
4. 3번 과정을 수행하면 dataset폴더에 train.txt파일과 val.txt파일이 생성됩니다. dataset폴더 안에 위치한 data.yaml파일을 열어 1, 2line의 경로를 각각 train.txt, val.txt의 경로로 수정합니다
5. 터미널, cmd, powershell에서 아래와 같은 코드를 실행하면 학습이 시작됩니다
    
    ```bash
    4. !python ./pet_yolo/yolov5/train.py --img 640 --batch 32 --epochs 50 --data ./pet_yolo/dataset/data.yaml --cfg ./pet_yolo/yolov5/models/yolov5s.yaml --weights ./pet_yolo/yolov5/yolov5s.pt --name yolov5_sample
    ```
    
## Ptl 추출 및 apk 생성하기
1. 터미널, cmd, powershell에서 아래와 같은 코드를 실행합니다.
    ```bash
     !python export.py --weights runs/train/exp/weights/best.pt --include torchscript
    ```
    이때, --weights는 Yolov5 학습결과 생성된 자신의 best.pt 경로로 수정합니다.
2. 1을 수행하면, --weights의 경로에 ptl파일이 생성됩니다.
3. 생성된 ptl파일을 ./PetCCTV/app/src/main/assets/ 로 이동합니다.
4. Android Studio를 설치한 뒤, PetCCTV를 Project의 경로로 지정하고 Build하면 자신이 커스텀한 모델을 사용한 apk를 생성할 수 있습니다.
![image](https://user-images.githubusercontent.com/84885408/178965559-2663b066-c4cb-4d94-9c04-fa3a39440918.png)
5. Live 버튼을 클릭하여 Realtime object detection기능을 사용할 수 있습니다..
