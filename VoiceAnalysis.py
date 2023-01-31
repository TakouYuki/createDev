import librosa
import librosa.display
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.interpolate as scipl
import pandas as pd
import os
import azure.cognitiveservices.speech as speechsdk
import time
import sys
import pykakasi
import re



#A特性カーブ
def A(f0):
    RA=12194**2*f0**4/((f0**2+20.6**2)*((f0**2+107.7**2)*(f0**2+737.9**2))**(1/2)*(f0**2+12194**2))
    return 20*np.log10(RA)+2.00

# ファイル読み込み
filename = ".\\test2.wav"
filename2 = ".\\low.wav"
y, sr = librosa.load(filename)
y2, sr2 = librosa.load(filename2)


# 基本周波数をstftにより求める。
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
f02, voiced_flag, voiced_probs = librosa.pyin(y2, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0) 
times2 = librosa.times_like(f02) 


# 音量をrmsと常用対数により求める。
rms = librosa.feature.rms(y=y)   #音圧[Pa], rms➡音圧実効値
rms2 = librosa.feature.rms(y=y2)
vol = np.array([])
vol2 = np.array([])
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

for i in range(len(times2)) :
    if rms2[0][i]!=0 and 50<f02[i]<10000 :
            vol2=np.append(vol2, 20 * np.log10(rms2[0][i]/vol0))  #相手の音圧レベル
    else :
        vol2=np.append(vol2, 0)
    if vol2[i]-5<0 :
        vol2[i]=0


# dtごとに平均をとった音の大きさと高さのグラフを作成する。
dt=5
V_ave_dt=np.array([])
F_ave_dt=np.array([])
V2_ave_dt=np.array([])
F2_ave_dt=np.array([])
Sound_around=np.array([0,0])
V_everyday_Min=np.array([20,20])
V_everyday_Max=np.array([31,31])
V_loud_Min=np.array([58,58])
V_loud_Max=np.array([69,69])
F_all_ave=np.array([[150,150],[270,270]])


t_Max=np.array([0,times[len(times)-1] if len(times)>len(times2) else times2[len(times2)-1]])
t=np.array([])
t2=np.array([])

i,j=0,0
for i in range(int(len(times)/(dt*sr/512))) :
    Vtmp,Ftmp,jtmp,jjtmp=0,0,0,0
    for j in range(int(dt*sr/512)) :
        if vol[int(dt*sr/512*i+j)]>0:
            Vtmp+=vol[int(dt*sr/512*i+j)]
            jjtmp+=1
        if f0[int(dt*sr/512*i+j)]<10000:
            Ftmp+=f0[int(dt*sr/512*i+j)]
            jtmp+=1

    if jjtmp!=0:
        Vtmp/=jjtmp
    if jtmp!=0:
        Ftmp/=jtmp

    V_ave_dt=np.append(V_ave_dt, Vtmp)
    V_ave_dt=np.append(V_ave_dt, Vtmp)
    F_ave_dt=np.append(F_ave_dt, Ftmp)
    F_ave_dt=np.append(F_ave_dt, Ftmp)
    t=np.append(t, times[i*int(dt*sr/512)])
    t=np.append(t, times[(i+1)*int(dt*sr/512)])

Vtmp,Ftmp,jtmp,jjtmp=0,0,0,0
for k in range(len(times)-(i+1)*(j+1)) :
    if vol[(i+1)*(j+1)+k]>0:
        Vtmp+=vol[(i+1)*(j+1)+k]
        jjtmp+=1
    if f0[(i+1)*(j+1)+k]<10000 :
        Ftmp+=f0[(i+1)*(j+1)+k]
        jtmp+=1

if jjtmp!=0:
    Vtmp/=jjtmp
if jtmp!=0:
    Ftmp/=jtmp

V_ave_dt=np.append(V_ave_dt, Vtmp)
V_ave_dt=np.append(V_ave_dt, Vtmp)
F_ave_dt=np.append(F_ave_dt, Ftmp)
F_ave_dt=np.append(F_ave_dt, Ftmp)
t=np.append(t, times[(i+1)*int(dt*sr/512)])
t=np.append(t, times[len(times)-1])


for i in range(int(len(times2)/(dt*sr/512))) :
    V2tmp,F2tmp,j2tmp,jj2tmp=0,0,0,0
    for j in range(int(dt*sr/512)) :
        if vol2[int(dt*sr/512*i+j)]>0:
            V2tmp+=vol2[int(dt*sr/512*i+j)]
            jj2tmp+=1
        if f02[int(dt*sr/512*i+j)]<10000:
            F2tmp+=f02[int(dt*sr/512*i+j)]
            j2tmp+=1

    if jj2tmp!=0:
        V2tmp/=jj2tmp
    if j2tmp!=0:
        F2tmp/=j2tmp

    V2_ave_dt=np.append(V2_ave_dt, V2tmp)
    V2_ave_dt=np.append(V2_ave_dt, V2tmp)
    F2_ave_dt=np.append(F2_ave_dt, F2tmp)
    F2_ave_dt=np.append(F2_ave_dt, F2tmp)
    t2=np.append(t2, times2[i*int(dt*sr/512)])
    t2=np.append(t2, times2[(i+1)*int(dt*sr/512)])

V2tmp,F2tmp,j2tmp,jj2tmp=0,0,0,0
for k in range(len(times2)-(i+1)*(j+1)) :
    if vol2[(i+1)*(j+1)+k]>0:
        V2tmp+=vol2[(i+1)*(j+1)+k]
        jj2tmp+=1
    if f02[(i+1)*(j+1)+k]<10000 :
        F2tmp+=f02[(i+1)*(j+1)+k]
        j2tmp+=1

if jj2tmp!=0:
    V2tmp/=jj2tmp
if j2tmp!=0:
    F2tmp/=j2tmp

V2_ave_dt=np.append(V2_ave_dt, V2tmp)
V2_ave_dt=np.append(V2_ave_dt, V2tmp)
F2_ave_dt=np.append(F2_ave_dt, F2tmp)
F2_ave_dt=np.append(F2_ave_dt, F2tmp)
t2=np.append(t2, times2[(i+1)*int(dt*sr/512)])
t2=np.append(t2, times2[len(times2)-1])




plt.rcParams['font.family'] = "MS Gothic"
plt.plot(t2, V2_ave_dt, color="blue", label="相手")
plt.plot(t, V_ave_dt, color="red", label="あなた")
plt.plot(t_Max, Sound_around, color="k", ls=":", label="環境音(0[dB])")
plt.plot(t_Max, V_everyday_Min, color="k", ls="--", label="全体平均の目安(10～21[dB])")
plt.plot(t_Max, V_everyday_Max, color="k", ls="--")
plt.title("5秒ごとの平均音圧レベル")
plt.xlabel('時間[s]')
plt.ylabel('音圧レベル[dB]')
plt.legend(loc=0)
plt.savefig('volume(dt=5s).png')
plt.close()

plt.rcParams['font.family'] = "MS Gothic"
plt.plot(t2, F2_ave_dt, color="blue", label="相手")
plt.plot(t, F_ave_dt, color="red", label="あなた")
plt.plot(t_Max, F_all_ave[sex], color="k", ls="--", label="全体平均"+("(男)" if sex==0 else "(女)"))
plt.title("5秒ごとの平均周波数")
plt.xlabel('時間[s]')
plt.ylabel('基本周波数[Hz]')
plt.legend(loc=0)
plt.savefig('f0(dt=5s).png')
plt.close()




# 音の大きさの判定
Em_t=1.3
cntV_all,cntV_all_true,cntEm_all,cntEm,V_ave,cntcntEm,empty_ave=0,0,0,0,0,0,0
cntV2_all,cntV2_all_true,cntEm2_all,cntEm2,V2_ave,cntcntEm2,empty2_ave=0,0,0,0,0,0,0
Silent, Prop=0,0
for i in range(len(times)) :
    if vol[i]>0:
        cntV_all+=1                         #間なしのカウント
        cntV_all_true+=1                    #間ありのカウント
        cntEm=(int)(Em_t*sr/512)            #間判定の秒数(1s = sr個 = sr/512 times)
        V_ave+=vol[i]

    elif cntEm>=-1:
        if cntEm==(int)(Em_t*sr/512) :
            cntcntEm+=1                     #間になった瞬間にだけ間の回数を増やす。
        if cntEm>0:
            cntV_all_true+=1                #間の間も真にしゃべっている時間を増やす。
            cntEm_all+=1                    #間の時間をカウントする。
        if cntEm==0:                        #実は間ではなくもう話が終わっていたとき、すべて元に戻す。
            cntV_all_true-=(int)(Em_t*sr/512)
            cntEm_all-=(int)(Em_t*sr/512)
            cntcntEm-=1
        cntEm-=1                            #間判定の時間を経過させていく。
    
    if i<len(times2) and vol2[i]>0:
        cntV2_all+=1                         #間なしのカウント
        cntV2_all_true+=1                    #間ありのカウント
        cntEm2=(int)(Em_t*sr/512)            #間判定の秒数(1s = sr個 = sr/512 times)
        V2_ave+=vol2[i]

    elif cntEm2>=0 :
        if cntEm2==(int)(Em_t*sr/512) :
            cntcntEm2+=1                     #間になった瞬間にだけ間の回数を増やす。
        if cntEm2>0:
            cntV2_all_true+=1                #間の間も真にしゃべっている時間を増やす。
            cntEm2_all+=1                    #間の時間をカウントする。
        if cntEm2==0:                        #実は間ではなくもう話が終わっていたとき、すべて元に戻す。
            cntV2_all_true-=(int)(Em_t*sr/512)
            cntEm2_all-=(int)(Em_t*sr/512)
            cntcntEm2-=1
        cntEm2-=1                            #間判定の時間を経過させていく。

    if cntEm<0 and cntEm2<0:
        Silent+=1                            #どっちも黙ったと確証を得てから、黙っているカウントを増やす。


V_ave/=cntV_all
empty_ave=cntEm_all/cntcntEm*512/sr

V2_ave/=cntV2_all
empty2_ave=cntEm2_all/cntcntEm2*512/sr

times_all=len(y)/sr
time_speach=cntV_all_true/len(times)*times_all
time2_speach=cntV2_all_true/len(times)*times_all

Silent*=512/sr
Prop=time2_speach/time_speach


#音の高さの判定
cntF_all,F_ave,cntF2_all,F2_ave=0,0,0,0
for i in range(len(times)) :
    if 50<f0[i]<10000 :
        cntF_all+=1
        F_ave+=f0[i]
    if i<len(times2) and 50<f02[i]<10000 :
        cntF2_all+=1
        F2_ave+=f02[i]
F_ave/=cntF_all
F2_ave/=cntF2_all


#結果の出力
print(V_ave)                                #声の平均的な大きさが環境音の何倍か[dB] or 人の最小可聴値の何倍か[dB]
print(V2_ave)
print(empty_ave)                            #間の平均的な長さ[s]
print(empty2_ave)
print(time_speach)                          #話している時間[s]
print(time2_speach)
print(F_ave)                                #声の平均的な高さ[Hz]
print(F2_ave)
print(Silent)                               #黙っている時間
print(Prop)                                 #話している比
print(times_all)                            #全部の時間


#bigfiveを計算
def func(x, y, i):
    match i:
        case 0:
            return 12.386508614817*(-53.50075470756*x**2+14.389064689477*x-84.378980658059*y**2+16.561756149192*y+24.991783088367)-230.82382668797 #外向性
        case 1:
            return 52.312199204855*(49.35579530889*x**2-0.54460603183674*x+12.727457105757*y**2-4.5402945174996*y+19.20506882761)-983.93492362419  #情緒不安定性
        case 2:
            return 19.883482790846*(-63.60317068405*x**2+2.6943666934754*x-97.86211897341*y**2+10.680010971777*y+22.587194152335)-355.47292863818  #経験への開放性
        case 3:
            return 11.642121194482*(-85.2966634461*x**2-3.3536266295536*x-141.60276695818*y**2+24.997416986711*y+26.805124137738)-225.29600093137  #勤勉性
        case 4:
            return 16.448721111934*(-128.41373455909*x**2+3.1816457761492*x-157.14417768061*y**2-9.4417488311249*y+26.228817191891)-334.08668476026#協調性


Wpm=total_count/(time_speach/60)
f0_ave=[150, 270]
logF=np.log10(F_ave/f0_ave[sex])
logWpm=np.log10(Wpm/400)
bigfive=[]

for i in range(5) :
    bigfive.append(func(logF, logWpm, i))



#レーダーチャートの作成
data = {
    'A': [bigfive[0], bigfive[1], bigfive[2], bigfive[3], bigfive[4]],
    'B':[func(0,0,0),func(0,0,1),func(0,0,2),func(0,0,3),func(0,0,4)]
    }
df = pd.DataFrame(data, index=['\n\n外向性\n\n', '情緒不安定性\n\n', '\n\n経験への開放性', '\n\n勤勉性', '協調性\n\n'])
fig, ax = plt.subplots(1, 1, figsize=(7, 8), subplot_kw={'projection': 'polar'})
angles_A = np.linspace(start=0, stop=2*np.pi, num=len(df["A"])+1, endpoint=True)
values_A = np.concatenate((df["A"], [df["A"][0]]))
angles_B = np.linspace(start=0, stop=2*np.pi, num=len(df["B"])+1, endpoint=True)
values_B = np.concatenate((df["B"], [df["B"][0]]))
ax.plot(angles_A, values_A, 'o-', color="red", label="あなた")
ax.fill(angles_A, values_A, alpha=0.3, color="red")
ax.plot(angles_B, values_B, 'o-', color="blue", label="全体平均")
ax.fill(angles_B, values_B, alpha=0.3, color="blue")
columns = df.index
ax.set_thetagrids(angles_A[:-1] * 180 / np.pi, columns, fontsize=17)
ax.set_theta_zero_location('N')
ax.set_rlim(0, 100)
gridlines = ax.yaxis.get_gridlines()
#gridlines[2].set_color("black")
#gridlines[2].set_linewidth(2)
#gridlines[2].set_linestyle("--")
ax.set_title("聞き手が感じる性格印象", fontsize=25)
ax.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=2)

plt.savefig('Chart.png')
plt.close()




#3Dグラフの作成
# メッシュを作成
x = np.arange(-0.1, 0.1, 0.001)
y = np.arange(-0.15, 0.15, 0.001)
X, Y = np.meshgrid(x, y)

# plot_surfaceで曲面プロット
for i in range(5):
    plt.rcParams['font.family'] = "MS Gothic"
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection' : '3d'})
    fig.colorbar(ax.plot_surface(X, Y, func(X, Y, i), rstride=1, cstride=10, cmap='jet', alpha=0.4), ax=ax, shrink=0.5)
    ax.scatter3D(logF, logWpm, bigfive[i], s=10, color='red', depthshade=True)
    ax.plot(logF, logWpm, bigfive[i], c='r', marker='.', ls='None', label='あなた('+str(bigfive[i])+')')
    ax.plot(logF, logWpm, 0, c='k', marker='.')
    zl = np.linspace(0, bigfive[i])
    xl=zl*0+logF
    yl=zl*0+logWpm
    ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    ax.set_xlabel('\n\n周波数', size=15)
    ax.set_ylabel('\n\n発話速度', size=15)
    ax.set_xlabel('\n\n周波数(log scale)', size=15)
    ax.set_ylabel('\n\n発話速度(log scale)', size=15)
    ax.set_zticks([])
    ax.view_init(elev=50, azim=225)
    match i:
        case 0:
            ax.plot(0.1, 0.0981391, 100, c='b', marker='.', ls='None', label='最大(100)')
            ax.plot(0.1, 0.0981391, 0, c='k', marker='.')
            ax.legend(fontsize=7)
            zl = np.linspace(0, 100)
            xl=zl*0+0.1
            yl=zl*0+0.0981391
            ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
            ax.set_title('外向性\n', size=25)
            plt.savefig("E.png")
        case 1:
            ax.plot(0.00551714, 0.15, 0, c='k', marker='.')
            ax.plot(0.00551714, 0.15, 3, c='b', marker='.', ls='None', label='最小(0)')
            ax.legend(fontsize=7)
            ax.set_title('情緒不安定性\n', size=25)
            plt.savefig("N.png")
        case 2:
            ax.plot(0.0211811, 0.0545666, 100, c='b', marker='.', ls='None', label='最大(100)')
            ax.legend(fontsize=7)
            ax.plot(0.0211811, 0.0545666, 0, c='k', marker='.')
            zl = np.linspace(0, 100)
            xl=zl*0+0.0211811
            yl=zl*0+0.0545666
            ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
            ax.set_title('経験への開放性\n', size=25)
            plt.savefig("O.png")
        case 3:
            ax.plot(-0.0196586, 0.088266, 100, c='b', marker='.', ls='None', label='最大(100)')
            ax.legend(fontsize=7)
            ax.plot(-0.0196586, 0.088266, 0, c='k', marker='.')
            zl = np.linspace(0, 100)
            xl=zl*0-0.0196586
            yl=zl*0+0.088266
            ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
            ax.set_title('勤勉性\n', size=25)
            plt.savefig("C.png")
        case 4:
            ax.plot(0.0123883, -0.0300417, 100, c='b', marker='.', ls='None', label='最大(100)')
            ax.legend(fontsize=7)
            ax.plot(0.0123883, -0.0300417, 0, c='k', marker='.')
            zl = np.linspace(0, 100)
            xl=zl*0+0.0123883
            yl=zl*0-0.0300417
            ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
            ax.set_title('協調性\n', size=25)
            plt.savefig("A.png")
    plt.show()
    plt.close()



#相槌、割り込み、話し手聞き手の割合を判定する。
