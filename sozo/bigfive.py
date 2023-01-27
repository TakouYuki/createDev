# 使用するパッケージをインポート
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def func1(x, y, i):
    match i:
        case 0:
            return 7.4153882932119*(-53.50075470756*x**2+14.389064689477*x-84.378980658059*y**2+16.561756149192*y+24.991783088367)-98.524033847039 #外向性
        case 1:
            return 10.523312934435*(49.35579530889*x**2-0.54460603183674*x+12.727457105757*y**2-4.5402945174996*y+19.20506882761)-197.82355052927  #情緒不安定性
        case 2:
            return 6.4644778677204*(-63.60317068405*x**2+2.6943666934754*x-97.86211897341*y**2+10.680010971777*y+22.587194152335)-48.082440963659  #経験への開放性
        case 3:
            return 3.7329190850909*(-85.2966634461*x**2-3.3536266295536*x-141.60276695818*y**2+24.997416986711*y+26.805124137738)-4.3026120322499  #勤勉性
        case 4:
            return 3.6219890942118*(-128.41373455909*x**2+3.1816457761492*x-157.14417768061*y**2-9.4417488311249*y+26.228817191891)+4.4146212070231#協調性



# メッシュを作成
x = np.arange(-0.2, 0.4, 0.01)
y = np.arange(-0.2, 0.2, 0.01)
X, Y = np.meshgrid(x, y)

bigfive=[50,50,50,50,50]

# plot_surfaceで曲面プロット
for i in range(5):
    plt.rcParams['font.family'] = "MS Gothic"
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection' : '3d'})
    fig.colorbar(ax.plot_surface(X, Y, func1(X, Y, i), rstride=1, cstride=10, cmap='jet', alpha=0.4), ax=ax, shrink=0.5)
    ax.scatter3D(0.3, 0.1, bigfive[i], s=10, color='red', depthshade=True)
    
    ax.plot(0.3, 0.1, bigfive[i], c='r', marker='.', ls='None', label='あなた('+str(bigfive[i])+')')
    ax.plot(0.3, 0.1, 0, c='k', marker='.')
    ax.plot(0.134475, 0.0981391, 100, c='b', marker='.', ls='None', label='最大(100)')
    ax.plot(0.134475, 0.0981391, 0, c='k', marker='.')
    #ax.plot(0.3, 0.2, bigfive[i], c='k', marker='.')
    zl = np.linspace(0, bigfive[i])
    xl=zl*0+0.3
    yl=zl*0+0.1
    ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    zl = np.linspace(0, 100)
    xl=zl*0+0.134475
    yl=zl*0+0.0981391
    ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    #yl = np.linspace(0.1, 0.2)
    #xl=yl*0+0.3
    #zl=yl*0+bigfive[i]
    #ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    #xl = np.linspace(-0.2, 0.3)
    #yl=xl*0+0.1
    #zl=xl*0
    #ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    #ax.plot(xl, yl, zl+bigfive[i], c='k', ls=':', markersize=1)
    #yl = np.linspace(-0.2, 0.1)
    #xl=yl*0+0.3
    #zl=yl*0
    #ax.plot(xl, yl, zl, c='k', ls=':', markersize=1)
    #ax.plot(xl, yl, zl+bigfive[i], c='k', ls=':', markersize=1)
    ax.set_xlabel('\n\n周波数(log scale)', size=15)
    ax.set_ylabel('\n\n発話速度(log scale)', size=15)
    ax.set_zticks([])
    ax.view_init(elev=50, azim=225)
    ax.legend(fontsize=7)
    match i:
        case 0:
            ax.set_title('外向性\n', size=25)
            plt.savefig("E.png")
            plt.show()
        case 1:
            ax.set_title('情緒不安定性\n', size=25)
            plt.savefig("N.png")
            plt.show()
        case 2:
            ax.set_title('経験への開放性\n', size=25)
            plt.savefig("O.png")
            plt.show()
        case 3:
            ax.set_title('勤勉性\n', size=25)
            plt.savefig("C.png")
            plt.show()
        case 4:
            ax.set_title('協調性\n', size=25)
            plt.savefig("A.png")
            plt.show()
    plt.close()