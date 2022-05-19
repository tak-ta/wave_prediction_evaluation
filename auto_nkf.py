#!/usr/bin/python
# -*- coding: Shift-JIS -*-

#手打ちでnkfコマンドを打って＋組み合わせて、ナウファスデータを作ってたがそれを自動化したい
#numpyは漢字読み込めないし、空白の部分違うからカラム数変わっちゃうし、アイデアがない
#シェルをパイソンで動かしてcutコマンドを使いたい

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
dir_name = "速報台帳2021年"+month+"月(関東)/"
file_name = "H"+PLACE_CODE+"e.s"+year+month+".txt"

print(nowphas_dir+dir_name+file_name)

#cp =subprocess.run("nkf -w nowphas_202205161057/速報台帳2021年10月(関東)/H207e.s2110.txt | cut -c 15-37",shell=True,capture_output=True,text=True)
#print("stdout:", cp.stdout)
subprocess.run("nkf -w nowphas_202205161057/速報台帳2021年10月(関東)/H207e.s2110.txt | cut -c 15-37",shell=True,capture_output=True,text=True)

#data_nowphas = np.loadtxt(nowphas_dir+dir_name+file_name,encoding="shift-jis",skiprows=1)