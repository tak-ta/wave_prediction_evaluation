#!/usr/bin/python
# -*- coding: Shift-JIS -*-
#波浪の精度評価、３ヶ月分

"""
make_nowphas_txtで作ったdate/~.txtを読み込んでRMSEを計算したりする
期間は2021/10/01 ~ 2021/12/31 (12/23まで)
使うデータは date と　pre

やること
外れ値の処理、多分make~txtの方
プロッティング
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import date, datetime, timedelta
HGT_col = 2
PER_col = 3


def date_iterator_generator(begin, end):
  # 終了日と開始日の timedelta から日数を求める
  # 終了日を含むように+1
  length = (end - begin).days + 1
  # 0から日数分の数値シーケンス
  for n in range(length):
    yield begin + timedelta(n)


# 開始日・終了日
begin = datetime.strptime('20211001', '%Y%m%d').date()
end = datetime.strptime('20211223', '%Y%m%d').date()
#end   = date.today() # 今日の日付

# ジェネレータを生成
gen = date_iterator_generator(begin, end)
print('gen: ' + str(gen))

#pre,dateの共通読み込み部分設定
TxtNameStr="date/"
CsvNameStr="pre/NPHAS_ISHK-"

#
RMSE_HGT = []
RMSE_PER = []
def RMSE_calc(pre,data): #numpyの行列
    rmse = ((pre-data)*(pre-data)).sum()
    return np.sqrt(rmse/pre.shape[0])

chk_date = '20211001'

for i in gen:
   
    data_nowphas = np.loadtxt(TxtNameStr+str(i.strftime('%Y%m%d'))+'.txt')
    data_gsf = pd.read_csv(CsvNameStr+str(i.strftime('%Y%m%d'))+'00.csv')
    print(data_nowphas.shape)
    print(data_gsf.iat[0,HGT_col])
    print(data_nowphas[:,0])
    if i.strftime('%Y%m%d')==chk_date:
        data_nowphas_chk = data_nowphas
        data_gsf_chk = data_gsf    
    RMSE_HGT.append(RMSE_calc(data_gsf['SGFHGT'].values,data_nowphas[:,0]))
    RMSE_PER.append(RMSE_calc(data_gsf['SGFPER'].values,data_nowphas[:,1]))
    

print(RMSE_HGT)
print(RMSE_PER)

#X = range(len(RMSE_HGT))
X=[]

gen = date_iterator_generator(begin, end)

for i in gen: #str(i.strftime('%Y%m%d'))
    X.append(i)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111) 


ax.plot(X, RMSE_HGT,'C0', label='HGT')
ax.plot(X, RMSE_PER,'C1', label='PER')
ax.set_ylabel("RMSE", size = 14)
plt.legend()

plt.show()

X1 = range(data_gsf_chk.shape[0])
print(X1)
_, ax1 = plt.subplots(1,1)
ax1.set_title('data_plot'+chk_date)
ax1.plot(X1,data_nowphas_chk[:,0],'C0') 
ax1.plot(X1,data_gsf_chk['SGFHGT'],'C0',linestyle="dotted")
ax1.set_xlabel("plot per 3hours(8.5days)", size = 14)
ax2 = ax1.twinx()
ax2.plot(X1,data_nowphas_chk[:,1],'C1')
ax2.plot(X1,data_gsf_chk['SGFPER'],'C1',linestyle="dotted")

ax1.legend()
ax2.legend()
ax1.set_ylabel("high[m]", size = 14)
ax2.set_ylabel("T[s]", size = 14)
#plt.show()
plt.savefig('data_plot_10days'+chk_date)

os._exit(0)



#data = np.loadtxt('20211001/NPHAS_ISHK-2021100100.txt',encoding="utf-8")
#繝?繝ｼ繧ｿ隱ｭ縺ｿ霎ｼ縺ｿ
data_nowphas = np.loadtxt('20211001/NPHAS_ISHK-2021100100_nkf.txt')
data_gsf = pd.read_csv('20211001/NPHAS_ISHK-2021100100.csv', header=None)
#data_gsf =np.genfromtxt('20211001/NPHAS_ISHK-2021100100.csv',delimiter=',')

print(data_nowphas.shape)
print(data_gsf)
#繝励Ο繝?繝医ョ繝ｼ繧ｿ繧剃ｽ懊ｋ
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
ax1.plot(X,nowphas_SGFHGT,'C0') #C0縺ｯ髱?
ax1.plot(X,gsf_SGFHGT,'C0',linestyle="dotted")

ax2 = ax1.twinx()
ax2.plot(X,nowphas_SGFPER,'C1')
ax2.plot(X,gsf_SGFPER,'C1',linestyle="dotted")

ax1.legend()
ax2.legend()
ax1.set_ylabel("high[m]", size = 14)
ax2.set_ylabel("T[s]", size = 14)
plt.show()