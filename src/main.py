from ex1 import Ex1, Ex1Data
from ex2 import Ex2, Ex2Data
from utils import Resistor


def main():
    data = Ex1Data(
        j1_src=2.6,
        j2_src=26.4,
        e_src=87.6,
        r1=Resistor(64.2),
        r2=Resistor(197.1),
        r3=Resistor(42.8),
    )

    res1 = Ex1(data)()

    data2 = Ex2Data(
        e_src=28.7,
        r1=Resistor(26),
        r2=Resistor(16.3),
        r3=Resistor(13.2),
    )
    res2 = Ex2(data2)()

    print("<=== Ex 1 ===>")
    print(res1)
    print("<=== Ex 2 ===>")
    print(res2)


if __name__ == "__main__":
    main()
