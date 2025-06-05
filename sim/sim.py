from .common import *


class Sim:
    def __init__(self) -> None:
        self.l_m = TrackedVar("M", IV.m)
        self.l_n = TrackedVar("N", IV.n)
        self.l_h = TrackedVar("H", IV.h)
        self.l_V = TrackedVar("V", IV.V, unit=Unit.MILLIVOLTS)
    def run(self, time: mpf = mpf(1), *, pStart: mpf = mpf(0), pEnd: mpf = mpf(1)) -> None:
        """runs the simulation for the given time in seconds"""
        # time *= mpf(1000)
        # pStart *= mpf(1000)
        td = TIME_DELTA.mpf()/mpf(1000)
        # print(td)
        et = mpf(0)
        ITER = 0
        print(self.l_V.value, self.l_m.value, self.l_h.value, self.l_n.value, '\n', sep='\n', end='\n')
        while et < time:
            ITER += 1
            if ITER > 5:
                break
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
            ie = Value(Unit.MILLIVOLTS) if et < pStart or et > pEnd else IV.I_EXTERNAL
            (tau_v, v_inf) = V_PARTS(n=N, m=M, h=H, i_ext=ie)
            self.l_m.queue(m_inf.mpf() + ((M - m_inf).mpf()*exp(-td/tau_m.mpf())))
            self.l_h.queue(h_inf.mpf() + ((H - h_inf).mpf()*exp(-td/tau_h.mpf())))
            self.l_n.queue(n_inf.mpf() + ((N - n_inf).mpf()*exp(-td/tau_n.mpf())))
            self.l_V.queue(v_inf.mpf() + ((V - v_inf).mpf()*exp(-td/tau_v.mpf())))
            self.l_m.update(SET=True)
            self.l_h.update(SET=True)
            self.l_n.update(SET=True)
            self.l_V.update(SET=True)
            print(self.l_V.value, self.l_m.value, self.l_h.value, self.l_n.value, '\n', sep='\n', end='\n')
            et += td

MAIN_SIM = Sim()

MAIN_SIM.run()

print(f"{MAIN_SIM.l_V}\n\n{MAIN_SIM.l_n}\n\n{MAIN_SIM.l_m}\n\n{MAIN_SIM.l_h}")
