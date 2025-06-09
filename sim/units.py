from typing import *
# from enum import IntEnum

class UnitError(TypeError):
    ...

# Farad = float
# Second = float

class Units:
    Second = 0
    Farad = 1
    Volt = 2
    Siemens = 3
    Amp = 4
    Meter = 5
    def __getattribute__(self, name):
        if name == "Siemens":
            raise NameError("Siemens is no longer allowed")
        return super().__getattribute__(name)
    def len() -> int:
        return 6

UNIT_ABBRV: Final = ("s", "F", "V", "S", "A", "m")
PREFIX_ABBRV: Final = ("n","µ","m","","")
PREFIX_OFFSET: Final = PREFIX_ABBRV.index("")
type SingleUnit = Tuple[int, int]

def getUnitAbbrv(unit: SingleUnit) -> str:
    return f"{PREFIX_ABBRV[PREFIX_OFFSET+(unit[1]//3)]}{UNIT_ABBRV[unit[0]]}"

def fmtHalfUnit(unit: list[SingleUnit]) -> str:
    f = []
    i = 0
    l = len(unit)
    while i < l:
        c = unit.count(unit[i])
        p = getUnitAbbrv(unit[i])
        f.append(p if c == 1 else f"{p}^{c}")
        i += c
    return " * ".join(f)


class Unit:
    SECONDS: Self = None;MILLISECONDS: Self = None;MICROSECONDS: Self = None;NANOSECONDS: Self = None
    FARADS: Self = None;MILLIFARADS: Self = None;MICROFARADS: Self = None;NANOFARADS: Self = None
    VOLTS: Self = None;MILLIVOLTS: Self = None;MICROVOLTS: Self = None;NANOVOLTS: Self = None
    SIEMENS: Self = None;MILLISIEMENS: Self = None;MICROSIEMENS: Self = None;NANOSIEMENS: Self = None
    AMPS: Self = None;MILLIAMPS: Self = None;MICROAMPS: Self = None;NANOAMPS: Self = None
    METERS: Self = None;MILLIMETERS: Self = None;MICROMETERS: Self = None;NANOMETERS: Self = None
    DIMENSIONLESS: Self = None
    def __init__(self, numerator: List[SingleUnit] = None, denominator: List[SingleUnit] = None) -> None:
        BSU = TypeError("BAD SINGLE UNIT")
        self.numerator = sorted(numerator or [])
        self.denominator = sorted(denominator or [])
        for i in range(len(self.numerator)):
            # print(self.numerator[i])
            if (type(self.numerator[i]) != tuple):
                print(numerator)
                raise BSU
            if (type(self.numerator[i][0]) != type(self.numerator[i][1]) or type(self.numerator[i][0]) != int):
                print(numerator)
                raise BSU
        for i in range(len(self.denominator)):
            if (type(self.denominator[i]) != tuple):
                print(denominator)
                raise BSU
            if (type(self.denominator[i][0]) != type(self.denominator[i][1]) or type(self.denominator[i][0]) != int):
                print(denominator)
                raise BSU
        i = len(self.numerator) - 1
        while i >= 0:
            if (self.numerator[i] in self.denominator):
                self.denominator.remove(self.numerator[i])
                self.numerator.pop(i)
            i -= 1
    def __str__(self) -> str:
        return f"{fmtHalfUnit(self.numerator)}" + (f" / {fmtHalfUnit(self.denominator)}" if len(self.denominator) else "")
        # return f"{' * '.join([getUnitAbbrv(x) for x in self.numerator])}" + (f" / {' * '.join([getUnitAbbrv(x) for x in self.denominator])}" if len(self.denominator) else "")
    def __repr__(self) -> str:
        return f"Unit[{self}]"
    def __eq__(self, other) -> bool:
        return isinstance(other, Unit) and self.numerator == other.numerator and self.denominator == other.denominator
    def __mul__(self, other) -> Self:
        if (not isinstance(other, Unit)):
            raise TypeError("can only multiply units by other units")
        return Unit(self.numerator+other.numerator, self.denominator+other.denominator)
    def __truediv__(self, other) -> Self:
        if (not isinstance(other, Unit)):
            raise TypeError("can only divide units by other units")
        return Unit(self.numerator+other.denominator, self.denominator+other.numerator)
    def __neg__(self) -> Self:
        return Unit(self.denominator, self.numerator)
    def __pow__(self, power: int) -> Self:
        if (type(power) != int):
            raise TypeError("can only raise unit to integer power")
        r = Unit.DIMENSIONLESS
        for _ in range(power):
            r *= self
        return r
    def simplify(self, value: float) -> tuple[Self, float]:
        """simplifies the unit"""
        n = [[] for _ in range(Units.len())]
        d = [[] for _ in range(Units.len())]
        factor = 1.0
        for i in range(len(self.numerator)):
            n[self.numerator[i][0]].append(self.numerator[i])
        for i in range(len(self.denominator)):
            d[self.denominator[i][0]].append(self.denominator[i])
        for i in range(len(n)):
            while len(n[i]) > 0 and len(d[i]) > 0:
                ln = n[i].pop()
                ld = d[i].pop()
                factor /= (10**(-ln[1]))
                factor *= (10**(-ld[1]))
        for l in n:
            for i in range(len(l)):
                if l[i][1] != 0:
                    factor /= (10**(-l[i][1]))
                    l[i] = (l[i][0], 0)
        for l in d:
            for i in range(len(l)):
                if l[i][1] != 0:
                    factor *= (10**(-l[i][1]))
                    l[i] = (l[i][0], 0)
        return (Unit([x for i in range(len(n)) for x in n[i]], [x for i in range(len(d)) for x in d[i]]), value * factor)
    def similar(self, other: Self) -> bool:
        if (not isinstance(other, Unit)):
            raise TypeError("can only check similarity of Unit classes")
        if len(self.numerator) != len(other.numerator) or len(self.denominator) != len(other.denominator):
            return False
        n1 = [[] for _ in range(Units.len())]
        n2 = [[] for _ in range(Units.len())]
        d1 = [[] for _ in range(Units.len())]
        d2 = [[] for _ in range(Units.len())]
        for i in range(len(self.numerator)):
            n1[self.numerator[i][0]].append(self.numerator[i])
        for i in range(len(self.denominator)):
            d1[self.denominator[i][0]].append(self.denominator[i])
        for i in range(len(other.numerator)):
            n2[other.numerator[i][0]].append(other.numerator[i])
        for i in range(len(other.denominator)):
            d2[other.denominator[i][0]].append(other.denominator[i])
        for i in range(len(n1)):
            if len(n1[i]) != len(n2[i]):
                return False
        for i in range(len(d1)):
            if len(d1[i]) != len(d2[i]):
                return False
        return True


Unit.DIMENSIONLESS = Unit()
Unit.SECONDS = Unit([(Units.Second, 0)]);Unit.MILLISECONDS = Unit([(Units.Second, -3)]);Unit.MICROSECONDS = Unit([(Units.Second, -6)]);Unit.NANOSECONDS = Unit([(Units.Second, -9)])
Unit.FARADS = Unit([(Units.Farad, 0)]);Unit.MILLIFARADS = Unit([(Units.Farad, -3)]);Unit.MICROFARADS = Unit([(Units.Farad, -6)]);Unit.NANOFARADS = Unit([(Units.Farad, -9)])
Unit.VOLTS = Unit([(Units.Volt, 0)]);Unit.MILLIVOLTS = Unit([(Units.Volt, -3)]);Unit.MICROVOLTS = Unit([(Units.Volt, -6)]);Unit.NANOVOLTS = Unit([(Units.Volt, -9)])
Unit.AMPS = Unit([(Units.Amp, 0)]);Unit.MILLIAMPS = Unit([(Units.Amp, -3)]);Unit.MICROAMPS = Unit([(Units.Amp, -6)]);Unit.NANOAMPS = Unit([(Units.Amp, -9)])
Unit.SIEMENS = Unit.AMPS/Unit.VOLTS;Unit.MILLISIEMENS = Unit.MILLIAMPS/Unit.VOLTS;Unit.MICROSIEMENS = Unit.MICROAMPS/Unit.VOLTS;Unit.NANOSIEMENS = Unit.NANOAMPS/Unit.VOLTS
Unit.METERS = Unit([(Units.Meter, 0)]);Unit.MILLIMETERS = Unit([(Units.Meter, -3)]);Unit.MICROMETERS = Unit([(Units.Meter, -6)]);Unit.NANOMETERS = Unit([(Units.Meter, -9)])

class Value:
    def __init__(self, unit: Unit, val: float = 0.0) -> None:
        if (not isinstance(unit, Unit)):
            raise TypeError("Value requires a valid Unit")
        unit, val = unit.simplify(float(val))
        self.unit = unit
        self.value = val
    def mpf(self) -> float:
        return self.value
    def dbg(self, *args) -> Self:
        print(*args)
        print(self)
        return self
    def __float__(self) -> float:
        return self.value
    def __str__(self) -> str:
        return f"{self.value} {self.unit}"
    def __repr__(self) -> str:
        return f"Value[{self}]"
    def __add__(self, other) -> Self:
        if (not isinstance(other, Value)):
            raise TypeError("can't do math on non-values")
        if (self.unit != other.unit):
            print(self, other)
            raise UnitError("can't add mismatched units")
        return Value(self.unit, self.value + other.value)
    def __sub__(self, other) -> Self:
        if (not isinstance(other, Value)):
            raise TypeError("can't do math on non-values")
        if (self.unit != other.unit):
            # if self.unit.similar(other.unit):
            #     ...
            print(self, other)
            raise UnitError("can't subtract mismatched units")
        return Value(self.unit, self.value - other.value)
    def __mul__(self, other) -> Self:
        if (not isinstance(other, Value)):
            raise TypeError("can't do math on non-values")
        return Value(self.unit*other.unit, self.value * other.value)
    def __truediv__(self, other) -> Self:
        if (not isinstance(other, Value)):
            raise TypeError("can't do math on non-values")
        return Value(self.unit/other.unit, self.value / other.value)
    def __neg__(self) -> Self:
        return Value(self.unit, -self.value)
    def __pos__(self) -> Self:
        return Value(self.unit, +self.value)
    def __pow__(self, power: int) -> Self:
        if (type(power) != int):
            raise ArithmeticError("can't raise Value to non-integer power")
        return Value(self.unit, self.value**power)

class Conversion:
    def __init__(self, input: Unit, output: Unit, transform: Callable[[float], float]) -> None:
        self.input = input
        self.output = output
        self.transform = transform
    def __call__(self, value: Value) -> Value:
        if (value.unit != self.input):
            raise UnitError(f"cannot use {self.input} converter to convert {value.unit}")
        return Value(self.output, self.transform(float(value)))
    def coerce(value: Value, unit: Unit) -> Value:
        """attempts to convert the value into the given unit"""
        factor = 1
