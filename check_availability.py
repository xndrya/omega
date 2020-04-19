import requests
import pandas as pd
from bs4 import BeautifulSoup

# путь до справочника
directory = pd.read_excel('D:\Projects\WB scripts\data\SupplierNomenclature.xlsx', sheet_name='SupplierNomenclature', index_col="Номенклатура",
                          usecols="C")


def check_availability():
    out_of_stock = {}
    # перебираем все значения номенклатуры из справочника
    for i in range(len(directory.index)):
        page = requests.get(f"http://www.wildberries.ru/catalog/{str(directory.index[i])}/detail.aspx")
        # если есть признак отсутствия в наличии выводим наименование и ссылку на товар
        if "OutOfStock" in page.text:
            soup = BeautifulSoup(page.text, 'html.parser')
            out_of_stock[
                f"{(soup.title.text.strip())[:-43]}"] = f"http://www.wildberries.ru/catalog/{str(directory.index[i])}/detail.aspx"
    return out_of_stock


if __name__ == "__main__":
    list_out_of_stock = check_availability()
    count = 0
    for name, link in list_out_of_stock.items():
        print("---------------------------------------------------------------------------")
        print(name)
        print(link)
        count += 1
    print("---------------------------------------------------------------------------")
    print(f"На сайте отсутствует {str(count)} из {str(len(directory.index))} товаров")
