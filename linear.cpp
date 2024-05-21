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
      pwmValue = 255;
      analogWrite(ENA, pwmValue);
      delay(4000);
    }
    else if (direction == "close") {
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      pwmValue = 150;
      analogWrite(ENA, pwmValue);
      delay(4000);
    }
  }
}