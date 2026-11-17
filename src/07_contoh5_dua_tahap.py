# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 11: Program Untuk Contoh 5 (ODEINT) =====
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# fungsi yang mengembalikan dz/dt
def model(z, t, u):
    x = z[0]
    y = z[1]
    dxdt = (-x + u) / 2.0
    dydt = (-y + x) / 5.0
    dzdt = [dxdt, dydt]
    return dzdt

# kondisi awal
z0 = [0, 0]

# jumlah titik waktu
n = 401

# titik waktu
t = np.linspace(0, 40, n)

# input step
u = np.zeros(n)
# berubah menjadi 20 pada t = 5.0
u[50:] = 20.0

# penyimpanan solusi
x = np.empty_like(t)
y = np.empty_like(t)
# catat kondisi awal
x[0] = z0[0]
y[0] = z0[1]

# selesaikan ODE
for i in range(1, n):
    # rentang waktu untuk langkah berikutnya
    tspan = [t[i-1], t[i]]
    # selesaikan langkah berikutnya
    z = odeint(model, z0, tspan, args=(u[i-1],))
    # simpan solusi untuk plot
    x[i] = z[1][0]
    y[i] = z[1][1]
    # kondisi awal berikutnya
    z0 = z[1]

# plot hasil
plt.plot(t, u, 'g:',  label='$u(t)$')
plt.plot(t, x, 'b-',  label='$x(t)$')
plt.plot(t, y, 'r--', label='$y(t)$')
plt.ylabel('$u(t),\\; x(t),\\; y(t)$, (kg)')
plt.xlabel('$t$, (hari)')
plt.legend(loc='best', frameon=False)
plt.grid(alpha=0.3)
plt.show()


# ===== Program 12: Program Untuk Contoh 5 (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()                       # membuat model GEKKO
m.time = np.linspace(0, 40, 401)  # titik waktu

# membuat parameter GEKKO (step 0 ke 20 pada t = 5)
ustep = np.zeros(401)
ustep[50:] = 20.0
u = m.Param(value=ustep)

# membuat variabel GEKKO
x = m.Var(0.0)
y = m.Var(0.0)

# membuat persamaan GEKKO
m.Equation(2 * x.dt() == -x + u)
m.Equation(5 * y.dt() == -y + x)

# selesaikan ODE
m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

# plot hasil
plt.plot(m.time, u.value, 'g:',  label='$u(t)$')
plt.plot(m.time, x.value, 'b-',  label='$x(t)$')
plt.plot(m.time, y.value, 'r--', label='$y(t)$')
plt.xlabel('$t$, (hari)')
plt.ylabel('nilai (kg)')
plt.legend(loc='best')
plt.grid(alpha=0.3)
plt.show()


