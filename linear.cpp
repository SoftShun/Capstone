const int ENA = 5;
const int motorPin1 = 2;
const int motorPin2 = 3;
int pwmValue = 0;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String direction = Serial.readString();
    if (direction == "open") {
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      pwm(255, 9400);
      pwm(0, 100);
    }
    else if (direction == "close") {
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      pwm(40, 4000);
      pwm(150, 3000);
      pwm(0, 100);
    }
  }
}

void pwm(int pwmValue, int delay_time) {
  analogWrite(ENA, pwmValue);
  delay(delay_time);
}