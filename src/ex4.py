from dataclasses import dataclass
from typing import Tuple

from utils import *
from utils import calc_current_divider


@dataclass
class Ex4Data:
    rw: Resistor
    e_src: Voltage
    r1: Resistor
    r2: Resistor
    r3: Resistor
    r4: Resistor
    r5: Resistor
    r6: Resistor


@dataclass
class Ex4Result:
    current1: Current
    current2: Current
    current3: Current
    current4: Current
    u1: Voltage
    u2: Voltage

    def round_sig(self):
        for key, value in self.__dict__.items():
            self.__dict__[key] = round_sig(value)


class Ex4:
    data: Ex4Data

    def __init__(self, data: Ex4Data):
        self.data = data

    def __call__(self) -> Ex4Result:
        r14 = self.data.r1.parallel(self.data.r4)
        r56 = self.data.r5.parallel(self.data.r6)
        r356 = self.data.r3.parallel(r56)
        r13456 = r14 + r356
        r123456 = self.data.r2.parallel(r13456)
        req = self.data.rw + r123456

        current1 = self.data.e_src / req.value
        current2 = r13456.value / (self.data.r2 + r13456).value * current1
        current_x = current1 - current2
        current3 = r56.value / (self.data.r3 + r56).value * current2
        current4 = self.data.r3.value * current_x / (self.data.r3 + r56).value
        u1 = current_x * r14.value
        u2 = current4 * r56.value

        res = Ex4Result(
            current1=current1,
            current2=current2,
            current3=current3,
            current4=current4,
            u1=u1,
            u2=u2,
        )
        res.round_sig()
        return res
