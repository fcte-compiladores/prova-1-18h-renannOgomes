import builtins
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, not_, sub, truediv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ast import Value

__all__ = [
    "add",
    "eq",
    "ge",
    "gt",
    "le",
    "lt",
    "mul",
    "ne",
    "neg",
    "not_",
    "print",
    "show",
    "sub",
    "truthy",
    "truediv",
]

nan = float("nan")
inf = float("inf")


def print(value: "Value", **kwargs):
    """
    Imprime um valor lox.
    """
    builtins.print(show(value), **kwargs)


def show(value: "Value") -> str:
    """
    Converte valor lox para string.
    """
    if isinstance(value, float):
        return str(value).removesuffix(".0")
    return str(value)


def show_repr(value: "Value") -> str:
    """
    Mostra um valor lox, mas coloca aspas em strings.
    """
    if isinstance(value, str):
        return f'"{value}"'
    return show(value)


def truthy(value: "Value") -> bool:
    """
    Converte valor lox para booleano segundo a semântica do lox.
    """
    if value is None or value is False:
        return False
    return True
