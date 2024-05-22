import tkinter as tk
import serial
import time

# 시리얼 포트 설정
ser2 = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

# 버튼 클릭 시 호출되는 함수
def send_command(command):
    ser2.write(command.encode())

# Tkinter 창 설정
root = tk.Tk()
root.title("Motor Control")

# 'open' 버튼
open_button = tk.Button(root, text="Open", command=lambda: send_command("open"))
open_button.pack(pady=10)

# 'close' 버튼
close_button = tk.Button(root, text="Close", command=lambda: send_command("close"))
close_button.pack(pady=10)

# 'allopen' 버튼
allopen_button = tk.Button(root, text="All Open", command=lambda: send_command("allopen"))
allopen_button.pack(pady=10)

# 'allclose' 버튼
allclose_button = tk.Button(root, text="All Close", command=lambda: send_command("allclose"))
allclose_button.pack(pady=10)

# 'minopen' 버튼
allopen_button = tk.Button(root, text="Min Open", command=lambda: send_command("minopen"))
allopen_button.pack(pady=10)

# 'minclose' 버튼
allclose_button = tk.Button(root, text="Min Close", command=lambda: send_command("minclose"))
allclose_button.pack(pady=10)

# Tkinter 이벤트 루프 시작
root.mainloop()

# 프로그램 종료 시 시리얼 포트 닫기
ser2.close()
