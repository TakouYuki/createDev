import librosa
import matplotlib.pyplot as plt
import numpy as np
if __name__ == "__main__":
    filename = "C:\\Users\\black\\OneDrive\\ドキュメント\\創造設計1班\\sozo\\se_sad01.wav"
    y, sr = librosa.load(filename)
    rms = librosa.feature.rms(y) #音量の計算
    times = librosa.times_like(rms, sr) #時間軸の生成
    plt.plot(times, 20 * np.log10(rms[0]*2**(1/2))) #rms➡振幅➡人の感じる音量に変換
    plt.show()
    plt.close()
    print(len(times))
    print(rms.size)