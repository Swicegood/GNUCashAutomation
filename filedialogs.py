from tkinter import filedialog

def getfile():
    filename = filedialog.askopenfilename(initialdir = "~/",title = "choose your file")
                                        #  filetypes = [
                                        #  ("Banking files",".csv .oxf .oxf .qvf")
                                        #  ])
    print(filename)
    return filename
