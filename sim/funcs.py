from typing import *
# from .constants import CAPACITANCE, TIME_DELTA, CONDUCTANCE, BATTERY
# from .units import Units, Unit, Value, Conversion
from .common import *

type FTransform = Callable[[float], float]
type TauLike = Callable[[Value], Value]
type NinfLike = Callable[[Value], Value]
type TNDuo = Tuple[TauLike, NinfLike]

# def probability(voltage: float, alpha: Callable[[float], float], beta: Callable[[float], float]) -> float:
#     ...
def probability_funcs(*, alpha: FTransform = None, beta: FTransform = None) -> TNDuo:
    def tau(v: Value) -> Value:
        v + Value(Unit.MILLIVOLTS)
        f = v.mpf()
        return Value(-v.unit, mpf(1)/(alpha(f)+beta(f)))
    def n_inf(v: Value) -> Value:
        v + Value(Unit.MILLIVOLTS)
        f = v.mpf()
        a = alpha(f)
        return Value(Unit.DIMENSIONLESS, a/(a+beta(f)))
    return (tau, n_inf)

N_GATE: TNDuo = probability_funcs(
    alpha=(lambda x: mpf('0.01')*(x+mpf('55'))/(mpf(1)-exp(mpf('-0.1')*(x+mpf('55'))))),
    beta=(lambda x: mpf('0.125')*exp(mpf('-0.0125')*(x+mpf('65'))))
)
M_GATE: TNDuo = probability_funcs(
    alpha=(lambda x: mpf('0.1')*(x+mpf('40'))/(mpf('1')-exp(mpf('-0.1')*(x+mpf('40'))))),
    beta=(lambda x: mpf('4')*exp(mpf('-0.0556')*(x+mpf('65'))))
)
H_GATE: TNDuo = probability_funcs(
    alpha=(lambda x: mpf('0.07')*exp(mpf('-0.05')*(x+mpf('65')))),
    beta=(lambda x: mpf('1')/(1+exp(mpf('-0.1')*(x+mpf('35')))))
)

def V_PARTS(*, n: Value = None, m: Value = None, h: Value = None, i_ext: Value = None) -> tuple[Value, Value]:
    den = (CONDUCTANCE.LEAK + CONDUCTANCE.POTASSIUM*n**4 + CONDUCTANCE.SODIUM*h*m**3)
    return (
        CAPACITANCE/den,
        # (CONDUCTANCE.LEAK*BATTERY.LEAK +
        #     CONDUCTANCE.POTASSIUM*BATTERY.POTASSIUM*n**4 +
        #     CONDUCTANCE.SODIUM*BATTERY.SODIUM*h*m**3 +
        #     i_ext).dbg("VINF")/(den.dbg())
        (CONDUCTANCE.LEAK*BATTERY.LEAK +
            CONDUCTANCE.POTASSIUM*BATTERY.POTASSIUM*n**4 +
            CONDUCTANCE.SODIUM*BATTERY.SODIUM*h*m**3 +
            i_ext)/den
        )

class TERMS:
    def leak(v: Value) -> Value:
        return CONDUCTANCE.LEAK * (v - BATTERY.LEAK)
    def potassium(v: Value, n: Value) -> Value:
        return CONDUCTANCE.POTASSIUM * n**4 * (v - BATTERY.POTASSIUM)
    def sodium(v: Value, m: Value, h: Value) -> Value:
        return CONDUCTANCE.SODIUM * m**3 * h * (v - BATTERY.SODIUM)
