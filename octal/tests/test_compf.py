from pytest import approx, raises
from compf import Compf

class TestCompfOct:

    def setup_method(self):
        self.c = Compf()


    # БАЗОВЫЕ ТЕСТЫ
    def test_one_number(self):
        assert self.c.compile("0o12") == "10"

    def test_small_numbers(self):
        assert self.c.compile("0o1+0o2") == "1 2 +"

    def test_uppercase_hex(self):
        assert self.c.compile("0O12+0O17") == "10 15 +"

    def test_mixed_case_hex(self):
        assert self.c.compile("0o12*0O12") == "10 10 *"

    def test_addition(self):
        assert self.c.compile("0o12+0o13") == "10 11 +"

    def test_subtraction(self):
        assert self.c.compile("0o12-0o5") == "10 5 -"

    def test_multiplication(self):
        assert self.c.compile("0o3*0o4") == "3 4 *"

    def test_division(self):
        assert self.c.compile("0o10/0o2") == "8 2 /"


    # ПРИОРИТЕТЫ
    def test_priority1(self):
        assert self.c.compile("0o2+0o3*0o4") == "2 3 4 * +"

    def test_priority2(self):
        assert self.c.compile("0o2*0o3+0o4") == "2 3 * 4 +"

    def test_priority3(self):
        assert self.c.compile("0o10/0o4*0o2") == "8 4 2 * /"

    def test_priority4(self):
        assert self.c.compile("0o10/0o4+0o2") == "8 4 2 + /"


    # СКОБКИ
    def test_parentheses1(self):
        assert self.c.compile("(0o12)") == "10"

    def test_parentheses2(self):
        assert self.c.compile("(((((0o12)))))") == "10"

    def test_parentheses3(self):
        assert self.c.compile("(0o12+0o13)*0o2") == "10 11 + 2 *"

    def test_parentheses4(self):
        assert self.c.compile("0o2*(0o3+0o4)") == "2 3 4 + *"


    # СЛОЖНЫЕ ВЫРАЖЕНИЯ
    def test_expression1(self):
        assert self.c.compile("(0o12+0o13)*0o14") == "10 11 + 12 *"

    def test_expression2(self):
        assert self.c.compile("0o12+0o13*0o14") == "10 11 12 * +"

    def test_expression3(self):
        assert self.c.compile("(0o12+0o13)*(0o14+0o15)") == "10 11 + 12 13 + *"

    def test_expression4(self):
        assert self.c.compile("0o20*(0o2+0o3*0o4)") == "16 2 3 4 * + *"

    def test_expression5(self):
        assert self.c.compile("0o20*(0o2+0o3*0o4)/(0o2+0o2)") == \
               "16 2 3 4 * + * 2 2 + /"


    # ПРОБЕЛЫ
    def test_spaces(self):
        assert self.c.compile(" 0o12 + 0o13 ") == "10 11 +"

    def test_spaces_complex(self):
        assert self.c.compile(" ( 0o12 + 0o13 ) * 0o2 ") == \
               "10 11 + 2 *"


    # ОШИБКИ
    def test_invalid_symbol(self):
        with raises(Exception):
            self.c.compile("0o12 + Z")

    def test_invalid_hex(self):
        with raises(Exception):
            self.c.compile("0oG")

    def test_too_large_number(self):
        with raises(Exception):
            self.c.compile("0o7777")  # > 3999

    def test_empty_hex(self):
        with raises(Exception):
            self.c.compile("0o")

