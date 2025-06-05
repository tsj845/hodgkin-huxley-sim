from typing import *
from .units import Unit, Value
from .constants import DEBUG
from mpmath import mpf

class TrackedVar:
    def __init__(self, name: str, initval: mpf = mpf(0), *, unit: Unit = Unit.DIMENSIONLESS) -> None:
        self.unit = unit
        self.name = name
        self.val = None
        if (isinstance(initval, Value)):
            self.val = initval.mpf()
        else:
            self.val = mpf(initval)
        self.record = [initval]
        self._Qdelta = None
    @property
    def value(self) -> Value:
        return Value(self.unit, self.val)
    def update(self, delta: float = None, *, SET: bool = False) -> mpf:
        """adds delta to the current value, records it, and returns the new value"""
        if (delta is None):
            delta = self._Qdelta
        self._Qdelta = None
        if (delta is None):
            raise ValueError("no delta supplied")
        if DEBUG:
            if SET:
                print(f"{self.name} = {delta}")
            else:
                print(f"{self.name} += {delta}")
        if SET:
            self.val = delta
        else:
            self.val += delta
        self.record.append(self.val)
        return self.val
    def queue(self, delta: mpf) -> None:
        """queues delta for update"""
        self._Qdelta = delta
    def __str__(self) -> str:
        return f"{self.name} = {self.val} ({', '.join(map(str, self.record))})"
    def __repr__(self) -> str:
        return f"TrackedVar[{self.name} = {self.val} (+{len(self.record)})]"
