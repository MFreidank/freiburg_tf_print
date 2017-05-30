from subprocess import check_call, CalledProcessError


def extract_pages(filepath, outfile, pages):
    cmd = ["pdftk", filepath, "cat"] + pages + ["output", outfile]
    try:
        check_call(cmd)
    except CalledProcessError:
        raise ValueError("Failed extracting pages from PDF document {}!".format(filepath))
    else:
        return outfile


def number_pdf_pages(filepath):
    from PyPDF2 import PdfFileReader
    from PyPDF2.utils import PdfReadError

    with open(filepath, "rb") as f:
        try:
            reader = PdfFileReader(f)
        except PdfReadError:
            raise ValueError()
        else:
            try:
                return reader.getNumPages()
            except PdfReadError:
                raise ValueError()
