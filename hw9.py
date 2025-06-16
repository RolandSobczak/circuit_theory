import cmath
import math
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import sympy as sp
from sympy import Abs, Eq, I, Matrix, N, arg, deg, simplify, solve, symbols
from sympy.core.numbers import ImaginaryUnit

InputNumber = ImaginaryUnit | float


def round_sig(x, sig=4):
    # Handle complex numbers
    if isinstance(x, complex):
        real = round_sig(x.real, sig)
        imag = round_sig(x.imag, sig)
        return complex(real, imag)

    # Handle sympy complex numbers
    elif isinstance(x, sp.Expr):
        if x.free_symbols:  # expression contains symbols like V1
            return x
        elif x.is_real or x.is_complex:
            val = complex(x.evalf())
            return round_sig(val, sig)

    elif x == 0:
        return 0
    else:
        return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def print_results(data: Dict[str, float]):
    for key, value in data.items():
        out = value
        if not isinstance(value, str):
            out = round_sig(value)

        print(f"\t{key} = {out}")


@dataclass
class Task1Input:
    E1: float
    E2: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R: float


@dataclass
class Task2Input:
    E1: float
    E2: float
    J3: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float


@dataclass
class Task3Input:
    E1: InputNumber
    E2: InputNumber
    R1: InputNumber
    R2: InputNumber
    R3: InputNumber
    OMEGA: float
    L: float
    C: float


@dataclass
class Task4Input:
    E1: InputNumber
    E2: InputNumber
    R1: float
    R2: float
    R3: float
    R5: float
    XL1: float
    XL2: float
    XL3: float
    XC3: float
    XC4: float


@dataclass
class Task5Input:
    E1: InputNumber
    E2: InputNumber
    J3: InputNumber
    R1: InputNumber
    R3: InputNumber
    R4: InputNumber
    OMEGA: float
    C1: float
    L2: float
    C3: float


def calc_parallel_resistance(resistors: List[InputNumber]) -> InputNumber:
    value = 1 / sum([(1 / r) for r in resistors])
    return value


def task1(data: Task1Input):
    r_a = (data.R4 * data.R3) / sum([data.R3, data.R4, data.R5])
    r_b = (data.R4 * data.R5) / sum([data.R3, data.R4, data.R5])
    r_c = (data.R3 * data.R5) / sum([data.R3, data.R4, data.R5])
    r_a2 = r_a + data.R2
    r_c1 = data.R1 + r_c
    r_ac12 = (r_a2 * r_c1) / (r_a2 + r_c1)
    r_t = r_b + r_ac12

    v1, v2 = symbols("v1 v2")

    lhs1 = v1 * sum([data.R1, data.R2, data.R3]) - v2 * data.R3
    rhs1 = -data.E1
    eq1 = Eq(lhs1, rhs1)

    lhs2 = v2 * sum([data.R3, data.R4, data.R5]) - v1 * data.R3
    rhs2 = data.E2
    eq2 = Eq(lhs2, rhs2)

    solution = solve((eq1, eq2), (v1, v2))

    u_r2 = solution[v1] * data.R2
    u_r4 = solution[v2] * data.R4
    et = -1 * (u_r4 + u_r2)

    i_value = et / (r_t + data.R)
    p_value = i_value**2 * data.R

    output = {
        "RT": r_t,
        "ET": et,
        "I": i_value,
        "P": p_value,
    }

    print(" === Task 1 ===")
    print_results(output)


def task2(data: Task2Input):
    numerator = data.R5 * data.R4 + data.R4 * data.R3 + data.R3 * data.R5
    r_tb = numerator / data.R3
    r_tr = numerator / data.R4
    r_br = numerator / data.R5

    r_tr_prime = calc_parallel_resistance([r_tr, data.R1])
    r_br_prime = calc_parallel_resistance([r_br, data.R2])

    r_series = r_tr_prime + r_br_prime
    r_n = calc_parallel_resistance([r_tb, r_series])

    g_n = 1 / r_n

    vl, vr = symbols("vl vr")

    lhs1 = vl / data.R5 + vl / data.R4 + (vl - vr) / data.R3 - data.J3
    rhs1 = 0
    eq1 = Eq(lhs1, rhs1)

    lhs2 = (
        (vr - data.E1) / data.R1
        + (vr - data.E2) / data.R2
        + (vr - vl) / data.R3
        + data.J3
    )
    rhs2 = 0
    eq2 = Eq(lhs2, rhs2)

    solution = solve((eq1, eq2), (vl, vr))

    j_n = solution[vl] / data.R5 + (solution[vr] - data.E1) / data.R1

    current = j_n / 2
    power = current**2 * r_n

    output = {
        "GN": g_n,
        "JN": j_n.evalf(),
        "R": r_n,
        "I": current,
        "P": power,
    }
    print(" === Task 2 ===")
    print_results(output)


def task3(data: Task3Input):
    # zt = (1 / (data.R1 + I * data.OMEGA * data.L) + 1 / data.R2) ** -1

    z1 = data.R1 + I * data.OMEGA * data.L
    z2 = data.R2
    z3 = data.R3 + 1 / (I * data.OMEGA * data.C)

    zt = (1 / z1 + 1 / z2) ** -1

    u_c1 = data.E1 * z2 / (z1 + z2)
    u_c2 = data.E2 * z1 / (z1 + z2)
    et = u_c1 + u_c2

    i3 = et / (zt + z3)
    # i3 = et / (zt + data.R3)

    modulus = Abs(et)
    angle_rad = arg(et)
    angle_deg = deg(angle_rad)

    i3_modulus = Abs(i3)
    i3_angle_rad = arg(i3)
    i3_angle_deg = deg(i3_angle_rad)

    output = {
        "ZT": zt,
        "ET": f"(|z|={N(modulus, 4)} angle={N(angle_deg, 4)})",
        "i3": f"(|z|={N(i3_modulus, 4)} angle={N(i3_angle_deg, 4)})",
    }
    print(" === Task 3 ===")
    print(f"i3={i3.evalf()}")
    print_results(output)


def task4(data: Task4Input):
    z1 = data.R1 + I * data.XL1
    z4 = -I * data.XC4
    z14 = calc_parallel_resistance([z1, z4])
    z3 = sum([data.R3, -I * data.XC3, I * data.XL3])
    z35 = calc_parallel_resistance([z3, data.R5])
    zt = z14 + z35

    u_ab1 = data.E1 * z4 / (z1 + z4)

    z_e2_path = data.R3 + I * data.XL3 - I * data.XC3 + data.R5
    i_e2 = data.E2 / z_e2_path
    u_ab2 = i_e2 * data.R5

    # u_ab2 = data.E2 * data.R5 / (z1 + data.R5)
    # et = u_ab1 + u_ab2
    et = data.E1 * -I * data.XC4 / sum([data.R1, I * data.XL1, -I * data.XC4])

    modulus = Abs(et)
    angle_rad = arg(et)
    angle_deg = deg(angle_rad)

    output = {
        "ZT": zt.evalf(),
        "ET": f"(|z|={N(modulus, 4)} angle={N(angle_deg, 4)})",
    }

    print(" === Task 4 ===")
    print(f"zt={zt.evalf()}")
    print_results(output)


def task5(data: Task5Input):
    C1 = data.C1 * 10**-6
    C3 = data.C3 * 10**-6
    L2 = data.L2 * 10**-3

    omega = 260  # [rad/s]

    Zc1 = 1 / (1j * omega * C1)
    Zl2 = 1j * omega * L2
    Zc3 = 1 / (1j * omega * C3)
    Z3 = data.R3 + Zc3

    Z_branch1 = Zc1 + data.R1
    Z_branch2 = Zl2 + Z3

    Z_th = (Z_branch1 * Z_branch2) / (Z_branch1 + Z_branch2)
    Y_th = 1 / Z_th

    V_oc = 21.931 + 1j * 14.149

    J_N = V_oc / Z_th
    Y_N = 1 / Z_th

    Y_R4 = 1 / data.R4

    I4 = J_N * (Y_R4 / (Y_N + Y_R4))

    I4_mag = np.abs(I4)
    phi4_rad = np.angle(I4)
    phi4_deg = np.degrees(phi4_rad)
    P4 = I4_mag**2 * data.R4

    jn_modulus = Abs(J_N)
    jn_angle_rad = arg(J_N)
    jn_angle_deg = deg(jn_angle_rad)

    output = {
        "JN": f"(|z|={N(jn_modulus, 4)} angle={N(jn_angle_deg, 4)})",
        "YN": Y_N,
        "I4": I4_mag,
        "φ4": phi4_deg,
        "P4": P4,
    }
    print(" === Task 5 ===")
    print_results(output)


if __name__ == "__main__":
    task1_data = Task1Input(
        E1=95,
        E2=12,
        R1=3,
        R2=10,
        R3=8,
        R4=10,
        R5=7,
        R=3,
    )
    task1(task1_data)
    task2_data = Task2Input(
        E1=24,
        E2=89,
        J3=6,
        R1=7,
        R2=16,
        R3=6,
        R4=6,
        R5=10,
    )
    task2(task2_data)
    task3_data = Task3Input(
        E1=35 + 56 * I,
        E2=85 + 44 * I,
        R1=19,
        R2=19,
        R3=21,
        OMEGA=51,
        L=0.3,
        C=989 * (10**-6),
    )
    task3(task3_data)
    task4_data = Task4Input(
        E1=83 + I * 65,
        E2=29 + I * 22,
        R1=9.4,
        R2=9.2,
        R3=4.7,
        R5=13.5,
        XL1=7.6,
        XL2=8.2,
        XL3=5.9,
        XC3=4.1,
        XC4=4.3,
    )
    task4(task4_data)
    task5_data = Task5Input(
        E1=29 + 23 * I,
        E2=20 + 17 * I,
        J3=6 + 6 * I,
        R1=2.7,
        R3=2.2,
        R4=4.6,
        OMEGA=260,
        C1=1300,
        L2=50,
        C3=1300,
    )
    task5(task5_data)
