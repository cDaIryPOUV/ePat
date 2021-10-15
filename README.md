# ePat

ePat (extended PROVEAN annotation tool) is a software tool that extends the functionality of PROVEAN: a software tool for predicting whether amino acid substitutions and indels will affect the biological function of proteins.

ePat extends the conventional PROVEAN to enable the following two things.

1. To calculate the damage level of indel mutations with frameshift and mutations near splice junctions, for which the conventional PROVEAN could not calculate the damage level of these mutations.
2. Batch processing is used to calculate the damage level of multiple mutations in a mutation list (VCF file) in a single step.


In order to identify variants that are predicted to be functionally important from the mutation list, ePat can help filter out variants that affect biological functions by utilizing not only point mutation, and indel mutation that does not cause frameshift, but also frameshift, stop gain, and splice variant.

![スライド3](https://user-images.githubusercontent.com/85722434/137428088-8cf13c2d-6bde-4b63-9888-aa5d48fdd899.JPG)

# System Requirements

## Supported Distribution
- Ubuntu：Ubuntu20.04
- CentOS：CentOS7

## Memory
- 10024MB or above

## Singularity version
- Singularity 3.3.0 or above

# Installation

Download from Zenodo and unzip 

```
wget https://zenodo.org/record/5482094/files/ePat.zip 
```

 then

```
unzip ePat.zip
```

# Usage

1. Create a working directory `(YOUR_WORKDIR)` and place a VCF file for input `(YOUR_INPUTFILE)`, a FASTA file for reference genome `(YOUR_REF_GENOME)`, and a GTF file for annotation `(YOUR_REF_ANNO)` in `YOUR_WORKDIR`.  (HG38 is given as the default reference.)
2. Move to YOUR_WORKDIR. 
``` 
cd (YOUR_WORKDIR)  
```
3. Check current directory (Use this output as `WORKDIR`)
```
export WORKDIR=$PWD 
```
4. Prepare a directory to generate the intermediate files `(YOUR_TMPDIR)`.
5. Move to YOUR_TMPDIR.  
``` 
cd (YOUR_TMPDIR)  
```
6. Check current directory (Use this output as `TMPDIR`)
```
export TMPDIR=$PWD 
```
7. Move to YOUR_WORKDIR.  
``` 
cd $WORKDIR  
```
8. Execute the following command.
```
singularity run -B $WORKDIR:$WORKDIR -B $TMPDIR:/root/tmp -W $WORKDIR (PATH_TO_ePat.sif)/ePat.sif /root/script/automated_provean.sh -i (YOUR_INPUTFILE) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
```

9. After the analysis is finished, `(YOUR_WORKDIR)/output/output_provean_(PREFIX_OF_YOUR_INPUTFILE).txt` will be output as the output file.
10. The 'PROVEAN_score' column shows the effect of the mutation on the protein function, and the 'PROVEAN_pred' column shows whether the mutation is harmful or not.

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
singularity run -B $PATH_TO_EPAT/ePat/test_data:$PATH_TO_EPAT/ePat/test_data -B $PATH_TO_EPAT/ePat/tmp:/root/tmp -W $PATH_TO_EPAT/ePat/test_data $PATH_TO_EPAT/ePat/ePat.sif /root/script/automated_provean.sh -i input.vcf -f tmp.fa -g genes.gtf
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

# Detail

## Input File

The input data is a VCF file after variant calling, a FASTA file of the reference genome, and a GTF file with gene annotations.

## SnpEff Annotation

Using the given reference, we create a database for SnpEff and annotate with SnpEff. We then extract mutations that have a `HIGH` or `MODERATE` mutation hazard level as a result of the SnpEff annotation.

## Extract Variant Info

For each row of the VCF file, extract the information of the mutation annotated with SnpEff `([gene ID, mutation type, SnpEff annotated harmfulness, base mutation, amino acid mutation])` from the `INFO` column. From this information, the mutations are classified into (1) variants near the splice junction(`splice variants`), (2) `frameshift`, (3) `Stop Gain`, (4) `Start Lost`, and (5) `inframe variants` (point Mutation or indel mutations that do not cause frameshift).

## Calculate damage level score

Variants from (1) to (4) are given a damage level score as defined by ePat, and those (5) will be gived a damage level score by PROVEAN.
The damage level score defined by ePat is calculated with the following method.

For each position, calculate the damage level score when it is replaced by each of the 20 amino acids. The average of these damage level score is used as the damage level score for that position.
The maximum damage level score for each position is the damage level score of this mutation.

### 1. Mutations near splice junctions
Calculate the damage level score defined by ePat in the range from the splice junction where the mutation occurs to the stop codon.

Mutations that are annotated as `sequence_feature` (due to a bug in SnpEff that annotates the damage level as `HIGH`) and mutations that occur in introns after the stop codon are not given the damage level.

### 2. Frameshift
Damage score defined by ePat is calculated in the range from the amino acid where the frameshift starts to the stop codon.

### 3. Stop Gain
Calculate the damage level score defined by ePat in the range from the amino acid to be replaced by the stop codon to the original stop codon.

For `Stop Lost`, the damage level score is not calculated.

### 4. Start Lost
Calculate the damage score defined by ePat in the range from the original start codon to the next methionine.

### 5. Inframe Variant
Calculate the damage score by PROVEAN.

## Output Format

Assign these scores to the `PROVEAN_score` column, and assign `D` (Damaged) if the score is less than -2.5, or `N` (Neutral) if the score is greater than -2.5 to the `PROVEAN_pred` column.

The output is output as `output_provean_{PREFIX_OF_YOUR_INPUTFILE}.txt` and saved in the output directory.
