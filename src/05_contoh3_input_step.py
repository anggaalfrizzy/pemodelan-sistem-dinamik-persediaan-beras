# -*- coding: utf-8 -*-
# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

# ===== Program 7: Program Untuk Contoh 3 (ODEINT) =====
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# fungsi yang mengembalikan dy/dt
def model(y, t):
    # u naik dari 0 ke 20 pada t = 10
    if t < 10.0:
        u = 0
    else:
        u = 20
    dydt = (-y + u) / 5.0
    return dydt

# kondisi awal
y0 = 10

# titik waktu
t = np.linspace(0, 40, 1000)

# selesaikan ODE
y = odeint(model, y0, t)

# plot hasil
plt.plot(t, y, 'r-', label='Output, $y(t)$')
plt.plot([0, 10, 10, 40], [0, 0, 20, 20], 'b-', label='Input, $u(t)$')
plt.ylabel('$y(t)$ dan $u(t)$, (kg)')
plt.xlabel('$t$, (hari)')
plt.legend(loc='best', frameon=False)
plt.grid(alpha=0.3)
plt.show()


# ===== Program 8: Program Untuk Contoh 3 (GEKKO) =====
import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

m = GEKKO()                       # membuat model GEKKO
m.time = np.linspace(0, 40, 401)  # titik waktu

# membuat parameter GEKKO (step 0 ke 20 pada t = 10)
ustep = np.zeros(401)
ustep[100:] = 20.0
u = m.Param(value=ustep)

y = m.Var(10.0)                   # membuat variabel GEKKO
m.Equation(5 * y.dt() == -y + u)  # membuat persamaan GEKKO

# selesaikan ODE
m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

# plot hasil
plt.plot(m.time, y.value, 'r-', label='Output ($y(t)$)')
plt.plot(m.time, u.value, 'b-', label='Input ($u(t)$)')
plt.xlabel('$t$, (hari)')
plt.ylabel('nilai (kg)')
plt.legend(loc='best')
plt.grid(alpha=0.3)
plt.show()


