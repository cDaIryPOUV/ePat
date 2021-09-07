# ePat

ePat(extended PROVEAN annotation tool)は、アミノ酸置換やインデルがタンパク質の生物学的機能に影響を与えるかどうかを予測するソフトウェアツール：PROVEANの機能を拡張したソフトウェアツールです。

ePatは、従来のPROVEANを拡張し、以下の２つを可能にします。

①従来のPROVEANでは有害度を算出出来なかったフレームシフトを伴うindel変異とスプライスジャンクション近傍の変異に対しても有害度を算出する。
②変異リスト(VCFファイル)に含まれる変異についてバッチ処理を行い、一括で有害度を算出する。

ePatは、変異リストから機能的に重要であると予測されるバリアントを特定するために、これまでは活用出来なかったフレームシフトの情報なども活用して、生物学的機能に影響を及ぼすバリアントをフィルタリングするのに役立ちます。

画像

System Requirements
・カーネルバージョン
・Singularityバージョン

Installation
・Zenodoから

Usage

①作業ディレクトリ(YOUR_WORKDIR)を作成し、作業ディレクトリ内にInputのVCFファイル(YOUR_InputFile)、リファレンスゲノムのFASTAファイル(YOUR_REF_GENOME)、アノテーションのGTFファイル(YOUR_REF_ANNO)を配置する。(Defaultのリファレンスとして、HG38が与えられています。)
②中間ファイルを生成するためのディレクトリ(YOUR_TMPDIR)を用意する。
③(YOUR_WORKDIR)に移動
④以下のコマンドを実行する。
singularity run  -B (YOUR_WORKDIR):(YOUR_WORKDIR) -B (YOUR_TMPDIR):/root/tmp -W (YOUR_WORKDIR) (PATH_TO_ePat.sif)/ePat.sif /root/script/automated_provean.sh -i (YOUR_InputFile) -f (YOUR_REF_GENOME) -g (YOUR_REF_ANNO)
⑤解析は終了したのち、(YOUR_WORKDIR)/output/output_provean_(YOUR_InputFilePrefix).txtがアウトプットファイルとして出力される。
⑥'PROVEAN_score'列にその変異がタンパク質機能に与える影響が記載され、'PROVEAN_pred'列にその変異が有害か否かが記載される。
・結果のスクリーンショット

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
