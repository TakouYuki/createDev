import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as scipl


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
levelV=[0, 10, 20, 30, 40]
cntV,cntV_all,cntV_all_true,cntEm_all,cntEm,V_ave,cntcntEm,empty_ave=0,0,0,0,0,0,0,0
for i in range(len(times)) :
    if vol[i]>0:
        cntV_all+=1             #間なしのカウント
        cntV_all_true+=1        #間ありのカウント
        cntEm=0.4*sr/512        #間判定の秒数(1s = sr個 = sr/512 times)
        V_ave+=vol[i]

        if vol[i]>levelV[4] :
            cntV+=4
        elif vol[i]>levelV[3] :
            cntV+=3
        elif vol[i]-levelV[2] :
            cntV+=2
        elif vol[i]>levelV[1] :
            cntV+=1
    elif cntEm>0 :
        if cntEm==0.4*sr/512 :
            cntcntEm+=1              #間になった瞬間にだけ間の回数を増やす。
        cntV_all_true+=1             #間の間も真にしゃべっている時間を増やす。
        cntEm_all+=1                 #間の時間をカウントする。
        cntEm-=1                     #間判定の時間を経過させていく。

V_ave/=cntV_all
empty_ave=cntEm_all/cntcntEm*512/sr

time=cntV_all_true/len(times)*len(y)/sr


#音の高さの判定
levelF=[100, 500, 1000, 1500, 2000]
cntF,cntF_all,F_ave=0,0,0
for i in range(len(times)) :
    if levelF[0]<=f0[i]<=levelF[4] :
        cntF_all+=1
        F_ave+=f0[i]
        if f0[i]>levelF[4] :
            cntF+=4
        elif f0[i]>levelF[3] :
            cntF+=3
        elif f0[i]-levelF[2] :
            cntF+=2
        elif f0[i]>levelF[1] :
            cntF+=1
F_ave/=cntF_all


#結果の出力
if cntV_all!=0 :
    print(cntV/cntV_all)                    #声の平均的な大きさ(0~4の5段階評価)
    print(V_ave)                            #声の平均的な大きさが環境音の何倍か[dB] or 人の最小可聴値の何倍か[dB]
    print(empty_ave)                        #間の平均的な長さ[s]
else :
    print("声は録音されませんでした。")
print(time)                                 #話している時間[s]
if cntF_all!=0 :
    print(cntF/cntF_all)                    #声の平均的な高さ(0~4の5段階評価)
    print(F_ave)                            #声の平均的な高さ[Hz]





#相槌、割り込み、話し手聞き手の割合を判定する。



