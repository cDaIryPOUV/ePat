#!/bin/bash
script_dir=`dirname $0`
ref=hg38

# mkdir  ${input_file}_dir
# mkdir  ${input_file}_dir/output
# mkdir  ${input_file}_dir/tmp

# output_dir=${input_file}_dir/output/
# tmp_dir=${input_file}_dir/tmp/

#change after build
snp_path=/root/snpEff
tool_path=/root/provean-1.1.5/bin/provean.sh
python_path=/root/anaconda3/bin/python3
tmp_dir=/root/tmp/
#tmp_dir=/home/tmp/


while getopts ":i:f:g:" OPT ; do
    case $OPT in
        i) input_file=$OPTARG 
            mkdir  ${input_file}_dir
            mkdir  ${input_file}_dir/output
            #mkdir  ${input_file}_dir/tmp
            output_dir=${input_file}_dir/output/ ;;
            #tmp_dir=${input_file}_dir/tmp/ ;;
        f) fasta_path=$OPTARG ;;
        g) gtf_path=$OPTARG 
            if [ -e ${fasta_path} ]; then
                if [ -e ${gtf_path} ]; then
                    # echo ${fasta_path}
                    # echo ${gtf_path}
                    cp -r ${snp_path} ${input_file}_dir
                    snp_path=${input_file}_dir/snpEff
                    cp ${fasta_path} ${snp_path}/data/genomes/tmp.fa
                    cp ${gtf_path} ${snp_path}/data/tmp/genes.gtf
                    echo "tmp.genome : tmp" >> ${snp_path}/snpEff.config
                    java -jar ${snp_path}/snpEff.jar build -gtf22 -v tmp
                    ref=tmp
                else
                    echo "No such gtf file. fasta is required to create snpEff DB other then hg38."
                fi
            else
                echo "No such fasta file. fasta is required to create snpEff DB other then hg38."
            fi ;;
    esac
done

echo $ref

if [ -e ${input_file} ]; then
    ${python_path} ${script_dir}/main.py ${script_dir} ${input_file} ${output_dir} ${snp_path}/snpEff.jar ${ref} ${tool_path} ${tmp_dir}
else
    echo "No such input file"
fi
