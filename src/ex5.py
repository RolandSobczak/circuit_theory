from dataclasses import dataclass
from typing import Tuple

from utils import *
from utils import calc_current_divider


@dataclass
class Ex5Data:
    e1_src: Voltage
    e2_src: Voltage
    j3: Current
    j4: Current
    r1: Resistor
    r2: Resistor
    r3: Resistor
    r4: Resistor
    r5: Resistor
    r6: Resistor
    r7: Resistor


@dataclass
class Ex5Result:
    current1: Current
    current2: Current
    current3: Current
    current4: Current
    currentx: Current

    def round_sig(self):
        for key, value in self.__dict__.items():
            self.__dict__[key] = round_sig(value)


class Ex5:
    data: Ex5Data

    def __init__(self, data: Ex5Data):
        self.data = data

    def case_a(self) -> Current:
        r567 = calc_parallel_resistance([self.data.r5, self.data.r6, self.data.r7])
        r34567 = self.data.r3 + self.data.r4 + r567
        r234567 = self.data.r2.parallel(r34567)
        req = r234567 + self.data.r1

        current_a = self.data.e1_src / req.value
        out = self.data.r2.value / (self.data.r2 + r34567).value * current_a
        return out

    def case_b(self) -> Current:
        r567 = calc_parallel_resistance([self.data.r5, self.data.r6, self.data.r7])
        r34567 = self.data.r3 + self.data.r4 + r567
        r134567 = self.data.r1.parallel(r34567)
        req = self.data.r2 + r134567
        current_b = self.data.e2_src / req.value
        out = self.data.r1.value / (self.data.r1 + r34567).value * current_b
        return out

    def case_c(self) -> Current:
        r567 = calc_parallel_resistance([self.data.r5, self.data.r6, self.data.r7])
        r12 = self.data.r1.parallel(self.data.r2)
        r124567 = r12 + self.data.r4 + r567
        out = -1 * r124567.value / (self.data.r3 + r124567).value * self.data.j3
        return out

    def case_d(self) -> Current:
        r567 = calc_parallel_resistance([self.data.r5, self.data.r6, self.data.r7])
        r12 = self.data.r1.parallel(self.data.r2)
        r123567 = r12 + self.data.r3 + r567
        out = -1 * self.data.r4.value / (r123567 + self.data.r4).value * self.data.j4
        return out

    def __call__(self) -> Ex5Result:
        current1 = self.case_a()
        current2 = self.case_b()
        current3 = self.case_c()
        current4 = self.case_d()

        res = Ex5Result(
            current1=current1,
            current2=current2,
            current3=current3,
            current4=current4,
            currentx=current1 + current2 + current3 + current4,
        )
        res.round_sig()
        return res
