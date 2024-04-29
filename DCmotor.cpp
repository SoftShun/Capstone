const int ENA = 3;  // 모터 A의 속도 제어 핀
const int IN1 = 2;  // 모터 A의 방향 제어 핀 1
const int IN2 = 4;  // 모터 A의 방향 제어 핀 2
const int ENB = 5;  // 모터 B의 속도 제어 핀
const int IN3 = 6;  // 모터 B의 방향 제어 핀 1
const int IN4 = 7;  // 모터 B의 방향 제어 핀 2
// const int ENC = 10;  // 모터 C의 속도 제어 핀
// const int IN5 = 8;  // 모터 C의 방향 제어 핀 1
// const int IN6 = 9;  // 모터 C의 방향 제어 핀 2
// const int END = 11;  // 모터 D의 속도 제어 핀
// const int IN7 = 12;  // 모터 D의 방향 제어 핀 1
// const int IN8 = 13;  // 모터 D의 방향 제어 핀 2
int currentSpeed = 0;

void setup() {
  // 모터 핀을 출력으로 설정
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  // pinMode(ENC, OUTPUT);
  // pinMode(IN5, OUTPUT);
  // pinMode(IN6, OUTPUT);
  // pinMode(END, OUTPUT);
  // pinMode(IN7, OUTPUT);
  // pinMode(IN8, OUTPUT);

  Serial.begin(9600); // 시리얼 통신 초기화
}

void loop() {
  char direction;
  
  // 방향 입력 받기
  Serial.println("Enter direction (q: forward, w: backward, e: stop, r: backstop) : ");
  while (!Serial.available()) {} // 입력이 있을 때까지 대기
  direction = Serial.read(); // 입력 받기

  // 모터 A 제어
  if (direction == 'e') {
    motorCon(ENA, IN1, IN2, 0, 3); // 정지
    motorCon(ENB, IN3, IN4, 0, 3); // 정지
  }
  else if (direction == 'q') {
    motorCon(ENA, IN1, IN2, 250, 1); // 최대 속도로 전진
    motorCon(ENB, IN3, IN4, 250, 1); // 최대 속도로 전진
  }
  else if (direction == 'w') {
    motorCon(ENA, IN1, IN2, 250, 2); // 최대 속도로 후진
    motorCon(ENB, IN3, IN4, 250, 2); // 최대 속도로 후진
  }
  else if (direction == 'r') {
    motorCon(ENA, IN1, IN2, 0, 4);
    motorCon(ENB, IN3, IN4, 0, 4);
  }
}

// state 1 : 정방향, 3 : 정방향 정지, 2 : 후방향, 4 : 후방향 정지
// 모터  제어 함수
void motorCon(int enablePin, int dirPin1, int dirPin2, int velocity, int state) {  
  if (state == 2) {
    digitalWrite(dirPin1, LOW);  // 후진 방향 설정
    digitalWrite(dirPin2, HIGH);
    for (int pwmValue = 0; pwmValue <= velocity; pwmValue++) {
      analogWrite(enablePin, pwmValue); // PWM 값 설정하여 모터 가속
      delay(50); // 30ms마다 속도 증가 
      currentSpeed = pwmValue;
    }
  }
  else if (state == 1) {
    digitalWrite(dirPin1, HIGH); // 전진 방향 설정
    digitalWrite(dirPin2, LOW);
    for (int pwmValue = 0; pwmValue <= velocity; pwmValue++) {
      analogWrite(enablePin, pwmValue); // PWM 값 설정하여 모터 가속
      delay(50); // 15ms마다 속도 증가
      currentSpeed = pwmValue;
    }
  }
  else if (state == 3) {
    digitalWrite(dirPin1, HIGH); // 전진하다 정지
    digitalWrite(dirPin2, LOW);
    for (int pwmValue = currentSpeed; pwmValue >= 0; pwmValue--) {
      analogWrite(enablePin, pwmValue); // PWM 값 설정하여 모터 가속
      delay(50); // 15ms마다 속도 증가
      currentSpeed = pwmValue;
    }
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, LOW);
  }
  else if (state == 4) {  // 후진하다 정지
    digitalWrite(dirPin1, LOW); // 정지
    digitalWrite(dirPin2, HIGH);
    for (int pwmValue = currentSpeed; pwmValue >= 0; pwmValue--) {
      analogWrite(enablePin, pwmValue); // PWM 값 설정하여 모터 가속
      delay(50); // 15ms마다 속도 증가
      currentSpeed = pwmValue;
    }
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, LOW);
  }
}
