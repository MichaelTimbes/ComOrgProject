# GUI for Smart MIRROR
# Currently includes:
# - Title
# - Digital Clock that updates every 200ms
# -

from Tkinter import *
import time
import requests


###################################################
# Functions to be repeated and updated while running
def clockUpdate():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        Clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    Clock.after(200, clockUpdate)


def weatherAPICall():
    url = 'http://api.openweathermap.org/data/2.5/weather?APPID=301e59e1ab9370e1f7644445df46f156' # url goes here
    location = 'Clarksville' # adjust as required
    unit = 'metric'
    paramaters = {'q':location, 'units':unit}
    response = requests.get(url, params = paramaters)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Something went wrong')

    print data

    WeatherTemp.config(text = data[u'weather'][0][u'description']
                        + '\nTemperature: '
                        + str(data[u'main'][u'temp']))
###################################################




###################################################
# Initializing root. Main GUI Object Window
root = Tk()
###################################################



###################################################
# Clock Object
time1 = ''
Clock = Label(root, font=('times', 40, 'bold'), bg='black',fg='white')
Clock.pack(side=LEFT,expand=0)

WeatherTemp = Label(root, font=('times',40,'bold'),bg='black',fg= 'white')
WeatherTemp.pack(side = RIGHT, expand =0)

# Title Object
Title = Label(root, font=('times', 80, 'bold'), bg='black',fg='white')
Title.pack(side=TOP,expand=0)
Title.config(text = 'SMART MIRROR')

#Footer
Title = Label(root, font=('times',20, 'bold'), bg='black',fg='white')
Title.pack(side=BOTTOM,expand=0)
Title.config(text = 'Project by: Dominic Critchlow, Travis Hodge, Dylan Kellogg, Michael Timbes')
###################################################




###################################################
# Call Function for items
clockUpdate()
weatherAPICall()
###################################################




###################################################
# Main structure of window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.configure(background='black')
# Running of the GUI Loop
root.mainloop(  )
###################################################
