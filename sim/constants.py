from .units import Unit, Value, Conversion
from mpmath import mpf

DEBUG: bool = True
TIME_FREQ: int = 10**3
TIME_DELTA: Value = Conversion(Unit.SECONDS, Unit.MILLISECONDS, lambda x: x*mpf(1000))(Value(Unit.SECONDS, mpf(1)/mpf(TIME_FREQ)))

## nF/mm^2
CAPACITANCE = Value(Unit.NANOFARADS/(Unit.MILLIMETERS**2), 10)
class CONDUCTANCE:
    ## mS/mm^2
    _unit = Unit.MILLISIEMENS/(Unit.MILLIMETERS**2)
    LEAK = Value(_unit, mpf('0.003'))
    POTASSIUM = Value(_unit, mpf('0.36'))
    SODIUM = Value(_unit, mpf('1.2'))

class BATTERY:
    ## mV
    _unit = Unit.MILLIVOLTS
    LEAK = Value(_unit, mpf('-54.387'))
    POTASSIUM = Value(_unit, -77)
    SODIUM = Value(_unit, 50)

