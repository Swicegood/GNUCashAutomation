import csv
import decimal
from os import write
from typing_extensions import ParamSpecArgs
from filedialogs import getfile
from ofxparse import OfxParser
from decimal import Decimal, getcontext
import pdfreader
from pdfreader import SimplePDFViewer

def parse_paypal(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            line["account"] = "PayPal"
            line["date"] = line.pop('\ufeff"Date"')
            line["amount"] = Decimal(line.pop("Amount").replace("$","").replace(",",""))
            line["memo"] = ""
            line["desc"] = line.pop("Name")    
            line["id"] = ""
            print(line) 
            parsed_data.append(line)
    return parsed_data

def parse_amex(filename):
    parsed_data = []
    with open(filename, 'r') as data:

        for line in csv.DictReader(data):
            line["account"] = "Amex"
            line["date"] = line.pop("Date")
            line["amount"] = Decimal(line.pop("Amount"))
            line["memo"] = ""
            line["desc"] = line.pop("Description") 
            line["id"] = ""
            print(line)
            parsed_data.append(line)
    return parsed_data

def parse_xfx(filename):
    with open(filename) as fileobj:
        ofx = OfxParser.parse(fileobj)
    
    parsed_data= []
    account = ofx.account
    statement = account.statement
    for transaction in statement.transactions: 
        line = {}
        if account.type == 1:
            line["account"] = "Checking"
        else:
            line["account"] = str(account.type)
        line["date"] = transaction.date.strftime("%m/%d/%Y")
        line["amount"] = transaction.amount.quantize(Decimal('.00'))
        line["desc"] = transaction.payee
        line["memo"] = transaction.checknum
        line["id"] = ""
        print(line)
        parsed_data.append(line)
    return parsed_data

def parse_pdf(filename):
    fd = open(filename, "rb")
    viewer = SimplePDFViewer(fd)
    page_strings = []
    for canvas in viewer:
        page_strings.append(canvas.strings)
    parsed_data = []
    page_strings[0] = page_strings[0][2:]
    for pageofstrings in page_strings:
        pageofstrings = pageofstrings[7:-4]
        if len(pageofstrings)%8 == 0:
            x = int(len(pageofstrings)/8)
            for i in range(x):
                line = {}
                line["account"] = "PayPalPDF"
                line["date"] = pageofstrings[i*8 + 0]
                line["desc"] = pageofstrings[i*8 + 1]
                line["id"] = pageofstrings[i*8 + 2][5:]
                line["amount"] = Decimal(pageofstrings[i*8 + 5].replace("$","").replace(",",""))
                line["memo"] = ""
                print(line)
                parsed_data.append(line)
    return parsed_data

def parse_amazon(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            line["account"] = "Amazon"
            line["id"] = line.pop("\ufefforder id")
            try:
                line["amount"] = Decimal(line.pop("total"))
            except:
                line['amount'] = Decimal(0)
            finally:
                pass
            line["memo"] = ""
            line["desc"] = line.pop("items") 
            print(line)
            parsed_data.append(line)
    parsed_data = parsed_data[:-1]
    return parsed_data

def parse_accounts(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            print(line) 
            parsed_data.append(line)
    return parsed_data

def parse_export(csvfile, data):
        if data[0]["account"] == "Checking" or data[0]["account"] == "2":
            fieldnames = ["account", "date", "amount", "desc", "memo", "id", "tranfer_account"]
            fieldnames_notrns = ["account", "date", "amount", "desc", "memo", "id"]
        if data[0]["account"] == "PayPal":
            fieldnames = ["Time", "TimeZone", "Type", "Status", "Currency", "Receipt ID", "Balance", "account", "date", "amount", "desc", "memo", "id", "tranfer_account"]
            fieldnames_notrns = ["Time", "TimeZone", "Type", "Status", "Currency", "Receipt ID", "Balance", "account", "date", "amount", "desc", "memo", "id"]
        if data[0]["account"] == "Amex":
            fieldnames = ["Receipt", "account", "date", "amount", "memo", "desc", "id", "tranfer_account"]
            fieldnames_notrns = ["Receipt", "account", "date", "amount", "memo", "desc", "id"]
        if data[0]["account"] == "PayPalPDF":
            fieldnames = ["account", "date", "desc", "id", "amount", "memo", "tranfer_account"]
            fieldnames_notrns = ["account", "date", "desc", "id", "amount", "memo"]
        fieldsline = str(fieldnames).strip("[]")
        csvfile.write(fieldsline+"\n")
        for line in data:
            try:
                if line["tranfer_account"]:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="unix", quoting=csv.QUOTE_MINIMAL)   
                    writer.writerow(line)
            except:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames_notrns, dialect="unix", quoting=csv.QUOTE_MINIMAL)   
                writer.writerow(line)

if __name__ == "__main__":
    parse_accounts(getfile())