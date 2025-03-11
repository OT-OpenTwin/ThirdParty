# coding=utf-8
"""General Pyrit Exceptions

.. sectionauthor:: Bundschuh
"""


class PyritException(Exception):
    """Base class for all Pyrit exceptions"""


class InternalPyritError(PyritException):
    """Exception class for internal Pyrit errors. This exception should never be raised."""
