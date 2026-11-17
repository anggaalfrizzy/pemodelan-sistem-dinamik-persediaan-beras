# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 2: Simulasi Stok Beras dengan Pembelian dan Pemakaian (ODEINT) =====
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# model stok beras: pembelian dan pemakaian
def stok(S, t, kb, kc, ub, uc):
    dSdt = kb * ub - kc * uc      # laju pembelian - laju pemakaian
    return dSdt

# waktu simulasi 30 hari, setiap 0.1 hari
ts = np.linspace(0, 30, 301)

# operasi pembelian dan pemakaian
kb = 0.1                          # koefisien pembelian (kg/hari per %)
kc = 0.012                        # koefisien pemakaian (kg/hari per %)
ub = np.zeros(301)                # ub = intensitas pembelian (%)
for hari in [3, 11, 19, 27]:
    ub[hari*10:(hari+1)*10] = 100.0
uc = np.full(301, 100.0)          # uc = intensitas pemakaian (%) -> 1.2 kg/hari

# kondisi awal stok
S0 = 5.0

# penyimpanan hasil
z = np.zeros(301)
z[0] = S0

# simulasi dengan ODEINT
for i in range(300):
    y = odeint(stok, S0, [0, 0.1], args=(kb, kc, ub[i], uc[i]))
    S0 = y[-1, 0]
    z[i+1] = S0

# plot hasil
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(ts, z, 'b-')
plt.ylabel('Stok Beras $S(t)$, (kg)')
plt.grid(alpha=0.3)
plt.subplot(2, 1, 2)
plt.plot(ts, ub, 'r--', label='$u_b$')
plt.plot(ts, uc, 'g--', label='$u_c$')
plt.ylabel('Kontrol $u(t)$, (%)')
plt.xlabel('$t$, (hari)')
plt.legend(frameon=False)
plt.show()


