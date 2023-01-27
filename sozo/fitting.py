# 使用するパッケージをインポート
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def func(x, y, i):
    match i:
        case 0:
            return -53.50075470756*x**2+14.389064689477*x-84.378980658059*y**2+16.561756149192*y+24.991783088367   #外向性
        case 1:
            return 49.35579530889*x**2-0.54460603183674*x+12.727457105757*y**2-4.5402945174996*y+19.20506882761    #情緒不安定性
        case 2:
            return -63.60317068405*x**2+2.6943666934754*x-97.86211897341*y**2+10.680010971777*y+22.587194152335    #経験への開放性
        case 3:
            return-85.2966634461*x**2-3.3536266295536*x-141.60276695818*y**2+24.997416986711*y+26.805124137738     #勤勉性
        case 4:
            return -128.41373455909*x**2+3.1816457761492*x-157.14417768061*y**2-9.4417488311249*y+26.228817191891  #協調性

# メッシュを作成
x = np.arange(-0.2, 0.2, 0.01)    #実際は-0.2, 0.4の範囲で考えるだろう。通常の会話で発する声の高さ的に
y = np.arange(-0.2, 0.2, 0.01)
X, Y = np.meshgrid(x, y)


xp = np.array([-0.193820026,-0.096910013,0,0.096910013,0.193820026,-0.096910013,-0.096910013,-0.096910013,-0.096910013,0.096910013,0.096910013,0.096910013,0.096910013])
yp = np.array([0,0,0,0,0,0.193820026,0.096910013,-0.096910013,-0.193820026,0.193820026,0.096910013,-0.096910013,-0.193820026])

plt.rcParams['font.family'] = "MS Gothic"
for i in range(5):
    match i:
        case 0:
            zp = np.array([20.3,22,26,25.7,26,22.5,24.2,20.8,17.5,26,27.5,22.2,19.3])                #外向性
        case 1:
            zp = np.array([20.8,20.2,18.4,19.9,21.1,19.75,19.3,20.8,20.7,19.3,18.4,20.8,20.8])       #情緒不安定性
        case 2:
            zp = np.array([19.75,21.5,23.05,22,20.8,19.75,22,19.6,16.3,20.65,22.9,19.6,16.6])        #経験への開放性
        case 3:
            zp = np.array([24.85,26.5,28,25.3,22.75,25.6,27.25,21.7,15.7,25.6,26.2,21.7,16.3])       #勤勉性
        case 4:
            zp = np.array([21.55,24.7,27.55,24.85,21.7,16.45,21.55,23.5,20.65,18.1,23.35,24.1,21.7]) #協調性
    # plot_surfaceで曲面プロット
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection' : '3d'})
    fig.colorbar(ax.plot_surface(X, Y, func(X, Y,i), rstride=1, cstride=10, cmap='jet', alpha=0.4), ax=ax, shrink=0.5)
    ax.scatter3D(xp, yp, zp, s=10, color='red', depthshade=True)
    ax.set_xlabel('\n\n周波数(log scale)', size=15)
    ax.set_ylabel('\n\n発話速度(log scale)', size=15)
    ax.set_zticks([])
    ax.view_init(elev=50, azim=225)
    match i:
        case 0:
            ax.set_title('外向性\n', size=25)
            plt.savefig("E_original.png")
        case 1:
            ax.set_title('情緒不安定性\n', size=25)
            plt.savefig("N_original.png")
        case 2:
            ax.set_title('経験への開放性\n', size=25)
            plt.savefig("O_original.png")
        case 3:
            ax.set_title('勤勉性\n', size=25)
            plt.savefig("C_original.png")
        case 4:
            ax.set_title('協調性\n', size=25)
            plt.savefig("A_original.png")
    #plt.show()
    plt.close()
    R2,tmp1,tmp2,z_ave=0,0,0,np.average(zp)
    for j in range(13) :
        tmp1+=(zp[j]-func(xp[j],yp[j],i))**2
        tmp2+=(zp[j]-z_ave)**2
    R2=1-tmp1/tmp2
    print(R2)