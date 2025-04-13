from dataclasses import dataclass
from typing import Tuple

from utils import *
from utils import calc_current_divider


@dataclass
class Ex1Data:
    j1_src: Current
    j2_src: Current
    e_src: Voltage
    r1: Resistor
    r2: Resistor
    r3: Resistor


@dataclass
class Ex1Result:
    p1: Power
    p2: Power
    p3: Power


class Ex1:
    data: Ex1Data

    def case_a(self) -> Tuple[Current, Current, Current]:
        r23 = self.data.r2 + self.data.r3
        req = r23.parallel(self.data.r1)

        current1 = calc_current_divider(
            src=self.data.j1_src, req=req.value, rk=self.data.r1.value
        )
        current2 = current3 = calc_current_divider(
            src=self.data.j1_src, req=req.value, rk=r23.value
        )
        return current1, current2, current3

    def case_b(self) -> Tuple[Current, Current, Current]:
        req = self.data.r1 + self.data.r2 + self.data.r3
        current2 = current3 = round_sig(self.data.e_src / req.value)
        current1 = current2 * -1
        return current1, current2, current3

    def case_c(self) -> Tuple[Current, Current, Current]:
        r13 = self.data.r1 + self.data.r3
        req = r13.parallel(self.data.r2)
        current3 = calc_current_divider(
            src=self.data.j2_src, req=req.value, rk=r13.value
        )
        current1 = -1 * current3
        current2 = -1 * calc_current_divider(
            src=self.data.j2_src,
            req=req.value,
            rk=self.data.r2.value,
        )
        return current1, current2, current3

    def __init__(self, data: Ex1Data):
        self.data = data

    def __call__(self) -> Ex1Result:
        current_1a, current_2a, current_3a = self.case_a()
        current_1b, current_2b, current_3b = self.case_b()
        current_1c, current_2c, current_3c = self.case_c()

        current1 = round_sig(sum([current_1a, current_1b, current_1c]))
        current2 = round_sig(sum([current_2a, current_2b, current_2c]))
        current3 = round_sig(sum([current_3a, current_3b, current_3c]))
        p1 = round_sig(round_sig(current1**2) * self.data.r1.value)
        p2 = round_sig(round_sig(current2**2) * self.data.r2.value)
        p3 = round_sig(round_sig(current3**2) * self.data.r3.value)
        return Ex1Result(p1, p2, p3)
