from pytest import approx, raises
from calc import Calc


class TestCalcOct:

    def setup_method(self):
        self.c = Calc()

    # ----------------------------
    # БАЗОВЫЕ ПРОВЕРКИ
    # ----------------------------

    def test_invalid_symbol(self):
        with raises(Exception):
            self.c.compile('a')

    def test_one_number(self):
        assert self.c.compile('0o12') == 10

    # ----------------------------
    # СЛОЖЕНИЕ
    # ----------------------------

    def test_addition1(self):
        assert self.c.compile('0o1+0o2') == 3

    def test_addition2(self):
        assert self.c.compile('0o1+0o2+0o3+0o4') == 10

    def test_addition3(self):
        assert self.c.compile('(0o1+0o2)+(0o3+0o4)') == 10

    def test_addition4(self):
        assert self.c.compile('(0o1+(0o2+0o3)+0o4)') == 10

    # ----------------------------
    # ВЫЧИТАНИЕ
    # ----------------------------

    def test_subtraction1(self):
        assert self.c.compile('0o1-0o2') == -1

    def test_subtraction2(self):
        assert self.c.compile('0o5-0o2') == 3

    def test_subtraction3(self):
        assert self.c.compile('0o1-0o2-0o3') == -4

    def test_subtraction4(self):
        assert self.c.compile('(0o1-0o2)-(0o3-0o4)') == 0

    # ----------------------------
    # УМНОЖЕНИЕ
    # ----------------------------

    def test_multiplication1(self):
        assert self.c.compile('0o2*0o3') == 6

    def test_multiplication2(self):
        assert self.c.compile('0o0*0o3') == 0

    def test_multiplication3(self):
        assert self.c.compile('0o7*0o1*0o1') == 7

    def test_multiplication4(self):
        assert self.c.compile('0o2*0o5*0o2') == 20

    # ----------------------------
    # ДЕЛЕНИЕ (ВАЖНО!)
    # ----------------------------

    def test_division1(self):
        assert self.c.compile('0o1/0o2') == approx(0.5)

    def test_division2(self):
        assert self.c.compile('0o2/0o1') == approx(2.0)

    def test_division3(self):
        assert self.c.compile('0o0/0o3') == approx(0.0)

    # ----------------------------
    # СКОБКИ
    # ----------------------------

    def test_parentheses1(self):
        assert self.c.compile('(0o12)') == 10

    def test_parentheses2(self):
        assert self.c.compile('((0o12))') == 10

    def test_parentheses3(self):
        assert self.c.compile('(0o2+0o3)*0o4') == 20

    # ----------------------------
    # СЛОЖНЫЕ ВЫРАЖЕНИЯ
    # ----------------------------

    def test_expressions1(self):
        assert self.c.compile('(0o1-0o2)') == -1

    def test_expressions2(self):
        assert self.c.compile('(0o1+0o4)*0o7') == 35



    # ----------------------------
    # ПРОБЕЛЫ
    # ----------------------------

    def test_spaces(self):
        assert self.c.compile(' 0o12 + 0o13 ') == 21

    def test_spaces_complex(self):
        assert self.c.compile(' ( 0o2 + 0o3 ) * 0o4 ') == 20

    # ----------------------------
    # ГРАНИЦЫ
    # ----------------------------



    def test_overflow(self):
        with raises(Exception):
            self.c.compile('0o10000')  # 4096