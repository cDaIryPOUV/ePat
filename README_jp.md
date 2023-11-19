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

ZenodoからSingularityイメージとテストデータのダウンロードを行います。

```
wget https://zenodo.org/record/5800418/files/ePat.zip
```

ダウンロードが完了したら、zipファイルの解凍を行います。

```
unzip ePat.zip
```

# Usage

1. 作業ディレクトリ `(YOUR_WORKDIR)` を作成し、入力用の VCF ファイル `(YOUR_INPUTFILE)` 、参照ゲノム用の FASTA ファイル `(YOUR_REF_GENOME)` 、アノテーション用の GTF ファイル `(YOUR_REF_ANNO)` を `YOUR_WORKDIR` 配下に配置します。 (デフォルトのリファレンスとして HG38 が指定されています)。リファレンスを自身で用意する場合は https://asia.ensembl.org/index.html などからダウンロードできます。（Ensemblはゲノム解読された真核生物を対象として自動アノテーションを行い、その結果をデータベースとして公開しています）またバンドウイルカ(Tursiop truncatus)のリファレンス(FASTA: http://ftp.ensembl.org/pub/release-105/fasta/tursiops_truncatus/dna/Tursiops_truncatus.turTru1.dna.toplevel.fa.gz ,GTF: http://ftp.ensembl.org/pub/release-105/gtf/tursiops_truncatus/Tursiops_truncatus.turTru1.105.gtf.gz )ではリファレンスの改変などは特に不要でしたが、リファレンスによってはSnpEffとの互換性を保つためにGTFファイル修正を直接行う必要があります。
2. `YOUR_WORKDIR`に移動します. 
``` 
cd (YOUR_WORKDIR)  
```
3. カレントディレクトリの確認 (この出力を `WORKDIR` として使用します)
```
export WORKDIR=$PWD 
```
4. 中間ファイルを生成するためのディレクトリ `(YOUR_TMPDIR)` を用意します。
5. YOUR_TMPDIRに移動します。 
``` 
cd (YOUR_TMPDIR)  
```
6. カレントディレクトリのチェック (この出力を `TMPDIR` として使用します)
```
export TMPDIR=$PWD 
```
7. YOUR_WORKDIRに移動します。
``` 
cd $WORKDIR  
```
8. 以下のコマンドを実行してください
```
singularity run -B $WORKDIR:$WORKDIR -B $TMPDIR:/root/tmp -W $WORKDIR (PATH_TO_ePat.sif)/ePat.sif /usr/local/ePat/script/automated_provean.sh -i (YOUR_INPUTFILE) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
```

dockerを使うなら下記のコマンド
```
docker run -i --rm -v $WORKDIR:$WORKDIR -v $TMPDIR:/root/tmp -w $WORKDIR c2997108/epat:2 /usr/local/ePat/script/automated_provean.sh -i (YOUR_INPUTFILE) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
```

9. 解析終了後、出力ファイルとして `(YOUR_WORKDIR)/output/output_provean_(PREFIX_OF_YOUR_INPUTFILE).txt` が出力されます。
10. 「PROVEAN_score」列は変異がタンパク質の機能に与える影響を示し、「PROVEAN_pred」列は変異が有害であるか否かを示します。

![ePat結果](https://user-images.githubusercontent.com/85722434/136148112-9e8d24e6-7d15-49a4-83ed-222f3c764d06.png)

## Use Test Data

Zenodoからダウンロードし、解凍してください。(ePat/test_data` ディレクトリを `YOUR_WORKDIR` として使用します。）
```
wget https://zenodo.org/record/5482094/files/ePat.zip 
```

```
unzip ePat.zip
```

YOUR_TMPDIR`を作成します。

```
mkdir ePat/tmp
```

カレントディレクトリのチェック (この出力を `PATH_TO_EPAT` として使用します)

```
export PATH_TO_EPAT=$PWD 
```

YOUR_WORKDIR`に移動します。

```
cd ePat/test_data
```

ePatを実行します

```
singularity run -B $PATH_TO_EPAT/ePat/test_data:$PATH_TO_EPAT/ePat/test_data -B $PATH_TO_EPAT/ePat/tmp:/root/tmp -W $PATH_TO_EPAT/ePat/test_data $PATH_TO_EPAT/ePat/ePat.sif /usr/local/ePat/script/automated_provean.sh -i input.vcf -f tmp.fa -g genes.gtf
```

結果を確認します。

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

snpEff で構築したデータベース、または provean で整列した sss ファイルを ``SHARED_DIR`` で共有したい場合は、上記のコマンドでオプション "-f" と "-g" を指定して、以下のコマンドを実行してください。

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

入力データは、バリアントコール後の VCF ファイル、参照ゲノムの FASTA ファイル、および遺伝子アノテーションの GTF ファイルです。

## SnpEff Annotation

与えられたリファレンスをもとに、SnpEffのデータベースを作成し、VCFファイルにSnpEffのアノテーションを付与します。SnpEffのアノテーションの結果、病原性が`HIGH`または`MODERATE`であるバリアントを抽出します。

## Extract Variant Info

VCFファイルの各行について、SnpEffでアノテーションしたvariantの情報`([遺伝子ID, variant type, pathogenicity level, DNA mutation information, amino acid mutation information])` を `INFO` カラムから抽出します。この情報をもとに、(1) スプライスジャンクション近傍の変異(`splice variants`), (2) `frameshift`, (3) `Stop Gain`, (4) `Start Lost`, (5) `inframe variants` (point Mutation or indel mutations that not cause frameshift) に分類されます。

## Calculate pathogenicity

（1）～（4）の変異体にはePatが定義する有害度が付与され、（5）の変異体にはPROVEANが定義する有害度が付与されることになります。
ePatで定義された有害度は、以下の方法で算出されます。

各ポジションのアミノ酸について、20種類のアミノ酸のそれぞれで置換した場合の有害度を計算する。これらの有害度の平均をそのポジションの有害度とします。
各ポジションの有害度の最大値を、この変異の有害度とします。

### 1. Mutations near splice junctions
変異が生じたスプライスジャンクションからストップコドンまでの範囲で、ePatで定義された有害度を計算します。

`sequence_feature` としてアノテーションされた変異体（SnpEff のバグで `HIGH` とアノテーションされているため）と、ストップコドン以降のイントロンに発生する変異体は有害度が与えられません。

### 2. Frameshift
ePatで定義される有害度は、フレームシフトが始まるアミノ酸からストップコドンまでの範囲で計算されます。

### 3. Stop Gain
停止コドンで置換されるアミノ酸から元の停止コドンまでの範囲で、ePatで定義される有害度を計算します。

`Stop Lost`の場合、有害度は計算されません。

### 4. Start Lost
元の開始コドンから次のメチオニンまでの範囲でePatで定義された有害度を計算します。

### 5. Inframe Variant
PROVEANで有害度を算出します。

## Output Format

これらのスコアを `PROVEAN_score` 列に代入し、スコアが -2.5 より小さい場合は `D` (Damaged) を、スコアが -2.5 より大きい場合は `N` (Neutral) を `PROVEAN_pred` 列に記載します。

出力は `output_provean_{PREFIX_OF_YOUR_INPUTFILE}.txt` として出力され、出力ディレクトリに格納されます。

