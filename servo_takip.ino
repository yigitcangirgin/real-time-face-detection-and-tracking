#include <Servo.h>

Servo myServo;
const int servoPin = 9;  // Servo motorun bağlı olduğu pin
int servoPos = 90;  // Başlangıç pozisyonu (orta)
const int centerX = 320; // Kamera genişliğinin ortası
const int tolerance = 40; // Merkez toleransı (280-360 arası durur)
const int stepSize = 2;  // Her adımda servo motoru hareket ettirme miktarı
const int delayTime = 10; // Servo hareketleri arasındaki gecikme (ms)

void setup() {
    Serial.begin(9600);
    myServo.attach(servoPin);
    myServo.write(servoPos); // Servo başlangıçta ortada
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');  // Satır sonuna kadar oku
        int x = data.toInt();  // X koordinatını al

        if (x == -1) {
            return;  // Yüz görünmüyorsa hareket etme
        }

        // Yüz ortadaysa dur (tolerans aralığı)
        if (x > centerX - tolerance && x < centerX + tolerance) {
            // Yüz merkezdeyse servo hareket etmesin
            servoPos = 90;
        } 
        else if (x < centerX - tolerance) {  
            // Yüz sola kaydıysa, ne kadar uzaksa o kadar çok döndür
            int speed = map(centerX - x, 0, 320, 1, 5);
            servoPos -= speed;
        } 
        else if (x > centerX + tolerance) {  
            // Yüz sağa kaydıysa, ne kadar uzaksa o kadar çok döndür
            int speed = map(x - centerX, 0, 320, 1, 5);
            servoPos += speed;
        }

        // Servo pozisyonunu sınırlama (0-180 derece)
        servoPos = constrain(servoPos, 0, 180);

        // Servo motorunu küçük adımlarla hareket ettir
        int currentPos = myServo.read();
        if (currentPos < servoPos) {
            // Servo motoru sağa hareket ettir
            for (int pos = currentPos; pos < servoPos; pos += stepSize) {
                myServo.write(pos);
                delay(delayTime);  // Hareketler arasındaki gecikme
            }
        } else if (currentPos > servoPos) {
            // Servo motoru sola hareket ettir
            for (int pos = currentPos; pos > servoPos; pos -= stepSize) {
                myServo.write(pos);
                delay(delayTime);  // Hareketler arasındaki gecikme
            }
        }
    }
}
