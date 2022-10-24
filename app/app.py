#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,Markup
from flask import request
from werkzeug.utils import secure_filename
import os 
import random
import ast
import shutil
import re
from . import sent_bert
# from . import code
######

my_path = '/Users/saitouryousuke/prog/python/tkbcoder/app/'

class System:

    def __init__(self):
        self.comment = {
            "few_code":"申し訳ありません．まだデータが少なくて分析できません．他の例も教えてください",
            "instraction":"""
            面白いと思ったフレーズの範囲を指定して，Enterで決定してください　　　　
            ハイライトをつけることができます　　　　　
            また，このチャットボックスにメモを残すことができます　　　　　　　　　　　　　　　　　　　　　
            """,
            "plz_reason":"どうして興味を持ったのか理由を書いて教えてください",
            "plz_other_example":"理由を教えてくれてありがとうございます．他の例も教えてください",
            "show_code_keyword":"コード名：{}　には＜{}＞という言葉も当てはまるかもしれません",
            "show_code_sentences":"こちらの文章もチェックしてみてはどうですか？(同じコードとして追加したい文章については,「$コード＋文章番号」を入力しよう)　　　　　　　　　　　　{}",
        }
    
    def register_code(self,code_name,index):
        pass

        
#分析者用クラス
class AnalystData:
    def __init__(self):
        self.reason2choice = {}
        self.reasons = []
        self.choice_texts = []
        self.chat_data = [["system",system.comment["instraction"]]]
        self.phrase_reason = []

    def add_reason(self,reason):
        self.reasons.append(reason)

    def add_choice_texts(self,texts):
        for text in texts:
            self.choice_texts.append(text)
        self.choice_texts = self.get_unique(self.choice_texts)
    
    def add_data(self,reason,texts):
        texts = list(map(lambda x:ast.literal_eval(x),texts))
        # print(texts)
        #キー：理由，値：選択した文章の辞書
        self.reason2choice[reason] = texts
        #理由のlist
        self.add_reason(reason)
        #選択した文章のlist
        self.add_choice_texts(texts)

    def get_unique(self,seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]

    def save(self):
        target_dir = my_path + "files/data.txt"
        with open(target_dir,"w") as f:
            for k,v in self.reason2choice.items():
                for vv in v:
                    f.write("選択文章：{}".format(vv["sentence"]))
                f.write("理由:{}\n".format(k))
                f.write("=================\n")



#インタビューデータ用クラス
class QuestionnaireData:
    def __init__(self,file_name=None,file_path=None,texts=None,):
        self.file_name = file_name
        self.file_path = file_path
        self.texts = texts
        self.html_data = None
    
    def make_html_data(self):
        html_data = []
        for i,k in enumerate(self.texts):
            html_data.append({"index":i,"sentence":k,"tag":[]})
        self.html_data = html_data

    def file_save(self,f):
        #とりあえずローカルディレクトリに保存
        f.save(self.file_path)

    def add_tag(self,index,tag):
        self.html_data[int(index)]["tag"].append(tag)


def make_dir(path):
    target_dir = path + "files"
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)
######


#Flaskオブジェクトの生成
app = Flask(__name__)

#オブジェクトの初期化
system = System()
questionnaire_data = QuestionnaireData()
analyst_data = AnalystData()
user_hiright = []
graph_obj = sent_bert.SentBert()
node2index = {
    "大学の運営に少なからず不自由な面がある":3,
    '永田学長が思う大学の役割':10,
    '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか':12,
    '日本人学生に対して':15,
    '若者に対する考え，少しは厳しい状況に身を置くべき':20,
    '筑波大学キーワード':2,
    '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）':4,
    'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている':6,
    '永田学長の学長ぞうを象徴する言葉':8,
    '教員に対する思い':10,
    '大学の在り方':5,
    '繰り返し言及している':6,
    '分野の壁がないこと→教養教育において大事な環境':8
}
graph = {
    "node":[
        {'data': {'id': '大学の運営に少なからず不自由な面がある',"label":"0"}},
        {'data': {'id': '永田学長が思う大学の役割',"label":"1"}},
        {'data': {'id': '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか',"label":"2"}},
        {'data': {'id': '日本人学生に対して',"label":"1"}},
        {'data': {'id': '若者に対する考え，少しは厳しい状況に身を置くべき',"label":"0"}},
        {'data': {'id': '筑波大学キーワード',"label":"1"}},
        {'data': {'id': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）',"label":"2"}},
        {'data': {'id': 'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている',"label":"1"}},
        {'data': {'id': '永田学長の学長ぞうを象徴する言葉',"label":"1"}},
        {'data': {'id': '教員に対する思い',"label":"0"}},
        {'data': {'id': '大学の在り方',"label":"1"}},
        {'data': {'id': '繰り返し言及している',"label":"1"}},
        {'data': {'id': '分野の壁がないこと→教養教育において大事な環境',"label":"0"}}
    ],
    "edge":[
    {"data":{'source': '大学の運営に少なからず不自由な面がある', 'target': '大学の在り方'}},
    {"data":{'source': '大学の運営に少なからず不自由な面がある', 'target': '分野の壁がないこと→教養教育において大事な環境'}},
    {"data":{'source': '大学の運営に少なからず不自由な面がある', 'target': '若者に対する考え，少しは厳しい状況に身を置くべき'}},
    {"data":{'source': '永田学長が思う大学の役割', 'target': '筑波大学キーワード'}},
    {"data":{'source': '永田学長が思う大学の役割', 'target': '永田学長の学長ぞうを象徴する言葉'}},
    {"data":{'source': '永田学長が思う大学の役割', 'target': '大学の在り方'}},
    {"data":{'source': '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか', 'target': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）'}},
    {"data":{'source': '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか', 'target': '若者に対する考え，少しは厳しい状況に身を置くべき'}},
    {"data":{'source': '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '日本人学生に対して', 'target': '筑波大学キーワード'}},
    {"data":{'source': '日本人学生に対して', 'target': '教員に対する思い'}},
    {"data":{'source': '日本人学生に対して', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '若者に対する考え，少しは厳しい状況に身を置くべき', 'target': '大学の運営に少なからず不自由な面がある'}},
    {"data":{'source': '若者に対する考え，少しは厳しい状況に身を置くべき', 'target': '分野の壁がないこと→教養教育において大事な環境'}},
    {"data":{'source': '若者に対する考え，少しは厳しい状況に身を置くべき', 'target': '教員に対する思い'}},
    {"data":{'source': '筑波大学キーワード', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '筑波大学キーワード', 'target': '永田学長の学長ぞうを象徴する言葉'}},
    {"data":{'source': '筑波大学キーワード', 'target': '日本人学生に対して'}},
    {"data":{'source': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）', 'target': '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか'}},
    {"data":{'source': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）', 'target': '教員に対する思い'}},
    {"data":{'source': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）', 'target': '繰り返し言及している'}},
    {"data":{'source': 'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている', 'target': '大学の在り方'}},
    {"data":{'source': 'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている', 'target': '大学の運営に少なからず不自由な面がある'}},
    {"data":{'source': 'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '永田学長の学長ぞうを象徴する言葉', 'target': '筑波大学キーワード'}},
    {"data":{'source': '永田学長の学長ぞうを象徴する言葉', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '永田学長の学長ぞうを象徴する言葉', 'target': '日本人学生に対して'}},
    {"data":{'source': '教員に対する思い', 'target': '日本人学生に対して'}},
    {"data":{'source': '教員に対する思い', 'target': '若者に対する考え，少しは厳しい状況に身を置くべき'}},
    {"data":{'source': '教員に対する思い', 'target': '分野の壁がないこと→教養教育において大事な環境'}},
    {"data":{'source': '大学の在り方', 'target': '永田学長が思う大学の役割'}},
    {"data":{'source': '大学の在り方', 'target': '大学の運営に少なからず不自由な面がある'}},
    {"data":{'source': '大学の在り方', 'target': '筑波大学キーワード'}},
    {"data":{'source': '繰り返し言及している', 'target': '永田学長の学長ぞうを象徴する言葉'}},
    {"data":{'source': '繰り返し言及している', 'target': '筑波大学キーワード'}},
    {"data":{'source': '繰り返し言及している', 'target': '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）'}},
    {"data":{'source': '分野の壁がないこと→教養教育において大事な環境', 'target': '大学の運営に少なからず不自由な面がある'}},
    {"data":{'source': '分野の壁がないこと→教養教育において大事な環境', 'target': '若者に対する考え，少しは厳しい状況に身を置くべき'}},
    {"data":{'source': '分野の壁がないこと→教養教育において大事な環境', 'target': '教員に対する思い'}},
    ]
}
# graph = {
#     "node":[
#         {"data":{"id":"テスト1"}},
#         {"data":{"id":"テスト2"}}
#     ],
#     "edge":[
#         {"data":{'source': 'テスト1', 'target': 'テスト2'}},
#     ]
# }


@app.route("/",methods=["GET","POST"])
def index():   
    global questionnaire_data,analyst_data,system,user_hiright,graph
    if request.method == "POST":
        #postされたファイルオブジェクト取得
        f = request.files["file"]
        #ファイル情報の処理
        questionnaire_data.file_name = secure_filename(f.filename)
        if questionnaire_data.file_name != "":
            questionnaire_data.file_path = my_path + "files/" + questionnaire_data.file_name
            questionnaire_data.file_save(f)
            #ファイルを開き，センテンス情報の取得
            if os.path.isfile(questionnaire_data.file_path):
                with open(questionnaire_data.file_path,"r") as f:
                    questionnaire_data.texts = f.readlines()
                questionnaire_data.make_html_data()
                return render_template(
                    'result.html',
                    file_name=questionnaire_data.file_name,
                    lines=questionnaire_data.html_data,
                    result=analyst_data.chat_data,
                    graph=graph,
                    hiright=user_hiright)  
        else:
            return render_template('index.html')
    else:
        #（仮）/ページがGETされた時，すなわちトップページに戻ってきたらデータ初期化するように設定しておく
        system = System()
        questionnaire_data = QuestionnaireData()
        analyst_data = AnalystData()
        user_hiright = []
        node2index = {}
        #フォルダの初期化
        make_dir(my_path) 
        
        return render_template("index.html")

@app.route("/result",methods=["GET","POST"])
def result():
    global user_hiright,graph
    if request.method == "POST":
        print(11111111)
        tmp_reason = request.form.get("reason")
        #分析者が選択した文章と理由の取得＆処理
        analyst_data.add_data(request.form.get('reason'),request.form.getlist('sent'))

        #メモを保存
        user_hiright[-1]["memo"] = tmp_reason
        
        #分析者の投稿を保存
        if tmp_reason != "":
            analyst_data.chat_data.append(["analyst_reason",tmp_reason])
            if analyst_data.phrase_reason != []:
                analyst_data.phrase_reason[-1].append(tmp_reason)
        else:
            pass
        return render_template(
            "result.html",
            file_name=questionnaire_data.file_name,
            lines=questionnaire_data.html_data,
            result=analyst_data.chat_data,
            tmp_reason = tmp_reason
        )
    else:
        if questionnaire_data.html_data==None:
            lines = [{"index":999,"sentence":"データがありません"}]
        else:
            lines = questionnaire_data.html_data
            print(lines)
        return render_template(
            "result.html",
            file_name=questionnaire_data.file_name,
            lines=lines,
            result=analyst_data.chat_data,
            graph=graph,
            hiright = user_hiright
        )

@app.route("/history",methods=["GET"])
def history():
    analyst_data.save()
    return render_template("history.html",history_datas=analyst_data.reason2choice)


@app.route("/hiright",methods=["POST"])
def hiright():
    global user_hiright
    tmp_dic = {
        "id":request.form["a"],
        "startOffset":request.form["b"],
        "endOffset":request.form["c"],
        "text":request.form["d"]
    }
    user_hiright.append(tmp_dic)
    print(tmp_dic)
    return redirect(url_for("result"))

@app.route("/memo",methods=["POST"])
def memo():
    global user_hiright
    memo = request.form["memo"]
    row = request.form["tmp_range"]
    #メモを保存
    user_hiright[-1]["memo"] = memo
    #チャットデータにmemoを保存
    analyst_data.chat_data.append(["analyst_phrase",row + "　" + memo])
    #類似度の計算

    # node2index[memo] = user_hiright[-1]["id"]
    print(node2index)
    return redirect(url_for("result"))

@app.route("/node_tag",methods=["POST"])
def node_tag():
    tmp_node = request.form["node"]
    tag = re.sub("^\$TAG\$","",request.form["tag"])
    if re.search(r"\d+",tmp_node):
        node = tmp_node
        analyst_data.chat_data.append(["analyst_phrase",tmp_node + "　" + request.form["tag"]])
    else:
        node = node2index[tmp_node]
    if node != "" and tag != "":
        questionnaire_data.add_tag(node,tag)
    return redirect(url_for("result"))