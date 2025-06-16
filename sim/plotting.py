from typing import *
from .units import Unit, Value
from .constants import DEBUG
import matplotlib.pyplot as plt
# import numpy as np
from math import ceil

class TrackedVar:
    def __init__(self, name: str, initval: float = 0.0, *, unit: Unit = Unit.DIMENSIONLESS, xStep: int = 1, scale: float = 1.0, yLow: float = 0.0, yHigh: float = 100.0, yStep: float = 10.0, color: str = "blue", legend: str = "_") -> None:
        self.unit = unit
        self.name = name
        self.val = float(initval)
        # if (isinstance(initval, Value)):
        #     self.val = initval.mpf()
        # else:
        #     self.val = mpf(initval)
        self.record = [float(initval)]
        self._Qdelta = None
        self.settings = {"xStep":xStep, "scale":scale, "yLow":yLow, "yHigh":yHigh, "yStep":yStep, "color":color, "legend":legend}
    @property
    def value(self) -> Value:
        return Value(self.unit, self.val)
    def update(self, delta: float = None, *, SET: bool = False) -> float:
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
    def queue(self, delta: float) -> None:
        """queues delta for update"""
        self._Qdelta = delta
    def __str__(self) -> str:
        return f"{self.name} = {self.val} ({', '.join(map(str, self.record))})"
    def __repr__(self) -> str:
        return f"TrackedVar[{self.name} = {self.val} (+{len(self.record)})]"
    def __len__(self) -> int:
        return len(self.record)

def plot_var(v: TrackedVar, xStep: int = 1) -> None:
    fig, ax = plt.subplots()
    ax.plot(range(0,len(v)*xStep,xStep), v.record)
    plt.show()

def plot_var_overlay(vs: list[TrackedVar], s: TrackedVar) -> None:
    fig, ax = plt.subplots()
    yLow = s.settings["yLow"]
    yHigh = s.settings["yHigh"]
    yStep = s.settings["yStep"]
    xStep = s.settings["xStep"]
    ax.set_ylim(ymin=yLow, ymax=yHigh)
    ax.set_xlabel("Time (ms)")
    c = ceil((yHigh-yLow)/yStep)
    # ax.set_yticks([float(p)/c for p in range(c)], [float(i)*yStep for i in range(c)])
    ax.set_yticks([float(i)*yStep+yLow for i in range(c)], [float(i)*yStep+yLow for i in range(c)])
    ax.set_title(s.settings["title"])
    for v in vs:
        scale = v.settings["scale"]
        ax.plot(range(0,len(v)*xStep,xStep), list(map(lambda x: x*scale, v.record)), color=v.settings["color"], label=v.settings["legend"])
    fig.legend()
    plt.show()

def plot_ax_var(ax: plt.Axes, v: TrackedVar) -> None:
    xStep = v.settings["xStep"]
    scale = v.settings["scale"]
    yLow = v.settings["yLow"]
    yHigh = v.settings["yHigh"]
    yStep = v.settings["yStep"]
    ax.set_ylim(ymin=yLow, ymax=yHigh)
    c = ceil((yHigh-yLow)/yStep)
    # ax.set_yticks([float(p)/c for p in range(c)], [float(i)*yStep for i in range(c)])
    ax.set_yticks([float(i)*yStep+yLow for i in range(c)], [float(i)*yStep+yLow for i in range(c)])
    ax.set_title(v.name)
    ax.plot(range(0,len(v)*xStep,xStep), list(map(lambda x: x*scale, v.record)))
# def plot_ax_var(ax: plt.Axes, v: TrackedVar, scale: float = 1.0, xStep: int = 1) -> None:
#     ax.plot(range(0,len(v)*xStep,xStep), list(map(lambda x: x*scale, v.record)))

# def plot_4x4(vs: list[tuple[TrackedVar, float, int]|tuple[TrackedVar, float]]) -> None:
def plot_4x4(vs: list[TrackedVar]) -> None:
    fig, axs = plt.subplots(2, 2)
    i = 0
    for y in range(len(axs)):
        for x in range(len(axs[y])):
            plot_ax_var(axs[y][x], vs[i])
            # plot_ax_var(axs[y][x], vs[i][0], vs[i][1], 1 if len(vs[i]) == 2 else vs[i][2])
            i += 1
    plt.show()
