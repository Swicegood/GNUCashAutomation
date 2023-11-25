import piecash

# The path to the GNUCash file
gnucash_file_path = "/mnt/y/My Drive/GNUCash/test.gnucash"



# Open the GnuCash book
with piecash.open_book(gnucash_file_path, open_if_lock=False) as book:
    # Initialize a list to store import map data
    import_maps = []

    # Access the slots where import map data is stored
    for account in book.accounts:
        import_map = []
        for slot in account.slots:            
            # Assuming 'import-map' is a part of the slot name
            if "bayes" in slot._name:
                match_string = slot._name.split("/")[1]
                account_guid = slot._name.split("/")[-1]
                raw_value = slot.value
                import_map.append({"desc": match_string, "category": account_guid, "count": raw_value})
        import_maps.append({"account": account.name, "import_map": import_map})  # Add the account name and the import_map)
def getImportMap(account):
    for import_map in import_maps:
        if import_map["account"] == account:
            return import_map["import_map"]


def updateMap(account_obj, bayes_item):
    # put new bayes item into accounts new import-map-bayes slot
    # or simply update the slot's count if verbatim slot.name already exists
    return True

def getAccountObj(account_name):
    for account in book.accounts:
        if account_name in account.guid:
            return account
    
def getAccountNameFromGuid(account_guid):
    for account in book.accounts:
        if account_guid in account.guid:
            return account.name