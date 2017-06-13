
from subprocess import check_call, CalledProcessError
from os.path import basename

from printer.state import printer_state, PrinterState

from utils.pdf_documents import number_pdf_pages
from utils.errors import PrinterNotAvailableError, PrintCommandFailed, SSHCopyFailed


def calculate_print_costs(filepath, printer):
    cost_per_page = {"hp14": 0.05, "hp15": 0.05, "hpcolor": 0.10}
    pages = number_pdf_pages(filepath)
    return pages * cost_per_page[printer]


def determine_best_printer(user, printers, local=False):
    possible_printers = []
    for printer in printers:
        state = printer_state(user, printer, local=local)
        if state == PrinterState.READY:
            return printer
        elif state == PrinterState.PRINTING:
            possible_printers.append(printer)

    if possible_printers:
        # NOTE: It would be possible to optimize further here, by checking queue length and picking shortest queue
        return possible_printers[0]

    raise PrinterNotAvailableError("Found no available printer. Tried '{}'".format(", ".join(printers)))


def print_file(filename, printer, user, local=False):
    # Copy file to pool server.
    if local:
        file_basename = basename(filename)
        try:
            check_call(["lpr -P{printer} {filename}; lpq -P{printer}".format(printer=printer, filename=file_basename)])
        except CalledProcessError:
            raise PrintCommandFailed()
    else:
        try:
            check_call(["scp", filename,
                        "{user}@login.informatik.uni-freiburg.de:/home/{user}/".format(user=user)])
        except CalledProcessError:
            raise SSHCopyFailed()

        file_basename = basename(filename)
        # Issue printing command via ssh.
        try:
            check_call(["ssh", "{user}@login.informatik.uni-freiburg.de".format(user=user),
                       "lpr -P{printer} {filename}; lpq -P{printer}".format(printer=printer,
                                                                            filename=file_basename)])
        except CalledProcessError:
            raise PrintCommandFailed()
