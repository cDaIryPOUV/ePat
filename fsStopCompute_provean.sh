id=$1
tmpDir=$2
toolPath=$3
excelName=$4

if [ -f ${tmpDir}/${id}.sss ]; then
  ${toolPath} -q ${tmpDir}/${id}.fasta -v ${tmpDir}/${excelName}.var --supporting_set ${tmpDir}/${id}.sss |sed -n '/# VARIATION/,$p'|tail -n +2| cut -f 2 
else    
  ${toolPath} -q ${tmpDir}/${id}.fasta -v ${tmpDir}/${excelName}.var --save_supporting_set ${tmpDir}/${id}.sss |sed -n '/# VARIATION/,$p'|tail -n +2| cut -f 2 
fi


rm ${tmpDir}/${excelName}.var
