#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,Markup
from flask import request
from werkzeug.utils import secure_filename
import os 
import random
import ast
import shutil
######

my_path = '/Users/saitouryousuke/prog/python/tkbcoder/app/'

#分析者用クラス
class AnalystData:
    def __init__(self):
        self.reason2choice = {}
        self.reasons = []
        self.choice_texts = []
        self.chat_data = []

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



#アンケートデータ用クラス
class QuestionnaireData:
    def __init__(self,file_name=None,file_path=None,texts=None,):
        self.file_name = file_name
        self.file_path = file_path
        self.texts = texts
        self.html_data = None
    
    def make_html_data(self):
        html_data = []
        for i,k in enumerate(self.texts):
            html_data.append({"index":i,"sentence":k})
        self.html_data = html_data

    def file_save(self,f):
        #とりあえずローカルディレクトリに保存
        f.save(self.file_path)

def make_dir(path):
    target_dir = path + "files"
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)
######


#Flaskオブジェクトの生成
app = Flask(__name__)

#オブジェクトの初期化
questionnaire_data = QuestionnaireData()
analyst_data = AnalystData()

@app.route("/",methods=["GET","POST"])
def index():   
    global questionnaire_data,analyst_data
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
                    lines=questionnaire_data.html_data)        
        else:
            return render_template('index.html')
    else:
        #（仮）/ページがGETされた時，すなわちトップページに戻ってきたらデータ初期化するように設定しておく
        questionnaire_data = QuestionnaireData()
        analyst_data = AnalystData()
        #フォルダの初期化
        make_dir(my_path) 
        return render_template("index.html")

@app.route("/result",methods=["GET","POST"])
def result():
    if request.method == "POST":
        tmp_reason = request.form.get("reason")
        #分析者が選択した文章と理由の取得＆処理
        analyst_data.add_data(request.form.get('reason'),request.form.getlist('sent'))
        #分析者の投稿を保存
        if tmp_reason != "":
            analyst_data.chat_data.append(["analyst",tmp_reason])
            system_return = False
            #システム側からの返事を保存
            if system_return:
                pass
            else:
                comment = "ふむふむ"
                analyst_data.chat_data.append(["system",comment])
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
        print(analyst_data.chat_data)
        if questionnaire_data.html_data==None:
            lines = [{"index":999,"sentence":"データがありません"}]
        else:
            lines = questionnaire_data.html_data
        return render_template(
            "result.html",
            file_name=questionnaire_data.file_name,
            lines=lines,
            result=analyst_data.chat_data
        )

@app.route("/history",methods=["GET"])
def history():
    analyst_data.save()
    return render_template("history.html",history_datas=analyst_data.reason2choice)
