import serial, time
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import cv2 
import numpy as np

ser1 = serial.Serial('/dev/ttyACM0', 9600)
ser2 = serial.Serial('/dev/ttyACM1', 9600)
time.sleep(2)

# Room numbers and their respective forward times in seconds
room_times = {
    '401': 10,
    '402': 20,
    '403': 30,
    '404': 40,
    '405': 50,
    '406': 60
}
passwords = {
    '401': '1111',
    '402': '2222',
    '403': '3333',
    '404': '4444',
    '405': '5555',
    '406': '6666'
}

# Load YOLO model
try:
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
except Exception as e:
    print(f"YOLO Error : {e}")
    exit()
    
moving = False
room_number = None
entry = None
window = None
distance_threshold = 11000

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
    time.sleep(7)
    global moving
    moving = False
    send_command("turn")  # 'turn' 명령어 전송
    
    while True:  # 회전 완료 신호 대기
        response = ser1.readline().decode().strip()
        if response == "turn_complete":
            break
    
    moving = True
    duration = room_times[room_number]  # 이전 위치로의 주행 시간
    elapsed = 0
    send_command("go")  # 다시 주행 시작
    
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

# Function to detect obstacles using YOLO
def detect_obstacle(cap, distance_threshold):
    ret, frame = cap.read()
    if not ret:
        return False
    
    height, width, channels = frame.shape

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Pass the blob through the network and get predictions
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialize variables for person detection
    conf_threshold = 0.5  # Confidence threshold for detection
    obstacle_detected = False  # Variable to track obstacle detection

    # Loop over each detection
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold and classes[class_id] == "person":
                # Bounding box 좌표 추출
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # 거리 추정 (예시: bounding box 크기 기반)
                area = w * h
                color = (0, 255, 0)  # Green for far
                if area > distance_threshold:  # 사람도 포함하여 임계값보다 크면 장애물로 인식
                    obstacle_detected = True
                    color = (0, 0, 255)  # Red for close

                # Draw bounding box and label
                cv2.rectangle(frame, (center_x - w // 2, center_y - h // 2), (center_x + w // 2, center_y + h // 2), color, 2)

    # Show the frame in a separate window
    cv2.imshow("Camera Feed", frame)
    cv2.waitKey(1)

    return obstacle_detected

# Function to monitor obstacles
def monitor_obstacles():
    global moving
    cap = cv2.VideoCapture(0)  # Open the default camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    try:
        while True:
            if detect_obstacle(cap, distance_threshold):
                moving = False
            else:
                moving = True
                
            cv2.resizeWindow("Camera", 800, 600)
            time.sleep(0.6)
    finally:
        cap.release()

def main() :
    # Start obstacle monitoring in a separate thread
    obstacle_thread = threading.Thread(target=monitor_obstacles)
    obstacle_thread.daemon = True
    obstacle_thread.start()
    
    global window, distance_threshold
    
    distance_threshold = 12000  # 임계값 설정 (적절한 값으로 조정)
    window = tk.Tk()
    window.title("Autonomous Delivery")
    window.configure(background="#FFFFFF")

    window_width = 500
    window_height = 350
    window.geometry(f"{window_width}x{window_height}")

    center_window(window, window_width, window_height)

    show_start_screen()

    window.mainloop()

if __name__ == "__main__" :
    main()