import itertools as it
from meza.io import IterStringIO
from csv2ofx import utils
from csv2ofx.ofx import OFX
from csv2ofx.mappings.default import mapping
from operator import itemgetter
from decimal import Decimal
import re

def ofx_export(file, transactions_list):

    def replace_bank_id_in_file(f):
        f.seek(0)
        content = f.read()
        
            # Replace the BANKID content
        return re.sub(r'<BANKID>.*?</BANKID>', '<BANKID>084000026</BANKID>', content)


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
        file.write(ofxline.decode("utf-8"))

    if transactions_list[0]["account"] == "Amex":
        modified_content = replace_bank_id_in_file(file)
        file.seek(0)
        file.write(modified_content)
        file.truncate()

if __name__ == "__main__":
    print("Not to be used as stand-alone program.")