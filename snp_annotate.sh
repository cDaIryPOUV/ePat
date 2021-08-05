input_file_path=$1
snp_path=$2
ref=$3
tmp_path=$4

java -jar ${snp_path} ${ref} ${input_file_path} > ${tmp_path}/${prefix}.vcf