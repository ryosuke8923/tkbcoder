#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,redirect,url_for,Markup,send_file
from flask import request
from werkzeug.utils import secure_filename
import os 
import random
import ast
import shutil
import re
from collections import defaultdict
from . import sent_bert
from . import recommend
import datetime
from docx import Document
# from . import code
######

my_path = os.path.expanduser('~') + "/tkbcoder/app/" if os.path.expanduser('~') != "/Users/saitouryousuke" else os.path.expanduser('~') + "/prog/python/tkbcoder/app/"
print(my_path)

#メモ
#・全く同じ文章が含まれているときにバグをはく可能性あり．ただ，どこのそれを見ているかは判別不可 (rec_sent2index)


my_files_path = my_path + "files/"
my_log_path = my_path + "log/"
if not os.path.isdir(my_files_path):
    os.mkdir(my_files_path)
if not os.path.isdir(my_log_path):
    os.mkdir(my_log_path)
        
#分析者用クラス
class AnalystData:
    def __init__(self):
        self.reason2choice = {}
        self.reasons = []
        self.choice_texts = []
        self.chat_data = [["system","***"]]
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
        self.texts = None
        self.html_data = None
    
    def make_html_data(self):
        html_data = []
        for i,k in enumerate(self.texts):
            k = re.sub("\n","",k)
            html_data.append({"index":i,"sentence":k,"tag":[]})
        self.html_data = html_data

    def file_save(self,f):
        #とりあえずローカルディレクトリに保存
        f.save(self.file_path)

    def add_tag(self,index,tag):
        self.html_data[int(index)]["tag"].append(tag)


def make_dir(path,dir_name):
    target_dir = path + dir_name
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)

def make_sent(texts):
    sent_texts = []
    sent2index = defaultdict(list)
    exception_sent_index = []
    for i in range(len(texts)):
        sentence = [ re.sub("\n","",x) for x in re.split("[。．:;)]",texts[i]) if x != ""]
        sent_texts += sentence
        for j in sentence:
            sent2index[j] = i
    for i in range(len(sent_texts)):
        if len(sent_texts[i]) <= 8 or sent_texts[i] == "==================================================":
            exception_sent_index.append(i)
    return sent_texts,sent2index,exception_sent_index

def make_tag2sent(tags,user_hiright):
    for i in range(len(user_hiright)):
        if user_hiright[i]["tag"] not in tags and user_hiright[i]["tag"] != "":
            tags[user_hiright[i]["tag"]] = [user_hiright[i]["text"]]
        else:
            if user_hiright[i]["tag"] in tags:
                if user_hiright[i]["text"] not in tags[user_hiright[i]["tag"]]:
                    tags[user_hiright[i]["tag"]].append(user_hiright[i]["text"])


def read_word(file_path):
    document = Document(file_path)
    texts = []
    for i in document.paragraphs:
        print(i.paragraph_format)
        print(i.style)
        if i.text != []:
            texts.append(i.text)
    return texts
######


#Flaskオブジェクトの生成
app = Flask(__name__)

#オブジェクトの初期化
questionnaire_data = QuestionnaireData()
analyst_data = AnalystData()
user_hiright = []
tags={}
# graph_obj = sent_bert.SentBert()
rec_texts = []
rec_sent2index = {}
log_file_path = ""
recommends = [
]
remove_recommends = [
]
recommend_style = True



@app.route("/",methods=["GET","POST"])
def index():   
    global recommend_style,questionnaire_data,analyst_data,user_hiright,rec_texts,rec_sent2index,recommend_system,recommends,log_file_path,remove_recommends,tags

    if request.method == "POST":
        #postされたファイルオブジェクト取得
        files = request.files.getlist("file")
        file_name = ""
        all_text = []
        for f in files:
            file_name += f.filename + "/"
            file_path = my_path + "files/" + f.filename
            f.save(file_path)
            if os.path.isfile(file_path):
                if re.search("doc",f.filename):
                    all_text += read_word(file_path)
                else:
                    with open(file_path,"r") as f:
                        all_text += f.readlines()
                all_text.append("==================================================")
        #ログファイルの設定
        log_file_path = my_path + "log/log.txt"
        print(log_file_path)
        # 時刻，eventtype(自分，タグ削除，推薦○,推薦×，ジャンプ) 何行目の何文字目,テキスト 
        with open(log_file_path,"w") as f:
            f.write("time,eventtype,line,text,tag,level,\n")
        #ファイル情報の処理
        questionnaire_data.file_name = file_name
        if questionnaire_data.file_name != "":
            # questionnaire_data.file_path = my_path + "files/" + questionnaire_data.file_name
            # questionnaire_data.file_save(f)
            #ファイルを開き，センテンス情報の取得
            # with open(questionnaire_data.file_path,"r") as f:
            #     questionnaire_data.texts = f.readlines()
            questionnaire_data.texts = all_text
            questionnaire_data.make_html_data()
            rec_texts,rec_sent2index,exception_sent_index = make_sent(questionnaire_data.texts)
            recommend_system = recommend.Recommend(rec_texts,exception_sent_index)
            # recommend_system = recommend.Recommend(rec_texts)
            # return render_template(
            #     'result.html',
            #     file_name=questionnaire_data.file_name,
            #     lines=questionnaire_data.html_data,
            #     result=analyst_data.chat_data,
            #     graph=graph,
            #     hiright=user_hiright,
            #     recommends = recommends)  
            return redirect(url_for("result"))
        else:
            return render_template('index.html')
    else:
        #（仮）/ページがGETされた時，すなわちトップページに戻ってきたらデータ初期化するように設定しておく
        return render_template("index.html")

@app.route("/result",methods=["GET","POST"])
def result():
    global recommend_style,user_hiright,recommend_system,recommends
    if request.method == "POST":
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
            tmp_reason = tmp_reason,
            recommends = recommends,
            tags = tags
        )
        # download_file_path = "log/log.txt"
        # download_file_name = os.path.basename(download_file_path)
        # return send_file(download_file_path, as_attachment=True,
        #              attachment_filename=download_file_name,
        #              mimetype='text/plain')
    else:
        # print("user_hiright")
        # print(user_hiright)
        # print(recommend_system.Xs_threshold)
        # print("tags")
        # print(tags)
        # print(rec_sent2index)
        # print(questionnaire_data.html_data)
        if user_hiright != [] and user_hiright[-1]["tag"] != "":
            make_tag2sent(tags,user_hiright)
        if questionnaire_data.html_data==None:
            lines = [{"index":999,"sentence":"データがありません"}]
        else:
            lines = questionnaire_data.html_data
        return render_template(
            "result.html",
            file_name=questionnaire_data.file_name,
            lines=lines,
            result=analyst_data.chat_data,
            hiright = user_hiright,
            recommends = recommends,
            tags = tags
        )

@app.route("/download",methods=["GET"])
def download():
    filepath = "log/log.txt"
    filename = os.path.basename(filepath)
    return send_file(filepath, as_attachment=True,
                     attachment_filename=filename,
                     mimetype='text/plain')
                     
@app.route("/practice",methods=["GET"])
def practice():
    return render_template(
        "practice.html",
        file_name="test.doc",
        lines=[{"index":1,"sentence":"a","tag":"a"}],
        recommends = [["1","この文章にタグ付けをしよう","テスト"]],
        tags = {"テスト":"この文章にタグ付けをしよう．"}
        )

@app.route("/style",methods=["POST"])
def style():
    global recommend_style
    x = int(request.form["style"])
    if x == 0:
        recommend_style = False
    else:
        recommend_style = True
    print(recommend_style)
    return render_template("index.html")

@app.route("/reset",methods=["POST"])
def reset():
    global recommend_style,questionnaire_data,analyst_data,user_hiright,rec_texts,rec_sent2index,recommend_system,recommends,log_file_path,remove_recommends,tags
    questionnaire_data = QuestionnaireData()
    analyst_data = AnalystData()
    user_hiright = []
    tags = {}
    rec_texts = []
    rec_sent2index = {}
    recommend_style = True
    #フォルダの初期化
    make_dir(my_path,"files") 
    make_dir(my_path,"log") 
    recommends = []
    remove_recommends=[]
    print(user_hiright)
    return render_template("index.html")

@app.route("/history",methods=["GET"])
def history():
    analyst_data.save()
    return render_template("history.html",history_datas=analyst_data.reason2choice)


@app.route("/hiright",methods=["POST"])
def hiright():
    global recommend_style,user_hiright,recommends,remove_recommends
    if re.match("^apply_",request.form["d"]):
        tmp_dic = {
            "id":request.form["a"],
            "startOffset":request.form["b"],
            "endOffset":request.form["c"],
            "text":re.sub("apply_","",request.form["d"]),
            "tag":"",
        }
        output_log(eventtype="hiright_by_system",text=tmp_dic["text"],line=tmp_dic["id"])
    else:
        tmp_dic = {
            "id":request.form["a"],
            "startOffset":request.form["b"],
            "endOffset":request.form["c"],
            "text":request.form["d"],
            "tag":"",
        }
        output_log(eventtype="hiright_by_analyst",text=tmp_dic["text"],line=tmp_dic["id"])
    if tmp_dic not in user_hiright:
        user_hiright.append(tmp_dic)
        if tmp_dic["text"] not in remove_recommends:
            remove_recommends.append(tmp_dic["text"])
    return redirect(url_for("result"))

@app.route("/input_tag",methods=["POST"])
def input_tag():
    global recommend_style,recommend_system,user_hiright,recommends,remove_recommends
    tmp_tag = request.form["input_tag"]
    # print("tmp_tag")
    # print(tmp_tag)
    # print("user_hiright")
    # print(user_hiright[-1])
    if tmp_tag == "":
        for i in range(len(user_hiright)):
            if user_hiright[i]["tag"] == "":
                user_hiright.pop(i)
    else:
        if  len(user_hiright) != 0 and user_hiright[-1]["tag"] == "":
            user_hiright[-1]["tag"] = tmp_tag
            output_log(eventtype="tag",text=user_hiright[-1]["text"],tag=tmp_tag,line=user_hiright[-1]["id"])
        # 推薦アルゴリズム~recommendへappendまで
        # print(user_hiright[-1])
        if recommend_style:
            x = recommend_system.predict([user_hiright[-1]["text"]],user_hiright[-1]["tag"])
        else:
            x = False
        # print(x)
        if x:
            recommend_text = rec_texts[x]
            ids = rec_sent2index[recommend_text]-1
            tag = user_hiright[-1]["tag"] if user_hiright[-1]["tag"] != "" else "-"
            # print([ids,recommend_text[:10],tag])
            # print(recommend_system.Xs_threshold)
            # length = len(recommend_text) if len(recommend_text) <=20 else 20
            # if recommend_text[:length] not in remove_recommends:
            #     recommends.append([ids,recommend_text[:length],tag])
            if recommend_text not in remove_recommends:
                recommends.append([ids,recommend_text,tag])
                if recommend_text not in remove_recommends:
                    remove_recommends.append(recommend_text)
    print(user_hiright)
    return redirect(url_for("result"))

@app.route("/remove_tag",methods=["POST"])
def remove_tag():
    global recommend_style,tags,user_hiright
    tmp_text = request.form["remove_tag"]
    remove_tag = ""
    remove_text = ""
    for i in range(len(user_hiright)):
        if user_hiright[i]["text"] == tmp_text:
            remove_tag = user_hiright[i]["tag"]
            remove_text = user_hiright[i]["text"]
            output_log(eventtype="remove_tag",text=user_hiright[i]["text"],tag=user_hiright[i]["tag"],line=user_hiright[i]["id"])
            user_hiright.pop(i)
            break
    if remove_tag in tags:
        if remove_text in tags[remove_tag]:
            if len(tags[remove_tag]) == 1:
                tags.pop(remove_tag)
            else:
                tags[remove_tag].remove(remove_text)
    return redirect(url_for("result"))

@app.route("/remove_recommend",methods=["POST"])
def remove_recommend():
    global recommend_style,recommend_system,remove_recommends
    tmp_text = request.form["remove_recommend"]
    for i in range(len(recommends)):
        if recommends[i][1]== tmp_text:
            output_log(eventtype="remove_recommend",text=recommends[i][1],tag=recommends[i][2],line=recommends[i][0])
            recommends.pop(i)
            break
    # remove_recommends.append(tmp_text)
    # print(recommends)
    # print(remove_recommends)
    return redirect(url_for("result"))


#テキストデータで用意してもらう　複数のインタビュデータの場合，戻る→最後のタグ付与の場所へ．タグ一覧からのジャンプ, wordファイルが入力されます
#split コロン等含める　5文字以下は推薦の対象から外す，半角スペース，空行に罫線など　
#実験では時間とかタグの数とかではなく，感想．
#照山研と若林研でのログ，
# 時刻，eventtype(自分，タグ削除，推薦○,推薦×，ジャンプ) 何行目の何文字目,テキスト

@app.route("/rec_level",methods=["POST"])
def rec_level():
    global recommend_style,recommend_system,remove_recommends
    tmp_rec_level = request.form["rec_level"]
    output_log(eventtype="change_rec_level",level=tmp_rec_level)
    if tmp_rec_level == "0":
        recommend_system.Xs_threshold = recommend_system.threshold_high
    elif tmp_rec_level == "1":
        recommend_system.Xs_threshold = recommend_system.threshold_middle
    else:
        recommend_system.Xs_threshold = recommend_system.threshold_low
    return redirect(url_for("result"))

def output_log(eventtype="-",text="-",tag="-",line="-",level="-"):
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    string = "{},{},{},{},{},{}\n".format(time,eventtype,line,text,tag,level)
    with open(log_file_path,"a") as f:
        f.write(string)