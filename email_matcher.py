from tkinter import * 
from tkinter import ttk

def ematcher():
    t = Toplevel()
    t.title("Select Matching Email")

    
    content = ttk.Frame(t, width=700, height=100, border=2, relief=RIDGE, style="BW.TFrame")
    frame = ttk.Frame(t, width=700, height=300, border=2, relief=RIDGE, style="BW.TFrame")
    buttonframe = ttk.Frame(t, style="GREY.TFrame")
    content.grid(column=0, row=0)
    frame.grid(column=0, row=1)
    buttonframe.grid(column=0, row=2, sticky="e w")
    value = None

    def do_ok(event=None):
        t.destroy()

    def do_cancel():
        t.destroy()
    
    ok = ttk.Button(buttonframe, text="ok", command=do_ok)
    cancel = ttk.Button(buttonframe, text="cancel", command=do_cancel)
    accountlbl = ttk.Label(content, text="Account", background="white", foreground="grey50")
    datelbl = ttk.Label(content, text="Date", background="white", foreground="grey50")
    amountlbl = ttk.Label(content, text="Amount", background="white", foreground="grey50")
    desclbl = ttk.Label(content, text="Description", background="white", foreground="grey50")
    memolbl = ttk.Label(content, text="Memo", background="white", foreground="grey50")
    balancedlbl = ttk.Label(content, text="Balanced", background="white", foreground="grey50")
    s = ttk.Separator(content, orient=HORIZONTAL)

    confidencelbl = ttk.Label(frame, text="Confidence", background="white", foreground="grey50")
    date2lbl = ttk.Label(frame, text="Date", background="white", foreground="grey50")
    subjectlbl = ttk.Label(frame, text="Subject", background="white", foreground="grey50")
    linklbl = ttk.Label(frame, text="Link to Invoice", background="white", foreground="grey50")
    ss = ttk.Separator(frame, orient=HORIZONTAL)

    
    accountlbl.grid(column=0,row=0, sticky="W")
    datelbl.grid(column=1,row=0, sticky="W")
    amountlbl.grid(column=2,row=0, sticky="W")
    desclbl.grid(column=3,row=0, sticky="W")
    memolbl.grid(column=4,row=0, sticky="W")
    balancedlbl.grid(column=5,row=0, sticky="W")
    for i in range(6):
        content.grid_columnconfigure(i, weight=1)    
    s.grid(columnspan=6 ,sticky="E W")

    confidencelbl.grid(column=0,row=0, sticky="W")
    date2lbl.grid(column=1,row=0, sticky="W")
    subjectlbl.grid(column=2,row=0, sticky="W")
    linklbl.grid(column=3,row=0, sticky="W")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=2)
    frame.grid_columnconfigure(3, weight=3)
    ss.grid(columnspan=4 ,sticky="E W")

    content.grid_propagate(0)
    frame.grid_propagate(0)
    ok.pack(side="right")
    cancel.pack(side="right")
    t.wait_window(t)
    return value