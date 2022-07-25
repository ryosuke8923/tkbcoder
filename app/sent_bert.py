import sys
memo1 = ['大学の運営に少なからず不自由な面がある', 
    '永田学長が思う大学の役割',
    '個性が強い\u3000≒\u3000就職してからの夢を持てるかどうか', 
    '日本人学生に対して', 
    '若者に対する考え，少しは厳しい状況に身を置くべき', 
    '筑波大学キーワード', 
    '話しの中で見つけた一つの考え？（もともと持っていたのかは不明）', 
    'ある部分において， 企業の上層部と大学の役員を同じような位置付けに置いている', 
    '永田学長の学長ぞうを象徴する言葉', 
    '教員に対する思い', 
    '大学の在り方',
    '繰り返し言及している', 
    '分野の壁がないこと→教養教育において大事な環境'
]

memo2 = [
    '長いこと興味がある感じが伝わる', 
    'サッカー観戦も好き', 
    'チームを作るほどプレイするのも好き', 
    'アメリカ時代の話し', 
    'アメリカでの経験が学長の考えに影響を及ぼしているような気がする', 
    '一人の大学学長としてだけでなく，地域や市民に対する考えがある．つくばという地で学長をやっていることも影響しているのかも', 
    '過去にも言及していた内容．若者は安住していると述べている', 
    '世界進出に対する考え', 
    '環境やムード・雰囲気というものを大切にしているよう'
]
memo3 = [
    '相手と自分のイメージを擦り合わせて話しをしている', 
    '研究が持つべき姿勢', 
    '同じ立場であるということを伝えることで，学ぶ姿勢みたいなものが感じられる', 
    '社会に対して発信する役割．他のインタビューからも感じ取れた', 
    'スポーツを大切な文化と捉えている．過去のインタビューからも'
]

# 2. モデルの定義
from sentence_transformers import util, SentenceTransformer
import heapq
import re
import torch
import networkx as nx
from networkx.algorithms import community
import itertools

class SentBert:

    def __init__(self):

        self.model = SentenceTransformer("stsb-xlm-r-multilingual")
        self.memo = []
        self.embeddings = []
        self.cos_sim = []

    def add_memo(self,target_memo:str):
        self.memo.append(target_memo)

    def cal_emb_sim(self):
        for i in self.memo:
            embedding = self.model.encode(i, convert_to_tensor=True)
            if self.embeddings != []:
                self.cal_sim(embedding)
            else:
                self.cos_sim.append([0])
            self.embeddings.append(embedding)
        

    def cal_sim(self,embedding):
        embeddings = torch.stack(self.embeddings)
        scores = util.pytorch_cos_sim(embedding, embeddings)
        scores = scores.numpy().tolist()[0]
        tmp_sim = []
        for i in range(len(scores)):
            self.cos_sim[i].append(scores[i])
            tmp_sim.append(scores[i])
        self.cos_sim.append(tmp_sim+[0])
    
    def make_edge(self):
        edges = []
        for i in range(len(self.cos_sim)):
            index = [ self.cos_sim[i].index(j) for j in heapq.nlargest(3, self.cos_sim[i])]
            for k in index:
                edges.append({"data":{"source":self.memo[i],"target":self.memo[k]}})
        return edges
                
    def make_edge_cy(self):
        edges_cy = []
        for i in range(len(self.cos_sim)):
            index = [ self.cos_sim[i].index(j) for j in heapq.nlargest(3, self.cos_sim[i])]
            for k in index:
                edges_cy.append((self.memo[i],self.memo[k],self.cos_sim[i][k]))
        return edges_cy

    def cal_class(self,k=3):
        G = nx.Graph()
        x = self.make_edge_cy()
        G.add_weighted_edges_from(x)
        comp = community.girvan_newman(G)
        community_list = []
        for communities in itertools.islice(comp, k-1):
            community_list.append(tuple(sorted(c) for c in communities))
        community_list = list(community_list[k-2])
        tmp_lst = [0]*len(self.memo)
        for i in range(len(community_list)):
            for j in community_list[i]:
                tmp_lst[self.memo.index(j)] = i
        return tmp_lst
    
    def make_node(self):
        nodes = []
        node_class = self.cal_class()
        for i in range(len(self.memo)):
            nodes.append({"data":{"id":self.memo[i],"label":node_class[i]}})
        return nodes

            



# s = SentBert()

# for i in memo1:
#     s.add_memo(i)
# s.cal_emb_sim()
# node = s.make_node()
# ed = s.make_edge()
# print(node)
# print(ed)
# sys.exit()

# # モデルの読み込み
# model = SentenceTransformer('stsb-xlm-r-multilingual')

# all_memo = memo1+memo2+memo3
# all_memo = memo1
# # 入力文をベクトル表現に変換
# for i in range(len(all_memo)):

#     sentence = all_memo[i]
#     embedding = model.encode(sentence, convert_to_tensor=True)
#     print(embedding.shape)
#     # 検索対象文をベクトル表現に変換
#     sentences = all_memo[:i] + all_memo[i+1:]
#     embeddings = model.encode(sentences, convert_to_tensor=True)
#     print(embedding)
#     print(embeddings)
#     # print(1,embedding.size())
#     # print(2,embeddings[0].size())
#     # 入力文と検索対象文のベクトル表現の類似度を計算
#     scores = util.pytorch_cos_sim(embedding, embeddings)
#     scores = scores.numpy().tolist()
#     index = [ scores[0].index(tt) for tt in heapq.nlargest(3, scores[0])]
#     # print('文:', sentence)
#     # print(scores)
#     for j in range(len(index)):
#         # print("Rank:{} 類似文:{}".format(j+1,sentences[index[j]]))
#         print((sentence,sentences[index[j]],scores[0][index[j]]))
#     # print("====================")

# sys.exit()
# print("=======================================")
# print("=======================================")
# print("=======================================")
# #アンケート文との類似度

# with open("./files/4.csv","r") as f:
#     lines = list(map(lambda x:x.rstrip(),f.readlines()))
#     lines = lines[1:]
# lines = list(map(lambda x: re.sub(",永田,急速に変化する産業界に求められる人材,イノベーションの源泉～今こそ求められる教養教育と基礎研究の力$","",x),lines))
# text = []
# for l in lines:
#     if re.search(",花井,急速に変化する産業界に求められる人材,イノベーションの源泉～今こそ求められる教養教育と基礎研究の力$",l):
#         pass
#     else:
#         text.append(l)

# for i in range(len(text)):

#     sentence = text[i]
#     embedding = model.encode(sentence, convert_to_tensor=True)

#     # 検索対象文をベクトル表現に変換
#     sentences = memo1
#     embeddings = model.encode(sentences, convert_to_tensor=True)
#     # print(1,embedding.size())
#     # print(2,embeddings[0].size())
#     # 入力文と検索対象文のベクトル表現の類似度を計算
#     scores = util.pytorch_cos_sim(embedding, embeddings)
#     scores = scores.numpy().tolist()
#     index = [ scores[0].index(tt) for tt in heapq.nlargest(3, scores[0])]
#     print('文:', sentence)
#     print(scores)
#     for j in range(len(index)):
#         print("Rank:{} 類似文:{}".format(j+1,sentences[index[j]]))
#     print("====================")

