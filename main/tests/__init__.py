import copy

from django.template.context import BaseContext

_orig_copy = getattr(BaseContext, "__copy__", None)

def _patched_copy(self):
    duplicate = object.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate

BaseContext.__copy__ = _patched_copy
