import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# путь до справочника
directory = pd.read_excel('D:\Projects\WB scripts\data\SupplierNomenclature2.xlsx', sheet_name='SupplierNomenclature')


def check():
    out_of_stock = {}
    # перебираем все значения номенклатуры из справочника
    for i in range(len(directory.index)):
        page = requests.get(f"http://www.wildberries.ru/catalog/{str(directory['Номенклатура'][i])}/detail.aspx")
        # если есть признак отсутствия в наличии выводим наименование и ссылку на товар
        if "OutOfStock" in page.text:
            soup = BeautifulSoup(page.text, 'html.parser')
            out_of_stock[
                f"{(soup.title.text.strip())[:-47]}"] = f"http://www.wildberries.ru/catalog/{str(directory.index[i])}/detail.aspx"
    return out_of_stock


def get_wb_stock():
    count = 0
    stock = {}
    for i in range(len(directory.index)):
        if str(directory['Наличие'][i]) == 'да':
            page = requests.get(f"http://www.wildberries.ru/{str(directory['Номенклатура'][i])}/product/data")
            response = json.loads(page.text)
            quantity = response['value']['data']['productCard']['nomenclatures'][
                f'{str(directory["Номенклатура"][i])}']['sizes'][0]['quantity']
            print(f'{directory["Название"][i]} - {quantity}')
            stock[
                f"{directory['Название'][i]}"] = quantity
            if quantity == 0:
                count += 1
    print(f'Отсутствуют {count} шт наименований')
    return


if __name__ == "__main__":
    get_wb_stock()
