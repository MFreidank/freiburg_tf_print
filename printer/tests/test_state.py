import unittest
from printer.state import PrinterState


class TestPrinterStateFromOutput(unittest.TestCase):
    def test_from_output(self):
        output1 = "hp14: ready and printing"
        self.assertEqual(PrinterState.from_output(output1), PrinterState.PRINTING)

        output2 = "hp15: ready"
        self.assertEqual(PrinterState.from_output(output2), PrinterState.READY)

        output3 = "hp15: no pages left"
        self.assertEqual(PrinterState.from_output(output3), PrinterState.ERROR)


class TestPrinterAvailable(unittest.TestCase):
    def test_positive_available(self):
        for state in (PrinterState.READY, PrinterState.PRINTING):
            self.assertTrue(PrinterState.is_available(state))

    def test_negative_available(self):
        self.assertFalse(PrinterState.is_available(PrinterState.ERROR))
