import tkinter as tk
import winsound

# ---------------- SETTINGS ----------------
STUDY_TIME =  25 * 60   # 25 minutes
BREAK_TIME = 5 * 60    # 5 minutes
timer = None
time_left = 0
is_running = False

# ---------------- TIMER FUNCTIONS ----------------
def start_study():
    global time_left, is_running
    if is_running:
        return
    is_running = True
    lbl_status.config(text="Study Time ", fg="purple")
    time_left = STUDY_TIME
    count_down()

def start_break():
    global time_left, is_running
    if is_running:
        return
    is_running = True
    lbl_status.config(text="Break Time", fg="purple")
    time_left = BREAK_TIME
    count_down()

def count_down():
    global time_left, timer, is_running
    mins, secs = divmod(time_left, 60)
    canvas.itemconfig(timer_text, text=f"{mins:02d}:{secs:02d}")

    # Visual clock progress (arc)
    total = STUDY_TIME if "Study" in lbl_status.cget("text") else BREAK_TIME
    progress = (1 - time_left / total) * 360
    canvas.itemconfig(timer_arc, extent=progress)

    if time_left > 0 and is_running:
        time_left -= 1
        timer = window.after(1000, count_down)
    elif is_running:
        lbl_status.config(text="Done!")
        is_running = False

def cancel_timer():
    global timer, is_running, time_left
    if timer:
        window.after_cancel(timer)
    is_running = False
    time_left = 0
    lbl_status.config(text="Timer Reset ", fg="black")
    canvas.itemconfig(timer_text, text="00:00")
    canvas.itemconfig(timer_arc, extent=0)

def right_click_start(event):
    start_study()

# ---------------- UI SETUP ----------------
window = tk.Tk()
window.title("Pomodoro Timer ")
window.config(padx=40, pady=40, bg="#FFF9E6")

lbl_title = tk.Label(window, text="Pomodoro Timer", font=("Arial", 18, "bold"), bg="#FFF9E6")
lbl_title.pack(pady=10)

canvas = tk.Canvas(window, width=250, height=250, bg="#FFF9E6", highlightthickness=0)
timer_arc = canvas.create_arc(10, 10, 240, 240, start=90, extent=0, fill="#FF6F61", outline="")
timer_text = canvas.create_text(125, 125, text="00:00", fill="black", font=("Arial", 35, "bold"))
canvas.pack()

lbl_status = tk.Label(window, text="Ready!", bg="#FFF9E6", font=("Arial", 12))
lbl_status.pack(pady=10)

# Buttons
frame = tk.Frame(window, bg="#FFF9E6")
frame.pack()
btn_study = tk.Button(frame, text="Start Study", command=start_study, width=12, bg="#1FD655"
                                                                                   "", fg="white")
btn_study.grid(row=0, column=0, padx=5)
btn_break = tk.Button(frame, text="Start Break", command=start_break, width=12, bg="#1E90FF", fg="white")
btn_break.grid(row=0, column=1, padx=5)
btn_cancel = tk.Button(window, text="Cancel", command=cancel_timer, width=26, bg="#FF0800", fg="white")
btn_cancel.pack(pady=10)

# Right-click to start study session
canvas.bind("<Button-3>", right_click_start)

window.mainloop()
