from .units import Unit, Value
from .funcs import N_GATE, M_GATE, H_GATE
from mpmath import mpf

class IV:
    V = Value(Unit.MILLIVOLTS, -65)
    n = N_GATE[1](V)
    m = M_GATE[1](V)
    h = H_GATE[1](V)
    I_EXTERNAL = Value(Unit.NANOAMPS/(Unit.MILLIMETERS**2), 200)/Value(Unit.NANOAMPS, 1)*Value(Unit.MILLIAMPS, mpf(1)/mpf(1000))
