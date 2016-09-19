from tkinter import *

root = Tk()

def key(event):
    print("pressed", repr(event.char))

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)



frame = Frame(root, width=100, height=100)

frame.pack()
but = Entry(frame, text="hello")
but.pack()
but.bind('<Key>', key)
but.bind("<Button-1>", callback)



root.mainloop()