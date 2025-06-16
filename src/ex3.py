from dataclasses import dataclass
from typing import Tuple

from utils import *
from utils import calc_current_divider


@dataclass
class Ex3Data:
    e1_src: Voltage
    e3_src: Voltage
    j_src: Power
    r1: Resistor
    r2: Resistor
    r3: Resistor


@dataclass
class Ex3Result:
    current_1a: Current
    current_2a: Current
    current_3a: Current

    current_1b: Current
    current_2b: Current
    current_3b: Current

    current_1c: Current
    current_2c: Current
    current_3c: Current

    current1: Current
    current2: Current
    current3: Current

    def round_sig(self):
        for key, value in self.__dict__.items():
            self.__dict__[key] = round_sig(value)


class Ex3:
    data: Ex3Data

    def __init__(self, data: Ex3Data):
        self.data = data

    def case_a(self) -> Tuple[Current, Current, Current]:
        r23 = self.data.r2.parallel(self.data.r3)
        req = self.data.r1 + r23
        current = self.data.e1_src / req.value
        voltage_23 = current * r23.value
        current_1a = -1 * current
        current_2a = voltage_23 / self.data.r2.value
        current_3a = voltage_23 / self.data.r3.value
        return current_1a, current_2a, current_3a

    def case_b(self) -> Tuple[Current, Current, Current]:
        req = calc_parallel_resistance([self.data.r1, self.data.r2, self.data.r3])
        current_1b = self.data.j_src * req.value / self.data.r1.value
        current_2b = self.data.j_src * req.value / self.data.r2.value
        current_3b = self.data.j_src * req.value / self.data.r3.value
        return current_1b, current_2b, current_3b

    def case_c(self) -> Tuple[Current, Current, Current]:
        r12 = self.data.r2.parallel(self.data.r1)
        req = r12 + self.data.r3
        u12 = self.data.e3_src / req.value * r12.value
        current_1c = -1 * u12 / self.data.r1.value
        current_2c = -1 * u12 / self.data.r2.value
        current_3c = self.data.e3_src / req.value
        return current_1c, current_2c, current_3c

    def __call__(self) -> Ex3Result:
        current_1a, current_2a, current_3a = self.case_a()
        current_1b, current_2b, current_3b = self.case_b()
        current_1c, current_2c, current_3c = self.case_c()

        current1 = current_1a + current_1b + current_1c
        current2 = current_2a + current_2b + current_2c
        current3 = sum([current_3a, current_3b, current_3c])

        res = Ex3Result(
            current_1a=current_1a,
            current_2a=current_2a,
            current_3a=current_3a,
            current_1b=current_1b,
            current_2b=current_2b,
            current_3b=current_3b,
            current_1c=current_1c,
            current_2c=current_2c,
            current_3c=current_3c,
            current1=current1,
            current2=current2,
            current3=current3,
        )
        res.round_sig()
        return res
