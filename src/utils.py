import math
from dataclasses import dataclass
from typing import List

Voltage = float
Resistance = float
Power = float
Current = float


def round_sig(x, sig=4):
    if x == 0:
        return 0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def calc_parallel_resistance(resistors: List[any]) -> any:
    value = round_sig(1 / sum([round_sig(1 / r.value) for r in resistors]))
    return Resistor(value)


def calc_current_divider(src: Current, req: Resistance, rk: Resistance) -> Current:
    if type(src) != Current:
        raise ValueError("Invalid type for src.")

    if type(req) != Resistance:
        raise ValueError("Invalid type for req.")

    if type(rk) != Resistance:
        raise ValueError("Invalid type for rk.")

    resistance = round_sig(req / rk)
    return round_sig(src * resistance)


@dataclass
class Resistor:
    value: Resistance

    def __add__(self, rhs):
        value = round_sig(self.value + rhs.value)
        return Resistor(value)

    def parallel(self, rhs):
        return calc_parallel_resistance(
            [
                Resistor(self.value),
                Resistor(rhs.value),
            ]
        )
