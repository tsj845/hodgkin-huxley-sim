from .common import *
from .constants import I_EXT_UNIT
from .plotting import plot_var


class Sim:
    def __init__(self) -> None:
        self.l_m = TrackedVar("M", IV.m, scale=100.0, color="black", legend="m*100")
        self.l_n = TrackedVar("N", IV.n, scale=100.0, color="green", legend="n*100")
        self.l_h = TrackedVar("H", IV.h, scale=100.0, color="red", legend="h*100")
        self.l_V = TrackedVar("V", IV.V, unit=Unit.VOLTS, yLow=-90.0, yHigh=111.0, scale=1000.0, yStep=10.0, legend="V (mv)")
        self.l_V.settings.update(xLow=0, xStep=10, xScale=0.1)
    def run(self, time: float = 1.0, *, pStart: float = 0.0, pEnd: float = 1.0) -> None:
        """runs the simulation for the given time in seconds"""
        # time *= mpf(1000)
        # pStart *= mpf(1000)
        td: float = float(TIME_DELTA)
        print(td)
        et: float = 0.0
        ITER = 0
        # print(self.l_V.value, self.l_m.value, self.l_h.value, self.l_n.value, '\n', sep='\n', end='\n')
        while et < time:
            ITER += 1
            # if ITER > 7000:
            #     break
            V = self.l_V.value
            M = self.l_m.value
            N = self.l_n.value
            H = self.l_h.value
            tau_n = N_GATE[0](V)
            n_inf = N_GATE[1](V)
            tau_m = M_GATE[0](V)
            m_inf = M_GATE[1](V)
            tau_h = H_GATE[0](V)
            h_inf = H_GATE[1](V)
            ie = Value(I_EXT_UNIT) if et < pStart or et > pEnd else IV.I_EXTERNAL
            (tau_v, v_inf) = V_PARTS(n=N, m=M, h=H, i_ext=ie)
            # print((tau_n, n_inf), (tau_m, m_inf), (tau_h, h_inf), ie, (tau_v, v_inf), '\n', sep='\n', end='')
            # print(V)
            self.l_m.queue(float(m_inf) + (float(M - m_inf)*exp(-td/float(tau_m)*1000.0)))
            self.l_h.queue(float(h_inf) + (float(H - h_inf)*exp(-td/float(tau_h)*1000.0)))
            self.l_n.queue(float(n_inf) + (float(N - n_inf)*exp(-td/float(tau_n)*1000.0)))
            self.l_V.queue(float(v_inf) + (float(V - v_inf)*exp(-td/float(tau_v)*1000.0)))
            self.l_m.update(SET=True)
            self.l_h.update(SET=True)
            self.l_n.update(SET=True)
            self.l_V.update(SET=True)
            # print(self.l_V.value, self.l_m.value, self.l_h.value, self.l_n.value, '\n', sep='\n', end='\n')
            et += td

MAIN_SIM = Sim()

MAIN_SIM.run(0.07, pStart=0.01, pEnd=0.05)
# MAIN_SIM.run(0.5)
print(len(MAIN_SIM.l_V))

# print(f"{MAIN_SIM.l_V}\n\n{MAIN_SIM.l_n}\n\n{MAIN_SIM.l_m}\n\n{MAIN_SIM.l_h}")
