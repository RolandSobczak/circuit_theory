import tomllib
from dataclasses import asdict

from ex1 import Ex1, Ex1Data
from ex2 import Ex2, Ex2Data
from ex3 import Ex3, Ex3Data
from ex4 import Ex4, Ex4Data
from ex5 import Ex5, Ex5Data
from utils import Resistor


def print_res(res):
    for key, value in asdict(res).items():
        print(f"{key} = {value}")


def load_resistors(data: dict) -> dict:
    return {
        k: Resistor(v) if k.startswith("r") or k == "rw" else v for k, v in data.items()
    }


def main():
    with open("data.toml", "rb") as f:
        config = tomllib.load(f)

    res1 = Ex1(Ex1Data(**load_resistors(config["ex1"])))()
    res2 = Ex2(Ex2Data(**load_resistors(config["ex2"])))()
    res3 = Ex3(Ex3Data(**load_resistors(config["ex3"])))()
    res4 = Ex4(Ex4Data(**load_resistors(config["ex4"])))()
    res5 = Ex5(Ex5Data(**load_resistors(config["ex5"])))()

    print("<=== Ex 1 ===>")
    print_res(res1)
    print("<=== Ex 2 ===>")
    print_res(res2)
    print("<=== Ex 3 ===>")
    print_res(res3)
    print("<=== Ex 4 ===>")
    print_res(res4)
    print("<=== Ex 5 ===>")
    print_res(res5)


if __name__ == "__main__":
    main()
