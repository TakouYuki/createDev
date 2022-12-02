import os
import azure.cognitiveservices.speech as speechsdk
import time
import sys
import pykakasi
import re
# ファイルの長さの変数　time

speech_config = speechsdk.SpeechConfig(subscription="9b198a686fbf45c79fe8c1f24f02249d", region="japaneast")
speech_config.speech_recognition_language="ja-JP"
audio_config = speechsdk.audio.AudioConfig(filename="2022-11-18_13-40-34aaa.wav")
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

recognize = []                  #文字起こしのデータすべてを格納
done = False
extract = []                    #recognizeの中の会話内容を抽出
target1 = r'text="'             #会話内容の最初の場所を判定する用
target2 = r'",'                 #会話内容の最後の場所を判定する用
kks = pykakasi.kakasi()         #ひらがなに変換するために必要なオブジェクト
NG = ['あー','はい']
hiragana = []                   #ひらがなに変換した会話内容を格納
total_count = 0                 #合計文字数を格納

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
print('文字起こし')
[print(x) for x in extract]

NG_count = [0,0]

for a in extract:
    test = a
    NG_count[0] += test.count(NG[0])
    NG_count[1] += test.count(NG[1])

print('あー　',NG_count[0])
print('はい　',NG_count[1])
# NGワードをカウント(上のNGでワード管理)
for a in extract:
    test = a
    result = kks.convert(test)
    hiramoji = ''.join([item['hira'] for item in result])
    hiragana.append(re.sub("、|。|！|？","",hiramoji))
# ひらがなに変換
# print('ひらがな変換')
# [print(x) for x in hiragana]

for a in hiragana :
    test = a
    count = len(test)
    total_count += count
#文字数カウント

print('文字数トータル ',total_count)