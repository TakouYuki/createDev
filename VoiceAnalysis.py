import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as scipl
import pandas as pd

Wpm=400
sex=0
f0_ave=[150, 270]

#A特性カーブ
def A(f0):
    RA=12194**2*f0**4/((f0**2+20.6**2)*((f0**2+107.7**2)*(f0**2+737.9**2))**(1/2)*(f0**2+12194**2))
    return 20*np.log10(RA)+2.00

# ファイル読み込み
filename = ".\\test2.wav"
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
for i in range(len(times)) :                #ノイズの音圧実効値
    if (50<f0[i]<10000)==0 :
        vol0=rms[0][i]
        break
for i in range(len(times)) :
    if rms[0][i]!=0 and 50<f0[i]<10000 :
            vol=np.append(vol, 20 * np.log10(rms[0][i]/vol0))#+A(f0[i])+3.32786) #音圧実効値➡音圧レベルに変換   #環境音の何倍か(負の無限大にいかないようにオフセット残す)
    else :
        vol=np.append(vol, 0)
    if vol[i]-5<0 :
        vol[i]=0

plt.plot(times, vol)
plt.title("Noise Level-Time Graph")
plt.xlabel('Time[s]')
plt.ylabel('Noise Level[dB]')
plt.savefig('volume.png')
plt.close()


# dtごとに平均をとった音の大きさと高さのグラフを作成する。
dt=5
V_ave_dt=np.array([])
F_ave_dt=np.array([])
t=np.array([])
Vtmp,Ftmp=0,0
for i in range(int(len(times)/(dt*sr/512))) :
    Vtmp,Ftmp,jtmp=0,0,0
    for j in range(int(dt*sr/512)) :
        Vtmp+=vol[int(dt*sr/512*i+j)]
        if f0[int(dt*sr/512*i+j)]<10000:
            Ftmp+=f0[int(dt*sr/512*i+j)]
            jtmp+=1

    Vtmp/=dt*sr/512
    if jtmp!=0:
        Ftmp/=jtmp
    for j in range(int(dt*sr/512)):
        V_ave_dt=np.append(V_ave_dt, Vtmp)
        F_ave_dt=np.append(F_ave_dt, Ftmp)
Vtmp,Ftmp,jtmp=0,0,0
for k in range(len(times)-(i+1)*(j+1)) :
    Vtmp+=vol[(i+1)*(j+1)+k]
    if f0[(i+1)*(j+1)+k]<10000 :
        Ftmp+=f0[(i+1)*(j+1)+k]
        jtmp+=1
Vtmp/=len(times)-(i+1)*(j+1)
if jtmp!=0:
    Ftmp/=jtmp
for k in range(len(times)-(i+1)*(j+1)):
    V_ave_dt=np.append(V_ave_dt, Vtmp)
    F_ave_dt=np.append(F_ave_dt, Ftmp)
plt.plot(times, V_ave_dt)
plt.title("Noise Level-Time Graph (5s ave)")
plt.xlabel('Time[s]')
plt.ylabel('Noise Level[dB]')
plt.savefig('volume(dt=5s).png')
plt.close()

plt.plot(times, F_ave_dt)
plt.title("f0-Time Graph (5s ave)")
plt.xlabel('Time[s]')
plt.ylabel('f0[Hz]')
plt.savefig('f0(dt=5s).png')
plt.close()




# 音の大きさの判定
Em_t=1.3
cntV_all,cntV_all_true,cntEm_all,cntEm,V_ave,cntcntEm,empty_ave=0,0,0,0,0,0,0
for i in range(len(times)) :
    if vol[i]>0:
        cntV_all+=1                         #間なしのカウント
        cntV_all_true+=1                    #間ありのカウント
        cntEm=(int)(Em_t*sr/512)            #間判定の秒数(1s = sr個 = sr/512 times)
        V_ave+=vol[i]
    elif cntEm>=0 :
        if cntEm==(int)(Em_t*sr/512) :
            cntcntEm+=1                     #間になった瞬間にだけ間の回数を増やす。
        if cntEm>0:
            cntV_all_true+=1                #間の間も真にしゃべっている時間を増やす。
            cntEm_all+=1                    #間の時間をカウントする。
        if cntEm==0:
            cntV_all_true-=(int)(Em_t*sr/512)
            cntEm_all-=(int)(Em_t*sr/512)
            cntcntEm-=1
        cntEm-=1                            #間判定の時間を経過させていく。

V_ave/=cntV_all
empty_ave=cntEm_all/cntcntEm*512/sr

time=cntV_all_true/len(times)*len(y)/sr


#音の高さの判定
cntF_all,F_ave=0,0
for i in range(len(times)) :
    if 50<f0[i]<10000 :
        cntF_all+=1
        F_ave+=f0[i]
F_ave/=cntF_all


#結果の出力
if cntV_all!=0 :
    print(V_ave)                            #声の平均的な大きさが環境音の何倍か[dB] or 人の最小可聴値の何倍か[dB]
    print(empty_ave)                        #間の平均的な長さ[s]

else :
    print("声は録音されませんでした。")
print(time)                                 #話している時間[s]
if cntF_all!=0 :
    print(F_ave)                            #声の平均的な高さ[Hz]


#bigfiveを計算
logF=np.log10(F_ave/f0_ave[sex])
logWpm=np.log10(Wpm/400)
bigfive=[]

#外向性
bigfive.append(-53.50075470756*logF**2+14.389064689477*logF-84.378980658059*logWpm**2+16.561756149192*logWpm+24.991783088367)
#情緒不安定性
bigfive.append(49.35579530889*logF**2-0.54460603183674*logF+12.727457105757*logWpm**2-4.5402945174996*logWpm+19.20506882761)
#経験への開放性
bigfive.append(-63.60317068405*logF**2+2.6943666934754*logF-97.86211897341*logWpm**2+10.680010971777*logWpm+22.587194152335)
#勤勉性
bigfive.append(-85.2966634461*logF**2-3.3536266295536*logF-141.60276695818*logWpm**2+24.997416986711*logWpm+26.805124137738)
#協調性
bigfive.append(-128.41373455909*logF**2+3.1816457761492*logF-157.14417768061*logWpm**2-9.4417488311249*logWpm+26.228817191891)


#レーダーチャートの作成
plt.rcParams['font.family'] = "MS Gothic"
data = {'A': [bigfive[0], bigfive[1], bigfive[2], bigfive[3], bigfive[4]]}
df = pd.DataFrame(data, index=['\n\n外向性\n\n', '情緒不安定性\n\n', '\n\n経験への開放性', '\n\n勤勉性', '協調性\n\n'])
columns = df.index
fig, ax = plt.subplots(1, 1, figsize=(7, 8), subplot_kw={'projection': 'polar'})
values_A = df["A"]
angles_A = np.linspace(start=0, stop=2*np.pi, num=len(df["A"])+1, endpoint=True)
values_A = np.concatenate((df["A"], [df["A"][0]]))
ax.plot(angles_A, values_A, 'o-', color="blue", label="あなた")
ax.fill(angles_A, values_A, alpha=0.3, color="blue")
ax.set_thetagrids(angles_A[:-1] * 180 / np.pi, columns, fontsize=17)
ax.set_theta_zero_location('N')
ax.set_rlim(0, 100)
gridlines = ax.yaxis.get_gridlines()
gridlines[2].set_color("black")
gridlines[2].set_linewidth(2)
gridlines[2].set_linestyle("--")
ax.set_title("聞き手が感じる性格印象", fontsize=25)
ax.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=2)

plt.savefig('Chart.png')
plt.show()




#相槌、割り込み、話し手聞き手の割合を判定する。
