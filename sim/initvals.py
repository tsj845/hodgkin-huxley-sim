from .units import Unit, Value
from .funcs import N_GATE, M_GATE, H_GATE

class IV:
    V = Value(Unit.MILLIVOLTS, -65)
    n = N_GATE[1](V)
    m = M_GATE[1](V)
    h = H_GATE[1](V)
    # I_EXTERNAL = Value(Unit.NANOAMPS/(Unit.MILLIMETERS**2), 200)/Value(Unit.NANOAMPS, 1)*Value(Unit.MILLIAMPS, 1.0/1000.0)
    I_EXTERNAL = Value(Unit.NANOAMPS/(Unit.MILLIMETERS**2), 200)
    # I_EXTERNAL = Value(Unit.NANOAMPS/(Unit.MILLIMETERS**2), 0)
    # I_EXTERNAL = Value(Unit.NANOAMPS/(Unit.MILLIMETERS**2), 200)

print(IV.V)
print(IV.m)
print(IV.h)
print(IV.n)
print(IV.I_EXTERNAL)
