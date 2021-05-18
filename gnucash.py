from tkinter import *
from tkinter import ttk 

root = Tk()
root.title("Transaction Import Assistant")

ttk.Button(root, text="Cancel", command=(exit)).grid(padx=600, pady=400, sticky='SE')
ttk.Button(root, text="Next").grid()




root.mainloop()