import tkinter as tk
from tkinter import messagebox

passwords = {
    '401': '1111',
    '402': '2222',
    '403': '3333',
    '404': '4444',
    '405': '5555',
    '406': '6666'
}

def append_number(num):
    current = str(entry.get())
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(num))

def backspace():
    current = str(entry.get())
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def send_communication():
    global room_number
    room_number = entry.get()
    if room_number in passwords.keys():
        print(f"Room {room_number} communication sent.")  # Simulated communication
        messagebox.showinfo("Complete", f"Moving to room {room_number}.")
        show_receive_button()
    else:
        messagebox.showerror("Error", "Please enter a number between 401 and 406.")
        entry.delete(0, tk.END)

def show_receive_button():
    for widget in window.winfo_children():
        widget.destroy()
    global entry
    entry = tk.Entry(window, width=40, font=("Georgia", 15)) 
    entry.pack(pady=15)
    show_numpad()
    submit_button = tk.Button(window, text="Enter Password", command=check_password, height=2, width=20)
    submit_button.pack(pady=10)

def check_password():
    password = entry.get()
    if password == passwords[room_number]:  # Check the password based on the room number
        messagebox.showinfo("Receive Complete", "Please take the package.")
        show_complete_button()
    else:
        messagebox.showerror("Error", "Incorrect password.")
        entry.delete(0, tk.END)

def show_complete_button():
    for widget in window.winfo_children():
        widget.destroy()
    complete_button = tk.Button(window, text="Delivery Complete", command=end_process, height=4, width=30, font=("Calibri", 25))
    complete_button.pack(pady=50)

def end_process():
    messagebox.showinfo("Complete", "Delivery is complete.")
    window.quit()

def show_numpad():
    # Create the frame for the numpad.
    numpad_frame = tk.Frame(window, bg="#FFFFFF")
    numpad_frame.pack(pady=10)

    # Create and position the numpad buttons including backspace and confirm.
    buttons = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('←', 3, 0), ('0', 3, 1), ('OK', 3, 2)
    ]
    for text, row, col in buttons:
        if text == "←":
            button = tk.Button(numpad_frame, text=text, command=backspace, height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
            #button = tk.Button(numpad_frame, text=text, command=lambda num=text: append_number(num), height=3, width=7, bg="white", borderwidth=0, relief="flat", activebackground="gray")

        elif text == "OK":
            button = tk.Button(numpad_frame, text=text, command=send_communication, height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
        else:
            button = tk.Button(numpad_frame, text=text, command=lambda num=text: append_number(num), height=2, width=7, bg="#EFEFFB", relief="flat", borderwidth=2)
        button.grid(row=row, column=col, padx=5, pady=5)


window = tk.Tk()
window.title("Autonomous Delivery")
window.configure(background="#FFFFFF")

entry = tk.Entry(window, width=40, font=("Georgia", 15))
entry.pack(pady=15)

show_numpad()

window.mainloop()