from dataclasses import dataclass
from typing import Tuple

from utils import *
from utils import calc_current_divider


@dataclass
class Ex2Data:
    e_src: Voltage
    r1: Resistor
    r2: Resistor
    r3: Resistor


@dataclass
class Ex2Result:
    current: Current
    current1: Current
    current2: Current
    power: Power


class Ex2:
    data: Ex2Data

    def __init__(self, data: Ex2Data):
        self.data = data

    def __call__(self) -> Ex2Result:
        r23 = self.data.r2.parallel(self.data.r3)
        req = r23 + self.data.r1
        current = round_sig(self.data.e_src / req.value)
        voltage_xy = round_sig(current * r23.value)

        current1 = round_sig(voltage_xy / self.data.r3.value)
        current2 = round_sig(voltage_xy / self.data.r2.value)
        power = round_sig(current * self.data.e_src)

        return Ex2Result(current, current1, current2, power)
