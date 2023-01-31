import functools
from tkinter import * 
from tkinter import ttk
from gmail import grab_emails
from decimal import Decimal, getcontext
import webbrowser
from datetime import datetime, timedelta

def ematcher(emailmatches, transaction, paypal_txns, amazon_txns):
    t = Toplevel()
    t.title("Select Matching Email")

    #getcontext().prec=2
    search_str = Decimal.copy_abs(transaction["amount"])


    if not emailmatches:
        emailmatches = grab_emails(str(search_str))
    for emailmatch in emailmatches:
        emailmatch["link"] = "No Info"
    
    content = ttk.Frame(t, width=1200, height=100, border=2, relief=RIDGE, style="BW.TFrame")
    frame = ttk.Frame(t, width=1200, height=300, border=2, relief=RIDGE, style="BW.TFrame")
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
    ttk.Label(content, text=transaction["account"], style="BLUE.TLabel").grid(column=0, row=2, sticky='w e')
    ttk.Label(content, text=transaction["date"], style="BLUE.TLabel").grid(column=1, row=2, sticky='w e')
    ttk.Label(content, text=transaction["amount"], style="BLUE.TLabel").grid(column=2, row=2, sticky='w e')
    ttk.Label(content, text=transaction["desc"], style="BLUE.TLabel").grid(column=3, row=2, sticky='w e')
    ttk.Label(content, text=transaction["memo"], style="BLUE.TLabel").grid(column=4, row=2, sticky='w e')
    ttk.Label(content, text=transaction["amount"], style="BLUE.TLabel").grid(column=5, row=2, sticky='w e')

    confidencelbl = ttk.Label(frame, text="Confidence", background="white", foreground="grey50")
    date2lbl = ttk.Label(frame, text="Date", background="white", foreground="grey50")
    subjectlbl = ttk.Label(frame, text="Subject", background="white", foreground="grey50")
    linklbl = ttk.Label(frame, text="Link to Invoice", background="white", foreground="grey50")
    ss = ttk.Separator(frame, orient=HORIZONTAL)
    
    i = 0
    subjectlbls = []
    linklbls = []
    for emailmatch in emailmatches:
        if i == 0:
            mystyle = "BLUE.TLabel"
        else:
            mystyle = "BW.TLabel"
        date = ""
        subject = ""
        for item in emailmatch["payload"]["headers"]:
            if item["name"] == "Subject":
                subject = item["value"]
            if item["name"] == "Date":
                date = item["value"]
        link = invoice_matcher(transaction ,emailmatch, paypal_txns, amazon_txns)
        print(link)
        ttk.Label(frame, text=emailmatch["confidence"], style=mystyle).grid(column=0, row=2 + i, sticky="w e")
        ttk.Label(frame, text=date.split(" ")[:3], style=mystyle).grid(column=1, row=2 + i, sticky="w e")
        subjectlbls.append(ttk.Label(frame, text=subject, style=mystyle))
        subjectlbls[i].grid(column=2, row=2 + i, sticky="w e")
        subjectlbls[i].bind("<Button 1>", functools.partial(launch_browser, link="https://mail.google.com/mail/u/0/#all/"+emailmatch["id"])) 
        linklbls.append(ttk.Label(frame, text=link, style=mystyle))
        linklbls[i].grid(column=3, row=2 + i, sticky="w e")
        linklbls[i].bind("<Button 1>", functools.partial(launch_browser, link=link))        
        i += 1

    accountlbl.grid(column=0,row=0, sticky="W")
    datelbl.grid(column=1,row=0, sticky="W")
    amountlbl.grid(column=2,row=0, sticky="W")
    desclbl.grid(column=3,row=0, sticky="W")
    memolbl.grid(column=4,row=0, sticky="W")
    balancedlbl.grid(column=5,row=0, sticky="W")
    for i in range(6):
        content.grid_columnconfigure(i, weight=1)    
    s.grid(columnspan=6 , row=1, sticky="E W")
    
    confidencelbl.grid(column=0,row=0, sticky="W")
    date2lbl.grid(column=1,row=0, sticky="W")
    subjectlbl.grid(column=2,row=0, sticky="W")
    linklbl.grid(column=3,row=0, sticky="W")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=3)
    frame.grid_columnconfigure(3, weight=1)
    ss.grid(columnspan=4 ,row=1, sticky="E W")

    content.grid_propagate(0)
    frame.grid_propagate(0)
    ok.pack(side="right")
    cancel.pack(side="right")    

    t.wait_window(t)
    return value

def launch_browser(self, link):
    webbrowser.open(link, new=2)

def invoice_matcher(trxn, email, paypal_txns, amazon_txns):

    if trxn["id"]:
        return "https://www.paypal.com/myaccount/transactions/details/"+trxn["id"]
    else:
        for item in email["payload"]["headers"]:
             if item["name"] == "From":
                sender = item["value"]
                sender = sender.lower()
        if sender.find("amazon.com") != -1:
            matches = []
            for amazon_trxn in amazon_txns:
                if trxn["amount"] == amazon_trxn["amount"]:
                    matches.append(amazon_trxn)
            datematches = []
            if not matches:
                return "No Match"
            elif len(matches) == 1:
                return "https://smile.amazon.com/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&orderID="+matches[0]["id"]
            else:
                for match in matches:
                    for i in range(3):
                        TRANSACTION_CHECK = datetime.strptime(trxn["date"], "%m/%d/%Y")
                        start =  TRANSACTION_CHECK - timedelta(days=i)
                        end = TRANSACTION_CHECK + timedelta(days=i)
                        COMPANY_PURCHASE_CHECK = datetime.strptime(match["date"], "%Y-%m-%d")
                        if start <= COMPANY_PURCHASE_CHECK <= end:
                            return "https://smile.amazon.com/gp/css/summary/print.html/ref=ppx_od_dt_b_invoice?ie=UTF8&orderID="+match["id"]

        elif sender.find("paypal.com") != -1:
            matches = []
            for paypal_trxn in paypal_txns:
                if trxn["amount"] == paypal_trxn["amount"]:
                    matches.append(paypal_trxn)
            datematches = []
            if not matches:
                return "No Match"
            elif len(matches) == 1:
                return "https://www.paypal.com/myaccount/transactions/details/"+matches[0]["id"]
            else:
                for match in matches:
                    for i in range(3):
                        TRANSACTION_CHECK = datetime.strptime(trxn["date"], "%m/%d/%Y")
                        start =  TRANSACTION_CHECK - timedelta(days=i)
                        end = TRANSACTION_CHECK + timedelta(days=i)
                        COMPANY_PURCHASE_CHECK = datetime.strptime(match["date"], "%m/%d/%Y")
                        if start <= COMPANY_PURCHASE_CHECK <= end:
                            return "https://www.paypal.com/myaccount/transactions/details/"+match["id"]
        else:
            return "Unsupported Company"


if __name__ == "__main__":
    emailmatches = []
    transaction = { "account": "PayPal",
                    "date": "05/2/2021", 
                    "amount": Decimal("40.00"), 
                    "desc": "Vijaya Metha", 
                    "memo": "", 
                    "id": ""
                   }
    paypal_txns = []
    amazon_txns = []
    real = Tk()
    ematcher(emailmatches, transaction, paypal_txns, amazon_txns)