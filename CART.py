# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:00:00 2018

@author: xzt

CART TREE
"""
import pandas as pd
import math

#读取filename里的data，此处把ID列去掉
def getData(filename):
    #通过pd.read_csv读取csv文件，encoding编码是“gbk”，sep/delimiter分割符是“\t”
    data = pd.read_csv(filename, sep="\t+", encoding="gbk")
    #去掉ID列,通过df.drop实现，其中axis=1指定列，inplace表示修改原数据
    data.drop('ID', axis=1, inplace=True)
    #返回读取的数据
    return data

#将data，根据attr是否在value里，进行分割。
def splitData(data, attr, value):
    #如果是值判断，直接 == 就行，在list里用函数isin
    data1 = data[data[attr].isin(value)]
    #同理，取反，在前面加上“~”符号即可
    #这个符号是取反 ~True = -2 ~False =-1,这里可以这么使用
    data2 = data[~data[attr].isin(value)]
    #使用attr分割完后，删除attr
    data1 = data1.drop(attr, axis=1).copy()
    data2 = data2.drop(attr, axis=1).copy()
    return data1,data2

#多数人投票
def majVote(data):
    #labels是类列，df.iloc[:,:]取数，前面按行，后面按列
    labels = data.iloc[:,-1]
    #df.value_counts()可以实现R语言table()的功能
    counts = labels.value_counts()
    #df.index返回的名字，index[0]取得是频数最多的
    result = counts.index[0]
    return result

#计算Gini系数
def calGini(data):
    #labels是类列，df.iloc[:,:]取数，前面按行，后面按列
    labels = data.iloc[:,-1]
    #df.value_counts()可以实现R语言table()的功能
    #df.count()可以计数
    prob = labels.value_counts()/labels.count()
    #遗留一个问题，行累加，如何用函数来实现自己想要的累加
    Gini = 1- (prob**2).sum()
    return Gini

#对于一个属性，此处只假设属性是离散值，需要选择最优二分
'''
连续值如果二分是不是太……浪费了？？？ Note1
'''
def binSplit(data, attr):
    #df.unique 可以取集合
    toChoose = data[attr].unique()
    #Gini系数一定比1小，所以设置为1
    bestGini = 1
    bestValue =[]
    #这个循环将一堆集合分成两份
    '''
    使用itertool模块,itertools.combinations(i,j)可返回i中长度为j的所有可能tuple
    在此处，有一半是重复的，所以只需要取一半即可
    '''
    values =[]
    from itertools import combinations
    for i in range(1,toChoose.size):
        num = math.ceil(toChoose.size/2) 
        values.extend(list(combinations(toChoose[0:num],i)))
    #对于每一种分类，计算Gini，取最小的
    for value in values:
        data1,data2 = splitData(data, attr, value)
        newGini = len(data1)/len(data)*calGini(data1)+ \
                    len(data2)/len(data)*calGini(data2)
        #如果更小就替换
        if bestGini>newGini:
            bestGini = newGini
            bestValue = value
    return  bestGini,bestValue

#对于一个数据集，需要选择最优属性进行划分        
def bestSplit(data):
    bestGini = 1
    #df.shaple[0] 为行数，1为列数
    for i in range(0,data.shape[1]-1):
        tempGini,tempValue = binSplit(data,data.columns[i])
        #如果更小就替换
        if tempGini < bestGini:
            bestGini =tempGini
            bestValue =tempValue
            bestAttr = data.columns[i]          
    return bestGini,bestValue,bestAttr
"""
结点类，保存了绝大部分信息，方便查看
"""
class Node:
    #初始化结点信息，只需要他的深度以及父结点
    def __init__(self, data, parent=None,depth=1):
        self.parent = parent
        self.data = data
        self.depth =depth
        #画图用
        self.x = 0
        self.y =0
    
    #设置左结点    
    def setLeft(self,Node):
        self.left = Node
    
    #设置右结点    
    def setRight(self,Node):
        self.right = Node
    
    #生成左和右结点
    def grow(self):
        #当没有属性，进行majVote
        if self.data.shape[1] == 1:
            self.type ="LEAF"
            self.label = majVote(self.data)
            return
        #类标签一致，返回类标签
        if len(self.data.iloc[:,-1].value_counts())==1 :
            self.type ="LEAF"
            label = self.data.iloc[:,-1].value_counts().index[0]
            self.label = label
            return
        #否则就是普通结点
        else:
            self.type = "NODE"
        _,self.value,self.attr = bestSplit(self.data)
        data1,data2 = splitData(self.data, self.attr, self.value)
        self.setLeft(Node(data1,self,self.depth+1))
        self.setRight(Node(data2,self,self.depth+1))
    
    #输出结点信息，测试用    
    def show(self):
        if self.type =="LEAF":
            print(self.data,self.label)
        else:
            print(self.data,self.attr,self.value)
            
#通过层次遍历，将所有结点放入list中，方便进行可视化
def toList(root):
    #queue队存放仍需要分裂的结点
    queue = [root]
    #res保存层序遍历的结果
    res = [root]
    while len(queue)!=0 :
        node = queue[0]
        node.grow()
        #如果是叶节点，不用分裂
        if node.type == "LEAF":
            queue.pop(0)
            continue
        #否则，queue放入左右结点
        else:
            queue.append(node.left)
            queue.append(node.right)
            res.append(node.left)
            res.append(node.right)
            queue.pop(0)
    return res

#预测函数
def predict(root,toPredict):
    node = root
    #一层一层分下去，直到叶节点
    while node.type !="LEAF":
        #如果预测数据的值以往没出现过 （也就是数据为空 则返回父节点的多数人投票结果
        if toPredict[node.attr] not in root.data[node.attr].unique():
            return majVote(node.parent.data)
        #满足条件，就通往左结点
        elif toPredict[node.attr] in node.value:
            toPredict.drop(node.attr,inplace=True)
            node = node.left
        #否则通往右结点
        else:
            toPredict.drop(node.attr,inplace=True)
            node = node.right
    return node.label    
            

data = getData("data1.csv")
root = Node(data)
res=toList(root)
depth =res[-1].depth
m =predict(root,root.data.iloc[20])