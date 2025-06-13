import math
from dataclasses import dataclass
from typing import Dict

import numpy as np
import sympy as sp
from sympy import Eq, I, Matrix, simplify, solve, symbols
from sympy.core.numbers import ImaginaryUnit


@dataclass
class Task1Input:
    J1: float
    E2: float
    Z1: float
    Z2: ImaginaryUnit
    Z3: ImaginaryUnit
    Z4: float
    Z5: float


@dataclass
class Task2Input:
    E1: ImaginaryUnit | float
    E2: ImaginaryUnit | float
    R1: float
    R2: float
    R3: float
    XC1: float
    XL1: float


InputNumber = ImaginaryUnit | float


@dataclass
class Task3Input:
    E1: float
    E2: float
    Z1: InputNumber
    Z2: InputNumber
    Z3: InputNumber
    Z4: InputNumber
    Z5: InputNumber
    Z6: InputNumber
    Z7: InputNumber


@dataclass
class Task4Input:
    E1: InputNumber
    E2: InputNumber
    R1: InputNumber
    R2: InputNumber
    R3: InputNumber
    R5: InputNumber
    XL1: InputNumber
    XL2: InputNumber
    XC4: InputNumber
    XL3: InputNumber
    XC3: InputNumber


@dataclass
class Task5Input:
    E1: InputNumber
    E2: InputNumber
    R1: InputNumber
    R2: InputNumber
    R3: InputNumber
    XC1: InputNumber
    XL1: InputNumber


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
        print(f"\t{key} = {round_sig(value)}")


def task1(data: Task1Input):
    Y1 = 1 / data.Z1
    Y2 = 1 / data.Z2
    Y3 = 1 / data.Z3
    Y4 = 1 / data.Z4
    Y5 = 1 / data.Z5

    Y1, Y2, Y3, Y4, Y5 = map(simplify, [Y1, Y2, Y3, Y4, Y5])

    V1, V2 = symbols("V1 V2")

    Y11 = 1 / data.Z1 + 1 / data.Z2 + 1 / data.Z3
    Y22 = 1 / data.Z3 + 1 / data.Z4 + 1 / data.Z5
    Y12 = Y21 = Y3

    J11 = data.J1
    J22 = data.E2 / data.Z5

    A_matrix = Matrix([[Y11, -1 * Y12], [-1 * Y21, Y22]])
    B_matrix = Matrix([[V1], [V2]])
    C_matrix = Matrix([[J11], [J22]])

    product = A_matrix * B_matrix

    eqs = [Eq(product[i], C_matrix[i]) for i in range(product.rows)]

    solution = solve(eqs, (V1, V2))

    I2 = solution[V1] / data.Z2
    I3 = (solution[V1] - solution[V2]) / data.Z3
    I4 = solution[V2] / data.Z4
    I5 = (data.E2 - solution[V2]) / data.Z5

    output = {
        "Y11": Y11,
        "Y22": Y22,
        "Y12": -1 * Y12,
        "JZ11": J11,
        "V1": solution[V1],
        "V2": solution[V2],
        "I2": I2,
        "I3": I3,
        "I4": I4,
        "I5": I5,
    }
    print(" === Task 1 ===")
    print_results(output)


def task2(data: Task2Input):
    R1, R2, R3 = 8.3, 6.7, 9.8
    XC1 = 17.9
    XL1 = 17.4
    E1 = 17.6
    E2 = 4.7 - 7.4 * I

    # Impedancje
    Z1 = R1 - I * XC1
    Z2 = R2 + I * XL1
    Z3 = R3

    # Admitancje
    Y1 = 1 / Z1
    Y2 = 1 / Z2
    Y3 = 1 / Z3

    # Całkowita admitancja własna węzła
    Y11 = simplify(Y1 + Y2 + Y3)

    # Prąd źródłowy Jz11
    Jz11 = simplify(E1 / Z1 + E2 / Z2)

    # Równanie: Y11 * V1 = Jz11
    V1_val = simplify(Jz11 / Y11)

    # Prądy
    I1 = simplify(-1 * (V1_val - E1) / Z1)
    I2 = simplify(-1 * (V1_val - E2) / Z2)
    I3 = simplify(V1_val / Z3)
    output = {
        "Y11": Y11,
        "Jz11": Jz11,
        "V1": V1_val,
        "I1": I1,
        "I2": I2,
        "I3": I3,
    }

    print(" === Task 2 ===")
    print_results(output)


def task3(data: Task3Input):
    z11 = sum([data.Z1, data.Z2, data.Z7])
    z22 = sum([data.Z1, data.Z3, data.Z4])
    z33 = sum([data.Z2, data.Z4, data.Z5, data.Z6])

    z12 = -data.Z1
    z13 = -data.Z2
    z23 = -data.Z4

    e11 = data.E2
    e22 = -data.E1
    e33 = 0

    w_matrix = Matrix(
        [
            [z11, z12, z13],
            [z12, z22, z23],
            [z13, z23, z33],
        ]
    )
    w1_matrix = Matrix(
        [
            [e11, z12, z13],
            [e22, z22, z23],
            [e33, z23, z33],
        ]
    )
    w2_matrix = Matrix(
        [
            [z11, e11, z13],
            [z12, e22, z23],
            [z13, e33, z33],
        ]
    )
    w3_matrix = Matrix(
        [
            [z11, z12, e11],
            [z12, z22, e22],
            [z13, z23, e33],
        ]
    )

    w_det = w_matrix.det()
    w1_det = w1_matrix.det()
    w2_det = w2_matrix.det()
    w3_det = w3_matrix.det()

    c1 = w1_det / w_det
    c2 = w2_det / w_det
    c3 = w3_det / w_det

    i1 = c2 - c1
    i2 = c3 - c1
    i3 = -c2
    i4 = c3 - c2
    i5 = c3

    output = {
        "Z11": z11,
        "Z23": z23,
        "Z33": z33,
        "E22": e22,
        "E33": e33,
        "I1": i1,
        "I2": i2,
        "I3": i3,
        "I4": i4,
        "I5": i5,
    }

    print(" === Task 3 ===")
    print_results(output)


def task4(data: Task4Input):
    z11 = sum([data.R1, I * data.XL1, -I * data.XC4])
    z22 = sum([-I * data.XC4, data.R2, I * data.XL2, data.R5])
    z33 = sum([data.R5, data.R3, -I * data.XC3, I * data.XL3])

    z12 = I * data.XC4
    z13 = 0
    z23 = -data.R5

    e11 = data.E1
    e22 = 0
    e33 = -data.E2

    w_matrix = Matrix(
        [
            [z11, z12, z13],
            [z12, z22, z23],
            [z13, z23, z33],
        ]
    )
    w1_matrix = Matrix(
        [
            [e11, z12, z13],
            [e22, z22, z23],
            [e33, z23, z33],
        ]
    )
    w2_matrix = Matrix(
        [
            [z11, e11, z13],
            [z12, e22, z23],
            [z13, e33, z33],
        ]
    )
    w3_matrix = Matrix(
        [
            [z11, z12, e11],
            [z12, z22, e22],
            [z13, z23, e33],
        ]
    )

    w_det = w_matrix.det()
    w1_det = w1_matrix.det()
    w2_det = w2_matrix.det()
    w3_det = w3_matrix.det()

    c1 = w1_det / w_det
    c2 = w2_det / w_det
    c3 = w3_det / w_det

    i1 = c1
    i2 = c2
    i3 = c3
    i4 = c1 - c2
    i5 = c2 - c3

    output = {
        "Z11": z11,
        "Z33": z33,
        "Z23": z23,
        "E33": e33,
        "I1": i1,
        "I2": i2,
        "I3": i3,
        "I4": i4,
        "I5": i5,
    }
    print(" === Task 4 ===")
    print_results(output)


def task5(data: Task5Input):
    z11 = sum([data.R1, -I * data.XC1, data.R3])
    z22 = sum([data.R2, data.R3, I * data.XL1])
    z12 = -data.R3

    e11 = data.E1
    e22 = -data.E2

    w_matrix = Matrix(
        [
            [z11, z12],
            [z12, z22],
        ]
    )

    w1_matrix = Matrix(
        [
            [e11, z12],
            [e22, z22],
        ]
    )

    w2_matrix = Matrix(
        [
            [z11, e11],
            [z12, e22],
        ]
    )

    w_det = w_matrix.det()
    w1_det = w1_matrix.det()
    w2_det = w2_matrix.det()

    c1 = w1_det / w_det
    c2 = w2_det / w_det

    i1 = c1
    i2 = -c2
    i3 = c1 - c2

    output = {
        "Z11": z11,
        "Z22": z22,
        "Z12": z12,
        "E11": e11,
        "E22": e22,
        "I_I": c1,
        "I_II": c2,
        "I1": i1,
        "I2": i2,
        "I3": i3,
    }
    print(" === Task 5 ===")
    print_results(output)


if __name__ == "__main__":
    task1_data = Task1Input(
        J1=15,
        E2=29,
        Z1=7,
        Z2=9 * I,
        Z3=5 + 14 * I,
        Z4=15,
        Z5=6,
    )
    task1(task1_data)
    task2_data = Task2Input(
        E1=17.6,
        E2=4.7 - 7.4 * I,
        R1=8.3,
        R2=6.7,
        R3=9.8,
        XC1=17.9,
        XL1=17.4,
    )
    task2(task2_data)
    task3_data = Task3Input(
        E1=18,
        E2=152,
        Z1=8.8 + 5.8 * I,
        Z2=8.4 - 8.1 * I,
        Z3=5 + 8.7 * I,
        Z4=10 - 5.6 * I,
        Z5=6.8 + 4 * I,
        Z6=0 - 15.1 * I,
        Z7=17,
    )
    task3(task3_data)
    task4_data = Task4Input(
        E1=199,
        E2=0 + 70 * I,
        R1=9.6,
        R2=9.4,
        R3=8.6,
        R5=9.2,
        XL1=9.7,
        XL2=9.7,
        XC4=9.7,
        XL3=7.5,
        XC3=7.5,
    )
    task4(task4_data)
    task5_data = Task5Input(
        E1=17.3,
        E2=3.8 - 8.5 * I,
        R1=7.8,
        R2=6.9,
        R3=6.4,
        XC1=11.6,
        XL1=6.9,
    )
    task5(task5_data)
