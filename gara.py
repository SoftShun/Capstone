import serial, time
import tkinter as tk
from tkinter import messagebox, ttk

ser1 = serial.Serial('/dev/ttyACM0', 9600)
ser2 = serial.Serial('/dev/ttyACM1', 9600)
time.sleep(2)

# Room numbers and their respective forward times in seconds
room_times = {
    '401': 5,
    '402': 10,
    '403': 15,
    '404': 20,
    '405': 25,
    '406': 30
}
passwords = {
    '401': '1111',
    '402': '2222',
    '403': '3333',
    '404': '4444',
    '405': '5555',
    '406': '6666'
}

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def append_number(num):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(num))

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])
    
def show_start_screen():
    for widget in window.winfo_children():
        widget.destroy()
    start_button = tk.Button(window, text="Start", command=start_button_pressed, height=4, width=30, relief="flat", font=("Calibri", 25), bg="#FFFFFF")
    start_button.pack(pady=50)

def start_button_pressed() :
    send_commandz("open")
    show_room_entry_screen()

def show_room_entry_screen():
    for widget in window.winfo_children():
        widget.destroy()
    global entry
    label = tk.Label(window, text="Please enter your destination", bg="#FFFFFF", font=("Helvetica", 15))
    label.pack(pady=(15, 0))
    entry = tk.Entry(window, width=30, font=("Helvetica", 15), justify="center")
    entry.pack(pady=(0, 15))
    show_numpad()
    
def send_communication():
    global room_number
    room_number = entry.get()
    if room_number in passwords:
        print(f"Room {room_number} communication sent.")  # Simulated communication
        messagebox.showinfo("Complete", f"Moving to room {room_number}.")
        ready_close()
    else:
        messagebox.showerror("Error", "Please enter a number between 401 and 406.")
        entry.delete(0, tk.END)
    
def ready_close() :
    send_commandz("close")
    time.sleep(7)
    start_moving()
    
# Function to start moving
def start_moving():
    global moving
    moving = True
    for widget in window.winfo_children():
        widget.destroy()
    label = tk.Label(window, text="Moving...", bg="#FFFFFF", font=("Helvetica", 50))
    label.pack(pady=(120, 0))
    
    duration = room_times[room_number]
    elapsed = 0
    send_command("go")
    
    while elapsed < duration:
        if moving:
            time.sleep(1)
            elapsed += 1
        else:
            send_command("stop")
            while not moving:
                time.sleep(0.1)
            send_command("go")
    
    send_command("stop")
    show_receive_button()    
    
def show_receive_button():
    for widget in window.winfo_children():
        widget.destroy()
    global entry
    label = tk.Label(window, text=f"Password for room {room_number}", bg="#FFFFFF", font=("Helvetica", 15))
    label.pack(pady=(15, 0))
    entry = tk.Entry(window, width=30, font=("Helvetica", 15), justify="center")
    entry.pack(pady=(0, 15))
    show_numpad(mode='check_password')
    
def check_password():
    password = entry.get()
    if password == passwords[room_number]:
        password_complete()
    else:
        messagebox.showerror("Error", "Incorrect password.")
        entry.delete(0, tk.END)    
    
def password_complete() :
    send_commandz("open")
    show_complete_button()

def show_complete_button():
    for widget in window.winfo_children():
        widget.destroy()
    complete_button = tk.Button(window, text="Delivery Complete", command=end_close, height=4, width=30, relief="flat", font=("Calibri", 25), bg="#FFFFFF")
    complete_button.pack(pady=50)

def end_close() :
    send_commandz("close")
    time.sleep(8)
    send_command("turn")  # 'turn' 명령어 전송
    
    while True:  # 회전 완료 신호 대기
        response = ser1.readline().decode().strip()
        if response == "turn_complete":
            break
                
    duration = room_times[room_number]
    elapsed = 0
    send_command("go")
    
    while elapsed < duration:
        if moving:
            time.sleep(1)
            elapsed += 1
        else:
            send_command("stop\n")
            while not moving:
                time.sleep(0.1)
            send_command("go")        


    send_command("stop\n")
    send_command("turn")  # 'turn' 명령어 전송
    while True:  # 회전 완료 신호 대기
        response = ser1.readline().decode().strip()
        if response == "turn_complete":
            break
    end_process()

def end_process():
    show_start_screen()  # 맨 처음 화면으로 돌아가기

def show_numpad(mode='send_communication'):
    numpad_frame = tk.Frame(window, bg="#FFFFFF")
    numpad_frame.pack(pady=10)

    buttons = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('←', 3, 0), ('0', 3, 1), ('OK', 3, 2)
    ]

    for text, row, col in buttons:
        if text == "←":
            button = tk.Button(numpad_frame, text=text, command=backspace, height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
        elif text == "OK":
            if mode == 'send_communication':
                button = tk.Button(numpad_frame, text=text, command=send_communication, height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
            elif mode == 'check_password':
                button = tk.Button(numpad_frame, text=text, command=check_password, height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
        else:
            button = tk.Button(numpad_frame, text=text, command=lambda num=text: append_number(num), height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
        button.grid(row=row, column=col, padx=5, pady=5)

def send_command(command):
    ser1.write(command.encode())

def send_commandz(command) :
    ser2.write(command.encode())
    
window = tk.Tk()
window.title("Autonomous Delivery")
window.configure(background="#FFFFFF")

window_width = 500
window_height = 350
window.geometry(f"{window_width}x{window_height}")

center_window(window, window_width, window_height)

show_start_screen()

window.mainloop()    