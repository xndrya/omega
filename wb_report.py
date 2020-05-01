import pandas as pd

"""
скрипт для обработки отчета по продажам ВБ
"""

directory = pd.read_excel('C:\\Users\\X\\Desktop\\Отчет №1285021.xlsx', sheet_name='TDSheet', skiprows=25)
names = []
sums = []
counts = []


for i in range(1, len(directory.groupby(["2"]))):
    name = directory.groupby(["2"])["10"].sum().index[i]
    if name == "Наименование":
        continue
    sum = directory.groupby(["2"])["10"].sum().values[i]
    count = directory.groupby(["2"])["10"].count().values[i]
    names.append(name)
    sums.append(sum)
    counts.append(count)

out = pd.DataFrame({'Название':names, 'Количество':counts, "Сумма":sums})
out.to_excel('C:\\Users\\X\\Desktop\\Отчет №128502.xlsx', sheet_name='New')

