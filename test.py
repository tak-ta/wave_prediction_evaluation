#!/usr/bin/python
# -*- coding: Shift-JIS -*-
#波浪精度評価でできるだけ汎用的なファイルを作成する。精度評価とそれに必要な前処理もまとめる。

#5/19 やり残したこと　ナウファスの切り取りと予報値ファイルの日ごとのRSME計算

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import date, datetime, timedelta


#グローバル　（パーサーとかにした方がいいのか）
begin = datetime.strptime('20211001', '%Y%m%d').date()
end = datetime.strptime('20211223', '%Y%m%d').date()

PLACE = 'KAS'

observe_data_dir = 'nowphas_202205161057/'+PLACE+'/nowphas.txt'

observe_output_dir ='date_'+PLACE+'/' #下と同じだけど、前処理の保存先の意味　
observe_head="date_"+PLACE+"/"

prediction_head="pre/NPHAS_"+PLACE+"-"

observe_ext = '.txt'
prediction_ext = '00.csv'

result_dir = './result/'
def date_iterator_generator(begin, end):
  # 終了日と開始日の timedelta から日数を求める
  # 終了日を含むように+1
  length = (end - begin).days + 1
  # 0から日数分の数値シーケンス
  for n in range(length):
    yield begin + timedelta(n)

def get_amount_prediction():
    #予報値ファイルが3時間予報で、8.5or8日分あるので予報値の数を持つ配列を返す。
    amount_prediction = []
    gen = date_iterator_generator(begin, end)
    for i in gen:
        data_gsf = pd.read_csv(prediction_head+'{}{}'.format(i.strftime('%Y%m%d'),prediction_ext), header=None)
        #print(data_gsf.shape)
        amount_prediction.append(data_gsf.shape[0])
    
    return amount_prediction

def make_preprocessed_observed_data():
    #ナウファスから取得してきた観測値データを前処理する。予報値の数と観測値の値を合わせる
    #load_merge_nowphas()
    #nkf_cut_nowphas()
    HGT_col = 2
    PER_col = 3 #nkf_cutの仕方による

    data_nowphas = np.loadtxt(observe_data_dir,encoding="utf-8") #事前に加工したものをダウンロードする。
    amount_prediction = get_amount_prediction()
    print("観測値を読み込んで、予報値の更新頻度に合わせます。結果は{}に格納されます".format(observe_output_dir))
    gen = date_iterator_generator(begin, end)
    days = 0
    for i, pre_date in enumerate(gen):
        #print(pre_date.strftime('%Y%m%d'))
        #print(amount_prediction[i])
        nowphas2txt = []
        #print("days:",days)
        tmp = [0,0]
        for k in range(amount_prediction[i]-1): #headerの分抜く
            #print(data_nowphas[k*9][HGT_col],data_nowphas[k*9][PER_col])\
            #エラー処理書く
            if data_nowphas[k*9+days*72][0]==0:  #0 はフラグ
                tmp = [data_nowphas[k*9+days*72][HGT_col],data_nowphas[k*9+days*72][PER_col]]
            else: #フラグが以上の場合、前の値を使う処理
                a="hazure"
            
            nowphas2txt.append(tmp)
        #print(np.array(nowphas2txt))
        nowphas2txt_np = np.array(nowphas2txt)
        np.savetxt(observe_output_dir+'{}.txt'.format(pre_date.strftime('%Y%m%d')), nowphas2txt_np)
        days += 1

def RMSE_calc(pre,data): #numpyの行列
    rmse = ((pre-data)*(pre-data)).sum()
    return np.sqrt(rmse/pre.shape[0])

def get_evaluation_HGTPER():
    gen = date_iterator_generator(begin, end)
    RMSE_HGT = []
    RMSE_PER = []
    for i in gen:
        data_nowphas = np.loadtxt(observe_head+str(i.strftime('%Y%m%d'))+observe_ext)
        data_gsf = pd.read_csv(prediction_head+str(i.strftime('%Y%m%d'))+prediction_ext)
        RMSE_HGT.append(RMSE_calc(data_gsf['SGFHGT'].values,data_nowphas[:,0]))
        RMSE_PER.append(RMSE_calc(data_gsf['SGFPER'].values,data_nowphas[:,1]))
    
    return RMSE_HGT,RMSE_PER

def plot_RMSE(RMSE_HGT,RMSE_PER,result_name):
    gen = date_iterator_generator(begin, end)
    X=[]
    for i in gen: #str(i.strftime('%Y%m%d'))
        X.append(i)

    fig = plt.figure(figsize=(12, 8))
    ax  = fig.add_subplot(111) 
    ax.plot(X, RMSE_HGT,'C0', label='HGT')
    ax.plot(X, RMSE_PER,'C1', label='PER')
    ax.set_ylabel("RMSE", size = 14)
    plt.legend()

    plt.savefig(result_name)

def plot_oneday(input_oneday='20211001'):
   
    data_nowphas = np.loadtxt(observe_head+str(input_oneday)+observe_ext)
    data_gsf = pd.read_csv(prediction_head+str(input_oneday)+prediction_ext)

    X1 = range(data_gsf.shape[0])
    print(X1)
    _, ax1 = plt.subplots(1,1)
    ax1.set_title('data_plot'+str(input_oneday))
    ax1.plot(X1,data_nowphas[:,0],'C0') 
    ax1.plot(X1,data_gsf['SGFHGT'],'C0',linestyle="dotted")
    ax1.set_xlabel("plot per 3hours(8.5days)", size = 14)
    ax2 = ax1.twinx()
    ax2.plot(X1,data_nowphas[:,1],'C1')
    ax2.plot(X1,data_gsf['SGFPER'],'C1',linestyle="dotted")

    ax1.legend()
    ax2.legend()
    ax1.set_ylabel("high[m]", size = 14)
    ax2.set_ylabel("T[s]", size = 14)
    #plt.show()
    plt.savefig(result_dir+'data_plot_10days_'+PLACE+"_"+str(input_oneday)+'.png')

if __name__ == '__main__':
    
    print(get_amount_prediction())
    make_preprocessed_observed_data()
    RMSE_HGT,RMSE_PER = get_evaluation_HGTPER()
    plot_RMSE(RMSE_HGT,RMSE_PER,result_name=result_dir+'RMSE_'+PLACE+'_HGTPER.png')
    plot_oneday(input_oneday='20211115')