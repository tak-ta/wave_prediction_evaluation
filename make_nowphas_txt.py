#!/usr/bin/python
# -*- coding: Shift-JIS -*-

from os import lseek
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

HGT_col = 2
PER_col = 3



#nkf -w H611e.s2112.txt | cut -c 15-37  > nowphas_2112.txt 
#このコマンドでnowphasをエンコードかつ切り取り、手打ちなので自動化も考えたい

"""
str_common = 'nowphas_202205161057/ISHK/nowphas_'
year = '21'
month = '10'
file_ext = '.txt'
print('{}{}{}{}'.format(str_common,year,month,file_ext))
data_nowphas = np.loadtxt('{}{}{}{}'.format(str_common,year,month,file_ext),encoding="utf-8")
"""

data_nowphas = np.loadtxt('nowphas_202205161057/ISHK/nowphas.txt',encoding="utf-8")

# date オブジェクトのイテレータを返すジェネレータ関数
# 開始日: begin
# 終了日: end
#参考　https://qiita.com/niwasawa/items/40257b70c8560d19f0a3


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
#end = date.today() # 今日の日付

# ジェネレータを生成
gen = date_iterator_generator(begin, end)
print('gen: ' + str(gen))

#CSVを読み込んで、データ数を取得
str_common_gsf = 'pre/NPHAS_ISHK-'
file_ext_gsf = '00.csv'
csv_data = []
for i in gen:
    data_gsf = pd.read_csv('{}{}{}'.format(str_common_gsf,i.strftime('%Y%m%d'),file_ext_gsf), header=None)
    #print(data_gsf.shape)
    csv_data.append(data_gsf.shape[0])
print(",",len(csv_data))
#datetimeごとにcsvのデータ数（８.5日分）をTXTに出力する。
#3時間ごとのデータを取るには９飛ばし
#一日8個欲しい、０時から21時時 つまり８個×８日＋5個で69個（たまに67もある）


#作業メモ　全日程のtxtファイル作成、のために何個飛ばせばいいか考える。　外れ値処理
#多分７２

# ジェネレータを生成
gen = date_iterator_generator(begin, end)
days = 0
for i, pre_date in enumerate(gen):
    print(pre_date.strftime('%Y%m%d'))
    print(csv_data[i])
    tmp_HGT = 0
    tmp_PER = 0
    nowphas2txt = []
    print("days:",days)
    tmp = [0,0]
    for k in range(csv_data[i]-1): #headerの分抜く
        #print(data_nowphas[k*9][HGT_col],data_nowphas[k*9][PER_col])\
        #外れ値処理書く
        if data_nowphas[k*9+days*72][0]==9999:  #0 はフラグ
            a="boke"
        else: #外れ値の場合こっちを使う
            tmp = [data_nowphas[k*9+days*72][HGT_col],data_nowphas[k*9+days*72][PER_col]]
        
        nowphas2txt.append(tmp)
    print(np.array(nowphas2txt))
    nowphas2txt_np = np.array(nowphas2txt)
    np.savetxt('./date/{}.txt'.format(pre_date.strftime('%Y%m%d')), nowphas2txt_np)
    days += 1

"""
memo
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
    """