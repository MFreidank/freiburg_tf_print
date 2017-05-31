import unittest
import printer.printer as printer
from random import choice, randint


class TestCalculatePrintCosts(unittest.TestCase):
    def test_black_and_white(self):
        black_and_white_printers = ("hp14", "hp15")
        for i in range(400):
            val = randint(0, 1000)
            printer.number_pdf_pages = lambda _: val
            self.assertEqual(printer.calculate_print_costs(None, printer=choice(black_and_white_printers)), 0.05 * val)

    def test_color(self):
        for i in range(400):
            val = randint(0, 1000)
            printer.number_pdf_pages = lambda _: val
            self.assertEqual(printer.calculate_print_costs(None, printer="hpcolor"), 0.10 * val)


class TestDetermineBestPrinter(unittest.TestCase):
    # XXX: Implement at least one test for each possible situation (hp14 free, hp15 error), (hp14 error, hp15 free), (hp14 error, hp15 printing), (hp14 printing, hp15 error)
    #                                                              (hp14 printing, hp15 free), (hp14 free, hp15 printing), (both printing), (both free), (both error = assertRaises)
    pass
