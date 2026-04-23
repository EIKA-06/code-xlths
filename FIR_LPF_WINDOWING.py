import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

pf = float(input("Tần số dải thông (Hz): "))
sf = float(input("Tần số dải chặn (Hz): "))
d1 = float(input("Nhập độ gợn sóng : "))
fs = float(input("Nhập tần số lấy mẫu: "))

wp = 2 * np.pi * pf / fs
ws = 2 * np.pi * sf / fs
wc = (wp + ws) / 2
BW = abs(ws - wp)
As = -20 * np.log10(d1)

if As < 21: window_type, name, n = 'boxcar', 'Chữ nhật', int(np.ceil(4 * np.pi / BW))
elif As < 44: window_type, name, n = 'hann', 'Hanning', int(np.ceil(8 * np.pi / BW))
elif As < 53: window_type, name, n = 'hamming', 'Hamming', int(np.ceil(8 * np.pi / BW))
else: window_type, name, n = 'blackman', 'Blackman', int(np.ceil(12 * np.pi / BW))

m = n if n % 2 != 0 else n + 1
a = (m - 1) / 2
n_idx = np.arange(m)

# hd(n) lý tưởng
with np.errstate(divide='ignore', invalid='ignore'):
    hd = np.sin(wc * (n_idx - a)) / (np.pi * (n_idx - a))
hd[int(a)] = wc / np.pi 

# w(n) cửa sổ
if window_type == 'boxcar': w = np.ones(m)
elif window_type == 'hann': w = 0.5 * (1 - np.cos(2 * np.pi * n_idx / (m - 1)))
elif window_type == 'hamming': w = 0.54 - 0.46 * np.cos(2 * np.pi * n_idx / (m - 1))
elif window_type == 'blackman': w = 0.42 - 0.5 * np.cos(2 * np.pi * n_idx / (m - 1)) + 0.08 * np.cos(4 * np.pi * n_idx / (m - 1))

# h(n) thực tế
h = hd * w

# Đáp ứng tần số
w_freq, H = signal.freqz(h, worN=1000)
db = 20 * np.log10(np.abs(H) / np.max(np.abs(H)))

plt.figure(figsize=(12, 10))

# Hình 1: Đáp ứng xung lý tưởng 
plt.subplot(2, 2, 1)
plt.stem(n_idx, hd)
plt.title("Dãy đáp ứng xung của bộ lọc lý tưởng")
plt.xlabel("n")
plt.ylabel("hd(n)")
plt.grid(True)

# Hình 2: Dãy hàm cửa sổ
plt.subplot(2, 2, 2)
plt.stem(n_idx, w, 'orange')
plt.title(f"Dãy hàm cửa sổ ({name})")
plt.xlabel("n")
plt.ylabel("w(n)")
plt.grid(True)

# Hình 3: Đáp ứng xung thực tế
plt.subplot(2, 2, 3)
plt.stem(n_idx, h, 'green')
plt.title("Hàm độ lớn tuyệt đối của đáp ứng xung h(n)")
plt.xlabel("n")
plt.ylabel("h(n)")
plt.grid(True)

# Hình 4: Đáp ứng tần số dB 
plt.subplot(2, 2, 4)
plt.plot(w_freq / np.pi, db)
plt.title("Hàm độ lớn tương đối (dB) của đáp ứng tần số")
plt.xlabel("frequency in pi units")
plt.ylabel("Decibels")
plt.ylim([-100, 10])
plt.grid(True)

plt.tight_layout() 
plt.show()