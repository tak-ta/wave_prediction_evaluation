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
#���̃R�}���h��nowphas���G���R�[�h���؂���A��ł��Ȃ̂Ŏ��������l������

"""
str_common = 'nowphas_202205161057/ISHK/nowphas_'
year = '21'
month = '10'
file_ext = '.txt'
print('{}{}{}{}'.format(str_common,year,month,file_ext))
data_nowphas = np.loadtxt('{}{}{}{}'.format(str_common,year,month,file_ext),encoding="utf-8")
"""

data_nowphas = np.loadtxt('nowphas_202205161057/ISHK/nowphas.txt',encoding="utf-8")

# date �I�u�W�F�N�g�̃C�e���[�^��Ԃ��W�F�l���[�^�֐�
# �J�n��: begin
# �I����: end
#�Q�l�@https://qiita.com/niwasawa/items/40257b70c8560d19f0a3


def date_iterator_generator(begin, end):
  # �I�����ƊJ�n���� timedelta ������������߂�
  # �I�������܂ނ悤��+1
  length = (end - begin).days + 1
  # 0����������̐��l�V�[�P���X
  for n in range(length):
    yield begin + timedelta(n)


# �J�n���E�I����
begin = datetime.strptime('20211001', '%Y%m%d').date()
end = datetime.strptime('20211223', '%Y%m%d').date()
#end = date.today() # �����̓��t

# �W�F�l���[�^�𐶐�
gen = date_iterator_generator(begin, end)
print('gen: ' + str(gen))

#CSV��ǂݍ���ŁA�f�[�^�����擾
str_common_gsf = 'pre/NPHAS_ISHK-'
file_ext_gsf = '00.csv'
csv_data = []
for i in gen:
    data_gsf = pd.read_csv('{}{}{}'.format(str_common_gsf,i.strftime('%Y%m%d'),file_ext_gsf), header=None)
    #print(data_gsf.shape)
    csv_data.append(data_gsf.shape[0])
print(",",len(csv_data))
#datetime���Ƃ�csv�̃f�[�^���i�W.5�����j��TXT�ɏo�͂���B
#3���Ԃ��Ƃ̃f�[�^�����ɂ͂X��΂�
#���8�~�����A�O������21���� �܂�W�~�W���{5��69�i���܂�67������j


#��ƃ����@�S������txt�t�@�C���쐬�A�̂��߂ɉ���΂��΂������l����B�@�O��l����
#�����V�Q

# �W�F�l���[�^�𐶐�
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
    for k in range(csv_data[i]-1): #header�̕�����
        #print(data_nowphas[k*9][HGT_col],data_nowphas[k*9][PER_col])\
        #�O��l��������
        if data_nowphas[k*9+days*72][0]==9999:  #0 �̓t���O
            a="boke"
        else: #�O��l�̏ꍇ���������g��
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