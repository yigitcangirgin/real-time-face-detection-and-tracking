import cv2

cap = cv2.VideoCapture(1)  # Harici kamera genellikle 1 veya 2 olur

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamıyor!")
        break
    
    cv2.imshow("Harici Kamera", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basınca çık
        break

cap.release()
cv2.destroyAllWindows()
