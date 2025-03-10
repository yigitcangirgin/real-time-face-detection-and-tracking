import cv2
import serial
import time

# Arduino seri portunu aç (Kendi COM portunu kontrol et)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Arduino bağlantısı için bekleme süresi

def faceBox(faceNet, frame):
    frameHeight, frameWidth = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs = []

    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            bboxs.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame, bboxs

# Model dosyalarının yolları
faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

# Modeli yükle
faceNet = cv2.dnn.readNet(faceModel, faceProto)

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame, bboxs = faceBox(faceNet, frame)

    if bboxs:
        for bbox in bboxs:
            x_center = (bbox[0] + bbox[2]) // 2
            y_center = (bbox[1] + bbox[3]) // 2

            # Yüzün tam ortasına kırmızı nokta koy
            cv2.circle(frame, (x_center, y_center), 5, (0, 0, 255), -1)

            # Seri porta X koordinatını gönder
            ser.write(f"{x_center}\n".encode())

    else:
        # Yüz bulunamazsa, -1 gönder (Servo kendini sıfırlar)
        ser.write("-1\n".encode())

    cv2.imshow("Gerçek Zamanlı Yüz Takibi", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
ser.close()
