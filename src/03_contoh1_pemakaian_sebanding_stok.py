# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 3: Program Untuk Contoh 1 (ODEINT) =====
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# fungsi yang mengembalikan dS/dt
def model(y, t):
    k = 0.1
    dydt = -k * y
    return dydt

# kondisi awal
y0 = 10

# titik waktu
t = np.linspace(0, 20)

# selesaikan ODE
y = odeint(model, y0, t)

# plot hasil
plt.plot(t, y)
plt.xlabel('$t$, (hari)')
plt.ylabel('$y(t)$, (kg)')
plt.grid(alpha=0.3)
plt.show()


# ===== Program 4: Program Untuk Contoh 1 (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()                       # membuat model GEKKO
k = 0.1                           # konstanta
y = m.Var(10.0)                   # membuat variabel GEKKO
m.Equation(y.dt() == -k * y)      # membuat persamaan GEKKO
m.time = np.linspace(0, 20)       # titik waktu

# selesaikan ODE
m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

# plot hasil
plt.plot(m.time, y.value)
plt.xlabel('$t$, (hari)')
plt.ylabel('$y(t)$, (kg)')
plt.grid(alpha=0.3)
plt.show()


