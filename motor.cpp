const int ENA = 3;  // 모터 A의 속도 제어 핀
const int IN1 = 2;  // 모터 A의 방향 제어 핀 1
const int IN2 = 4;  // 모터 A의 방향 제어 핀 2
const int ENB = 5;  // 모터 B의 속도 제어 핀
const int IN3 = 6;  // 모터 B의 방향 제어 핀 1
const int IN4 = 7;  // 모터 B의 방향 제어 핀 2
const int ENC = 10; // 모터 C의 속도 제어 핀
const int IN5 = 8; // 모터 C의 방향 제어 핀 1
const int IN6 = 9; // 모터 C의 방향 제어 핀 2
const int END = 11; // 모터 D의 속도 제어 핀
const int IN7 = 12; // 모터 D의 방향 제어 핀 1
const int IN8 = 13; // 모터 D의 방향 제어 핀 2
int Speed = 0;
int carState = 0; // 0 : 정지, 1 : 전진, 2 : 후진 
int pwmValue = 0;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENC, OUTPUT);
  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(END, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);
  Serial.begin(9600); // 시리얼 통신 사용 준비, 9600bps=1초에 9600비트 전송
} 

void loop() {
  if (Serial.available() > 0) {
    String direction = Serial.readStringUntil('\n'); // 데이터 읽음
    direction.trim(); // 문자열 앞뒤 공백 제거
    Serial.print("Received : "); // "Received : " 문자열 출력
    Serial.println(direction);  // 수신한 데이터 출력
    
    // 모터 제어
    if (direction == "go") { // 가속 (전진)
      motorSelect(1);
      carState = 1;  // 전진 상태
      pwm(150);
    }
    
    else if (direction == "back") {  // 가속 (후진)
      motorSelect(2);
      carState = 2;  // 후진 상태
      pwm(150);
    }

    else if (direction == "slow") {  // 감속 
      motorSelect(3);
      for (int pwmValue = Speed; pwmValue >= 0; pwmValue--) {
        analogWrite(ENA, pwmValue); // PWM 값 설정하여 모터 가속
        analogWrite(ENB, pwmValue); // PWM 값 설정하여 모터 가속
        analogWrite(ENC, pwmValue); // PWM 값 설정하여 모터 가속
        analogWrite(END, pwmValue); // PWM 값 설정하여 모터 가속
        delay(10); // 100ms마다 속도 감소 
        Speed = pwmValue;
        if (pwmValue == 0) {
          carState = 0;
        }
      }
    }
    else if (direction == "stop") {  // 급정지 
      motorSelect(4);
      carState = 0; // 정지 상태
    }
    else if (direction == "right") {  // 오른쪽 
      motorSelect(1);
      pwmValue = 120;
      analogWrite(ENA, pwmValue + 36);
      analogWrite(ENB, pwmValue);
      analogWrite(ENC, pwmValue + 36);
      analogWrite(END, pwmValue);
      Speed = pwmValue;
    }
    else if (direction == "left") {  // 왼쪽
      motorSelect(1);
      pwmValue = 120;
      analogWrite(ENA, pwmValue);
      analogWrite(ENB, pwmValue + 85);
      analogWrite(ENC, pwmValue);
      analogWrite(END, pwmValue + 75);
    }
    else if (direction == "turn") { // 회전
      motorSelect(7);
      pwm(200);
      delay(700);
      Serial.println("turn_complete");
    }
    else if (direction == "leftturn") {
      motorSelect(8);
      pwm(200);
    }
  }
} 

// 모터 방향 선택
void motorSelect(int num) {
  if (num == 1) { // 전진 
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    digitalWrite(IN5, HIGH);
    digitalWrite(IN6, LOW);
    digitalWrite(IN7, HIGH);
    digitalWrite(IN8, LOW);
  }
  else if (num == 2) {  // 후진 
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    digitalWrite(IN5, LOW);
    digitalWrite(IN6, HIGH);
    digitalWrite(IN7, LOW);
    digitalWrite(IN8, HIGH);
  }
  else if (num == 3) {  // 감속
    if (carState == 1) {  // 전진 상태일 때 
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      digitalWrite(IN5, HIGH);
      digitalWrite(IN6, LOW);
      digitalWrite(IN7, HIGH);
      digitalWrite(IN8, LOW);
    }
    else if (carState == 2) {  // 후진 상태일 때
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      digitalWrite(IN5, LOW);
      digitalWrite(IN6, HIGH);
      digitalWrite(IN7, LOW);
      digitalWrite(IN8, HIGH);
    }
  }
  else if (num == 4) { // 급정지
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    digitalWrite(IN5, LOW);
    digitalWrite(IN6, LOW);
    digitalWrite(IN7, LOW);
    digitalWrite(IN8, LOW);
  }
  else if (num == 5) { // 오른쪽
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    digitalWrite(IN5, LOW);
    digitalWrite(IN6, HIGH);
    digitalWrite(IN7, HIGH);
    digitalWrite(IN8, LOW);
  }
  else if (num == 6) { // 왼쪽
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    digitalWrite(IN5, HIGH);
    digitalWrite(IN6, LOW);
    digitalWrite(IN7, LOW);
    digitalWrite(IN8, HIGH);
  }
  else if (num == 7) {  // 회전
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    digitalWrite(IN5, HIGH);
    digitalWrite(IN6, LOW);
    digitalWrite(IN7, LOW);
    digitalWrite(IN8, HIGH);
  }
    else if (num == 8) {  // 회전
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    digitalWrite(IN5, LOW);
    digitalWrite(IN6, HIGH);
    digitalWrite(IN7, HIGH);
    digitalWrite(IN8, LOW);
  }
}

void pwm(int pwm_Value) {
    analogWrite(ENA, pwm_Value);
    analogWrite(ENB, pwm_Value + 30);
    analogWrite(ENC, pwm_Value);
    analogWrite(END, pwm_Value + 15);
    Speed = pwm_Value;
}