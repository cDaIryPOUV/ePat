# coding: utf-8
import sys
import openpyxl as px
import subprocess
import os

def excel_convert(vcf_path,tmp_dir,prefix):
    excel_path = tmp_dir + "/" + prefix +".xlsx"

    #新しいExcelシートを作成
    book=px.Workbook()
    sheet1=book.active
    sheet1.title='sheet1'

    f = open(vcf_path)
    i=0
    for line in f:
        #先頭の不要な情報をトリミング
        if "##" in line:
            continue
        #各列をタブ区切りで分割
        line = line.replace("\n","")
        cells = line.split()
        #7行目までをcellに書き込む(INFO行の端が削られるが問題ない)
        #HIGHとMODERATEの変異だけを抽出
        if "INFO" in cells[7] or "HIGH" in cells[7] or "MODERATE" in cells[7]:
            for j in range(len(cells)):
                sheet1.cell(row=i+1, column=j+1, value=cells[j])
            i+=1
    book.save(excel_path)


