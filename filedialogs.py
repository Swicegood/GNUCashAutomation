from tkinter import filedialog

def getfile():
    filename = filedialog.askopenfilename(initialdir = "~/",title = "choose your file")
                                        #  filetypes = [
                                        #  ("Banking files",".csv .oxf .oxf .qvf")
                                        #  ])
    print(filename)
    return filename

def file_save():
    name=filedialog.asksaveasfile(mode='w',defaultextension=".csv")
    if name is None:
        return        
    return name

if __name__ == "__main__":
    file_save()