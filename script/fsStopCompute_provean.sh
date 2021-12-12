set -x

provean_tmp_dir=/root/snpEff/provean_tmp

id=`echo $1|sed 's/[.][0-9]\+//'`
tmpDir=$2
toolPath=$3
excelName=$4

if [ -f ${tmpDir}/${id}.sss ]; then
  ${toolPath} -q ${tmpDir}/${id}.fasta -v ${tmpDir}/${excelName}.var --supporting_set ${tmpDir}/${id}.sss |sed -n '/# VARIATION/,$p'|tail -n +2| cut -f 2 
else
 if [ -f $provean_tmp_dir/${id}.sss ]; then
  cp $provean_tmp_dir/${id}.sss ${tmpDir}/${id}.sss
  ${toolPath} -q ${tmpDir}/${id}.fasta -v ${tmpDir}/${excelName}.var --supporting_set ${tmpDir}/${id}.sss |cut -f 2|tail -n 1
 else    
  ${toolPath} --num_threads 8 -q ${tmpDir}/${id}.fasta -v ${tmpDir}/${excelName}.var --save_supporting_set ${tmpDir}/${id}.sss |sed -n '/# VARIATION/,$p'|tail -n +2| cut -f 2 
 fi
fi

if [ ! -f $provean_tmp_dir/${id}.sss ]; then
 mkdir -p $provean_tmp_dir
 cp ${tmpDir}/${id}.sss ${tmpDir}/${id}.fasta $provean_tmp_dir
fi


rm ${tmpDir}/${excelName}.var
