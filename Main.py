# -*- coding: utf-8 -*-

#def py2neodb():
#    test_graph = Graph(
#    'http://59.110.243.182:7474',
#    username='neo4j',
#    password='ysx714454'
#    )
#    return test_graph#
#

#def keywords(keywords):
#    test_graph = py2neodb()
#    find_node  = test_graph.run(
#        "match(n) where n.name =~'%s.*' return \
#        n.name,n.uuid limit 5"%(keywords))
#    if find_node:
#        return list(find_node) #
#

#def path(entity1,entity2):
#    test_graph = py2neodb()
#    find_path = test_graph.run(
#        'MATCH (p1{name:"%s"}),(p2{name:"%s"}),\
#        p=shortestpath((p1)-[r*..10]-(p2)) \
#        return r,p1.uuid,p2.uuid'%(entity1,entity2))
#    if find_path:
#        return list(find_path)#

#def net(entity,limit_num):
#    limit_num = str(limit_num)
#    test_graph = py2neodb()
#    find_path = test_graph.run(
#        'MATCH (p1{ name:"%s"})<-[r]->(p2) \
#        RETURN r,p1.uuid,p2.uuid limit %s'%(entity,limit_num))
#    if find_path:
#        return list(find_path)
from urllib import response

from scipy import spatial
from transformers import GPT2Tokenizer
import logging
from transformers import GPT2LMHeadModel
from torch.autograd import Variable
import time
import torch
from dns import tokenizer
from py2neo import Graph,Node,Relationship,NodeMatcher
#版本说明：Py2neo v4
class Neo4j_Handle():
    graph = None
    matcher = None
    def __init__(self):
        self.graph = Graph("bolt: // localhost:7687", username="neo4j", password="ysx714454")
        self.matcher = NodeMatcher(self.graph)

    #实体查询，用于命名实体识别：馆名+类型+规格
    def matchEntityItem(self,value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        return answer

    def matchRelatedEntity(self,value):
        answer  = self.graph.run(
            "match(n) where n.name =~'%s.*' return n.name,n.uuid limit 5"%(value)).data()
        if answer:
            return list(answer)

    def matchShortestPath(self,entity1,entity2):
        answer = self.graph.run('MATCH (p1{name:"%s"}),(p2{name:"%s"}),p=shortestpath((p1)-[r*..10]-(p2)) \
        return r,p1.uuid,p2.uuid'%(entity1,entity2))
        if answer:
            return list(answer.data())

    def matchEntityNets(self,entity,limit_num):
        limit_num = str(limit_num)
        answer = self.graph.run('MATCH (p1{ name:"%s"})<-[r]->(p2) RETURN r,p1.uuid,p2.uuid limit %s'%(entity,limit_num))
        if answer:
            return list(answer)

    #实体查询
    def getEntityRelationbyEntity(self,value):
        #查询实体：不考虑实体类型，只考虑关系方向
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN rel,entity2").data()
        if(len(answer) == 0):
            #查询实体：不考虑关系方向
            answer = self.graph.run("MATCH (entity1) - [rel] - (entity2)  WHERE entity1.name = \"" + value + " \" RETURN rel,entity2").data()
        #print(answer)
        return answer

    #关系查询:实体1
    def findRelationByEntity1(self,entity1):
        #基于馆名查询
        answer = self.graph.run("MATCH (n1{name:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\""+entity1+" \"})- [rel] - (n2) RETURN n1,rel,n2" ).data()
        return answer
    #关系查询：实体2
    def findRelationByEntity2(self,entity1):
        #基于类型
        answer = self.graph.run("MATCH (n1)<- [rel] - (n2{name:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：实体1+关系
    def findOtherEntities(self,entity,relation):
        print("MATCH (n1{name:\"" + entity + "\"})- [rel:`"+relation+"`}] -> (n2) RETURN n1,rel,n2")
        answer = self.graph.run("MATCH (n1{name:\"" + entity + "\"})- [rel:`"+relation+"`] -> (n2) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：关系+实体2
    def findOtherEntities2(self,entity,relation):
        print("findOtherEntities2==")
        print(entity,relation)
        answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:Bank {name:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:Serise {name:\"" + entity + " \"}) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：实体1+实体2(注意Entity2的空格）
    def findRelationByEntities(self,entity1,entity2):
        #类型 + 类型
        answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            # 馆名 + 系列
            answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Serise{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            # 系列 + 馆名
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            # 系列 + 系列
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel] -> (n2:Serise{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        return answer

    #查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self,entity1,relation,entity2):
        answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Bank{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Serise{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Bank{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Serise{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()

        return answer

import random

import openai

from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path="/static")



# -*- coding: utf-8 -*-
import os
import urllib
import re
import time
from bs4 import BeautifulSoup
import requests

from Trivia.QA.Tools.Html_Tools import get_html_baike

headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}


def get_info(basicInfo_block):
    info = {}

    for bI_LR in basicInfo_block.contents[1:3]:
        for bI in bI_LR:
            if bI.name == None:
                continue
            ##print(bI.name)
            ##print(bI.string)
            if bI.name == 'dt':
                # 获取属性名
                for bi in bI.contents:
                    attrName = bi.string.strip().replace(u" ", u"")
            elif bI.name == 'dd':
                info[attrName] = bI.contents
    return info

@app.route("/answer")
def answer():
    question = request.args.get("q", "")
    # 在这里进行问题处理和回答的生成
    # Replace YOUR_API_KEY with your actual API key
    openai.api_key = "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"
    # openai.api_key = "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"

    # Set up the prompt and model parameters
    prompt = question
    print(len(prompt))
    # 问题长度超过100个字也采用chatGPT补充回答的形式进行问题回复
    if len(prompt) <= 100:
        prompt += "Just answer the question. No additional information is required."
        # print(random.randint(50,80))
    # else:
        #print(random.randint(10, 50))

    model_engine = "text-davinci-003"
    # model_engine = "gpt-3.5-turbo"

    # Call the API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        # 随机性
        temperature=0.2,
        max_tokens=2000
    )

    # Extract the response text
    text = response.choices[0].text.strip()
    # print(len(prompt))
    # time.sleep(2)
    return jsonify({"answer": f"回答：{text}"})

def answer2():
    text = request.args.get("q", "")
    # 在这里进行问题处理和回答的生成

    # Set up the prompt and model parameters
    prompt = text
    print(len(prompt))

    # Extract the response text
    indexed_tokens = tokenizer.encode(text)
    tokens_tensor = torch.tensor([indexed_tokens])
    total_predicted_text = text
    text = response.choices[0].text.strip()
    # print(len(prompt))
    # time.sleep(2)
    # 余弦相似度
    cos_sim = 1 - spatial.distance.cosine(text, indexed_tokens)
    # print(int(cos_sim * 100))
    if int(cos_sim * 100 >= 70):
        return jsonify({"answer": f"回答：{text}"})
    else:
        answer()


def query(entity, attr):
    """
    发起查询
    :param entity: 询问实体
    :param attr: 询问属性
    """
    soup = get_html_baike("http://google.com/item/" + entity)
    basicInfo_block = soup.find(class_='basic-info cmn-clearfix')
    if not basicInfo_block:
        return ''
    else:
        info = get_info(basicInfo_block)
        if info.get(attr):
            return info[attr]
        else:
            attr_list = re.T.load_baikeattr_name(
                os.path.dirname(os.path.split(os.path.realpath(__file__))[0]) + '/resources/Attribute_name.txt')

    ##print(basicInfo_block)

@app.route("/")
def index():
    return app.send_static_file("index.html")

def load_synonyms_word_inattr(word, synsdic, attr):
    fr = open(synsdic, 'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                    tar_word = w
                    break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return tar_word

def load_baikeattr_name(attrdic):
    fr = open(attrdic, 'r')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return attr


if __name__ == "__main__":
    app.run(debug=True)