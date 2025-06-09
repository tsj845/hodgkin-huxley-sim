from .units import Unit, Value, Conversion

DEBUG: bool = False
TIME_FREQ: int = 10**4
TIME_DELTA: Value = Value(Unit.SECONDS, 1.0/float(TIME_FREQ))

I_EXT_UNIT = Unit.MILLIAMPS/(Unit.MILLIMETERS**2)

## nF/mm^2
CAPACITANCE = Value(Unit.NANOFARADS/(Unit.MILLIMETERS**2), 10)
# CAPACITANCE = Value(Unit.FARADS/(Unit.METERS**2), 10)
class CONDUCTANCE:
    ## mS/mm^2
    # _unit = Unit.MILLISIEMENS/(Unit.MILLIMETERS**2)
    # LEAK = Value(_unit, 0.003)
    # POTASSIUM = Value(_unit, 0.36)
    # SODIUM = Value(_unit, 1.2)
    _unit = Unit.MICROSIEMENS/(Unit.MILLIMETERS**2)
    LEAK = Value(_unit, 0.003e3)
    POTASSIUM = Value(_unit, 0.36e3)
    SODIUM = Value(_unit, 1.2e3)

class BATTERY:
    ## mV
    _unit = Unit.MILLIVOLTS
    LEAK = Value(_unit, -54.387)
    POTASSIUM = Value(_unit, -77)
    SODIUM = Value(_unit, 50)

print(CAPACITANCE)
print(CONDUCTANCE.LEAK, CONDUCTANCE.POTASSIUM, CONDUCTANCE.SODIUM)
print(BATTERY.LEAK, BATTERY.POTASSIUM, BATTERY.SODIUM)

