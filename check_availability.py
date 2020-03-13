import requests
import pandas as pd

# путь до справочника
directory = pd.read_excel('SupplierNomenclature.xls', sheet_name='SupplierNomenclature', index_col="Номенклатура", usecols="C")
for i in range(len(directory.index)):
    page = requests.get("http://www.wildberries.ru/catalog/" + str(directory.index[i]) + "/detail.aspx")
    if "OutOfStock" in page.text:
        print("http://www.wildberries.ru/catalog/" + str(directory.index[i]) + "/detail.aspx")
