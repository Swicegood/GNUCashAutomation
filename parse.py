import csv
from typing_extensions import ParamSpecArgs
from filedialogs import getfile
from ofxparse import OfxParser
from decimal import Decimal
import pdfreader
from pdfreader import SimplePDFViewer

def parse_paypal(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            print(line)
            line["account"] = "PayPal"
            line["date"] = line.pop("Date")
            line["amount"] = line.pop("Amount")
            line["memo"] = ""
            line["desc"] = line.pop("Name") 
            parsed_data.append(line)
    return parsed_data

def parse_amex(filename):
    parsed_data = []
    with open(filename, 'r') as data:

        for line in csv.DictReader(data):
            line["account"] = "Amex"
            line["date"] = line.pop("Date")
            line["amount"] = line.pop("Amount")
            line["memo"] = ""
            line["desc"] = line.pop("Description") 
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
            line["account"] = account.type
        line["date"] = transaction.date.strftime("%d %b, %Y")
        line["amount"] = transaction.amount
        line["desc"] = transaction.payee
        line["memo"] = transaction.checknum
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
                line["account"] = "PayPal"
                line["date"] = pageofstrings[i*8 + 0]
                line["desc"] = pageofstrings[i*8 + 1]
                line["id"] = pageofstrings[i*8 + 2][5:]
                line["amount"] = pageofstrings[i*8 + 5]
                print(line)
                parsed_data.append(line)
    return parsed_data

def parse_amazon(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            line["account"] = "Amazon"
            line["id"] = line.pop("\ufefforder id")
            line["amount"] = line.pop("total")
            line["memo"] = ""
            line["desc"] = line.pop("items") 
            print(line)
            parsed_data.append(line)
    parsed_data = parsed_data[:-1]
    return parsed_data

if __name__ == "__main__":
    parse_amazon(getfile())