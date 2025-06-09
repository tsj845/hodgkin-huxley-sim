from .common import TERMS
from .sim import MAIN_SIM as s, plot_var
from .plotting import plot_4x4, plt, plot_var_overlay

def show():
    # plot_4x4([s.l_V, s.l_m, s.l_h, s.l_n])
    s.l_V.settings["title"] = "TMP"
    plot_var_overlay([s.l_V, s.l_m, s.l_h, s.l_n], s.l_V)
    # plot_4x4([[s.l_V, 1000.0]]+[[x, 100.0] for x in (s.l_m, s.l_h, s.l_n)])
show()
# plot_var(s.l_V)

# leak = TERMS.leak(IV.V)
# potassium = TERMS.potassium(IV.V, IV.n)
# sodium = TERMS.sodium(IV.V, IV.m, IV.h)

# print(leak, potassium, sodium)
# print(leak + potassium + sodium)
