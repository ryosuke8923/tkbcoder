# tkbcoder

# 主要なファイル概要

### app/static
・cssファイル，jsファイルが管理されている

### app/templates
・htmlファイルが管理されている

### index.html
・トップページ
### after_upload.html
・トップページからファイルをアップロードした際に遷移するページ
### result.html
・初回の操作（文章選択＆理由記述→送信）後に遷移するページ
・右側にサイドバーが表示されており，システム側からの情報を提示する場所（？）
（現在は特に何の処理も行っておらず，操作の確認のためユーザが選択した文章がそのまま表示されるようになっている．確認の意も込めて）
### history.html
・ユーザの投稿履歴を表示するページ
・今後必要になるかどうかはわからないが，現時点では置いてある．
### app/app.py
・バックエンドでの処理もろもろ
 
# Requirement
 
requirement.txtを参照してください
 
# Installation
 
```bash
pip install Flask==2.1.1
```
 
# Usage

基本的な流れ
 
```bash
git clone git@github.com:ryosuke8923/tkbcoder.git
cd tkbcoder
python run.py
```
run.pyを起動することでwebサーバが立ち上がるので，http://127.0.0.1:5000 にアクセスしてください

# Note
いくつか使用上での注意があるのでご確認ください．

・トップページでアンケートデータをupする必要がありますが，現段階ではそのファイルは自身のローカルにフォルダを自動で作ってそこに保存しています．
その際にpathの指定が必要となるため，app.py上部にある変数my_pathの値を変更してください．(~/app/まで)  
・ブラウザはSafariが良いかと思うのですが，いまいち動作が重いことがあります．(自分だけかも知れません)  
もし操作的な面を簡単に試したい場合は，Chromeで開いていただくとサクサクできると思います．（UIが崩れてしまう部分もあるのですが．．．）  
・画面上部にアイコンを3つ設定してあります．Homeアイコンはトップページに戻る機能に加えて，現状ではアップロードしたファイル等の保存データを全て初期化するように設定してあるのでお気をつけください．historyアイコンはhistory.htmlへの遷移，analysisアイコンはresult.htmlへ遷移します．  

# 照山研との実験用
https://github.com/ryosuke8923/tkbcoder_experiment

# Other
その他何かありましたらまたご連絡ください．
