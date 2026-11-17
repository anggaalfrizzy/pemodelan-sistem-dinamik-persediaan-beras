# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 5: Program Untuk Contoh 2 (ODEINT) =====
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# fungsi yang mengembalikan dy/dt
def model(y, t, k):
    dydt = -k * y
    return dydt

# kondisi awal
y0 = 20

# titik waktu
t = np.linspace(0, 20)

# selesaikan ODE untuk tiga nilai k
k = 0.05
y1 = odeint(model, y0, t, args=(k,))
k = 0.1
y2 = odeint(model, y0, t, args=(k,))
k = 0.2
y3 = odeint(model, y0, t, args=(k,))

# plot hasil
plt.plot(t, y1, 'r-',  label='$k=0.05$')
plt.plot(t, y2, 'b--', label='$k=0.1$')
plt.plot(t, y3, 'g:',  label='$k=0.2$')
plt.xlabel('$t$, (hari)')
plt.ylabel('$y(t)$, (kg)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()


# ===== Program 6: Program Untuk Contoh 2 (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()                       # membuat model GEKKO
k = m.Param()                     # konstanta
y = m.Var(20.0)                   # membuat variabel GEKKO
m.Equation(y.dt() == -k * y)      # membuat persamaan GEKKO
m.time = np.linspace(0, 20)       # titik waktu

# selesaikan ODE dan plot
m.options.IMODE = 4
m.options.NODES = 3
m.options.TIME_SHIFT = 0

k.value = 0.05
m.solve(disp=False)
plt.plot(m.time, y.value, 'r-', linewidth=2, label='$k=0.05$')

k.value = 0.1
m.solve(disp=False)
plt.plot(m.time, y.value, 'b--', linewidth=2, label='$k=0.1$')

k.value = 0.2
m.solve(disp=False)
plt.plot(m.time, y.value, 'g:', linewidth=2, label='$k=0.2$')

plt.xlabel('$t$, (hari)')
plt.ylabel('$y(t)$, (kg)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()


