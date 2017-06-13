from subprocess import check_output
from enum import Enum


class PrinterState(Enum):
    READY = 1,
    PRINTING = 2,
    ERROR = 3

    @staticmethod
    def from_output(output):
        if "ready and printing" in output:
            return PrinterState.PRINTING
        elif "ready" in output:
            return PrinterState.READY
        return PrinterState.ERROR

    @staticmethod
    def is_available(state):
        return state in (PrinterState.READY, PrinterState.PRINTING)


def printer_state(user, printer, local=False):
    """ Use ssh to check state of printer `printer`.

    Parameters
    ----------
    printer : string

    Name of printer to query availability for.
    e.g. hp14


    Returns
    -------
    'PrinterState' enum discretizing state of `printer`.

    """
    if local:
        output = check_output(["lpq -P{printer}".format(printer=printer)])
    else:
        output = check_output(["ssh",
                               "{user}@login.informatik.uni-freiburg.de".format(user=user),
                               "lpq -P{printer}".format(printer=printer)])

    return PrinterState.from_output(str(output))
