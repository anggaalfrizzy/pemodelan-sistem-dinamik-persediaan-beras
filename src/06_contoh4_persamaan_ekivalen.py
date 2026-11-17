# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 9: Program Untuk Contoh 4 (ODEINT) =====
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# fungsi yang mengembalikan dz/dt
def model(z, t):
    dxdt = 3.0 * np.exp(-t)
    dydt = -z[1] + 3
    dzdt = [dxdt, dydt]
    return dzdt

# kondisi awal
z0 = [0, 0]

# titik waktu
t = np.linspace(0, 5)

# selesaikan ODE
z = odeint(model, z0, t)

# plot hasil
plt.plot(t, z[:, 0], 'b-',  label=r'$\frac{dx}{dt}=3\,\exp(-t)$')
plt.plot(t, z[:, 1], 'r--', label=r'$\frac{dy}{dt}=-y+3$')
plt.ylabel('$x(t),\\; y(t)$, (kg)')
plt.xlabel('$t$, (hari)')
plt.legend(loc='best', frameon=False)
plt.grid(alpha=0.3)
plt.show()


# ===== Program 10: Program Untuk Contoh 4 (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()                       # membuat model GEKKO
m.time = np.linspace(0, 5)        # titik waktu

t = m.Var(0.0)                    # membuat waktu sebagai variabel GEKKO
x = m.Var(0.0)                    # membuat variabel GEKKO x
y = m.Var(0.0)                    # membuat variabel GEKKO y

# membuat persamaan GEKKO
m.Equation(t.dt() == 1)
m.Equation(x.dt() == 3 * m.exp(-t))
m.Equation(y.dt() == 3 - y)

# selesaikan ODE
m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

# plot hasil
plt.plot(t.value, x.value, 'b-',  label=r'$\frac{dx}{dt}=3\,e^{-t}$')
plt.plot(t.value, y.value, 'r--', label=r'$\frac{dy}{dt}=-y+3$')
plt.ylabel('respon (kg)')
plt.xlabel('waktu (hari)')
plt.legend(loc='best')
plt.grid(alpha=0.3)
plt.show()


