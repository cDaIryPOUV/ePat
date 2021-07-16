#!/bin/bash
script_dir=`dirname $0`
#default reference is hg38
ref=hg38

#change after build
snp_path=/root/snpEff
tool_path=/root/provean-1.1.5/bin/provean.sh
python_path=/root/anaconda3/bin/python3
tmp_dir=/root/tmp/

while getopts ":i:r:f:g:" OPT ; do
    case $OPT in
        i) input_file=$OPTARG 
            mkdir  ${input_file}_dir
            mkdir  ${input_file}_dir/output
            output_dir=${input_file}_dir/output/ ;;
        r) ref=$OPTARG ;; #only hg19 and hg38 is allowed
        f) fasta_path=$OPTARG ;;
        g) gtf_path=$OPTARG 
            if [ -e ${fasta_path} ]; then
                if [ -e ${gtf_path} ]; then
                    cp -r ${snp_path} ${input_file}_dir
                    snp_path=${input_file}_dir/snpEff
                    cp ${fasta_path} ${snp_path}/data/genomes/tmp.fa
                    cp ${gtf_path} ${snp_path}/data/tmp/genes.gtf
                    echo "tmp.genome : tmp" >> ${snp_path}/snpEff.config
                    java -jar ${snp_path}/snpEff.jar build -gtf22 -v tmp
                    ref=tmp
                else
                    echo "No such gtf file."
                fi
            else
                echo "No such fasta file."
            fi ;;
    esac
done

echo $ref

if [ -e ${input_file} ]; then
    ${python_path} ${script_dir}/main.py ${script_dir} ${input_file} ${output_dir} ${snp_path}/snpEff.jar ${ref} ${tool_path} ${tmp_dir}
else
    echo "No such input file"
fi
