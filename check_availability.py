import requests
import pandas as pd
from bs4 import BeautifulSoup

# путь до справочника
directory = pd.read_excel('data/SupplierNomenclature.xlsx', sheet_name='SupplierNomenclature', index_col="Номенклатура",
                          usecols="C")

count = 0
# перебираем все значения номенклатуры из справочника
for i in range(len(directory.index)):
    page = requests.get("http://www.wildberries.ru/catalog/" + str(directory.index[i]) + "/detail.aspx")

    # если есть признак отсутствия в наличии выводим наименование и ссылку на товар
    if "OutOfStock" in page.text:
        soup = BeautifulSoup(page.text, 'html.parser')
        print("-------------------------------")
        print(str(count + 1) + ". " + (soup.title.text.strip())[:-43])
        print("http://www.wildberries.ru/catalog/" + str(directory.index[i]) + "/detail.aspx")
        count += 1
print("-------------------------------")
print("На сайте отсутствует " + str(count) + " из " + str(len(directory.index)) + " товаров")
