# use Tkinter to show a digital clock
# tested with Python24    vegaseat    10sep2006
from Tkinter import *
import time
from PIL import Image, ImageTk
root = Tk()
time1 = ''
clock = Label(root, font=('times', 40, 'bold'), bg='black',fg='white')
label1 = Label(root, font=('times', 80, 'bold'), bg='black',fg='white')
clock.pack(side=LEFT,expand=0)
label1.pack(side=TOP,expand=0)
label1.config(text = 'SMART MIRROR')






def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
tick()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.configure(background='black')




root.mainloop(  )
