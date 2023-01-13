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

# file = open('result.txt','w')

recognize = []                  #文字起こしのデータすべてを格納
done = False
extract = []                    #recognizeの中の会話内容を抽出
target1 = r'text="'             #会話内容の最初の場所を判定する用
target2 = r'",'                 #会話内容の最後の場所を判定する用
kks = pykakasi.kakasi()         #ひらがなに変換するために必要なオブジェクト
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

# [print(x) for x in recognize]

for a in recognize:
    test = a
    f = test.find(target1)
    l = test.find(target2)
    con = test[f+len(target1):l]
    extract.append(con)
# ここで余分な情報を排除

print('---------------\n')
# file.write('文字起こし\n---------------\n')
[print(x) for x in extract]
# for x in extract:
#     file.write("%s\n" % x)


for a in extract:
    test=list((t.tokenize(a)))
    for x in test:
        tango.append(x)
# [print(x) for x in tango]
# 分かち書き

eee = tango.index('え')
if(tango[eee] == tango[eee+1]):
    tango[eee] = 'えー'
    del tango[eee+1]


for a in tango:
    test = a
    result = kks.convert(test)
    hiramoji = ''.join([item['hira'] for item in result])
    hiragana.append(re.sub("、|。|！|？","",hiramoji))
# ひらがなに変換

# [print(x) for x in hiragana]

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
    if(trush == 0):
        print('\nひげ')
        trush += 1
    # file.write('---------------\nひげ\n')
    print(a,b)
    # file.write(a)
    # file.write(' ')
    # file.write(str(b))
    # file.write('\n')

print('\nひげ総数 ',hige_total_count)
    # file.write('\nひげ総数 ')
    # file.write(str(hige_total_count))
    # file.write('\n')

# ひげのカウント

f.close()

with open ('test.txt','r',encoding = "utf-8") as f:
    NG = f.read().splitlines()

for a in NG:
    NG_count.append(0)

for a in tango:
    test = a
    for i, x in enumerate(NG):
        if test==x:
            NG_count[i] += 1

if NG != []:   
    print('\nNGワード')
    # file.write('\nNGワード\n')

for a, b in zip(NG, NG_count):
    print(a,b)
    # file.write(a)
    # file.write(' ')
    # file.write(str(b))
    # file.write('\n')

# NGワードをカウント(上のNGでワード管理)

f.close()

for a in hiragana:
    test = a
    count = len(test)
    total_count += count
#文字数カウント

print('\n文字数トータル ',total_count)
# file.write('\n文字数トータル ')
# file.write(str(total_count))
# file.write('\n')

# bpm = total_count / time
# print('1分あたりの話量',bpm)
# file.close()
 
with wave.open(FILE_PATH, 'rb') as wr:
    fr = wr.getframerate()
    fn = wr.getnframes()
    time = fn / fr

    print("\n再生時間 ",1.0 * time)
#とりあえずtimeをwavファイルの半分にするためのやつ 後で消す

time = time / 2