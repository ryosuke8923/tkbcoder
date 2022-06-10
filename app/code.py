import MeCab
import re
from torchtext.legacy import data
from torchtext.vocab import Vectors
import torch.nn.functional as F
from . import code_data

class Code:

    def __init__(self,phrase_reason=None,csv_file=None,my_path=""):

        self.phrase_reason = phrase_reason
        self.csv_file = csv_file
        self.tagger = MeCab.Tagger('-Owakati')
        self.path = my_path
        self.TEXT = None
        self.train_ds = None
        self.vec = None
        self.code = []


    def tokenizer_mecab(self,text):
        text = self.tagger.parse(text)  # これでスペースで単語が区切られる
        ret = text.strip().split()  # スペース部分で区切ったリストに変換
        return ret

    def preprocessing_text(self,text):
        # 改行、半角スペース、全角スペースを削除
        text = re.sub('\r', '', text)
        text = re.sub('\n', '', text)
        text = re.sub('　', '', text)
        text = re.sub(' ', '', text)

        # 数字文字の一律「0」化
        # text = re.sub(r'[0-9 ０-９]', '0', text)  # 数字

        return text

    def tokenizer_with_preprocessing(self,text):
        text = self.preprocessing_text(text)  # 前処理の正規化
        ret = self.tokenizer_mecab(text)  # Mecabの単語分割

        return ret

    def cal_similarity(self,lst,*index):
        self.TEXT.build_vocab(self.train_ds, vectors=self.vec, min_freq=1)
        lst1 = []
        lst2 = []
        for k,i in self.TEXT.vocab.stoi.items():
            if len(index) == 1:
                value = F.cosine_similarity(self.TEXT.vocab.vectors[index[0]], self.TEXT.vocab.vectors[i],dim=0)
                if i != index[0]:
                    lst1.append((value,k))
            else:
                value = 0
                for j in range(len(index)):
                    value += F.cosine_similarity(self.TEXT.vocab.vectors[index[j]], self.TEXT.vocab.vectors[i],dim=0)
                value = value / len(index)
                if i not in index:
                    lst1.append((value,k))
        lst1.sort(reverse=True)
        lst1 = list(zip(*lst1))
        return lst1[1][:5]

    def show_code(self):
        for i in self.code:
            print(vars(i))


    def estimate(self,flag=False):

        max_length = 25
        TEXT = data.Field(sequential=True, tokenize=self.tokenizer_with_preprocessing,
                                    use_vocab=True, lower=True, include_lengths=True, batch_first=True, fix_length=max_length)
        LABEL = data.Field(sequential=False, use_vocab=False)
        LABEL2 = data.Field(sequential=False, use_vocab=False)
        LABEL3 = data.Field(sequential=False, use_vocab=False)

        

        train_data = self.csv_file
        validation_data = self.csv_file
        train_ds,test_ds = data.TabularDataset.splits(
            path=self.path+"files/", train=train_data, validation=validation_data,format='csv',
            fields=[('Text', TEXT), ('Label', LABEL),('Label2', LABEL2),('Label3', LABEL3)])

        if flag:
            return train_ds
        

        print('データの数', len(train_ds))
        print('1つ目のデータ', vars(train_ds[1]))
        print(vars(train_ds[1])['Text'])
        print(vars(train_ds[1])['Label'])
        print(vars(train_ds[1])['Label2'])
        print(vars(train_ds[1])['Label3'])

        japanese_word2vec_vectors = Vectors(name=self.path+'model/japanese_word2vec_vectors.vec')

        # 単語ベクトルの中身
        print("1単語を表現する次元数：", japanese_word2vec_vectors.dim)
        print("単語数：", len(japanese_word2vec_vectors.itos))

        # ベクトル獲得
        TEXT.build_vocab(train_ds, vectors=japanese_word2vec_vectors, min_freq=1)

        # ボキャブラリーのベクトルを確認します
        print(TEXT.vocab.vectors.shape)  # 6518個の単語と200次元のベクトル

        target_lst = [["歴史"],["自然"],["テクノロジー"]]

        # インデックスを探す
        for i in range(len(target_lst)):
            index = TEXT.vocab.stoi[target_lst[i][0]]
            target_lst[i].append(index)
        print(target_lst)

        self.TEXT = TEXT
        self.train_ds = train_ds
        self.vec = japanese_word2vec_vectors

        x = self.cal_similarity(target_lst,227,568,121)
        keyword_lst = list(x)
        sentence_lst = []
        i_lst = []
        for i in range(len(train_ds)):
            for xx in x:
                if xx in vars(train_ds[i])["Text"]:
                    if i not in i_lst:
                        if len("".join(vars(train_ds[i])["Text"])) >= 10:
                            j = "".join(vars(train_ds[i])["Text"])[:10]
                        else:
                            j = "".join(vars(train_ds[i])["Text"])
                        sentence_lst.append([str(i),j])
                        i_lst.append(i)
        if len(i_lst) >= 6 :
            i_lst = i_lst[:5]
        #データクラスを作成して，appendする
        self.code.append(code_data.CodeData(i_lst,"つくば市",target_lst,keyword_lst))
        self.show_code()

        #以下は表示のため
        keywords = "，".join(keyword_lst)
        sentences = ""
        for s in sentence_lst:
            t = " ".join(s)
            sentences += t 
            print(len(t))
        print(keywords,sentences,i_lst)
        return keywords, sentences, i_lst
