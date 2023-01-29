import os
import azure.cognitiveservices.speech as speechsdk
import time
import sys
import pykakasi
import re
from janome.tokenizer import Tokenizer
import numpy as np
import matplotlib.pyplot as plt
import pylab
import wave

FILE_PATH = "test1.wav"
speech_config = speechsdk.SpeechConfig(subscription="9b198a686fbf45c79fe8c1f24f02249d", region="japaneast")
speech_config.speech_recognition_language="ja-JP"
audio_config = speechsdk.audio.AudioConfig(filename=FILE_PATH)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


recognize = []                  #文字起こしのデータすべてを格納
done = False
extract = []                    #recognizeの中の会話内容を抽出
target1 = r'text="'             #会話内容の最初の場所を判定する用
target2 = r'",'                 #会話内容の最後の場所を判定する用
kks = pykakasi.kakasi()         #ひらがなに変換するために必要なオブジェクト
mf_check = re.compile(r'^[mMfF]+$') #性別判定
mf = ''
NG = []
NG_count = []
HIGE = []
hige_count = []
hiragana = []                   #ひらがなに変換した会話内容を格納
tango = []
total_count = 0                 #合計文字数を格納
hige_total_count = 0
trush = 0
t = Tokenizer(wakati = True)
# ファイルの長さ　time

def stop_cb(evt):
    speech_recognizer.stop_continuous_recognition()
    global done 
    done = True

speech_recognizer.recognized.connect(lambda evt:recognize.append(format(evt)))
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)
speech_recognizer.start_continuous_recognition()
#ここまでで音声を文字起こし
while not done:
    time.sleep(.5)


for a in recognize:
    test = a
    f = test.find(target1)
    l = test.find(target2)
    con = test[f+len(target1):l]
    extract.append(con)
# ここで余分な情報を排除

print('---------------\n')
[print(x) for x in extract]


for a in extract:
    test=list((t.tokenize(a)))
    for x in test:
        tango.append(x)
# 分かち書き

for i,x in enumerate(tango):
    if(x == 'え'):
        tango[i] = 'えー'
        del tango[i+1]

for a in tango:
    test = a
    result = kks.convert(test)
    hiramoji = ''.join([item['hira'] for item in result])
    hiragana.append(re.sub("、|。|！|？","",hiramoji))
# ひらがなに変換


with open('hige.txt','r',encoding = "utf-8") as f:
    HIGE = f.read().splitlines()

for a in HIGE:
    hige_count.append(0)

for a in tango:
    test = a
    for i,x in enumerate(HIGE):
        if(test == x):
            hige_count[i] += 1

      
print('---------------')
   
for a, b in zip(HIGE,hige_count):
    hige_total_count += b
    if(b != 0):
        if(trush == 0):
            print('\nひげ')
            trush += 1
        print(a,b)
if(hige_total_count != 0):
    print('\nひげ総数 ',hige_total_count)
# ひげのカウント

f.close()

with open ('test.txt','r',encoding = "utf-8") as f:
    NG = f.read().splitlines()

mf = NG[0]
del NG[0]

if 'm' in mf:
    sex = 0
elif 'M' in mf:
    sex = 0
elif 'f' in mf:
    sex = 1
elif 'F' in mf:
    sex = 1

print(sex)    

for a in NG:
    NG_count.append(0)

for a in tango:
    test = a
    for i, x in enumerate(NG):
        if test==x:
            NG_count[i] += 1

if NG != []:   
    print('\nNGワード')

for a, b in zip(NG, NG_count):
        print(a,b)

# NGワードをカウント(上のNGでワード管理)

f.close()

for a in hiragana:
    test = a
    count = len(test)
    total_count += count
#文字数カウント

print('\n文字数トータル ',total_count)

 

# ここから下は一番最後にしてほしい

file = open("mojiokosi.txt","w",encoding = 'utf-8')

for x in extract:
    file.write(x)
    file.write('\n')

file.write('\n総文字数 ',total_count)
file.close()

file = open("result.txt","w",encoding = 'utf-8')


trush = 0
for a, b in zip(HIGE,hige_count):
    if(b != 0):
        if(trush == 0):
            file.write('ひげ')
            file.write('\n')
            trush += 1
        file.write(a)
        file.write(' ', b)
        file.write('\n')

file.write('\n')
file.write('NG')

for a, b in zip(NG, NG_count):
    file.write(a)
    file.write(' ', b)
    file.write('\n')

file.write('外向性 ',bigfive[0])
file.write('\n')
file.write('情緒不安定性 ',bigfive[1])
file.write('\n')
file.write('経験への開放性 ',bigfive[2])
file.write('\n')
file.write('勤勉性 ',bigfive[3])
file.write('\n')
file.write('協調性 ',bigfive[4])
file.write('\n')

file.write('話者が話している時間[s] ',times_all)
file.write('\n')

file.write('声の周波数全国平均[Hz] 男性',f0_ave[0])
file.write('\n')
file.write('声の周波数全国平均[Hz] 女性',f0_ave[1])
file.write('\n')
file.write('1分間話量全国平均[文字/分] ',400)
file.write('\n')

file.write('測定者の声の大きさの平均[dB] ',V_ave)
file.write('\n')
file.write('測定者の声の高さの平均[Hz] '.F_ave)
file.write('\n')
file.write('測定者の間の長さの平均[s] ',empty_ave)
file.write('\n')

file.write('発話速度[文字/m] ',Wpm)
file.write('\n')
file.write('双方が無言である総時間[s] ',Silent)
file.write('\n')
file.write('自分を1とした相手の話量の比 ',Prop)
file.write('\n')

file.close()

#　出力データ
#　文字起こしの原文 mojiokosi.txt
#　その他データ　result.txt
#　ひげ、NGワードとその量
#　ひげ、NGワードの総数
#　BigFiveの具体的な値 5 bigfive[5]の0~4　外向性、情緒不安定性、経験への開放性、勤勉性、協調性の順
#　音声ファイルのうちのしゃべっている時間 1 times_all
#　声の全国平均（高さ、1分間話量) 3 f0_ave[2] 0がm 1がf 話量400
#　声の平均的な大きさ（環境音との比）1、V_ave 平均的な高さ 1 F_ave
#　平均的な間の長さ 1 empty_ave
#　発話速度 1 Wpm
#　両方が黙っている時間の総量 1 Silent
#　自分を1としてあいての話量の比率 1 Prop