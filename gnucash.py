from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from email_matcher import ematcher
from parse import parse_paypal

emailmatches = []
transaction = { "account": "PayPal",
                "date": "05/3/2021", 
                "amount": "419.25", 
                "desc": "eBay Purchase", 
                "memo": "", 
                "balanced":True }
paypal_txns = []
amazon_txns = []

root = Tk()
root.title("Transaction Import Assistant")

style = ttk.Style()
style.theme_use("classic")
style.configure("BW.TFrame", foreground="black", background="white")
style.configure("GREY.TFrame", foreground="black", background="grey85")
style.configure("BW.TLabel", foreground="black", background="white")
style.configure("GREY.TLabel", foreground="black", background="grey75")
style.configure("BLUE.TLabel", foreground="white", background="royal blue")
style.configure("BLUE.TCheckbutton", foreground="black", background="royal blue")
content = ttk.Frame(root, style="GREY.TFrame")
frame = ttk.Frame(content, width=1200, height=700)
listframe = ttk.Frame(frame, style="BW.TFrame", relief=RIDGE)
stepsframe = ttk.Frame(content, style="BW.TFrame", relief=RIDGE)
nextframe = ttk.Frame(frame)

next = ttk.Button(frame, text="Next", command=lambda: ematcher(emailmatches, transaction, paypal_txns, amazon_txns))           
startlbl = ttk.Label(stepsframe, text="Start", style="GREY.TLabel")
importlbl = ttk.Label(stepsframe, text="Select Transaction File to Import",style="BW.TLabel" )
amazonlbl = ttk.Label(stepsframe, text="Select Amazon Tranaction File to Use",style="BW.TLabel" )
paypallbl = ttk.Label(stepsframe, text="Select Paypal Tranaction File to Use",style="BW.TLabel" )
matchlbl = ttk.Label(stepsframe, text="Match Transactions with Accounts",style="BW.TLabel" )
sumlbl = ttk.Label(stepsframe, text="Summary and Export",style="BW.TLabel" )


datelbl = ttk.Label(listframe, text="Date", background="white", foreground="grey50")
amountlbl = ttk.Label(listframe, text="Amount", background="white", foreground="grey50")
desclbl = ttk.Label(listframe, text="Description", background="white", foreground="grey50")
infolbl = ttk.Label(listframe, text="Info", background="white", foreground="grey50")
memolbl = ttk.Label(listframe, text="Additional Comments", background="white", foreground="grey50")
s = ttk.Separator(listframe, orient=HORIZONTAL)

content.grid(column=0, row=0)
frame.grid(column=1, row=0, columnspan=5, rowspan=2)
listframe.grid(pady=40, padx=10, sticky="n e w s", ipady=5, ipadx=5)
stepsframe.grid(column=0, row=0, columnspan=1, rowspan=2, sticky="N S", padx=10, pady=10)
startlbl.grid(column=0, row=0, sticky="w e", padx=10, pady=5)
importlbl.grid(column=0, row=1, sticky="w", padx=10, pady=5)
amazonlbl.grid(column=0, row=2, sticky="w", padx=10, pady=5)
paypallbl.grid(column=0, row=3, sticky="w", padx=10, pady=5)
matchlbl.grid(column=0, row=4, sticky="w", padx=10, pady=5)
sumlbl.grid(column=0, row=5, sticky="w", padx=10, pady=5)

infolbl.grid(column=3,row=0, sticky="W E")
datelbl.grid(column=0,row=0, sticky="W E")
amountlbl.grid(column=1,row=0, sticky="W E")
desclbl.grid(column=2,row=0, sticky="W E")
memolbl.grid(column=4,row=0, sticky="W E")
    
listframe.grid_columnconfigure(0, weight=1)
listframe.grid_columnconfigure(1, weight=1)
listframe.grid_columnconfigure(2, weight=2)
listframe.grid_columnconfigure(3, weight=1)
listframe.grid_columnconfigure(4, weight=5)
s.grid(columnspan=5, row=1, sticky="W E")

frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

next.grid(column=0, row=0, sticky="e s")
frame.grid_propagate(0)
root.mainloop()


