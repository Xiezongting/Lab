# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:54:40 2018

@author: pcc

pandans入门
"""
import pandas as pd

#导入数据
df = pd.read_csv("data1.csv", header=0, encoding ='gbk', delimiter="\t")

#查看前五行
df.head(5)

#查看最后五行
df.tail(5)

#查看列名，或者用list更改列名
df.columns = []

#查看总行数
len(df)

#一个简单的统计数据
df["age"].describe()

#简单的调取列，等价
df["age"]
df.age

#布尔过滤 boolean masking
df.income == "high"
df[df.income == "high"]

#混合过滤
'''
必须要用 & 否则会引起操作顺序的错误
字符串函数同样适合~
'''
df[df.income == "low " & df.age =="31-40"]
df[df.age.str.startswith(">")]

#读取行 如果行标签的数字
#integer loc  
df.iloc[10]

#默认是数字索引 下面演示更换
#吃惊 更换后 age就没了~！！
df = df.set_index(["age"])

#更改后就不是数字啦，基于字符串查询
df.loc["31-40"]

#通用的,注意虽然快，但有不稳定性
df.ix[3]

#很有用的 对索引排序
df.sort_index(ascending=False).head()

#将索引变回去
df = df.reset_index(drop = False)
df = df.reset_index()
df.head()

#取列
df.iloc[:,1:4]

def getFirst(word):
    return word[0]

#对一类整体运用函数
df.age =df.age.apply(getFirst)

#对整个df运用函数
df = df.applymap(getFirst)

#groupby
df.groupby(df.age).max()
df.groupby([df.age,df.income]).max()

#unstack
x = df.groupby([df.age,df.income]).max()
x.unstack()

#数据透视表 
'''
此处空缺 需要加强学习
'''

#h合并两个datafr，通过on参数可以选定列
df.merge(a,b)


