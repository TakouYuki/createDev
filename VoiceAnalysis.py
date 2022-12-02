import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np


#A特性カーブ
def A(f0):
    RA=12194**2*f0**4/((f0**2+20.6**2)*((f0**2+107.7**2)*(f0**2+737.9**2))**(1/2)*(f0**2+12194**2))
    return 20*np.log10(RA)+2.00

# ファイル読み込み
filename = "C:\\Users\\black\\OneDrive\\ドキュメント\\創造設計1班\\sozo\\2022-11-18_13-40-34aaa.wav"
y, sr = librosa.load(filename)


# 基本周波数をstftにより求める。
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0) 

#plt.plot(times, y)
plt.show()
plt.close()
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
fig, ax = plt.subplots()
img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN fundamental frequency estimation')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
ax.legend(loc='upper right')
plt.savefig('stft.png')
plt.close()

# 音量をrmsと常用対数により求める。
rms = librosa.feature.rms(y=y)   #音圧[Pa], rms➡音圧実効値
vol = np.array([])
vol0=rms[0][10]                 #ノイズの音圧実効値
cout_all=0
for i in range(len(times)) :
    if rms[0][i]!=0 and f0[i]<10000 :
            vol=np.append(vol, 20 * np.log10(rms[0][i]/vol0)+A(f0[i])-A(f0[10])) #音圧実効値➡音圧レベルに変換   #環境音の何倍か(負の無限大にいかないようにオフセット残す)
    else :
        vol=np.append(vol, 0)
    if vol[i]-4<0 :
        vol[i]=0

plt.plot(times, vol)
plt.title("Noise Level-Time Graph")
plt.xlabel('Time[s]')
plt.ylabel('Noise Level[dB]')
plt.savefig('volume.png')
plt.close()
print()


# 音の大きさ、高さを判定する。
levelV=[0, 10, 20, 30, 40]
cntV,cntV_all=0,0
for i in range(len(times)) :
    if vol[i]>levelV[0] :
        cntV_all+=1
        if vol[i]>levelV[4] :
            cntV+=4
        elif vol[i]>levelV[3] :
            cntV+=3
        elif vol[i]-levelV[2] :
            cntV+=2
        elif vol[i]>levelV[1] :
            cntV+=1



if cntV_all!=0 :
    print(cntV/cntV_all)
else :
    print("声は録音されませんでした。")

time=cntV_all/len(times)*len(y)/sr
print(time)


levelF=[100, 500, 1000, 1500, 2000]
cntF,cntF_all=0,0
for i in range(len(times)) :
    if levelF[0]<=f0[i]<=levelF[4] :
        cntF_all+=1
        if f0[i]>levelF[4] :
            cntF+=4
        elif f0[i]>levelF[3] :
            cntF+=3
        elif f0[i]-levelF[2] :
            cntF+=2
        elif f0[i]>levelF[1] :
            cntF+=1

if cntF_all!=0 :
    print(cntF/cntF_all)


# 間の長さ、相槌、割り込み。話し手聞き手の割合を判定する。
