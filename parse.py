import csv
from filedialogs import getfile

def parse_paypal(filename):
    parsed_data = []
    with open(filename, 'r') as data:
        
        for line in csv.DictReader(data):
            print(line)
            parsed_data.append(line)
    return parsed_data

if __name__ == "__main__":
    parse_paypal(getfile())