import tkinter as tk
import serial
import time

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 시리얼 포트 초기화 시간 대기

def send_command(command):
    ser.write(command.encode())
    print(f'Sent: {command}')

# Tkinter 설정
root = tk.Tk()
root.title("Arrow Buttons")

def on_button_press(command):
    send_command(command)

# 화면 크기 설정
root.geometry("400x300")

# 프레임 생성
frame = tk.Frame(root)
frame.pack(expand=True)

# 버튼 크기 설정
button_width = 10
button_height = 2

# 화살표 버튼 생성
button_up = tk.Button(frame, text="go", command=lambda: on_button_press('go\n'), width=button_width, height=button_height)
button_down = tk.Button(frame, text="back", command=lambda: on_button_press('back\n'), width=button_width, height=button_height)
button_left = tk.Button(frame, text="left", command=lambda: on_button_press('left\n'), width=button_width, height=button_height)
button_right = tk.Button(frame, text="right", command=lambda: on_button_press('right\n'), width=button_width, height=button_height)
button_stop = tk.Button(frame, text="stop", command=lambda: on_button_press('stop\n'), width=button_width, height=button_height)
button_slow = tk.Button(frame, text="slow", command=lambda: on_button_press('slow\n'), width=button_width, height=button_height)

# 버튼 배치
button_up.grid(row=0, column=1, pady=5)
button_left.grid(row=1, column=0, padx=5)
button_right.grid(row=1, column=2, padx=5)
button_down.grid(row=2, column=1, pady=5)
button_stop.grid(row=1, column=1)
button_slow.grid(row=3, column=1, pady=5)

# Tkinter 이벤트 루프 시작
root.mainloop()

# 종료 시 시리얼 포트 닫기
ser.close()
