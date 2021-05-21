from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import email_matcher


def getfile():
    root.filename = filedialog.askopenfilename(initialdir = "~/",title = "choose your file",filetypes = (
        ("csv files","*.csv"),
        ("oxf files","*.oxf"),
        ("qxf files","*.qxf"),
        ("all files","*.*")
        ))
    print(root.filename)
    pass

root = Tk()
root.title("Transaction Import Assistant")

style = ttk.Style()
style.theme_use("classic")
style.configure("BW.TFrame", foreground="black", background="white")
style.configure("GREY.TFrame", foreground="black", background="grey85")
style.configure("BW.TLabel", foreground="black", background="white")
content = ttk.Frame(root, style="BW.TFrame")
frame = ttk.Frame(content, borderwidth=2, relief=RIDGE, width=1200, height=700)
stepsframe = ttk.Frame(content, style="BW.TFrame")
nextframe = ttk.Frame(frame)

next = ttk.Button(frame, text="Next", command=email_matcher.ematcher)
startlbl = ttk.Label(stepsframe, text="Start", style="BW.TLabel")
file1lbl = ttk.Label(stepsframe, text="Select Transaction File to Import",style="BW.TLabel" )

content.grid(column=0, row=0)

frame.grid(column=1, row=0, columnspan=5, rowspan=2)
stepsframe.grid(column=0, row=0, columnspan=1, rowspan=2, sticky="N")
startlbl.grid(column=0, row=0)
file1lbl.grid(column=0, row=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

next.grid(column=0, row=0, sticky="e s")
frame.grid_propagate(0)
root.mainloop()


