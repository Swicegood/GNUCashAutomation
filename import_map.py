import piecash

# The path to the GNUCash file
gnucash_file_path = "/mnt/y/My Drive/GNUCash/test.gnucash"



# Open the GnuCash book
with piecash.open_book(gnucash_file_path, open_if_lock=False) as book:
    # Initialize a list to store import map data
    import_maps = []

    # Access the slots where import map data is stored
    for account in book.accounts:
        if "1008" in account.name:
            for slot in account.slots:            
                # Assuming 'import-map' is a part of the slot name
                if "bayes" in slot._name:
                    match_string = slot._name.split("/")[1]
                    account_guid = slot._name.split("/")[-1]
                    raw_value = slot.value
                    import_maps.append({"desc": match_string, "category": account_guid, "count": raw_value})

    # Write the import map data to a CSV file
    # with open('import_map.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Match String", "Account","Count"])
    #     writer.writerows(import_maps)

def getImportMap(account):
    return import_maps


def updateMap(account, bayes_item):
    # put new bayes item into accounts new import-map-bayes slot
    # or simply update the slots count if verbatim slot.name already exists
    return True

def getAccountObj(account_name):
    if account_name in account.name:
        return account