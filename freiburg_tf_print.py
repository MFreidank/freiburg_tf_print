#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
"""
Authors: Moritz Freidank, Moritz Rocholl

Script that uses ssh to remotely print locally stored documents
on any of the computer pool printers:

    * hp14
    * hp15
    * hpcolor

By default, uses the first available black-and-white printer (hp14, hp15).
Optional argument '--printer' must be used to explicitly request
'hpcolor' for color printing.

"""
import argparse
from os.path import basename, expanduser, isfile
from subprocess import check_call, check_output, CalledProcessError
from sys import version_info

from printer.state import PrinterState, printer_state
from printer.printer import calculate_print_costs, determine_best_printer, print_file

from utils.errors import PrinterNotAvailableError, SSHCopyFailed, PrintCommandFailed
from utils.pdf_documents import extract_pages
from utils.package_system import check_package_installed

# NOTE: Extensions: print final lpquota after the fact.

__authors__ = ["Moritz Freidank", "Moritz Rocholl"]


def main():
    parser = argparse.ArgumentParser(description="Print remotely on printers located in the computer pool at Uni Freiburg.")
    parser.add_argument("--available-printers", help="All printers to try for remote printing, specified as comma-separated list, default: 'hp14,hp15'. Ignored when --printer is specified.",
                        default="hp14,hp15")
    parser.add_argument("--pages", action="store_true", dest="pages", help="Interactively ask user to specify page ranges for each file requested, extract the pages and print only those.", default=False)
    parser.add_argument("--printer", help="Try remote printer PRINTER instead of the first available black-and-white printer.")
    parser.add_argument("--user", help="Use remote user USER instead of cached one.")
    parser.add_argument("files", help="Paths to local files that we want to print remotely.", nargs="+")
    args = parser.parse_args()

    if args.user:
        user = args.user
    else:
        cache_path = expanduser("~/.config/print_pool/cache.txt")
        if isfile(cache_path):
            # Read stored pool user from cache
            print("Found cached pool username at '{}'... loading from cache.".format(cache_path))
            with open(cache_path, "r") as f:
                user = f.read()
            print("Using user: {}".format(user))
        else:
            # Ask for pool user and cache it.
            if version_info.major >= 3:
                user = input("Enter pool account username:")
            else:
                # for safe backwards compliance
                user = raw_input("Enter pool account username:") # flake8: noqa

            check_call(["mkdir", "-p", expanduser("~/.config/print_pool")])

            with open(cache_path, "w") as f:
                f.write(user)

    for filename in args.files:
        if args.pages:
            check_package_installed("pdftk")

            print("Requested document: {}".format(filename))

            page_ranges = input("Enter page ranges to print from this document: (e.g.: '1,2,3' or '12-22,24-34'): ")
            pages = page_ranges.split(",")


            import tempfile

            with tempfile.NamedTemporaryFile(suffix='_print_pool.pdf', delete=False) as outfile:
                # cut the pages and print the resulting smaller file instead
                filename = extract_pages(filename, outfile.name, pages)


        if args.printer:
            # single printer specified, try it and raise error if it is in an error state.
            if printer_state(user, args.printer) in (PrinterState.READY, PrinterState.PRINTING):
                printer = args.printer
            else:
                raise PrinterNotAvailableError("Tried specified printer '{}', which is not available at the moment!".format(printer))
        else:
            # no single printer specified, let's explore available options and make the best pick.

            printers = [printer.strip() for printer in args.available_printers.split(",")]

            # Determine best printer
            printer = determine_best_printer(user, printers)

            print("Found best suited printer: {}".format(printer))

        try:
            print_costs_euro = calculate_print_costs(filename, printer)
        except (ImportError, ValueError, KeyError) as _: # if this fails, just skip it
            print("Could not calculate print costs for the given document.\n"
                  "If you care, run: 'pip3 install pyPDF2'.\n"
                  "For now, we'll just print ahead.")
        else:
            print("Printing this document costs {} euro.".format(print_costs_euro))
        print_file(filename=filename, printer=printer, user=user)


if __name__ == "__main__":
    main()
