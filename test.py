#!/usr/bin/python
# -*- coding: Shift-JIS -*-
#�g�Q���x�]���łł��邾���ėp�I�ȃt�@�C�����쐬����B���x�]���Ƃ���ɕK�v�ȑO�������܂Ƃ߂�B

#5/19 ���c�������Ɓ@�i�E�t�@�X�̐؂���Ɨ\��l�t�@�C���̓����Ƃ�RSME�v�Z

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import date, datetime, timedelta


#�O���[�o���@�i�p�[�T�[�Ƃ��ɂ������������̂��j
begin = datetime.strptime('20211001', '%Y%m%d').date()
end = datetime.strptime('20211223', '%Y%m%d').date()

PLACE = 'KAS'

observe_data_dir = 'nowphas_202205161057/'+PLACE+'/nowphas.txt'

observe_output_dir ='date_'+PLACE+'/' #���Ɠ��������ǁA�O�����̕ۑ���̈Ӗ��@
observe_head="date_"+PLACE+"/"

prediction_head="pre/NPHAS_"+PLACE+"-"

observe_ext = '.txt'
prediction_ext = '00.csv'

result_dir = './result/'
def date_iterator_generator(begin, end):
  # �I�����ƊJ�n���� timedelta ������������߂�
  # �I�������܂ނ悤��+1
  length = (end - begin).days + 1
  # 0����������̐��l�V�[�P���X
  for n in range(length):
    yield begin + timedelta(n)

def get_amount_prediction():
    #�\��l�t�@�C����3���ԗ\��ŁA8.5or8��������̂ŗ\��l�̐������z���Ԃ��B
    amount_prediction = []
    gen = date_iterator_generator(begin, end)
    for i in gen:
        data_gsf = pd.read_csv(prediction_head+'{}{}'.format(i.strftime('%Y%m%d'),prediction_ext), header=None)
        #print(data_gsf.shape)
        amount_prediction.append(data_gsf.shape[0])
    
    return amount_prediction

def make_preprocessed_observed_data():
    #�i�E�t�@�X����擾���Ă����ϑ��l�f�[�^��O��������B�\��l�̐��Ɗϑ��l�̒l�����킹��
    #load_merge_nowphas()
    #nkf_cut_nowphas()
    HGT_col = 2
    PER_col = 3 #nkf_cut�̎d���ɂ��

    data_nowphas = np.loadtxt(observe_data_dir,encoding="utf-8") #���O�ɉ��H�������̂��_�E�����[�h����B
    amount_prediction = get_amount_prediction()
    print("�ϑ��l��ǂݍ���ŁA�\��l�̍X�V�p�x�ɍ��킹�܂��B���ʂ�{}�Ɋi�[����܂�".format(observe_output_dir))
    gen = date_iterator_generator(begin, end)
    days = 0
    for i, pre_date in enumerate(gen):
        #print(pre_date.strftime('%Y%m%d'))
        #print(amount_prediction[i])
        nowphas2txt = []
        #print("days:",days)
        tmp = [0,0]
        for k in range(amount_prediction[i]-1): #header�̕�����
            #print(data_nowphas[k*9][HGT_col],data_nowphas[k*9][PER_col])\
            #�G���[��������
            if data_nowphas[k*9+days*72][0]==0:  #0 �̓t���O
                tmp = [data_nowphas[k*9+days*72][HGT_col],data_nowphas[k*9+days*72][PER_col]]
            else: #�t���O���ȏ�̏ꍇ�A�O�̒l���g������
                a="hazure"
            
            nowphas2txt.append(tmp)
        #print(np.array(nowphas2txt))
        nowphas2txt_np = np.array(nowphas2txt)
        np.savetxt(observe_output_dir+'{}.txt'.format(pre_date.strftime('%Y%m%d')), nowphas2txt_np)
        days += 1

def RMSE_calc(pre,data): #numpy�̍s��
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