import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firls, lfilter, freqz

print("=== FIR THÔNG THẤP - Least Squares ===")

# ====== Nhập ======
fs = float(input("Tần số lấy mẫu: "))
t_start = float(input("Thời gian bắt đầu: "))
t_end = float(input("Thời gian kết thúc: "))
f_signal = float(input("Tần số tín hiệu sin: "))
num_taps = int(input("Độ dài FIR: "))
cutoff_norm = float(input("Tần số cắt (theo Nyquist): "))

# ====== Fix num_taps ======
if num_taps % 2 == 0:
    num_taps += 1

# ====== Tín hiệu ======
t = np.arange(t_start, t_end, 1/fs)
x = np.sin(2*np.pi*f_signal*t) + 0.5*np.random.randn(len(t))

# ====== Thiết kế FIR ======
nyq = fs / 2
cutoff = cutoff_norm * nyq

transition = 0.1 * nyq
ws = cutoff + transition

if ws >= nyq:
    ws = cutoff + (nyq - cutoff)*0.5

bands = [0, cutoff, ws, nyq]
desired = [1, 1, 0, 0]

b = firls(num_taps, bands, desired, fs=fs)

# ====== Lọc ======
y = lfilter(b, 1, x)

# ====== Đáp ứng tần số (dB) ======
w, H = freqz(b, worN=1024, fs=fs)
H_dB = 20 * np.log10(np.abs(H) + 1e-6)

# ====== Vẽ ======
plt.figure(figsize=(10,8))

# trước lọc
plt.subplot(3,1,1)
plt.plot(t, x)
plt.title("Tín hiệu trước lọc")
plt.xlabel("Thời gian (s)")
plt.grid()

# sau lọc
plt.subplot(3,1,2)
plt.plot(t, y, color='green')
plt.title("Tín hiệu sau lọc")
plt.xlabel("Thời gian (s)")
plt.grid()

# đáp ứng tần số dB
plt.subplot(3,1,3)
plt.plot(w, H_dB)
plt.title("Đáp ứng tần số (dB)")
plt.xlabel("Tần số (Hz)")
plt.ylabel("Biên độ (dB)")
plt.grid()

plt.tight_layout()
plt.show()