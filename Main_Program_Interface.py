#######################################################
################## GUI FOR TRACKING ###################
#######################################################

import sys
import os
import tkinter as tk

input_param = ""

if sys.argv.__len__() == 1:
    print(sys.argv[0], "   has to be run with: -c / --close (for close objects) ")
    print("or -f / --far (for far objects) ")
    exit("missing parameter error!")

else:
    inp1 = sys.argv[1]

    if inp1 == "-c" or inp1 == "--close":
        input_param = "close objects tracking..."
        print(input_param)

    elif inp1 == "-f" or inp1 == "--far":
        input_param = "far objects tracking..."
        print(input_param)

    else:
        print("unknown param input:   (", inp1, ")")
        exit("unknown parameter input error!")


def start():
    print("start tracking...")

    text_box = tk.Text(root, height=2, width=25, padx=15, pady=15)
    text_box.insert(1.0, input_param)
    text_box.grid(column=1, row=2)

    # execute the Main Tracking program #
    os.system('python Main_Tracking_Api.py')


def stop():
    print("stop tracking!")

    text_box = tk.Text(root, height=2, width=25, padx=15, pady=15)
    text_box.insert(1.0, "stop tracking!")
    text_box.grid(column=1, row=2)


root = tk.Tk()
canvas = tk.Canvas(root, width=650, height=400)
canvas.grid(columnspan=3, rowspan=3)

start_text = tk.StringVar()
start_btn = tk.Button(root, textvariable=start_text, command=lambda: start(), font="Raleway", bg="#20bebe", fg="white", height=2, width=10)
start_text.set("Start")
start_btn.grid(column=0, row=0)

stop_text = tk.StringVar()
stop_btn = tk.Button(root, textvariable=stop_text, command=lambda: stop(), font="Raleway", bg="red2", fg="white", height=2, width=10)
stop_text.set("Stop")
stop_btn.grid(column=0, row=1)

root.mainloop()
