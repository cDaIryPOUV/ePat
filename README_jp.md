# ePat

ePat（extended PROVEAN annotation tool）は、アミノ酸置換やインデルがタンパク質の生物学的機能に影響を与えるかどうかを予測するソフトウェアツールであるPROVEANの機能を拡張したソフトウェアツールです。

ePatは、従来のPROVEANを拡張し、以下の2点を可能にしました。

1. 従来のPROVEANでは有害度を計算できなかったフレームシフトを伴うインデルの変異体やスプライスジャンクション近傍の変異体の有害度を計算できるようになりました。
2. バッチ処理により、変異リスト（VCFファイル）中の複数のバリアントの有害度を一度に計算します。


3.変異リストから機能的に重要と予測されるバリアントを同定するために、ePatはフレームシフトを起こさないミスセンスバリアントやインデルバリアントだけでなく、フレームシフト、ストップゲイン、スプライスのバリアントも活用し、生体機能に影響を与えるバリアントをフィルタリングすることが可能です。

![ePat画像](https://user-images.githubusercontent.com/85722434/138379432-078ebc17-247a-41a5-9fa4-77a023e582c0.jpg)


# System Requirements

## Supported Distribution
- Ubuntu：Ubuntu20.04
- CentOS：CentOS7

## Memory
- 10024MB or above

## Singularity version
- Singularity 3.3.0 or above

# Installation

ZenodoからSingularityイメージとテストデータのダウンロードを行う。

```
wget https://zenodo.org/record/5800418/files/ePat.zip
```

ダウンロードが完了したら、zipファイルの解凍を行う。

```
unzip ePat.zip
```

# Usage

1. 作業ディレクトリ `(YOUR_WORKDIR)` を作成し、入力用の VCF ファイル `(YOUR_INPUTFILE)` 、参照ゲノム用の FASTA ファイル `(YOUR_REF_GENOME)` 、アノテーション用の GTF ファイル `(YOUR_REF_ANNO)` を `YOUR_WORKDIR` 配下に配置する。 (デフォルトのリファレンスとして HG38 が指定されている)。
2. `YOUR_WORKDIR`に移動する. 
``` 
cd (YOUR_WORKDIR)  
```
3. カレントディレクトリの確認 (この出力を `WORKDIR` として使用する)
```
export WORKDIR=$PWD 
```
4. 中間ファイルを生成するためのディレクトリ `(YOUR_TMPDIR)` を用意する。
5. YOUR_TMPDIRに移動する。 
``` 
cd (YOUR_TMPDIR)  
```
6. カレントディレクトリのチェック (この出力を `TMPDIR` として使用する)
```
export TMPDIR=$PWD 
```
7. YOUR_WORKDIRに移動する。
``` 
cd $WORKDIR  
```
8. 以下のコマンドを実行する
```
singularity run -B $WORKDIR:$WORKDIR -B $TMPDIR:/root/tmp -W $WORKDIR (PATH_TO_ePat.sif)/ePat.sif /usr/local/ePat/script/automated_provean.sh -i (YOUR_INPUTFILE) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
```

9. 解析終了後、出力ファイルとして `(YOUR_WORKDIR)/output/output_provean_(PREFIX_OF_YOUR_INPUTFILE).txt` が出力される。
10. 「PROVEAN_score」列は変異がタンパク質の機能に与える影響を示し、「PROVEAN_pred」列は変異が有害であるか否かを示す。

![ePat結果](https://user-images.githubusercontent.com/85722434/136148112-9e8d24e6-7d15-49a4-83ed-222f3c764d06.png)

## Use Test Data

Download from Zenodo and unzip. (Use `ePat/test_data` directry as `YOUR_WORKDIR`)

```
wget https://zenodo.org/record/5482094/files/ePat.zip 
```

```
unzip ePat.zip
```

Make `YOUR_TMPDIR`

```
mkdir ePat/tmp
```

Check current directory (Use this output as `PATH_TO_EPAT`)

```
export PATH_TO_EPAT=$PWD 
```

Move to `YOUR_WORKDIR`

```
cd ePat/test_data
```

Run ePat

```
singularity run -B $PATH_TO_EPAT/ePat/test_data:$PATH_TO_EPAT/ePat/test_data -B $PATH_TO_EPAT/ePat/tmp:/root/tmp -W $PATH_TO_EPAT/ePat/test_data $PATH_TO_EPAT/ePat/ePat.sif /usr/local/ePat/script/automated_provean.sh -i input.vcf -f tmp.fa -g genes.gtf
```

Check Result

```
cat $PATH_TO_EPAT/ePat/test_data/input.vcf_dir/output/output_provean_input.txt
```

```
#CHROM  POS       ID           REF  ALT  QUAL   FILTER  INFO                                                                                                                                                                                                                                                                  FORMAT  HG00096  PROVEAN_pred  PROVEAN_score
22      24698294  rs202142165  C    G    100.0  PASS    AC=1;AF=0.000199681;AN=5008;NS=2504;DP=18536;EAS_AF=0;AMR_AF=0;AFR_AF=0.0008;EUR_AF=0;SAS_AF=0;AA=C|||;VT=SNP;EX_TARGET;ANN=G|missense_variant|MODERATE|SPECC1L|SPECC1L|transcript|NM_015330|protein_coding|3/17|c.95C>G|p.Ser32Cys|389/6763|95/3354|32/1117||        GT      0|0      N             -1.005
22      24709317  rs548017612  G    A    100.0  PASS    AC=1;AF=0.000199681;AN=5008;NS=2504;DP=20098;EAS_AF=0;AMR_AF=0;AFR_AF=0;EUR_AF=0;SAS_AF=0.001;AA=G|||;VT=SNP;EX_TARGET;ANN=A|missense_variant|MODERATE|SPECC1L|SPECC1L|transcript|NM_015330|protein_coding|4/17|c.190G>A|p.Gly64Arg|484/6763|190/3354|64/1117||       GT      0|0      N             -2.165
22      24709321  rs569594248  G    C    100.0  PASS    AC=1;AF=0.000199681;AN=5008;NS=2504;DP=19830;EAS_AF=0;AMR_AF=0;AFR_AF=0;EUR_AF=0.001;SAS_AF=0;AA=G|||;VT=SNP;EX_TARGET;ANN=C|missense_variant|MODERATE|SPECC1L|SPECC1L|transcript|NM_015330|protein_coding|4/17|c.194G>C|p.Gly65Ala|488/6763|194/3354|65/1117||       GT      0|0      N             -0.881
22      24709420  rs35783914   C    T    100.0  PASS    AC=4;AF=0.000798722;AN=5008;NS=2504;DP=19262;EAS_AF=0;AMR_AF=0.0014;AFR_AF=0;EUR_AF=0.003;SAS_AF=0;AA=C|||;VT=SNP;EX_TARGET;ANN=T|missense_variant|MODERATE|SPECC1L|SPECC1L|transcript|NM_015330|protein_coding|4/17|c.293C>T|p.Ser98Phe|587/6763|293/3354|98/1117||  GT      0|0      N             -1.051
22      24709423  rs371780453  A    G    100.0  PASS    AC=1;AF=0.000199681;AN=5008;NS=2504;DP=19367;EAS_AF=0;AMR_AF=0;AFR_AF=0;EUR_AF=0;SAS_AF=0.001;AA=A|||;VT=SNP;EX_TARGET;ANN=G|missense_variant|MODERATE|SPECC1L|SPECC1L|transcript|NM_015330|protein_coding|4/17|c.296A>G|p.Lys99Arg|590/6763|296/3354|99/1117||       GT      0|0      N             -0.388

```

## Advanced usage

If you want to share a database built with snpEff or sss files aligned with provean to ```SHARED_DIR```.　The following commands can be run after the above command using the options "-f" and "-g" has been executed.

```
### Change follows to fit your environment. ###
i=input.vcf
SHARED_DIR=$PATH_TO_EPAT/ePat/test_data/input.vcf_dir/snpEff
WORK_DIR=$PATH_TO_EPAT/ePat/test_data
TMP_DIR=/tmp/$i
###############################################
mkdir -p $TMP_DIR 
singularity run -B $TMP_DIR:/root/tmp -B $SHARED_DIR:/root/snpEff -B $WORK_DIR:$WORK_DIR -W $WORK_DIR $PATH_TO_EPAT/ePat/ePat.sif /usr/local/ePat/script/automated_provean.sh -i $i -r tmp
rm -rf $TMP_DIR
```

# Detail

## Input File

The input data is a VCF file after variant call, a FASTA file of the reference genome, and a GTF file with gene annotations.

## SnpEff Annotation

With given reference, we create a database for SnpEff and annotate the VCF file with SnpEff. We then extract variants that have a `HIGH` or `MODERATE` pathogenicity level as a result of the SnpEff annotation.

## Extract Variant Info

For each row of the VCF file, extract the information of the variants annotated with SnpEff `([gene ID, variant type, pathogenicity level, DNA mutation information, amino acid mutation information])` from the `INFO` column. With this information, the variants are classified into (1) variants near the splice junction(`splice variants`), (2) `frameshift`, (3) `Stop Gain`, (4) `Start Lost`, and (5) `inframe variants` (point Mutation or indel mutations that do not cause frameshift).

## Calculate pathogenicity

Variants from (1) to (4) are given pathogenicity as defined by ePat, and those (5) will be given pathogenicity by PROVEAN.
The pathogenicity defined by ePat is calculated with the following method.

For each position, calculate the pathogenicity when it is replaced by each of the 20 amino acids. The average of these pathogenicity is used as the pathogenicity for that position.
The maximum pathogenicity for each position is the pathogenicity of this mutation.

### 1. Mutations near splice junctions
Calculate the pathogenicity defined by ePat in the range from the splice junction where the mutation occurs to the stop codon.

variants annotated as `sequence_feature` (due to a bug in SnpEff that annotates the pathogenicity as `HIGH`) and variants occuring in introns after the stop codon are not given the pathogenicity.

### 2. Frameshift
Pathogenicity defined by ePat is calculated in the range from the amino acid where the frameshift starts to the stop codon.

### 3. Stop Gain
Calculate the pathogenicity defined by ePat in the range from the amino acid to be replaced by the stop codon to the original stop codon.

For `Stop Lost`, the pathogenicity is not calculated.

### 4. Start Lost
Calculate the pathogenicity defined by ePat in the range from the original start codon to the next methionine.

### 5. Inframe Variant
Calculate the pathogenicity by PROVEAN.

## Output Format

Assign these scores to the `PROVEAN_score` column, and assign `D` (Damaged) if the score is less than -2.5, or `N` (Neutral) if the score is greater than -2.5 to the `PROVEAN_pred` column.

The output is output as `output_provean_{PREFIX_OF_YOUR_INPUTFILE}.txt` and saved in the output directory.

