import itertools as it
from meza.io import IterStringIO
from csv2ofx import utils
from csv2ofx.ofx import OFX
from csv2ofx.mappings.default import mapping
from operator import itemgetter
from decimal import Decimal

def ofx_export(filename, transactions_list):

    def convert_decimal_to_string(data):
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = convert_decimal_to_string(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = convert_decimal_to_string(data[i])
        elif isinstance(data, Decimal):
            data = str(data)
        return data

    convert_decimal_to_string(transactions_list)

    mapping = {
        'account': itemgetter('account'),
        'date': itemgetter('date'),
        'amount': itemgetter('amount'),
        'payee': itemgetter('desc'),
        'notes': itemgetter('memo'),
        'class': itemgetter('tranfer_account'),
        'type': itemgetter('type')
        }
    
    ofx = OFX(mapping)
    groups = ofx.gen_groups(transactions_list)
    trxns = ofx.gen_trxns(groups)
    cleaned_trxns = ofx.clean_trxns(trxns)
    data = utils.gen_data(cleaned_trxns)
    content = it.chain([ofx.header(), ofx.gen_body(data), ofx.footer()])

    for ofxline in IterStringIO(content):
        print(ofxline.decode("utf-8"))
        filename.write(ofxline.decode("utf-8"))

if __name__ == "__main__":
    print("Not to be used as stand-alone program.")