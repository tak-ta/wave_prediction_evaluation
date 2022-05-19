#!/usr/bin/python
# -*- coding: Shift-JIS -*-
#波浪予測の精度評価をする
#一旦、2021年10月1日のデータで行う。　場所は石狩

"""
やりたいこと
・グラフへのプロットの関数を作る、X、Yを投げたら描画、オプションも指定可のを作る
・前処理部も自動化したい
    ・今の所nkfが手打ち
・データはdfで操る？
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HGT_col = 2
PER_col = 3

#data = np.loadtxt('20211001/NPHAS_ISHK-2021100100.txt',encoding="utf-8")
#データ読み込み
data_nowphas = np.loadtxt('20211001/NPHAS_ISHK-2021100100_nkf.txt')
data_gsf = pd.read_csv('20211001/NPHAS_ISHK-2021100100.csv', header=None)
#data_gsf =np.genfromtxt('20211001/NPHAS_ISHK-2021100100.csv',delimiter=',')

print(data_nowphas.shape)
print(data_gsf)
#プロットデータを作る
nowphas_SGFHGT =[]
nowphas_SGFPER =[]
gsf_SGFHGT =[]
gsf_SGFPER =[]

print(data_gsf.iat[0,3])

tmp_HGT = 0
tmp_PER = 0

for i in range(0,data_gsf.shape[0]):
    if data_nowphas[i*9][HGT_col]==99.99:
        nowphas_SGFHGT.append(tmp_HGT)
        nowphas_SGFPER.append(tmp_PER)
    else:
        nowphas_SGFHGT.append(data_nowphas[i*9][HGT_col])
        nowphas_SGFPER.append(data_nowphas[i*9][PER_col])
        tmp_HGT = data_nowphas[i*9][HGT_col]
        tmp_PER = data_nowphas[i*9][PER_col]
    gsf_SGFHGT.append(data_gsf.iat[i,HGT_col])
    gsf_SGFPER.append(data_gsf.iat[i,PER_col])
   

print(len(nowphas_SGFHGT))
print(len(nowphas_SGFPER))
print(len(gsf_SGFHGT))
print(len(gsf_SGFPER))

#print(nowphas_SGFHGT)
#print(nowphas_SGFPER)
#print(gsf_SGFHGT)
#print(gsf_SGFPER)

X = range(data_gsf.shape[0])




fig, ax1 = plt.subplots(1,1)
ax1.set_title('hyouka')
ax1.plot(X,nowphas_SGFHGT,'C0') #C0は青
ax1.plot(X,gsf_SGFHGT,'C0',linestyle="dotted")

ax2 = ax1.twinx()
ax2.plot(X,nowphas_SGFPER,'C1')
ax2.plot(X,gsf_SGFPER,'C1',linestyle="dotted")

ax1.legend()
ax2.legend()
ax1.set_ylabel("high[m]", size = 14)
ax2.set_ylabel("T[s]", size = 14)
plt.show()