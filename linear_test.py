import tkinter as tk
import serial

# 시리얼 포트 설정
# ser2 = serial.Serial('/dev/ttyACM0', 9600)

# 버튼 클릭 시 호출되는 함수
def send_command(command):
    # ser2.write(command.encode())
    print()
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

# Tkinter 이벤트 루프 시작
root.mainloop()

# 프로그램 종료 시 시리얼 포트 닫기
ser2.close()
