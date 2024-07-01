import cv2
import torch
import torchvision
from torchvision import transforms
from PIL import Image
import serial
import binascii
import threading
import math

# 종료 플래그 정의
stop_thread = threading.Event()

# 카메라 각도를 상수로 정의
CAM_ANGLE = 19
distance = None  # 전역 변수로 distance 선언
COM_PORT = 'COM3'

#############################
## V I D E O _ S T R E A M ##
#############################

# 객체 탐지 모델 로드 (여기서는 Faster R-CNN 예제 사용)
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 이미지 변환 정의
transform = transforms.Compose([
    transforms.ToTensor()
])

def detect_objects(frame):
    # OpenCV 이미지에서 PIL 이미지로 변환
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = transform(img)
    img = img.unsqueeze(0)  # 배치 차원 추가
    
    with torch.no_grad():
        predictions = model(img)
    
    return predictions[0]

def draw_boxes(frame, predictions, distance):
    boxes = predictions['boxes'].cpu().numpy()
    scores = predictions['scores'].cpu().numpy()

    for box, score in zip(boxes, scores):
        if score > 0.5:  # 신뢰도가 50% 이상인 경우만 표시
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, f'{score:.2f}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
            # 객체가 차지하는 비율 계산
            k = abs(x2 - x1)
            n = k / 640  # 객체의 가로 길이를 카메라 화면의 가로 길이로 나눔

            # 객체의 거리 계산
            if distance is not None:
                l = 2 * distance * math.tan(math.radians(CAM_ANGLE)) * n
                cv2.putText(frame, f'Size: {l:.2f} mm', (int(x1), int(y2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def Stream_Video():
    video = cv2.VideoCapture(0)
    
    if not video.isOpened():
        print("Can't open video")
        exit()

    # 비디오 프레임의 해상도를 640x480으로 설정
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while not stop_thread.is_set():
        ret, frame = video.read()
    
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # 객체 탐지
        predictions = detect_objects(frame)
                
        # 탐지 결과 박스 그리기 및 거리 계산
        draw_boxes(frame, predictions, distance)
        
        # 프레임 표시
        cv2.imshow('Video Frame', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_thread.set()
            break

    # 캡처 객체 해제 및 창 닫기
    video.release()
    cv2.destroyAllWindows()

###################################
##### L I D A R _ S E N S O R #####
###################################

def read_lidar():
    global distance  # 전역 변수로 distance 사용 선언
    
    idx = 0
    local_distance = 0  # 지역 변수로 distance 선언
    
    try:
        # Change Serial('COM Port to your environment')
        with serial.Serial(COM_PORT, 115200) as ser:
            count = 0
            while not stop_thread.is_set():  # 플래그가 설정되면 루프 종료
                if ser.in_waiting > 0:  # 수신 대기 데이터가 있을 경우에만 처리
                    s = ser.read(ser.in_waiting)  # 수신 대기 중인 모든 데이터 한 번에 읽기
                    for byte in s:
                        hex_string = format(byte, '02x')  # 바이트를 16진수 문자열로 변환
        
                        if idx == 4 or idx == 5:
                            # Append incoming hex values and convert to decimal
                            if idx == 4:
                                local_distance = int(hex_string, 16) << 8  # Shift left by 8 bits for the high byte
                            elif idx == 5:
                                local_distance += int(hex_string, 16)  # Add the low byte value
                                count += 1
                                if count % 100 == 0:
                                    print(f"Distance: {local_distance} mm, Count: {count}")  # Print the distance
                                    print("\n")
                                    distance = local_distance  # 전역 변수 distance 업데이트
        
                        if idx == 6 and hex_string != '00':
                            print("WARNING: Out of range!")
                        # Index increment
                        idx += 1
                        
                        if hex_string == 'fa':
                            # Reset packet on end signal
                            idx = 0
                            local_distance = 0
                                
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        exit(1)

#############
## M A I N ##
#############

def main():
    # 비디오 스트림 스레드 시작
    video_thread = threading.Thread(target=Stream_Video)
    video_thread.start()

    # Lidar 센서 스레드 시작
    lidar_thread = threading.Thread(target=read_lidar)
    lidar_thread.start()

    try:
        # 두 스레드가 종료될 때까지 대기
        video_thread.join()
        lidar_thread.join()
    except KeyboardInterrupt:
        # 종료 플래그 설정
        stop_thread.set()
        video_thread.join()
        lidar_thread.join()
        print("Threads have been stopped.")

if __name__ == "__main__":
    main()
