set -x

provean_tmp_dir=/root/snpEff/provean_tmp

AAQUERY=`echo $1|sed 's/[.][0-9]\+//'`

if [ -f $2/$AAQUERY.fasta ]; then
  :
else
 if [ -f $provean_tmp_dir/$AAQUERY.fasta ]; then
  cp $provean_tmp_dir/$AAQUERY.fasta $2/$AAQUERY.fasta
 else
  echo '>'$AAQUERY > $2/$AAQUERY.fasta
  java -jar $3 show -nodownload $4 $AAQUERY |grep Protein|tail -n -1|cut -f 4|sed 's/[?]/X/g' >>$2/$AAQUERY.fasta
 fi
fi

cat $2/$AAQUERY.fasta|tail -n 1

