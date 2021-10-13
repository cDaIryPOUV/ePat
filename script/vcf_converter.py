# coding: utf-8
import xlrd
import sys

def vcf_converter(output_dir,prefix):
    input_excel_path = output_dir + '/output_provean_' + prefix + ".xlsx"
    output_vcf_path = output_dir + '/output_provean_' + prefix + ".txt"

    # input_excel_path = prefix
    # output_vcf_path = output_dir +  "test.vcf"

    f = xlrd.open_workbook(input_excel_path)
    g = open(output_vcf_path, "w")
    sheets = f.sheets()
    sheet = sheets[0]
    nrow = sheet.nrows
    for i in range(nrow):
        row = sheet.row_values(i)
        row = list(map(str, row))
        row = "\t".join(row)
        row = row + "\n"
        g.write(row)
    g.close()
