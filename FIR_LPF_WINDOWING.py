import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

print("FIR THÔNG THẤP PP CỬA SỔ")
delta = float(input("Nhập độ gợn δ : "))
wp_input = float(input("Nhập wp (theo π): "))
ws_input = float(input("Nhập ws (theo π): "))
wp = wp_input * np.pi
ws = ws_input * np.pi
#suy hao
A = -20 * np.log10(delta)

#Chọn cửa sổ
if A < 21:
    window = "rectangular"
elif A < 44:
    window = "hanning"
elif A < 53:
    window = "hamming"
else:
    window = "hamming"   

#Độ rộng chuyển tiếp
dw = ws - wp

#Tính N
N = int(np.ceil(8 * np.pi / dw))
if N % 2 == 0:
    N += 1

print(f"\nA = {A:.2f} dB")
print(f"N = {N}")
print(f"Window = {window}")

#Tần số cắt
wc = (wp + ws) / 2

M = (N - 1) // 2
n = np.arange(N)

#Đáp ứng xung lý tưởng
hd = np.zeros(N)
for i in range(N):
    if i == M:
        hd[i] = wc / np.pi
    else:
        hd[i] = np.sin(wc * (i - M)) / (np.pi * (i - M))

#Cửa sổ
if window == "hamming":
    w = 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))
elif window == "hanning":
    w = 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))
else:
    w = np.ones(N)

#Bộ lọc
h = hd * w

#Đáp ứng tần số
w_freq, H = freqz(h, worN=1024)
H_dB = 20 * np.log10(np.abs(H) + 1e-6)

plt.figure(figsize=(10,8))

plt.subplot(2,2,1)
plt.stem(n, hd)
plt.title("Dãy đáp ứng xung của bộ lọc lý tưởng")
plt.grid()
plt.xlabel("n")
plt.ylabel("hd(n)")

plt.subplot(2,2,2)
plt.stem(n, w)
plt.title("Dãy hàm cửa sổ")
plt.grid()
plt.xlabel("n")
plt.ylabel("w(n)")

plt.subplot(2,2,3)
plt.stem(n, h)
plt.title("Hàm độ lớn tuyệt đối của đáp ứng tần số")
plt.grid()
plt.xlabel("n")
plt.ylabel("h(n)")

plt.subplot(2,2,4)
plt.plot(w_freq/np.pi, H_dB)
plt.title("Hàm độ lớn tương đối (dB) của đáp ứng tần số")
plt.xlabel("f / π")
plt.ylabel("Decibels)")
plt.grid()

plt.tight_layout()
plt.show()