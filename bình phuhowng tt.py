import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

print("Thiết kế bộ lọc FIR THÔNG THẤP dùng phương pháp Bình phương tối thiểu (Least Squares)")

# 1. Nhập thông số bộ lọc
fs = float(input("Tần số lấy mẫu (fs): "))
t_start = float(input("Thời gian bắt đầu: "))
t_end = float(input("Thời gian kết thúc: "))
f_signal = float(input("Tần số của tín hiệu sin: "))
num_taps = int(input("Độ dài bộ lọc (số lượng mẫu - nên là số lẻ): "))
cutoff = float(input("Tần số cắt (Hz): "))

# 2. Tạo tín hiệu thời gian và tín hiệu nhiễu
t = np.arange(t_start, t_end, 1/fs)
x = np.sin(2 * np.pi * f_signal * t) + 0.5 * np.random.randn(len(t))

# 3. Thiết kế bộ lọc FIR Thông Thấp bằng firls
# Tần số trong firls của scipy được chuẩn hóa theo Nyquist (fs/2)
nyquist = fs / 2

# Định nghĩa các dải tần số (từ 0 đến Nyquist)
# Ví dụ: [Dải thông từ 0 đến cutoff, Dải chặn từ cutoff*1.2 đến Nyquist]
bands = np.array([0, cutoff, cutoff * 1.2, nyquist])
# Định nghĩa biên độ mong muốn tương ứng cho từng dải
# Thông thấp: Dải đầu tiên biên độ 1, dải sau biên độ 0
desired = np.array([1, 1, 0, 0])

# Tính toán các hệ số bộ lọc b
b = signal.firls(num_taps, bands, desired, fs=fs)

# 4. Áp dụng bộ lọc cho tín hiệu
y = signal.lfilter(b, 1, x)

# 5. Vẽ biểu đồ so sánh
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.title('Tín hiệu đầu vào (Sin + Nhiễu)')
plt.xlabel('Thời gian (s)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, y, color='green')
plt.title('Tín hiệu đầu ra sau khi lọc THÔNG THẤP (Least Squares)')
plt.xlabel('Thời gian (s)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()