from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text,text='00:00')
    timer_label.config(text='TIMER',font=(FONT_NAME,15,'bold'),highlightthickness=0)
    check_marks.config(text='')
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text='LONG BREAK', font=(FONT_NAME, 15, 'bold'), fg = RED, highlightthickness=0)
    elif reps % 2 == 0:
            count_down(short_break_sec)
            timer_label.config(text='SHORT BREAK', font=(FONT_NAME, 15, 'bold'), fg = PINK, highlightthickness=0)
    else:
        count_down(work_sec)
        timer_label.config(text='WORK',fg = GREEN, font=(FONT_NAME,15,'bold'),highlightthickness=0)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    minute = count // 60
    #sau math.floor(count / 60)
    second = count % 60

    canvas.itemconfig(timer_text,text=f'{minute:02d}:{second:02d}')
    if count > 0:
        global timer
        timer = window.after(1000,count_down,count-1)
    else:
        start_timer()
        marks = ''
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += '✅'
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100,pady=50,bg=YELLOW)


#use fg (frontground colour)

canvas = Canvas(width=200, height=224,bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100,130,text='00:00',fill='white',font=(FONT_NAME,35,'bold'))
canvas.grid(row=2,column=1)

timer_label = Label(text='TIMER',font=(FONT_NAME,15,'bold'),highlightthickness=0)
timer_label.grid(row=1,column=1)

start_button = Button(text='Start',command=start_timer, highlightthickness=0)
start_button.grid(row=3,column=0)
reset_button = Button(text='Reset',highlightthickness=0, command=reset_timer)
reset_button.grid(row=3,column=2)
stop_button = Button(text='Stop',highlightthickness=0, command=reset_timer)
stop_button.grid(row=1,column=3)

check_marks = Label(text='',highlightthickness=0)
check_marks.grid(row=3,column=1)


window.mainloop()