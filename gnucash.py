#!/home/jaga/.accounting_venv/bin/python3

import tkinter as tk
from tkinter import Frame, ttk
from tkinter import messagebox
from tkinter.constants import VERTICAL
from email_matcher import ematcher
from parse import parse_amazon, parse_paypal, parse_amex, parse_pdf, parse_xfx, parse_accounts
from ofxwriter import ofx_export
from filedialogs import file_save, getfile
import functools
from PIL import ImageTk, Image
import traceback
import categorizer

ACCOUNTS_FILE = "accounts.csv"

class GnuCashApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global paneframe
        self.geometry("1300x700")
        self.grid_rowconfigure(0, weight=1) # this needed to be added
        self.grid_columnconfigure(0, weight=1) # as did this
        self.title("Transaction Import Assistant")
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("BW.TFrame", foreground="black", background="white")
        style.configure("GREY.TFrame", foreground="black", background="grey85")
        style.configure("BW.TLabel", foreground="black", background="white")
        style.configure("GREY.TLabel", foreground="black", background="grey75")
        style.configure("BLUE.TLabel", foreground="white", background="royal blue")
        style.configure("BLUE.TCheckbutton", foreground="black", background="royal blue")
        style.configure("LIME.TLabel", foreground="black", background="#bbffbd")
        style.configure("SUNSHINE.TLabel", foreground="black", background="#fdd236")
        content = ttk.Frame(self, style="GREY.TFrame")
        content.grid_rowconfigure(0, weight = 1)
        content.grid_columnconfigure(1, weight = 1)
        paneframe = ttk.Frame(content, width=1200, height=700)    
        content.grid(column=0, row=0, sticky="nsew")

        paneframe.grid(column=1, row=0, columnspan=5, rowspan=2, sticky="nsew")
        self.stepsframe_ = StepsFrame(parent=content, controller=self)

        self.pageframes = {}
        
        for F in (StartPage, ImportTrxnFilePage, ListPage):
            page_name = F.__name__
            pageframe = F(parent=paneframe, controller=self)
            self.pageframes[page_name] = pageframe
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            pageframe.grid(column=0, row=0, pady=40, padx=10, sticky="nsew", ipady=5, ipadx=5)

        paneframe.grid_columnconfigure(0, weight=1)
        paneframe.grid_rowconfigure(0, weight=1)       

        nextframe = ttk.Frame(paneframe)
        next = ttk.Button(paneframe, text="Next", command=self.nextstep)
        next.grid(column=0, row=1, sticky="e s")
        self.skipbtn = ttk.Button(paneframe, text="Skip", command=self.skipstep)
        self.skipbtn.grid(column=1, row=1, sticky="e s")
        self.show_frame("ImportTrxnFilePage")
        self.step = 2
        self.skip = False

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''        
        xframe = self.pageframes[page_name]
        xframe.tkraise()

    def skipstep(self):
        self.skip = True
        self.step += 1
        if self.step > 6:
            self.step = 1
        self.nextstep()
        self.skip == False
        
    def nextstep(self):
        filename = ''
        savename = None
        if self.step == 1:
            self.show_frame("ImportTrxnFilePage")
            self.stepsframe_.startlbl.config(style="GREY.TLabel")
        else:
            self.stepsframe_.startlbl.config(style="BW.TLabel")
        if self.step == 2:           
            self.stepsframe_.importlbl.config(style="GREY.TLabel")
            self.transactions = []
            filename = getfile()
            if len(filename):
                if self.pageframes["ImportTrxnFilePage"].bank.get() == "xfx":
                    self.transactions = parse_xfx(filename)
                if self.pageframes["ImportTrxnFilePage"].bank.get() == "paypal":
                    self.transactions = parse_paypal(filename)
                if self.pageframes["ImportTrxnFilePage"].bank.get() == "amex":
                    self.transactions = parse_amex(filename)
                if self.pageframes["ImportTrxnFilePage"].bank.get() == "paypalpdf":
                    self.transactions = parse_pdf(filename)
                    self.skip = True
                for child in self.pageframes["StartPage"].winfo_children():
                    child.destroy()
                self.pageframes["StartPage"].setFilename(filename)
                self.pageframes["StartPage"].newlabel()
                self.show_frame("StartPage")
                app.title("Transaction Import Assistant  -- "+filename)
        else:            
            self.stepsframe_.importlbl.config(style="BW.TLabel")
        if self.step == 3:
            self.stepsframe_.paypallbl.config(style="GREY.TLabel")
            filename = getfile()
            if len(filename):
                self.pageframes["ListPage"].paypal_txns = []
                self.pageframes["ListPage"].paypal_txns = parse_pdf(filename)
                self.pageframes["StartPage"].setFilename(filename)
                self.pageframes["StartPage"].newlabel()
        else:
            self.stepsframe_.paypallbl.config(style="BW.TLabel")
        if self.step == 4:
            self.stepsframe_.amazonlbl.config(style="GREY.TLabel")
            filename = getfile()
            if len(filename):  #valid filename (not empty)
                self.pageframes["ListPage"].amazon_txns = []
                self.pageframes["ListPage"].amazon_txns = parse_amazon(filename)
                self.pageframes["StartPage"].setFilename(filename)
                self.pageframes["StartPage"].newlabel()   
        else:                       
            self.stepsframe_.amazonlbl.config(style="BW.TLabel")
        if self.step == 5: 
            self.stepsframe_.matchlbl.config(style="GREY.TLabel") 
            self.pageframes["ListPage"].destroy
            self.pageframes["ListPage"] == ListPage(parent=paneframe, controller=self)
            self.show_frame("ListPage")
            self.pageframes["ListPage"].propagate_transactions(self.transactions)
            self.skipbtn.grid_remove()
        else:
            self.skipbtn.grid(column=1, row=1, sticky="e s")            
            self.stepsframe_.matchlbl.config(style="BW.TLabel")
        if self.step == 6:
            self.stepsframe_.sumlbl.config(style="GREY.TLabel")
            self.show_frame("StartPage")
            savename = file_save()            
            if savename:
                if self.transactions:                
                    ofx_export(savename, self.transactions)
                    messagebox.showinfo("info", "SUCCESS! Transactions Exported to File.")
                else:
                    messagebox.showinfo("info", "No Data to Write.")
        else:
            self.stepsframe_.sumlbl.config(style="BW.TLabel")
       
        # x = len(filename)  #len > 0 is valid filename        
        if (filename and len(filename)) or savename  or self.step == 5 or self.step == 1:
            self.step += 1   
        if self.step > 6:
            self.step = 0
        
        def show_error(self, *args):
            err = traceback.format_exception(*args)
            messagebox.showerror('Exception',err)

        tk.Tk.report_callback_exception = show_error

class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="GREY.TFrame", relief=tk.RIDGE)
        self.controller = controller
        self.grid_rowconfigure(0, weight=0) # this needed to be added
        self.grid_columnconfigure(0, weight=1) # as did this
        self.row = 0
        self.filename = ""

    def setFilename(self, filename):
        self.filename = filename

    def newlabel(self):
        filelbl = ttk.Label(self, text="LOADED SUCCESSFULLY: "+self.filename)
        filelbl.grid(column=0, row=self.row, padx=40, pady=40, sticky="wn")
        filelbl.rowconfigure(self.row, weight=0)
        self.row += 1


class ImportTrxnFilePage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="GREY.TFrame", relief=tk.RIDGE)    
        self.bank = tk.StringVar()
        firsthorizon = ttk.Radiobutton(self, text='First Horizon (OFX)', variable=self.bank, value='xfx')
        suntrust = ttk.Radiobutton(self, text='Suntrust (QFX', variable=self.bank, value='xfx')
        amex = ttk.Radiobutton(self, text='American Express (CSV', variable=self.bank, value='amex')
        paypal = ttk.Radiobutton(self, text='Paypal (CSV)', variable=self.bank, value='paypal')
        paypalpdf = ttk.Radiobutton(self, text='Paypal (PDF)', variable=self.bank, value='paypalpdf')
        firsthorizon.grid(column=0,row=0, padx=40, sticky="w")
        amex.grid(column=0,row=1, padx=40, sticky="w")
        paypal.grid(column=0,row=3, padx=40, sticky="w")
        paypalpdf.grid(column=0,row=4, padx=40, sticky="w")
        suntrust.grid(column=0,row=2, padx=40, sticky="w")
        self.contoller = controller

class ListPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="BW.TFrame", relief=tk.RIDGE) 
        self.logo = ImageTk.PhotoImage(Image.open("confidence_meter.png"))

        self.scrolledframe = VerticalScrolledFrame(self)
        self.scrolledframe.grid(column=0, row=0, sticky="nsew")
        self.scrolledframe.rowconfigure(0, weight=1)
        self.scrolledframe.columnconfigure(0, weight=1)
        datelbl = ttk.Label(self.scrolledframe.interior, text="Date", background="white", foreground="grey50")
        amountlbl = ttk.Label(self.scrolledframe.interior, text="Amount", background="white", foreground="grey50")
        desclbl = ttk.Label(self.scrolledframe.interior, text="Description", background="white", foreground="grey50")
        infolbl = ttk.Label(self.scrolledframe.interior, text="Info", background="white", foreground="grey50")
        memolbl = ttk.Label(self.scrolledframe.interior, text="Additional Comments", background="white", foreground="grey50")
        s = ttk.Separator(self.scrolledframe.interior, orient=tk.HORIZONTAL)
        infolbl.grid(column=3,row=0, sticky="W E")
        datelbl.grid(column=0,row=0, sticky="W E")
        amountlbl.grid(column=1,row=0, sticky="W E")
        desclbl.grid(column=2,row=0, sticky="W E")
        memolbl.grid(column=4,row=0, sticky="W E")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)    

        self.scrolledframe.interior.grid_columnconfigure(0, weight=1)
        self.scrolledframe.interior.grid_columnconfigure(1, weight=1)
        self.scrolledframe.interior.grid_columnconfigure(2, weight=4)
        self.scrolledframe.interior.grid_columnconfigure(3, weight=1)
        self.scrolledframe.interior.grid_columnconfigure(4, weight=5)
        s.grid(columnspan=5, row=1, sticky="W E")

        self.emailmatches = []
        self.transaction = { "account": "PayPal",
                        "date": "05/3/2021", 
                        "amount": "419.25", 
                        "desc": "eBay Purchase", 
                        "memo": "", 
                        "balanced":True }
        self.paypal_txns = []
        self.amazon_txns = []


    def changecolor(self, event, master, color):
        # Makes all rows white
        for Labels in self.Labelset:
            for label in Labels:
                label.config(style="SUNSHINE.TLabel")
            # Makes clicked row highlighted
            for line_num in self.green_lines:
                Labels[line_num].config(style="LIME.TLabel")
            Labels[master].config(style=color)     

    def start_ematcher(self, event, trxn, master):
        self.changecolor(event, master, "BLUE.TLabel")
        ematcher(self.emailmatches, trxn, self.paypal_txns, self.amazon_txns)

    def start_accounts_diag(self, event, master):
        acc_diag = AccountsDialog(controller=self, master=master, ACCOUNTS_FILE=ACCOUNTS_FILE)

    def set_account(self, value, master):
        self.transactions[master]["tranfer_account"] = value
        self.comlbls[master].config(text=value)
        self.changecolor(event=None, master=master, color="LIME.TLabel")
        self.green_lines.add(master)

    def unset_account(self, master):
        self.transactions[master]["transfer_account"] = ""
        self.comlbls[master].config(text="New, UNBALANCED (need account to transfer)")
        self.changecolor(event=None, master=master, color="SUNSHINE.TLabel")
        self.green_lines.remove(master)

    def get_comment_text(self, description, memo, master):
        transaction = {
        "desc": description,
        "memo": memo
        }

        category = categorizer.getCategory(transaction, 
                                           categorizer.clf, 
                                           categorizer.vectorizer, 
                                           categorizer.label_encoder)
        if category:            
            self.transactions[master]["tranfer_account"] = category
            return category
        else:
            return "New, UNBALANCED (need account to transfer "
            

    def propagate_transactions(self, transactions):
        self.transactions = transactions
        self.green_lines = set()
        self.Labelset = [] 
        self.datelbls = []
        self.amountlbls = []
        self.desclbls = []
        self.infolbls = []
        self.comlbls = [] 
        i = 0
        for line in transactions:
            if i == 0:
                mystyle = "BLUE.TLabel"
            else:
                mystyle = "SUNSHINE.TLabel"
            info = 7
            comments = "New, UNBALANCED (need account to transfer "
            self.datelbls.append(ttk.Label(self.scrolledframe.interior, text=line["date"], style=mystyle))
            self.datelbls[i].grid(column=0, row=i+2, sticky="w e")
            self.datelbls[i].bind("<Button 1>", functools.partial(self.changecolor, master=i, color="BLUE.TLabel"))
            self.amountlbls.append(ttk.Label(self.scrolledframe.interior, text=str(line["amount"]), style=mystyle))
            self.amountlbls[i].grid(column=1, row=i+2, sticky="w e")
            self.amountlbls[i].bind("<Button 1>", functools.partial(self.changecolor, master=i, color="BLUE.TLabel"))
            self.desclbls.append(ttk.Label(self.scrolledframe.interior, text=line["desc"], style=mystyle))
            self.desclbls[i].grid(column=2, row=i+2, sticky="w e")
            self.desclbls[i].bind("<Button 1>", functools.partial(self.changecolor, master=i, color="BLUE.TLabel"))
            self.infolbls.append(ttk.Label(self.scrolledframe.interior, image=self.logo, style=mystyle))
            self.infolbls[i].grid(column=3, row=i+2, sticky="w e")
            self.infolbls[i].bind("<Button 1>", functools.partial(self.start_ematcher, trxn=line, master=i))
            self.comlbls.append(ttk.Label(self.scrolledframe.interior, text=self.get_comment_text(line["desc"], line["memo"], master=i), style=mystyle))
            self.comlbls[i].grid(column=4, row=i+2, sticky="w e")
            self.comlbls[i].bind("<Button-1>", functools.partial(self.changecolor, master=i, color="BLUE.TLabel"))
            self.comlbls[i].bind("<Double-Button-1>", functools.partial(self.start_accounts_diag, master=i))
            i += 1 
        self.Labelset.append(self.datelbls)
        self.Labelset.append(self.amountlbls)
        self.Labelset.append(self.desclbls)
        self.Labelset.append(self.infolbls)
        self.Labelset.append(self.comlbls)

class StepsFrame(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="BW.TFrame", relief=tk.RIDGE)
        self.startlbl = ttk.Label(self, text="Start", style="GREY.TLabel")
        self.importlbl = ttk.Label(self, text="Select Transaction File to Import",style="BW.TLabel" )
        self.amazonlbl = ttk.Label(self, text="Select Amazon Tranaction File to Use",style="BW.TLabel" )
        self.paypallbl = ttk.Label(self, text="Select Paypal Tranaction File to Use",style="BW.TLabel" )
        self.matchlbl = ttk.Label(self, text="Match Transactions with Accounts",style="BW.TLabel" )
        self.sumlbl = ttk.Label(self, text="Summary and Export",style="BW.TLabel" )
        self.grid(column=0, row=0, columnspan=1, rowspan=2, sticky="N S", padx=10, pady=10)
        self.startlbl.grid(column=0, row=0, sticky="w e", padx=10, pady=5)
        self.importlbl.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self.amazonlbl.grid(column=0, row=3, sticky="w", padx=10, pady=5)
        self.paypallbl.grid(column=0, row=2, sticky="w", padx=10, pady=5)
        self.matchlbl.grid(column=0, row=4, sticky="w", padx=10, pady=5)
        self.sumlbl.grid(column=0, row=5, sticky="w", padx=10, pady=5)

class AccountsDialog(tk.Toplevel):

    def __init__(self, controller, master, ACCOUNTS_FILE):
        tk.Toplevel.__init__(self, width=400)
        self.geometry("400x400")
        self.controller = controller
        self.master_index = master
        self.title("Choose Transfer Account")
        self.accounts = parse_accounts(ACCOUNTS_FILE)    
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)  
        self.rowconfigure(0, weight=1)      
        self.tree = ttk.Treeview(self)
        self.tree.grid(column=0, row=0, sticky="senw", columnspan=2)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.grid(column=0, row=0, sticky="sen", columnspan=2)
        self.tree.configure(yscrollcommand=self.scrollbar.set)   
        for line in self.accounts:
            self.tree.insert("", "end", text=line["full_name"])
        self.tree.bind("<<TreeviewSelect>>", self.on_row_click)
        button = ttk.Button(self, text="Clear", command=self.clear)
        button.grid(column=0, row=1)
        ok_button = ttk.Button(self, text="Ok", command=self.do_ok)
        ok_button.grid(column=1, row=1, sticky="w")

    def do_ok(self, event=None):
        self.destroy()

    def clear(self):
        self.controller.unset_account(self.master_index)

    def on_row_click(self, event):        
        print(self.tree.selection())
        item = self.tree.selection()[0]
        self.selected_account = self.tree.item(item, "text")
        self.controller.set_account(self.selected_account, self.master_index)

class VerticalScrolledFrame(ttk.Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        vscrollbar = tk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.grid(column=5, row=0, sticky="ns")
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.grid(column=0,row=0, sticky="nsew")
        vscrollbar.config(command=canvas.yview)

                # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        

app = GnuCashApp()
app.mainloop()
