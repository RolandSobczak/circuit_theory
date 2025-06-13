import math
from dataclasses import dataclass
from typing import Dict

import numpy as np
from sympy import Eq, solve, symbols


@dataclass
class Task1Input:
    E1: float
    E2: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R6: float
    R7: float
    R8: float


@dataclass
class Task2Input:
    J1: float
    E2: float
    E3: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float


@dataclass
class Task3Input:
    E1: float
    E2: float
    E3: float
    E4: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R6: float
    R7: float
    R8: float
    R9: float


@dataclass
class Task4Input:
    E1: float
    E2: float
    E3: float
    E4: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R6: float
    R7: float


@dataclass
class Task5Input:
    E1: float
    E2: float
    E3: float
    E4: float
    J5: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R6: float
    R7: float
    R8: float
    R9: float


def round_sig(x, sig=4):
    if x == 0:
        return 0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def print_results(data: Dict[str, float]):
    for key, value in data.items():
        print(f"\t{key} = {round_sig(value)}")


def task1(data: Task1Input):
    voltage_row1 = data.E1 + data.E2
    voltage_row2 = -1 * data.E2
    r_1_1 = sum([data.R1, data.R2, data.R3, data.R4])
    r_2_1 = -1 * data.R4
    r_2_2 = sum([data.R4, data.R5, data.R6, data.R7, data.R8])
    r_1_2 = -1 * data.R4

    W = np.linalg.det(np.array([[r_1_1, r_2_1], [r_1_2, r_2_2]]))
    W1 = np.linalg.det(np.array([[voltage_row1, r_2_1], [voltage_row2, r_2_2]]))
    W2 = np.linalg.det(np.array([[r_1_1, voltage_row1], [r_1_2, voltage_row2]]))

    circle_current_1 = W1 / W
    circle_current_2 = W2 / W
    current1 = circle_current_1
    current2 = circle_current_1 - circle_current_2
    current3 = -1 * circle_current_2

    output = {
        "circle_current1": circle_current_1,
        "circle_current2": circle_current_2,
        "current1": current1,
        "current2": current2,
        "current3": current3,
    }

    print("task1:")
    print_results(output)


def task2(data: Task2Input):
    v1, v2 = symbols("v1 v2")

    lhs1 = v1 * (1 / data.R1 + 1 / data.R2 + 1 / data.R4) - v2 * (1 / data.R1)
    rhs1 = -1 * data.E2 / data.R4 - data.J1
    eq1 = Eq(lhs1, rhs1)

    lhs2 = v2 * (1 / data.R1 + 1 / data.R3 + 1 / data.R5) - v1 * (1 / data.R1)
    rhs2 = data.E3 / data.R5 + data.J1
    eq2 = Eq(lhs2, rhs2)
    solution = solve((eq1, eq2), (v1, v2))

    current1 = data.J1
    current2 = (data.E2 + solution[v1]) / data.R4
    current3 = (data.E3 - solution[v2]) / data.R5
    current4 = (solution[v2] - solution[v1]) / data.R1
    current5 = -1 * solution[v1] / data.R2
    current6 = solution[v2] / data.R3

    output = {
        "v1": round_sig(solution[v1]),
        "v2": round_sig(solution[v2]),
        "I1": round_sig(current1),
        "I2": round_sig(current2),
        "I3": round_sig(current3),
        "I4": round_sig(current4),
        "I5": round_sig(current5),
        "I6": round_sig(current6),
    }

    print("task2:")
    print_results(output)


def task3b(data: Task3Input):
    # Define symbolic variables
    v1, v2 = symbols("v1 v2")

    # Precompute repeated expressions
    R_total_1 = sum([data.R1, data.R2, data.R7, data.R8])
    R_total_2 = sum([data.R5, data.R9])

    # Equation 1: Node voltage method (v1)
    lhs1 = v1 * (1 / R_total_1 + 1 / data.R4 + 1 / data.R3) - v2 * (1 / data.R3)
    rhs1 = data.E1 / R_total_1 - data.E2 / data.R4 + data.E3 / data.R3
    eq1 = Eq(lhs1, rhs1)

    # Equation 2: Node voltage method (v2)
    lhs2 = v2 * (1 / data.R3 + 1 / data.R6 + 1 / R_total_2) - v1 * (1 / data.R3)
    rhs2 = data.E4 / R_total_2 - data.E3 / data.R3
    eq2 = Eq(lhs2, rhs2)

    # Solve the system of equations
    solution = solve((eq1, eq2), (v1, v2))
    return {"v1": round_sig(solution[v1]), "v2": round_sig(solution[v2])}


def task3(data: Task3Input):
    task_b = task3b(data)

    voltage_row1 = data.E1 + data.E2
    voltage_row2 = -1 * data.E2 - data.E3
    voltage_row3 = -1 * data.E4

    r_1_1 = sum([data.R1, data.R2, data.R4, data.R7, data.R8])
    r_2_1 = -1 * data.R4
    r_1_2 = -1 * data.R4
    r_2_2 = sum([data.R3, data.R4, data.R6])
    r_3_2 = -1 * data.R6
    r_2_3 = -1 * data.R6
    r_3_3 = sum([data.R5, data.R6, data.R9])

    W = np.linalg.det(
        np.array(
            [
                [r_1_1, r_2_1, 0],
                [r_1_2, r_2_2, r_3_2],
                [0, r_2_3, r_3_3],
            ]
        )
    )

    W1 = np.linalg.det(
        np.array(
            [
                [voltage_row1, r_2_1, 0],
                [voltage_row2, r_2_2, r_3_2],
                [voltage_row3, r_2_3, r_3_3],
            ]
        )
    )

    W2 = np.linalg.det(
        np.array(
            [
                [r_1_1, voltage_row1, 0],
                [r_1_2, voltage_row2, r_3_2],
                [0, voltage_row3, r_3_3],
            ]
        )
    )

    W3 = np.linalg.det(
        np.array(
            [
                [r_1_1, r_2_1, voltage_row1],
                [r_1_2, r_2_2, voltage_row2],
                [0, r_2_3, voltage_row3],
            ]
        )
    )
    circle_current1 = W1 / W
    circle_current2 = W2 / W
    circle_current3 = W3 / W

    output = {
        "circle_current1": circle_current1,
        "circle_current2": circle_current2,
        "circle_current3": circle_current3,
    }
    output.update(task_b)
    print("task3:")
    print_results(output)


def task4(data: Task4Input):
    voltage_row1 = data.E1 - data.E2 - data.E3
    voltage_row2 = data.E2 + data.E4
    voltage_row3 = data.E3

    r_1_1 = sum([data.R1, data.R2, data.R3])
    r_2_1 = -1 * data.R3
    r_1_2 = -1 * data.R3
    r_2_2 = sum([data.R3, data.R4, data.R6])
    r_3_2 = -1 * data.R4
    r_2_3 = -1 * data.R4
    r_3_3 = sum([data.R4, data.R5, data.R7])

    W = np.linalg.det(
        np.array(
            [
                [r_1_1, r_2_1, 0],
                [r_1_2, r_2_2, r_3_2],
                [0, r_2_3, r_3_3],
            ]
        )
    )

    W1 = np.linalg.det(
        np.array(
            [
                [voltage_row1, r_2_1, 0],
                [voltage_row2, r_2_2, r_3_2],
                [voltage_row3, r_2_3, r_3_3],
            ]
        )
    )

    W2 = np.linalg.det(
        np.array(
            [
                [r_1_1, voltage_row1, 0],
                [r_1_2, voltage_row2, r_3_2],
                [0, voltage_row3, r_3_3],
            ]
        )
    )

    W3 = np.linalg.det(
        np.array(
            [
                [r_1_1, r_2_1, voltage_row1],
                [r_1_2, r_2_2, voltage_row2],
                [0, r_2_3, voltage_row3],
            ]
        )
    )

    circle_current1 = W1 / W
    circle_current2 = W2 / W
    circle_current3 = W3 / W

    output = {
        "circle_current1": round_sig(circle_current1),
        "circle_current2": round_sig(circle_current2),
        "circle_current3": round_sig(circle_current3),
        "I1": round_sig(circle_current1),
        "I2": round_sig(circle_current2 - circle_current1),
        "I3": round_sig(circle_current3 - circle_current1),
        "I4": round_sig(circle_current2),
        "I5": round_sig(circle_current2 - circle_current3),
        "I6": round_sig(circle_current3),
    }
    print("task4:")
    print_results(output)


def task5(data: Task5Input):
    v1, v2, v3 = symbols("v1 v2 v3")

    lhs1 = (
        v1 * (1 / sum([data.R1, data.R2, data.R3]) + 1 / data.R4 + 1 / data.R6)
        - v2 * (1 / data.R6)
        - v3 * (1 / data.R4 + 1 / sum([data.R1, data.R2, data.R3]))
    )
    rhs1 = data.J5 - data.E2 / data.R6 - data.E1 / sum([data.R1, data.R2, data.R3])
    eq1 = Eq(lhs1, rhs1)

    lhs2 = v2 * (1 / sum([data.R8, data.R9]) + 1 / data.R7 + 1 / data.R6) - v1 * (
        1 / data.R6
    )
    rhs2 = data.E2 / data.R6 + data.E3 / data.R7 - data.E4 / sum([data.R8, data.R9])
    eq2 = Eq(lhs2, rhs2)

    lhs3 = v3 * (
        1 / sum([data.R1, data.R2, data.R3]) + 1 / data.R4 + 1 / data.R5
    ) - v1 * (1 / data.R4 + 1 / sum([data.R1, data.R2, data.R3]))
    rhs3 = data.E1 / sum([data.R1, data.R2, data.R3]) - data.J5
    eq3 = Eq(lhs3, rhs3)

    solution = solve((eq1, eq2, eq3), (v1, v2, v3))

    I1 = (solution[v1] - solution[v3] + data.E1) / sum([data.R1, data.R2, data.R3])
    I2 = (solution[v1] - solution[v2] + data.E2) / data.R6
    I3 = (data.E3 - solution[v2]) / data.R7
    I4 = (solution[v2] + data.E4) / (data.R8 + data.R9)
    I6 = (solution[v3] - solution[v1]) / data.R4
    I7 = -1 * solution[v3] / data.R5

    output = {
        "v1": solution[v1],
        "v2": solution[v2],
        "v3": solution[v3],
        "I1": I1,
        "I2": I2,
        "I3": I3,
        "I4": I4,
        "I6": I6,
        "I7": I7,
    }

    print("task5:")
    print_results(output)


if __name__ == "__main__":
    task1_data = Task1Input(
        E1=27.6,
        E2=37.1,
        R1=25.9,
        R2=47.9,
        R3=21,
        R4=20.3,
        R5=45.3,
        R6=29.5,
        R7=38.7,
        R8=10.6,
    )
    task1(task1_data)
    task2_data = Task2Input(
        J1=3.4,
        E2=14.4,
        E3=18,
        R1=12.3,
        R2=6.7,
        R3=17.3,
        R4=15.4,
        R5=21.1,
    )
    task2(task2_data)
    task3_data = Task3Input(
        E1=40.3,
        E2=22,
        E3=26.8,
        E4=12.2,
        R1=6.4,
        R2=13.4,
        R3=17.2,
        R4=8,
        R5=20,
        R6=7.2,
        R7=9.6,
        R8=8.2,
        R9=45.7,
    )
    task3(task3_data)
    task4_data = Task4Input(
        E1=22.6,
        E2=15.8,
        E3=15.2,
        E4=43.7,
        R1=26.4,
        R2=15.4,
        R3=40.1,
        R4=35.7,
        R5=12.3,
        R6=11.4,
        R7=35.1,
    )
    task4(task4_data)
    task5_data = Task5Input(
        E1=38.8,
        E2=45.2,
        E3=10.4,
        E4=32.9,
        J5=4.9,
        R1=29,
        R2=7.8,
        R3=30.4,
        R4=15.3,
        R5=24.8,
        R6=9.5,
        R7=10.7,
        R8=41.1,
        R9=16.5,
    )
    task5(task5_data)
