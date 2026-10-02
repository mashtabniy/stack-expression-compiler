#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv, lshift, rshift
from stack import Stack
from compf import Compf


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только цифры [0-9]
    """

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()

    # Интерпретация арифметического выражения
    def compile(self, str):

        Compf.compile(self, str)
        return self.r.top()


    def process_symbol(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop() #На самом деле это мы удаляем левую скобку
        elif c in "+-*/><":
            self.process_suspended_operators(c)
            self.s.push(c)
        else:
            self.check_symbol(c)
            self.process_value(c)

    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-" or c == '<' or c == '>') \
            else 2

    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Calc.priority(a) >= Calc.priority(b)

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul, '>':
                         rshift, '<': lshift, "/": truediv}[c](first,
                                                         second))

if __name__ == "__main__":
    c = Calc()
    while True:
        str = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(str)}")
        print()
