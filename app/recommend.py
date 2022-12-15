from sentence_transformers import util, SentenceTransformer
import torch
import numpy as np
import heapq
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
import json
import tqdm

class Recommend:
    
    def __init__(self,data=None,exception_sent_index=None,alg_name="cos_sim"):
        
        self.alg_name = alg_name
        self.model =  SentenceTransformer("stsb-xlm-r-multilingual")
        self.Xs = data
        self.sent2index = defaultdict(int)
        self.Xs_sent = data
        self.Xs_sent_emb = None if data == None else self.cal_embedding()
        self.Xs_threshold= None if data == None else self.cal_threshold() 
        self.threshold_high = self.Xs_threshold
        self.threshold_middle = self.threshold_high - 0.1
        self.threshold_low = self.threshold_high - 0.2
        self.exception_sent_index = exception_sent_index
#         self.umap_lst,self.umap_ys = self.make_umap()   
#         self.Xs_block = self.make_sent_block()

    # def read_data(self,data):
    #     Xs = []
    #     with open(data,"r") as f:
    #         for line in f.readlines():
    #             line = json.loads(line)
    #             Xs.append(line)
    #     return Xs
    
    
    # def make_sent(self):
    #     Xs_sent = []
    #     for i in range(len(self.Xs)):
    #         dic = self.Xs[i]
    #         sentence = dic["sentence"]
    #         Xs_sent.append(sentence)
    #     return Xs_sent

    
    def cal_embedding(self):
        return torch.cat([ self.model.encode(self.Xs_sent[i],convert_to_tensor=True).unsqueeze(0) for i in range(len(self.Xs_sent))],dim=0)
    
    def make_umap(self):
        umap_Xs = []
        umap_ys = []
        for i in range(len(self.Xs)):
            tag = self.Xs[i]["tag"]
            true_y = [ i for i,v in enumerate(tag) if v==1 ]
            if len(true_y) == 1:
                umap_Xs.append(self.Xs_sent_emb[i].unsqueeze(0))
                umap_ys.append(true_y[0])
            else:
                for j in true_y:
                    umap_Xs.append(self.Xs_sent_emb[i].unsqueeze(0))
                    umap_ys.append(j)
        umap_Xs = torch.cat(umap_Xs,dim=0)
        return umap_Xs,umap_ys
            
        
        
    def recommend(self,sentence,tag):
        if self.alg_name == "cos_sim":
            return self.alg_simple_cos_recommend(sentence,tag)
        if self.alg_name == "distance":
            return self.alg_simple_distance(sentence,tag)
#         alg = {
#             "cos_sim":self.alg_simple_cos_recommend(sentence,tag),
#             "distance":self.alg_simple_distance(sentence,tag)
#         }
#         print(1)
#         print(alg[self.alg_name])
#         return alg[self.alg_name]
    
    #return 二重配列 [[sent,tag]]
    def alg_simple_cos_recommend(self,target_sent:list,target_tag:str,topn=10,use_model=False):
        #targetの分散表現獲得
        candidate_lst = []
        index_lst = []
        l = np.zeros(len(self.Xs_sent))
        # print(self.Xs_sent_emb.shape)
        # print(target_sent)
        for i in range(len(target_sent)):
            embedding = self.model.encode(target_sent[i],convert_to_tensor=True)
            # print("target_emb:{}".format(embedding))
            scores = util.pytorch_cos_sim(embedding, self.Xs_sent_emb)
            l += scores.numpy()[0]
#             scores = scores.numpy().tolist()[0]
#             candidate_lst += [ (t,scores.index(t)) for t in heapq.nlargest(topn, scores) if scores.index(t) not in target_index]
        l = l / len(target_sent)
        l = l.tolist()
        # print(l)
        candidate_lst += [ (t,l.index(t)) for t in heapq.nlargest(topn, l)]
        candidate_lst = sorted(candidate_lst,reverse=True)
        candidate_lst.pop(0)
        while candidate_lst[0][1] in self.exception_sent_index:
            candidate_lst.pop(0)
        # print(candidate_lst)
#         print(candidate_lst)
        # if use_model:
        #     suggest_sentence = self.Xs[self.sent2index[index[0]]]["sentence"]
        #     lr_model = self.logistic_negative_sampling(target_sent)
        #     ans = lr_model.predict([self.model.encode(suggest_sentence,convert_to_tensor=True).unsqueeze(0)][0])
        #     return index[0] if ans else False
        if candidate_lst == []:
            return False
#         print("cos:{}".format(candidate_lst[0][1]))
#         print(candidate_lst[0][0])
        return candidate_lst[0][1] if candidate_lst[0][0] >= self.Xs_threshold else False
    
#     def alg_simple_distance(self,sent,tag):
#         return True
    def alg_simple_distance(self,target_index:list,target_tag:str,topn=10):
        print(2)
        scores = []
        for i in range(len(target_index)):
            target_emb = self.model.encode(self.Xs_sent[target_index[i]],convert_to_tensor=True)
            tmp_scores = []
            for emb in self.Xs_sent_emb:
                tmp_scores.append(np.linalg.norm(target_emb-emb))
            scores.append(tmp_scores)
        scores = [ sum(i) for i in zip(*scores)]
#         print(len(scores))
#         print(scores)
        index = [ (t,scores.index(t)) for t in heapq.nsmallest(topn, scores) if scores.index(t) not in target_index]
        if index == []:
            return False
        print("dis:{}".format(index[0][1]))
        return index[0][1] if index[0][0] >= self.Xs_threshold else False
        
#         return index[0] if scores[index[0]] <= self.Xs_threshold else False
    
    def cal_threshold(self):
        if self.alg_name == "cos_sim":
            return self.cos_sim_threshold()
        if self.alg_name == "distance":
            return self.distance_threshold()
#         alg = {
#             "cos_sim":self.cos_sim_threshold(),
#             "distance":self.distance_threshold()
#         }
        
#         threshold = alg[self.alg_name]
#         return threshold
    
    def cos_sim_threshold(self):
        value = 0
        for embedding in self.Xs_sent_emb:
            value += torch.sort(util.pytorch_cos_sim(embedding, self.Xs_sent_emb))[0][0][-2]
        return value/len(self.Xs_sent_emb)
    
    def distance_threshold(self):
        value = 0
        for a in self.Xs_sent_emb:
            lst = []
            for b in self.Xs_sent_emb:
                distance=np.linalg.norm(a-b)
                lst.append(distance)
            value += sorted(lst)[1]
        return value/len(self.Xs_sent_emb)       
        
        
    #復元できない可能性ありそう

    def logistic_negative_sampling(self,target_sent,num=29):
        #target_sentの文章単位のインデックス取得
        index = self.Xs_sent.index(target_sent)
        #ブロック単位のインデックスを取得し，元タグを取得
        ori_sentence = self.Xs[self.sent2index[index]]["tag"]
        tag_index = [ i  for i in range(len(ori_sentence)) if ori_sentence[i] == 1 ]
        negative_sentences = []
        for i in range(len(self.Xs)):
            if len(tag_index) == sum([True if self.Xs[i]["tag"][j] == 0 else False for j in tag_index]): 
                negative_sentences.append(self.Xs[i]["sentence"])
            if len(negative_sentences) == num:
                break
        X = torch.cat([ self.model.encode(i,convert_to_tensor=True).unsqueeze(0) for i in [target_sent]+negative_sentences],dim=0)
        Y = [1] + [0]*len(negative_sentences)
        print(X)
        print(Y)
        lr = LogisticRegression() # ロジスティック回帰モデルのインスタンスを作成
        lr.fit(X, Y)
        return lr


    def predict(self,sentences:list,tag):
        return self.recommend(sentences,tag)
    
    def evaluate(self,test_Y,num=100,tag="タグ"):
        
        for i in tqdm.tqdm(range(1,6)):
            ans,suggest_num,not_suggest = 0,0,0
            true_lst = []
            false_lst = []
            for j in test_Y[i]:
                given_all_sentence = [self.Xs[index]["sentence"] for index in j ]
                given_tag_value = [self.Xs[index]["tag"] for index in j]
                #どのクラスのタグが与えられているかがわからない．
                true_y = set([ i for i,v in enumerate(zip(*given_tag_value)) if any(x==1 for x in v)])
#                 print("before:{}".format(true_y))
                suggest_index = self.recommend(j,tag)
#                 print("suggest_:{}".format(suggest_index))
                if suggest_index:
                    suggest_num += 1
                    suggest_sentence = self.Xs[suggest_index]["sentence"]
                    suggest_tag_value = self.Xs[suggest_index]["tag"]
                    pred_y = set([n for n, v in enumerate(suggest_tag_value) if v == 1])
#                     print("after:{}".format(pred_y))
                    if pred_y & true_y:
                        ans += 1
                        true_lst.append([given_all_sentence,suggest_sentence])
                    else:
                        false_lst.append([given_all_sentence,suggest_sentence])
                else:
                    not_suggest += 1
            print("The number of sentences gave by user {}".format(i)) 
            print("number of trials : {}, number of suggestion : {}".format(num,suggest_num))
            print("===========================")
            print("accuracy:{}" .format(ans/suggest_num))
