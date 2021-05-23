from tkinter import filedialog

def getfile():
    filename = filedialog.askopenfilename(initialdir = "~/",title = "choose your file",filetypes = (
        ("csv files","*.csv"),
        ("oxf files","*.oxf"),
        ("qxf files","*.qxf"),
        ("all files","*.*")
        ))
    print(filename)
    return filename
