# coding: utf-8
import sys
import re
import subprocess
from statistics import mode
import os
# import xlrd
# import openpyxl as px

#pycファイルを作成しない設定
sys.dont_write_bytecode = True

#引数を所得
argv = sys.argv
script_dir = argv[1]
input_file_path = argv[2]
output_dir = argv[3]
snp_path = argv[4]
ref = argv[5]
tool_path = argv[6]
tmp_path = argv[7]

#ファイルのPrefixを所得　+　拡張子を所得
basename = os.path.split(input_file_path)[1]
root_ext_pair = os.path.splitext(basename)
prefix = root_ext_pair[0]
etx = root_ext_pair[1]
print(prefix)

print("END option setting")

#vcfファイルの場合
import excel_converter
if "vcf" in etx:
    #snpEffでvcfファイルをアノテーション。tmp_path/tmp.vcfに出力。
    subprocess.check_output(["bash",  script_dir + "/snp_annotate.sh", input_file_path, snp_path, ref, tmp_path, prefix])
    input_file_path = tmp_path + "/" + prefix + ".vcf"
    #Excelに変換
    excel_converter.excel_convert(input_file_path,tmp_path,prefix)
    input_file_path = tmp_path + "/" + prefix + ".xlsx"

print("#END snpEff get seq")

#excel_import
import excel_process
excel_process_class = excel_process.ExcelProcess(input_file_path,output_dir,prefix)
infoList = excel_process_class.colAquire('INFO','col')
colLen = excel_process_class.colLenAquire()
proveanPredCol = excel_process_class.proveanPredCol

print("#END get INFO")

#compute
import compute
for i in range(0,colLen):
    print(i+1)
    if  infoList[i] == "text:'INFO'" or infoList[i] == "empty:''" or 'text' in proveanPredCol[i]:
        print('Already exists')
        continue
    else:
        print("compute.Compute: ",infoList[i],i,script_dir,snp_path,ref,tool_path,prefix,tmp_path)
        compute_class = compute.Compute(infoList[i],i,script_dir,snp_path,ref,tool_path,prefix,tmp_path)
        result = compute_class.run()
        excel_process_class.writeExcel(result, i)

print("#END compute")

import vcf_converter
if "vcf" in etx: 
    vcf_converter.vcf_converter(output_dir,prefix)

#vcf_converter.vcf_converter(output_dir,prefix)
