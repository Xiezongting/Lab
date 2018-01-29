# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:43:45 2018

@author: pcc
"""
#导入tkinter包进行可视化
from tkinter import *
from CART import *

#画结点，此处需要坐标以及文本信息
def drawNode(x,y,text):
    canvas.create_rectangle(x-rec_hfwidth,y-rec_hfheight,x+rec_hfwidth,y+rec_hfheight)
    canvas.create_text(x,y,text=text)

#画叶子，此处需要坐标及文本信息    
def drawLeaf(x,y,text):
    canvas.create_oval(x-oval_hfwidth,y-oval_hfheight,x+oval_hfwidth,y+oval_hfheight)
    canvas.create_text(x,y,text=text)

#画线，此处需要坐标已经文本信息
def drawLine(x,y,text,xgap):
    canvas.create_line(x,y+rec_hfheight,x-xgap,y+ygap+rec_hfheight)
    canvas.create_text(x-xgap/2,y+ygap/2+rec_hfheight,text=text)
    canvas.create_line(x,y+rec_hfheight,x+xgap,y+ygap+rec_hfheight)
    canvas.create_text(x+
                       xgap/2,y+ygap/2+rec_hfheight,text="else")
 
#从写的CART.py中生成决策树，可以得到存储所有结点的list以及深度depth
#data = getData("data1.csv")
from pandas import read_csv
data = read_csv("xigua.csv",sep=" +",encoding="gbk",engine="python")
data.drop("ID",inplace =True,axis=1)
root = Node(data)
res=toList(root)
depth =res[-1].depth

'''
请在此处设置参数：
rec_hfwidth = oval_hfwidth :结点宽度的一半，因为坐标计算时增量都为长度的一半
rec_hfheight = oval_hfheight:结点高度的一半，理由同上
ygap:结点之间y轴即高度的间隔
xgap:最底层结点之间x轴即宽度的间隔 tips:xgap>rec_hfwidth
'''
rec_hfwidth=oval_hfwidth = 30
rec_hfheight=oval_hfheight=20
ygap =50
xgap= 40
    
#初始化tkinter画布
tk = Tk()
tk.title("决策树可视化")
width = (2**depth)*xgap
height = (depth-1)*(2*rec_hfheight+ygap) + ygap
canvas = Canvas(tk,width=2**depth*xgap,height=500)
canvas.pack()


#将结果集每一个结点都画
while len(res)!= 0:
    node = res[0]
    #根节点的x为宽度的一般，y随意
    if node == root:
        node.x = width/2
        node.y =30
    #左结点为父节点的x- △xgap，该值自底向上加倍
    elif node == node.parent.left:
        node.x = node.parent.x - 2**(depth-node.depth)*xgap
        node.y = node.parent.y + 2*rec_hfheight+ygap
    #右结点同理
    else:
        node.x = node.parent.x + 2**(depth-node.depth)*xgap
        node.y = node.parent.y + 2*rec_hfheight+ygap
    #如果是结点，就画Node，否则画Leaf
    if node.type =="NODE":
        drawNode(node.x,node.y,node.attr)
        drawLine(node.x,node.y,",".join(node.value),2**(depth-1-node.depth)*xgap)
    else:
        drawLeaf(node.x,node.y,node.label)
    res.pop(0)

canvas.mainloop()


