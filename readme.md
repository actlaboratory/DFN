# 読ターFor NVDA Ver1.1.5 説明書

(更新:  2025-02-24)


## 目次

1. 読ター For NVDA について
2. 公開場所について
3. 動作環境
4. インストール方法
5. 使い方
6. 著作権
7. ご寄付・ご協力のお願い
8. 更新履歴
9. 問い合わせ先


## 1. 読ター For NVDA について

### 概要

読ター For NVDA (DFN) は、NVDA向け理療科用読み辞書プログラムです。
本プログラムをお手元のNVDAにインストールすることにより、通常では読み上げが困難な理療科専門用語の読み上げが可能になります。

### 特徴

* 理療科用読み辞書の適用状態を切り替えながら利用可能<br>
    理療科専門用語には、特定の漢字に対して特殊な読み方をさせる用語が多数あり、理療科用読み辞書を適用した状態では、通常の作業に影響が出てしまいます。
    本プログラムでは、この読み辞書の適用状態を切り替えながら利用できるので、そのような心配はありません。
* 利用者が登録した読み辞書を常に利用<br>
    本プログラムでは、利用者が登録した人名や地名などといった読み辞書は、優先的に使用されるようになっています。
    具体的には、NVDAに搭載されている３つの読み上げ辞書（既定の辞書、音声辞書、一時辞書）が、理療科用読み辞書に優先して使用されます。<br>
    これにより、理療科用読み辞書のために、利用者が再度読み辞書登録をやり直す必要がありません。
    なお、理療科用読み辞書は、誤って編集したり、操作が複雑化したりすることを防ぐため、編集できないようになっています。

### 理療科用読み辞書「読ター」について

読ターは、日本理療科教員連盟の成果物である、理療科用読み辞書です。
本読み辞書は、今後の教科書のデジタル化や電子書籍の利用を推進する目的で、スクリーンリーダーなどの読み上げ機能において、理療に関する専門用語を正しく読み上げさせるために、開発されたものです。

### NVDAについて

NonVisual Desktop Access (NVDA) は、Microsoft Windows用の無料でオープンソースのスクリーンリーダーです。
NVDAによって視覚障害者は、合成音声や点字を利用して、Windowsコンピューターを晴眼者と同じコストで使えるようになります。
NVDAは、コミュニティーの援助によりNV Accessが開発しました。<br>
NVDA日本語版はNVDA日本語チームが NV Access の成果を利用して開発したものです。

### NVDAアドオンについて

NVDAには、アドオンと呼ばれる、利用者が機能を追加できる仕組みが取り入れられています。
読ター For NVDA も、このアドオンのうちの一つです。<br>
ですから、以下、読ター For NVDA のことも、本アドオンなどと表記します。

### 読ター For NVDAのご利用に当たって

本アドオンは、日本理療科教員連盟の成果物である理療科用読み辞書を、NVDA利用者が容易に使用できるようにしたものです。

なお、読ター For NVDA は無保証です。ご自身の責任の下でご利用ください。

## 2. 公開場所について

本アドオンは、以下のページにて公開しております。
最新版のアドオンとともに、更新内容なども案内しておりますのでご確認ください。

* 読ター For NVDA のページ: <a href="https://actlab.org/software/DFN">https://actlab.org/software/DFN</a>

## 3. 動作環境

本アドオンを利用するには、以下の環境が必要です。

* NVDA 2019.3jp以降
* NVDAプログラムと同じドライブに、10MB以上の空き容量
* その他、Windows、およびNVDAが快適に動作する環境

なお、本アドオンは、日本語環境で利用されるNVDA日本語版を対象としています。


## 4. インストール方法

### NVDAがインストールされている場合

1. インストールされているNVDAを起動します。
2. dfn.nvda-addon を開きます。
3. アドオンをインストール、または更新するかどうかの確認が求められるので、「はい(Y)」を選択します。
4. NVDAの再起動が要求されるので、これに従い、NVDAを再起動します。

### ポータブル版のNVDAをご利用の場合、または、上記手順が実行できない場合

1. 本アドオンをご利用予定のポータブル版NVDA、またはインストールされているNVDAを起動します。
2. NVDAメニュー ([NVDA] + N) を開き、「ツール(T)」から、「アドオンマネージャー(A)」を開きます。
3. 「インストール(I)」ボタンを選択し、「アドオン パッケージ ファイルを選択」ダイアログを表示します。
4. 開いたダイアログ内で、dfn.nvda-addon を探して開きます。
5. アドオンをインストール、または更新するかどうかの確認が求められるので、「はい(Y)」を選択します。
6. インストール作業が終わったのち、「閉じる(C)」を選択して、アドオンマネージャーを閉じます。
7. NVDAの再起動が要求されるので、これに従い、NVDAを再起動します。

## 5. 使い方

### 理療科用読み辞書の適用状態を切り替える

理療科用読み辞書の適用状態を切り替えるには、次のいずれかの操作を行います。

* [NVDA] + [Ctrl] + [Shift] + Dを押す
* NVDAメニューから「読ター For NVDA」を選択し、「理療科用読み辞書を適用する」または「理療科用読み辞書を解除する」を実行

切り替え時には、切り替え方向と処理状況を、以下のようにビープ音と音声でお知らせします。

* 音声
    * 通常状態から理療科用読み辞書を適用した: 理療科用読み辞書使用中
    * 理療科用読み辞書適用中から通常状態へ戻した: 理療科用読み辞書解除
* ビープ音
    * 理療科用読み辞書の適用処理を開始した: ピ
    * 処理完了: ピピ

なお、NVDA起動直後の理療科用読み辞書の適用状態は、以下の方法で切り替えることができます。
NVDA起動直後に理療科用読み辞書が適用される場合は、上記のうち、処理開始をお知らせするビープ音はなりません。

* NVDAメニューから「読ター For NVDA」を選択し、「起動時の理療科用読み辞書の適用を有効化」または「起動時の理療科用読み辞書の適用を無効化」を実行

### アップデートの確認と実行

本アドオンは、読み辞書や機能の更新、および不具合の修正などのため、アップデートが提供されることがあります。
アドオンのアップデートは、NVDAメニューから「読ター For NVDA」を選択し、「アップデートの確認」を実行することでいつでも確認することができます。
アップデートが見つかると、更新を促すメッセージが表示されます。案内に従ってアップデート作業を行ってください。

また、本アドオンには、NVDA起動時に自動でアップデートを確認する機能が搭載されています。
NVDAメニューから「読ター For NVDA」を選択し、「起動時のアップデートの確認を無効化」あるいは「起動時のアップデートの確認を有効化」を実行することで設定を変更できます。

## 6. 著作権

(c) 2021 Hiroki Fujii - ACT Laboratory

GNU General Public License, version 2 or later. (一部を除く)

* URL: <a href="https://actlab.org/">https://actlab.org/</a>

ただし、以下については、日本理療科教員連盟が権利を保有しており、無断での複製、改変はできません。

* riryou_dict.dat (理療科用読み辞書)


## 7. ご寄付・ご協力のお願い

ACT Laboratory(Accessible Tools Laboratory)は、プログラミングを学ぶ視覚障害者の集まりです。<br>
本アドオンは無償ですが、公開には多少の経費も掛かっています。

本アドオンを気に入っていただけた方などで、活動にご支援・ご協力を頂ける方がいらっしゃいましたら、ぜひお力をお貸しください。
なお、ご支援を頂きました方につきましては、TwitterやACT Laboratoryサイトにてご紹介させて頂く予定です。

詳しくはこちらへ<br>
<a href="https://actlab.org/donate/">https://actlab.org/donate/</a>


## 8. 更新履歴

* 1.1.5 (2025/02/24)
    * NVDA 2025.1に対応

* 1.1.4 (2024/01/21)
    * NVDA 2024.1に対応

* 1.1.3 (2023/03/06)
    * NVDA 2023.1に対応

* 1.1.2 (2022/09/23)
    * 一部環境で、長い単語を正常に読み上げられないことがあった問題を修正
    * NVDAメニューの表示を「読ター For NVDA」に変更
    * 処理状況の通知方法を改善

* 1.1.1 (2022/05/20)
    * 本家の読み辞書更新(1.21)を適用

* 1.1.0 (2022/05/03)
    * NVDA 2022.1に対応
    * アップデーターを搭載
    * NVDAメニューからの操作に対応
    * NVDA起動時の読み辞書の状態を切り替える設定を追加


## 9. 問い合わせ先

本アドオンを利用しての感想やご要望、不具合のご報告などは、以下のメールアドレスまたは掲示板へご連絡ください。

* ACT Laboratory サポート: support@actlab.org
* ACT Laboratory 掲示板: <a href="https://actlab.org/bbs/">https://actlab.org/bbs/</a>

理療科読み辞書に関しては、以下までご連絡ください。

* 日本理療科教員連盟: yomijisho@rikyouren.com
