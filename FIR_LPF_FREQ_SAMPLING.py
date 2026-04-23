import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

print('Thiết kế bộ lọc thông thấp dùng phương pháp lấy mẫu tần số')

# 1. Nhập thông số bộ lọc
M = int(input('Số mẫu: '))  # Số mẫu
Wp = float(input('Tần số cắt dải truyền Wp (Wp * pi): ')) # Tần số cắt
f1 = float(input('Tần số thứ nhất (Hz): '))
f2 = float(input('Tần số thứ hai (Hz): '))
f3 = float(input('Tần số thứ ba (Hz): '))

fs = 2000 # Tần số lấy mẫu
m = np.arange(0, M // 2 + 1)
Wm = 2 * np.pi * m / (M + 1)

# 2. Thiết kế bộ lọc thông thấp (LPF)
# Ad = 1 trong dải thông (Wm <= Wp) và 0 trong dải chặn
Ad = (Wm <= Wp).astype(float)

# Xử lý dải quá độ (tương tự Ad(mtr) = 0.28 trong code của bạn)
mtr = np.where(Wm > Wp)[0]
if len(mtr) > 0:
    Ad[mtr[0]] = 0.28 

# Định nghĩa vector lấy mẫu trên miền tần số H(k)
Hd_half = Ad * np.exp(-1j * 0.5 * M * Wm)

# Tạo phổ đối xứng để đảm bảo h(n) là số thực
# Kết hợp phần dương và phần liên hợp đảo ngược
Hd = np.concatenate([Hd_half, np.conj(np.flip(Hd_half[1 : (M + 1) // 2 + 1]))])

# h(n) = IDFT[H(k)]
h = np.real(np.fft.ifft(Hd))

# 3. Tính toán đáp ứng tần số để vẽ đồ thị
w_plot, H_plot = signal.freqz(h, 1, worN=1000, fs=fs)

# FIGURE 1: Phản ứng biên độ
plt.figure(1, figsize=(8, 5))
plt.plot(w_plot / (fs/2), 20 * np.log10(np.abs(H_plot)))
plt.xlabel('Tần số chuẩn hóa (x pi rad/sample)')
plt.ylabel('G Gain/dB')
plt.title('Phản ứng biên độ của bộ lọc thông thấp')
plt.axis([0, 1, -60, 5])
plt.grid(True)

# 4. Tạo tín hiệu mô phỏng
t = np.arange(0, 0.25, 1/fs)
s = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + np.sin(2 * np.pi * f3 * t)

# FIGURE 2: Trước khi lọc
plt.figure(2, figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(t, s)
plt.title('Đồ thị miền thời gian trước khi lọc')
plt.xlabel('Thời gian/s')
plt.ylabel('Biên độ')

plt.subplot(2, 1, 2)
Fs = np.fft.fft(s, 512)
AFs = np.abs(Fs[:256])
f_axis = np.arange(256) * fs / 512
plt.plot(f_axis, AFs)
plt.title('Đồ thị miền tần số trước khi lọc')
plt.xlabel('Tần số/Hz')
plt.ylabel('Biên độ')
plt.tight_layout()

# 5. Lọc tín hiệu
sf = signal.lfilter(h, 1, s)

# FIGURE 3: Sau khi lọc
plt.figure(3, figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(t, sf)
plt.title('Đồ thị miền thời gian sau khi lọc')
plt.xlabel('Thời gian/s')
plt.ylabel('Biên độ')

plt.subplot(2, 1, 2)
Fsf = np.fft.fft(sf, 512)
AFsf = np.abs(Fsf[:256])
plt.plot(f_axis, AFsf)
plt.title('Đồ thị miền tần số sau khi lọc')
plt.xlabel('Tần số/Hz')
plt.ylabel('Biên độ')
plt.tight_layout()

plt.show()