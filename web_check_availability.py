import requests
import pandas as pd
from bs4 import BeautifulSoup

# путь до справочника
directory = pd.read_excel('D:\Projects\WB scripts\data\SupplierNomenclature2.xlsx', sheet_name='SupplierNomenclature',
                          index_col="Номенклатура",
                          usecols="B")


def check():
    out_of_stock = {}
    # перебираем все значения номенклатуры из справочника
    for i in range(len(directory.index)):
        page = requests.get(f"http://www.wildberries.ru/catalog/{str(directory.index[i])}/detail.aspx")
        # если есть признак отсутствия в наличии выводим наименование и ссылку на товар
        if "OutOfStock" in page.text:
            soup = BeautifulSoup(page.text, 'html.parser')
            out_of_stock[
                f"{(soup.title.text.strip())[:-47]}"] = f"http://www.wildberries.ru/catalog/{str(directory.index[i])}/detail.aspx"
    return out_of_stock


if __name__ == "__main__":
    list_out_of_stock = check()
    count = 0
    for name, link in list_out_of_stock.items():
        print("---------------------------------------------------------------------------")
        print(name)
        print(link)
        count += 1
    print("---------------------------------------------------------------------------")
    print(f"На сайте отсутствует {str(count)} из {str(len(directory.index))} товаров")
