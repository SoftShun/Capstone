void setup() {
  Serial.begin(9600); // 시리얼 통신 시작, 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    String received = Serial.readString(); // 데이터 읽기
    Serial.print("Received: "); // "Received: " 문자열 출력
    Serial.println(received); // 수신한 데이터 출력
  }
}
