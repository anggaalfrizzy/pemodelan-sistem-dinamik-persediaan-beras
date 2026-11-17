# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 13: Simulasi Persediaan Beras Rumah Tangga dengan Kebijakan Pembelian (ODEINT) =====
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# ---------------- parameter ----------------
n_orang = 4          # jumlah anggota keluarga
c_orang = 0.3        # konsumsi beras (kg/orang/hari)
kc = n_orang * c_orang / 100.0   # koefisien pemakaian (kg/hari per %) = 0.012
kb = 0.1             # koefisien pembelian (kg/hari per %)
ks = 0.002           # laju susut/rusak beras (1/hari)
ROP = 3.0            # titik pemesanan ulang (kg)
lama_beli = 1.0      # lama satu kali belanja (hari) -> 1 x 10 kg

# ---------------- model ----------------
def beras(S, t, ub, uc):
    pakai = kc * uc if S > 0 else 0.0     # tidak bisa memakai jika stok habis
    dSdt = kb * ub - pakai - ks * S
    return dSdt

# ---------------- simulasi satu skenario ----------------
def simulasi(u_hemat, T=60, dt=0.1, S0=10.0):
    N = int(T/dt)
    ts = np.linspace(0, T, N+1)
    S  = np.zeros(N+1); S[0] = S0
    ub = np.zeros(N+1); uc = np.zeros(N+1)
    sedang_beli, akhir_beli = False, 0.0
    jumlah_beli = 0
    for i in range(N):
        # kebijakan: beli 1 hari penuh jika stok <= ROP
        if sedang_beli and ts[i] >= akhir_beli:
            sedang_beli = False
        if (not sedang_beli) and S[i] <= ROP:
            sedang_beli, akhir_beli = True, ts[i] + lama_beli
            jumlah_beli += 1
        ub[i] = 100.0 if sedang_beli else 0.0
        # pemakaian: normal 100%, naik 150% saat ada acara keluarga (hari 30-37)
        faktor = 1.5 if 30 <= ts[i] < 37 else 1.0
        uc[i] = 100.0 * faktor * (1 - u_hemat)
        y = odeint(beras, S[i], [0, dt], args=(ub[i], uc[i]))
        S[i+1] = max(y[-1, 0], 0.0)
    ub[N], uc[N] = ub[N-1], uc[N-1]
    return ts, S, ub, uc, jumlah_beli

# ---------------- tiga skenario penghematan ----------------
hasil = {}
for u in [0.0, 0.1, 0.2]:
    hasil[u] = simulasi(u)
    ts, S, ub, uc, nb = hasil[u]
    total_beli = np.sum(kb * ub) * 0.1
    hari_habis = np.sum(S <= 0) * 0.1
    print(f'u = {u:.1f} | beli {nb} kali | total {total_beli:.0f} kg | '
          f'stok habis {hari_habis:.1f} hari | stok akhir {S[-1]:.2f} kg')

# ---------------- plot hasil ----------------
warna = {0.0: 'b-', 0.1: 'g--', 0.2: 'r:'}
plt.figure(figsize=(9, 6))
plt.subplot(2, 1, 1)
for u in hasil:
    plt.plot(hasil[u][0], hasil[u][1], warna[u], label=f'$u={u}$')
plt.axhline(ROP, color='gray', linestyle='--', linewidth=1)
plt.text(1, ROP - 0.6, 'ROP = 3 kg', color='gray')
plt.axvspan(30, 37, color='orange', alpha=0.15)
plt.ylabel('Stok Beras $S(t)$, (kg)')
plt.legend(frameon=False, ncol=3, loc='lower center', bbox_to_anchor=(0.5, 1.0))
plt.grid(alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(hasil[0.0][0], hasil[0.0][3], 'g-',  label='$u_c$ ($u=0$)')
plt.plot(hasil[0.0][0], hasil[0.0][2], 'r--', label='$u_b$ ($u=0$)')
plt.axvspan(30, 37, color='orange', alpha=0.15)
plt.ylabel('Kontrol $u(t)$, (%)')
plt.xlabel('$t$, (hari)')
plt.legend(frameon=False, loc='upper right')
plt.grid(alpha=0.3)
plt.show()


# ===== Program 14: Simulasi Persediaan Beras Rumah Tangga (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

# parameter sama dengan Program 13
kc, kb, ks = 0.012, 0.1, 0.002

# jadwal pembelian ub dan pemakaian uc skenario u = 0 diambil dari Program 13
ts, S_odeint, ub, uc, _ = hasil[0.0]

m = GEKKO()
m.time = ts
UB = m.Param(value=ub)           # intensitas pembelian (%)
UC = m.Param(value=uc)           # intensitas pemakaian (%)
S  = m.Var(10.0)                 # stok beras (kg)

# persamaan stok beras
m.Equation(S.dt() == kb * UB - kc * UC - ks * S)

# selesaikan ODE
m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

# bandingkan dengan hasil ODEINT
selisih = np.max(np.abs(np.array(S.value) - S_odeint))
print(f'Selisih maksimum GEKKO vs ODEINT = {selisih:.3f} kg')

plt.plot(ts, S_odeint, 'b-', label='ODEINT')
plt.plot(m.time, S.value, 'r--', label='GEKKO')
plt.xlabel('$t$, (hari)')
plt.ylabel('Stok Beras $S(t)$, (kg)')
plt.legend(frameon=False)
plt.grid(alpha=0.3)
plt.show()


