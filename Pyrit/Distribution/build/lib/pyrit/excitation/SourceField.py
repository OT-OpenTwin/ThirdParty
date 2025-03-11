# coding=utf-8
"""A source field

.. sectionauthor:: Bundschuh
"""

from . import Exci


class SourceField(Exci):
    """A source field"""

    def __init__(self, value, name: str = ''):
        super().__init__(value, name)


class SourceDField(SourceField):
    """A source D field"""


class SourceHField(SourceField):
    """A source H field"""
