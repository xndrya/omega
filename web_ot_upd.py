# -*- coding: cp1251 -*-
import datetime
import openpyxl
import pandas as pd
from lxml import etree


def make_ot_upd(file_path, type):
    # ���� �� �����
    invoice = openpyxl.load_workbook(file_path, read_only=True)
    sheet_invoice = invoice["TDSheet"]

    # ���� �� �����������
    dir = pd.read_excel('D:\Projects\WB scripts\data\directory.xlsx', sheet_name='directory',
                        index_col="��������")

    # ���� �� ����� xml
    if type == "OT":
        template_path = 'D:\\Projects\\WB scripts\\data\\template_main3.xml'
    elif type == "WB":
        template_path = 'D:\\Projects\\WB scripts\\data\\template_main2.xml'
    else:
        template_path = 'D:\\Projects\\WB scripts\\data\\template_main.xml'

    doc = etree.parse(template_path)
    num = 0
    # ��������� ���-�� ������� � ����� � 25 �� 150 ������
    for k in range(25, 150, 1):
        if sheet_invoice.cell(row=k, column=2).value != None:
            num = sheet_invoice.cell(row=k, column=2).value
        else:
            break

    total_sum_without_nds = 0
    total_sum = 0
    total_quantity = 0
    table_root = doc.find("//����������")
    i = 0

    for i in range(num):
        # ����������
        quantity = sheet_invoice.cell(row=i + 25, column=20).value

        # ���� �������� ������ ���, ����� �� ������� � ��������� ���� ��� ��� ��� ���
        price = sheet_invoice.cell(row=i + 25, column=25).value
        nds = sheet_invoice.cell(row=i + 25, column=29).value
        price_without_nds = round(price / (1 + nds * 0.01), 2)
        total_sum_per_good = sheet_invoice.cell(row=i + 25, column=37).value

        # ������� ������� ������� � �������� ���������
        good = etree.Element("�������")
        good.set("������", str(quantity) + ".000")

        # ������������ ������ ����� �� �����
        item = sheet_invoice.cell(row=i + 25, column=4).value
        good.set("�������", item)
        good.set("�����", str(nds) + "%")
        good.set("������", str(i + 1))
        good.set("����_���", "796")
        sum_price_without_nds = round(price_without_nds * quantity, 2)
        good.set("�����������", str(sum_price_without_nds))
        good.set("����������", str(total_sum_per_good))
        good.set("�������", str(price_without_nds))

        acc = etree.SubElement(good, '�����')
        acc_free = etree.SubElement(acc, '��������')
        acc_free.text = "��� ������"

        tax_sum = etree.SubElement(good, '������')
        tax_sum2 = etree.SubElement(tax_sum, '������')
        item_nds = round(total_sum_per_good - (price_without_nds * quantity), 2)
        tax_sum2.text = str(item_nds)

        td = etree.SubElement(good, '����')
        td.set("���������", str(dir["��� ������"][item]))
        td.set("�������", str(dir["���"][item]))

        addit = etree.SubElement(good, '����������')
        addit.set("������", str(dir["��������"][item]))
        addit.set("�����������", dir["������"][item])
        addit.set("���������", "��")
        addit.set("��������", "1")

        info = etree.SubElement(good, '���������2')
        info.set("������", str(dir["��������"][item]))
        info.set("�������", "��")

        info2 = etree.SubElement(good, '���������2')
        info2.set("������", str(dir["��������"][item]))
        info2.set("�������", "���")

        info3 = etree.SubElement(good, '���������2')
        info3.set("������", str(dir["��������"][item]))
        info3.set("�������", "��")

        info4 = etree.SubElement(good, '���������2')
        info4.set("������", str(dir["��������"][item]))
        info4.set("�������", "�������������")

        info5 = etree.SubElement(good, '���������2')
        info5.set("������", item)
        info5.set("�������", "������������������")

        info6 = etree.SubElement(good, '���������2')
        info6.set("������", item)
        info6.set("�������", "������������������")

        info7 = etree.SubElement(good, '���������2')
        info7.set("������", str(dir["�������"][item]))
        info7.set("�������", "��")

        table_root = doc.find("//����������")

        # ������� �������� ����� � ��� � ��� � ����������
        total_sum_without_nds += sum_price_without_nds
        total_sum += total_sum_per_good
        total_quantity += quantity

        # ��������� �������
        table_root.insert(i, good)

    # ����������� �������� ����� � ��� � ��� � ����������
    total = etree.Element("��������")
    total.set("����������������", str(round(total_sum_without_nds, 2)))
    total.set("���������������", str(total_sum))
    total_nds = etree.SubElement(total, "�����������")
    total_nds2 = etree.SubElement(total_nds, "������")
    total_nds3 = round(total_sum - total_sum_without_nds, 2)
    total_nds2.text = str(total_nds3)
    total_quantity2 = etree.SubElement(total, "����������")
    total_quantity2.text = str(total_quantity)
    table_root.insert(i + 1, total)

    # ��������� �������  ����, ����� � ����������� � ��������
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    time = datetime.datetime.today().strftime("%H.%M.%S")

    doc.find("//��������").attrib['���������'] = date
    doc.find("//��������").attrib['���������'] = time
    doc.find("//��������").attrib['�������'] = date
    doc.find("//�����").attrib['�������'] = date
    doc.findall("//��������")[0].attrib['������'] = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
    doc.findall("//��������")[2].attrib['������'] = date
    doc.findall("//��������")[4].attrib['������'] = date
    doc.findall("//��������")[5].attrib['������'] = date

    f = doc.write("D:\\Projects\\WB scripts\\output\\output.xml", encoding="cp1251", pretty_print=True,
                  xml_declaration=True)
    return f


if __name__ == "__main__":
    make_ot_upd('input/invoice.xlsx')
