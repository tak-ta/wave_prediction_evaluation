#!/usr/bin/python
# -*- coding: Shift-JIS -*-

#��ł���nkf�R�}���h��ł��ā{�g�ݍ��킹�āA�i�E�t�@�X�f�[�^������Ă��������������������
#numpy�͊����ǂݍ��߂Ȃ����A�󔒂̕����Ⴄ����J�������ς�����Ⴄ���A�A�C�f�A���Ȃ�
#�V�F�����p�C�\���œ�������cut�R�}���h���g������

#nkf -w H611e.s2112.txt | cut -c 15-37  > nowphas_2112.txt 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import date, datetime, timedelta
import subprocess

PLACE = "KAS"
PLACE_CODE = "207"
year = "21"
month = "10"
nowphas_dir = "nowphas_202205161057/"
dir_name = "����䒠2021�N"+month+"��(�֓�)/"
file_name = "H"+PLACE_CODE+"e.s"+year+month+".txt"

print(nowphas_dir+dir_name+file_name)

#cp =subprocess.run("nkf -w nowphas_202205161057/����䒠2021�N10��(�֓�)/H207e.s2110.txt | cut -c 15-37",shell=True,capture_output=True,text=True)
#print("stdout:", cp.stdout)
subprocess.run("nkf -w nowphas_202205161057/����䒠2021�N10��(�֓�)/H207e.s2110.txt | cut -c 15-37",shell=True,capture_output=True,text=True)

#data_nowphas = np.loadtxt(nowphas_dir+dir_name+file_name,encoding="shift-jis",skiprows=1)