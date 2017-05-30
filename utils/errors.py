""" Error cases that may occur at different stages of printing.  """


class PrinterNotAvailableError(ValueError):
    """ Raised if all specified printers were not available. """


class SSHCopyFailed(ValueError):
    """ Raised if 'scp' command to get file onto remote server failed. """


class PrintCommandFailed(ValueError):
    """ Raised if copy command was successful, but printing file via ssh
        gave us an error (check 'lpquota' output on remote host to see
        if there isn't enough money to print)"""
