from stack import Stack

class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):

    G0:
        F  ->  T  |  F+T  |  F-T
        T  ->  M  |  T*M  |  T/M
        M  -> (F) |   V
        V  ->  a  |   b   |   c   |  ...  |    z

    Gs:
        e  ->  e e + | e e - | e e * | e e / |
                     | a | b | ... | z
    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-z]
    """
    def __init__(self):
        # Создание стека отложенных операций
        self.s = Stack()
        # Создание списка с результатом компиляции
        self.data = []

    def tokenize(self, expr):
        tokens = []
        length = len(expr)
        pos = 0

        while pos < length:
            char = expr[pos]

            if char == ' ':
                pos += 1
                continue

            if char in '+-*/()':
                tokens.append(char)
                pos += 1
                continue

            if char == '0' and pos + 1 < length and expr[pos + 1] in (
            'o', 'O'):
                start = pos
                pos += 2

                while pos < length and expr[pos] in '01234567':
                    pos += 1

                tokens.append(expr[start:pos])
                continue

            raise Exception(f'Недопустимый символ {char}')

        return tokens

    def compile(self, expr):
        self.data.clear()
        # Последовательный вызов для всех символов
        # взятой в скобки формулы метода process_symbol
        tokens = ['('] + self.tokenize(expr) + [')']

        for c in tokens:
            self.process_symbol(c)
        return " ".join(self.data)

    # Обработка символа
    def process_symbol(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        else:

            self.process_value(c)

    # Обработка отложенных операций
    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    # Обработка имени переменной
    def process_value(self, c):
        if len(c) <= 2:
            raise Exception(f'Некорректное число {c}')

        value = int(c, 8)

        if value > 3999:
            raise Exception(f'Число слишком большое:{c}')

        self.data.append(str(value))

    # Обработка символа операции
    def process_oper(self, c):
        self.data.append(c)

    # Определение приоритета операции
    @staticmethod
    def priority(c):
        if (c == "+" or c == "-"): return 1
        elif c == '/': return 0
        else: return 2

    # Определение отношения предшествования
    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)

if __name__ == "__main__":
    c = Compf()
    while True:
        expr = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(expr)}")
        print()


