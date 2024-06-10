# --------------------------------------------------
# from ultralytics import YOLO
# model = YOLO('./custom_yolov8n.pt')
# model.train(data="C:/Users/admin/Desktop/github/Apple Finder/data.yaml", epochs=60)
# --------------------------------------------------

# from ultralytics import YOLO
# import torch

# model = torch.load("./custom_yolov8n.pt")
# print(model)


#----------------------------------------------------
### image predict

from ultralytics import YOLO

# Load a model
model = YOLO("./best.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
# results = model(["app.jpg"])  # return a list of Results objects
results = model(["./sets/result.jpg"])

idx = 0
# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    idx = idx + 1
    result.save(filename=f"result_{idx}.jpg")  # save to disk

#-----------------------------------------------------------

# import torch
# from ultralytics import YOLO

# # ------------ 모델 경로 및 파일 수정 시간은 수정하기 --------------
# model_path = '../best.pt' 
# model_generated_time = "  24-06-03, 20:02"
# # ------------------------------------------------

# model = YOLO(model_path)

# # 모델의 가중치 확인
# model_weights = model.model.state_dict()
# torch.set_printoptions(threshold=torch.inf)
# idx = 0
# while idx < len(model_weights):
#     name = list(model_weights.keys())[idx]
#     param = model_weights[name]
#     if "model." in name:
#         output_file = f"{name}.txt" 
#         with open(output_file, "w") as f:
#             f.write("Weights Information:\n")
#             f.write("# weights ver.2\n\n")
#             f.write(f"Model Path: {model_path}\n")
#             f.write(f"Model Generated Time: {model_generated_time}\n\n")
#             f.write(f"Layer: {name} | Size: {param.size()}\n")
#             f.write(str(param) + "\n")  
#     idx += 1


# ------------------------------------------------------------
# # 레이어 정보만 가져오기
# import torch
# from ultralytics import YOLO

# # 모델 경로 및 파일 수정 시간 설정
# model_path = '../best.pt' 
# model_generated_time = "24-06-03, 20:02"

# # YOLO 모델 로드
# model = YOLO(model_path)

# # 모델의 가중치 확인
# model_weights = model.model.state_dict()

# # 레이어 정보를 저장할 파일 생성
# with open("layers.txt", "w") as f:
#     f.write("Layer Information:\n")
#     f.write(f"Model Path: {model_path}\n")
#     f.write(f"Model Generated Time: {model_generated_time}\n\n")

# # 각 레이어 정보를 파일에 기록
# with open("layers.txt", "a") as f:
#     for idx, (name, param) in enumerate(model_weights.items()):
#         f.write(f"Layer {idx}:\n")
#         f.write(f"Name: {name}\n")
#         f.write(f"Size: {param.size()}\n")





# --------------------------------------------------
# stereo cam 적용시키기(apple2_leftcam.jpg, apple2_rightcam.jpg)

# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt

# imgL = cv.imread('./sets/apple2_leftcam.jpg', cv.IMREAD_GRAYSCALE)
# imgR = cv.imread('./sets/apple2_rightcam.jpg', cv.IMREAD_GRAYSCALE)
# stereo = cv.StereoBM_create(numDisparities=16, blockSize=7)
# disparity = stereo.compute(imgL,imgR)
# plt.imshow(disparity,'gray')

# plt.savefig('result.jpg')
# plt.show()