"""
ATENcaO: EVITE MODIFICAR ESTE ARQUIVO!

Exececões usadas no compilador Lox.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ast import Value


class SemanticError(Exception):
    """
    Excecao para erros semânticos.
    """

    def __init__(self, msg, token=None):
        super().__init__(msg)
        self.token = token


class ForceReturn(Exception):
    """
    Excecao que serve para forcar uma funcao a retornar durante a avaliacao
    da mesma.
    """

    def __init__(self, value: "Value"):
        self.value = value
        super().__init__(self.value)
