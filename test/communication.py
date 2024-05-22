import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600) # 시리얼 포트 설정
time.sleep(2) # 아두이노 초기화를 위한 잠시 대기

send_time = time.time() # 데이터를 보내는 시간 기록 (초 단위)
data = "Hello, Arduino!"
ser.write(data.encode()) # 데이터 전송

while True:
    if ser.inWaiting() > 0:
        response = ser.readline().decode().strip() # 아두이노로 부터 응답 수신
        if response == "Received":
            receive_time = time.time() # 응답을 받은 시간 기록
            break

# 전송 및 응답 시간 계산 후 출력
duration = receive_time - send_time
print(f"Round-trip time: {round(duration, 2)} seconds")
