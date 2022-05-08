from tkinter import *

root = Tk()

buff = StringVar()
buff.set("")

label = Label(root, textvariable = buff)
label.pack()


def make_cmd(n):
    return lambda : buff.set('button %d pressed' % n)


for x in range(4):
    button = Button(root, text = "Button %d" % x, command = make_cmd(x))
    button.pack()

root.mainloop()