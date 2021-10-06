# ePat

ePat (extended PROVEAN annotation tool) is a software tool that extends the functionality of PROVEAN: a software tool for predicting whether amino acid substitutions and indels will affect the biological function of proteins.

ePat extends the conventional PROVEAN to enable the following two things.

1. To calculate the damage level of indel mutations with frameshift and mutations near splice junctions, for which the conventional PROVEAN could not calculate the damage level of these mutations.
2. Batch processing is used to calculate the damage level of multiple mutations in a mutation list (VCF file) in a single step.


In order to identify variants that are predicted to be functionally important from the mutation list, ePat can help filter out variants that affect biological functions by utilizing not only point mutation, and indel mutation that does not cause frameshift, but also frameshift, stop gain, and splice variant.

![ePat説明図](https://user-images.githubusercontent.com/85722434/136146389-c82a8176-da15-4873-9ebc-01b2f4d06591.png)

# System Requirements

## Kernel version
- Ubuntu：Ubuntu2004 or above
- CentOS：CentOS7 or above

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
2. Prepare a directory to generate the intermediate files `(YOUR_TMPDIR)`.
3. Move to YOUR_WORKDIR.  ``` cd (YOUR_WORKDIR)  ```

4. Execute the following command.
```
singularity run -B (YOUR_WORKDIR):(YOUR_WORKDIR) -B (YOUR_TMPDIR):/root/tmp -W (YOUR_WORKDIR) (PATH_TO_ePat.sif)/ePat.sif /root/script/automated_provean.sh -i (YOUR_InputFile) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
```

5. After the analysis is finished, `(YOUR_WORKDIR)/output/output_provean_(Prefix of YOUR_InputFile).txt` will be output as the output file.
6. The 'PROVEAN_score' column shows the effect of the mutation on the protein function, and the 'PROVEAN_pred' column shows whether the mutation is harmful or not.

![ePat結果](https://user-images.githubusercontent.com/85722434/136148112-9e8d24e6-7d15-49a4-83ed-222f3c764d06.png)

Detail

まずインプットデータとして、バリアントコール後のVCFファイルとリファレンスゲノムのFASTAファイルと遺伝子アノテーションが記載されたGTFファイルを与えます。

与えられたリファレンスを使って、SnpEffのデータベースを作成し、SnpEffによりアノテーションを付与します。その後にSnpEffのアノテーションを行った結果として、遺伝子の変異の有害度が"HIGH"、もしくは"MODERATE"となっている突然変異のみを抽出します。

抽出された遺伝子候補の各行に関して、INFO列からSnpEffでアノテーションされた突然変異の情報([遺伝子ID, 変異の種類, SnpEffでアノテーションされた有害度, 塩基の変異,アミノ酸変異])を抜き出す。この情報から変異を①スプライスジャンクション付近のバリアント、②フレームシフト、③Stop Gain、④Start Lost、⑤Inframeなバリアント(Point Mutationやフレームシフトを生じないIndel変異)に区別する。

①~④に関してはePatで定義した有害度スコアを付与する。⑤に関してはPROVEANによって有害度スコアを付与する。
ePatで定義した有害度スコアは以下の方法で算出する。
ある範囲のアミノ酸について、各ポジションで２０種類のアミノ酸への置換が起こった場合の有害度をそれぞれproveanを用いて算出し、その平均値を計算する。
ポジションの平均値について、全ポジションの中で最小値を計算し、これを有害度スコアとする。

①スプライスジャンクション付近の変異
変異が生じているスプライスジャンクション以降から停止コドンまでの範囲で、ePatで定義した有害度スコアを算出する。
sequence_featureとしてアノテーションされている変異(SnpEffのバグで有害度がHIGHとアノテーションされてしまうため)と、スプライスジャンクション付近の変異のうち停止コドンよりも後ろのイントロンで起こっている変異は有害度スコアを算出しない。

②フレームシフト
フレームシフトが開始しているアミノ酸から停止コドンまでの範囲で、ePatで定義した有害度スコアを算出する。

③Stop Gain
停止コドンに置換されるアミノ酸から元の停止コドンまでの範囲で、ePatで定義した有害度スコアを算出する。
Stop Lostに関しては、有害度スコアを算出しない。

④Start Lost
本来の開始コドンから次に現れるメチオニンまでの範囲で、ePatで定義した有害度スコアを算出する。

⑤Inframe Variant
PROVEANによって有害度スコアを算出

これらのスコアを'PROVEAN_score'列に付与し、このスコアが-2.5以下の場合はD(Damaged)、-2.5よりも大きい場合はN(Neutral)を'PROVEAN_pred'列に付与する。

出力は'output_provean_{元のvcfファイルのprefix}.txt'で出力され、outputディレクトリに保存される。
