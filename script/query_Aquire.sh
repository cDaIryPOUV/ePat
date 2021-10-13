if [ -f $2/$1.fasta ]; then
  :
else
  echo '>'$1 > $2/$1.fasta
  java -jar $3 show -nodownload $4 $1 |grep Protein|tail -n -1|cut -f 4 >>$2/$1.fasta
fi  

cat $2/$1.fasta|tail -n 1