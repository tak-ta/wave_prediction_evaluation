#!/usr/bin/python
# -*- coding: Shift-JIS -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

#������ɕϐ��𖄂ߍ��ގQ�lhttps://qiita.com/niwasawa/items/27641b803db31f93b8e6
#data_gsf = pd.read_csv('20211001/NPHAS_ISHK-2021100100.csv', header=None)

str_common_gsf = 'pre/NPHAS_ISHK-'
year = '2021'
month ='11'
date = '01'
file_ext = '00.csv'

print('{}{}{}{}{}'.format(str_common_gsf,year,month,date,file_ext))
data_gsf = pd.read_csv('{}{}{}{}{}'.format(str_common_gsf,year,month,date,file_ext), header=None)
print(data_gsf)

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
end = datetime.strptime('20211231', '%Y%m%d').date()
#end   = date.today() # �����̓��t

# �W�F�l���[�^�𐶐�
gen = date_iterator_generator(begin, end)
print('gen: ' + str(gen))
"""
#���t���o��
for target in gen:
  print(target.strftime('%Y%m%d'))
"""

for i in gen:
    data_gsf = pd.read_csv('{}{}{}'.format(str_common_gsf,i.strftime('%Y%m%d'),file_ext), header=None)
    print(data_gsf.shape)