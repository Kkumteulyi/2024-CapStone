# --------------------------------------------------
import torch
from ultralytics import YOLO

def main():
    # CUDA가 사용 가능한지 확인
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')

    # YOLO 모델 로드 및 GPU로 전송
    model = YOLO('yolov8n.pt')
    model.to(device)

    # 모델 훈련
    model.train(data="C:/Users/admin/Desktop/Apple_Finder_v2/data.yaml", epochs=60, device=device)

if __name__ == "__main__":
    main()


# --------------------------------------------------

# from ultralytics import YOLO
# import torch

# model = torch.load("./custom_yolov8n.pt")
# print(model)


#----------------------------------------------------
### image predict

# from ultralytics import YOLO

# # Load a model
# model = YOLO("./best.pt")  # pretrained YOLOv8n model

# # Run batched inference on a list of images
# # results = model(["app.jpg"])  # return a list of Results objects
# results = model(["./sets/result.jpg"])

# idx = 0
# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     idx = idx + 1
#     result.save(filename=f"result_{idx}.jpg")  # save to disk

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


#-----------------------------------------------------------
# # realtime stereo vision
# import cv2
# import numpy as np

# # 스테레오 비전 설정
# # left_camera_index와 right_camera_index는 카메라 인덱스를 나타냅니다.
# left_camera_index = 0
# right_camera_index = 1

# left_camera = cv2.VideoCapture(left_camera_index)
# right_camera = cv2.VideoCapture(right_camera_index)

# # 스테레오 매칭 알고리즘 설정 (StereoBM 또는 StereoSGBM)
# stereo = cv2.StereoBM_create(numDisparities=32, blockSize=9)

# while True:
#     ret_left, frame_left = left_camera.read()
#     ret_right, frame_right = right_camera.read()

#     if not ret_left or not ret_right:
#         break

#     # 그레이스케일 변환
#     gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
#     gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

#     # 스테레오 매칭을 통해 깊이 지도 생성
#     disparity = stereo.compute(gray_left, gray_right)

#     # 시각화를 위해 깊이 지도를 정규화
#     disp = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
#     disp = np.uint8(disp)

#     # 결과 출력
#     cv2.imshow('Left Camera', frame_left)
#     cv2.imshow('Right Camera', frame_right)
#     cv2.imshow('Disparity', disp)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# left_camera.release()
# right_camera.release()
# cv2.destroyAllWindows()
