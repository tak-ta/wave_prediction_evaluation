#!/usr/bin/python
# -*- coding: Shift-JIS -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

#文字列に変数を埋め込む参考https://qiita.com/niwasawa/items/27641b803db31f93b8e6
#data_gsf = pd.read_csv('20211001/NPHAS_ISHK-2021100100.csv', header=None)

str_common_gsf = 'pre/NPHAS_ISHK-'
year = '2021'
month ='11'
date = '01'
file_ext = '00.csv'

print('{}{}{}{}{}'.format(str_common_gsf,year,month,date,file_ext))
data_gsf = pd.read_csv('{}{}{}{}{}'.format(str_common_gsf,year,month,date,file_ext), header=None)
print(data_gsf)

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
end = datetime.strptime('20211231', '%Y%m%d').date()
#end   = date.today() # 今日の日付

# ジェネレータを生成
gen = date_iterator_generator(begin, end)
print('gen: ' + str(gen))
"""
#日付を出力
for target in gen:
  print(target.strftime('%Y%m%d'))
"""

for i in gen:
    data_gsf = pd.read_csv('{}{}{}'.format(str_common_gsf,i.strftime('%Y%m%d'),file_ext), header=None)
    print(data_gsf.shape)