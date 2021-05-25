import tkinter as tk
from tkinter import Frame, ttk
from tkinter import filedialog
from email_matcher import ematcher
from parse import parse_paypal
from filedialogs import getfile
import functools

class GnuCashApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Transaction Import Assistant")
        style = ttk.Style()
        style.configure("BW.TFrame", foreground="black", background="white")
        style.configure("GREY.TFrame", foreground="black", background="grey85")
        style.configure("BW.TLabel", foreground="black", background="white")
        style.configure("GREY.TLabel", foreground="black", background="grey75")
        style.configure("BLUE.TLabel", foreground="white", background="royal blue")
        style.configure("BLUE.TCheckbutton", foreground="black", background="royal blue")
        content = ttk.Frame(self, style="GREY.TFrame")
        frame = ttk.Frame(content, width=1200, height=700)  
        content.grid(column=0, row=0)
        frame.grid(column=1, row=0, columnspan=5, rowspan=2)
        startframe = ttk.Frame(frame, style="GREY.TFrame", relief=tk.RIDGE)
        startframe.grid(column=0, row=0, pady=40, padx=10, sticky="n e w s", ipady=5, ipadx=5)
        self.pageframes = {}
        
        # for F in (StartPage,):
        #     page_name = F.__name__
        #     pageframe = F(parent=frame, controller=self)
        #     self.pageframes[page_name] = pageframe

        #     # put all of the pages in the same location;
        #     # the one on the top of the stacking order
        #     # will be the one that is visible.
        #     breakpoint()
        #     pageframe.grid(column=0, row=0, pady=40, padx=10, sticky="n e w s", ipady=5, ipadx=5)
        # self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.pageframes[page_name]
        frame.tkraise()


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="GREY.TFrame", relief=tk.RIDGE)
        self.controller = controller


app = GnuCashApp()
app.mainloop()
