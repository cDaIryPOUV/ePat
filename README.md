# ePat

ePat(extended PROVEAN annotation tool)は、アミノ酸置換やインデルがタンパク質の生物学的機能に影響を与えるかどうかを予測するソフトウェアツール：PROVEANの機能を拡張したソフトウェアツールです。

ePatは、従来のPROVEANと異なり、以下の２つを可能にします。

①従来のPROVEANでは有害度を算出出来なかったフレームシフトを伴うindel変異、スプライスジャンクション近傍の変異に対しても有害度を算出する。
②バリアントコール後のvcfファイルに含まれる変異コールの中で特に有害なものに対して、一括で有害度を算出する。

ePatは、バリアントコール後のvcfファイルから機能的に重要であると予測されるバリアントを特定するために、生物学的機能に影響を及ぼすバリアントをフィルタリングするのに役立ちます。
