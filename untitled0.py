# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:49:58 2018

@author: pcc
"""

from draw import *
from CART import *

data = getData("data1.csv")
root = Node(data)
res=toList(root)

tree = res
while len(tree)!= 1:
    _,tree = chooseAlpha(tree)
    draw(tree)
    