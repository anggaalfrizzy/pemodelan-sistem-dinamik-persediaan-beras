# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 1: Simulasi Stok Beras Hanya dengan Pembelian (ODEINT) =====
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# model stok beras: hanya ada pembelian, pemakaian diabaikan
def stok(S, t, kb, ub):
    dSdt = kb * ub                # laju penambahan stok (kg/hari)
    return dSdt

# waktu simulasi 30 hari, setiap 0.1 hari
ts = np.linspace(0, 30, 301)

# operasi pembelian
kb = 0.1                          # koefisien pembelian (kg/hari per %)
ub = np.zeros(301)                # ub = intensitas pembelian (%)
for hari in [3, 11, 19, 27]:      # belanja selama 1 hari penuh
    ub[hari*10:(hari+1)*10] = 100.0

# kondisi awal stok
S0 = 5.0

# penyimpanan hasil
z = np.zeros(301)
z[0] = S0

# simulasi dengan ODEINT
for i in range(300):
    y = odeint(stok, S0, [0, 0.1], args=(kb, ub[i]))
    S0 = y[-1, 0]                 # ambil titik terakhir
    z[i+1] = S0                   # simpan stok untuk plot

# plot hasil
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(ts, z, 'b-')
plt.ylabel('Stok Beras $S(t)$, (kg)')
plt.grid(alpha=0.3)
plt.subplot(2, 1, 2)
plt.plot(ts, ub, 'r--')
plt.ylabel('Pembelian $u_b(t)$, (%)')
plt.xlabel('$t$, (hari)')
plt.show()


