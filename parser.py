"""
ATENcaO: EVITE MODIFICAR ESTE ARQUIVO!

Define a gramatica da Linguagem e funcões para realizar a analise sintatica,
analise léxica, etc.
"""

from pathlib import Path
from typing import Iterator

from lark import Lark, Token, Tree

from .ast import Expr, Program
from .transformer import LoxTransformer

DIR = Path(__file__).parent
GRAMMAR_PATH = DIR / "grammar.lark"


ast_parser = Lark(
    GRAMMAR_PATH.open(),
    transformer=LoxTransformer(),
    parser="lalr",
    start=["start", "expr"],
)
cst_parser = Lark(
    GRAMMAR_PATH.open(),
    parser="lalr",
    start=["start", "expr"],
)


def parse(src: str) -> Program:
    """
    Funcao que recebe um código fonte e retorna a arvore sintatica.

    A funcao usa o Lark para fazer a analise léxica e sintatica do código
    fonte. O resultado é uma arvore sintatica que representa a estrutura
    do código usando os nós definidos na classe `Node`.

    Args:
        src (str):
            Código fonte a ser analisado.
    """
    tree = ast_parser.parse(src, start="start")
    if isinstance(tree, Tree):
        msg = f"Obteve um lark.Tree. Sera que você nao esqueceu de implementar {tree.data!r} no Transformer?"
        raise ValueError(msg)
    assert isinstance(tree, Program), f"Esperava um Program, mas recebi {type(tree)}"
    tree.validate_tree()
    tree.desugar_tree()
    return tree


def parse_expr(src: str) -> Expr:
    """
    Funcao que recebe um código fonte e retorna a arvore sintatica
    representando uma expressao.

    Similar à funcao `parse`, mas analisa o código como se fosse
    apenas uma expressao. Isso é util para avaliar expressões
    isoladas, sem a necessidade de um bloco de código completo. Isto também
    facilita o teste de expressões individuais.

    Args:
        src (str):
            Código fonte a ser analisado.

    Examples:
        >>> parse_expr("1 + 2")
        BinOp(left=Literal(value=1), right=Literal(value=2), op=op.add)
        >>> ctx = Ctx()
        >>> parse_expr("1 + 2 * 3").eval(Ctx())
        7
    """
    tree = ast_parser.parse(src, start="expr")
    if isinstance(tree, Tree):
        msg = f"Obteve um lark.Tree. Sera que você nao esqueceu de implementar {tree.data!r} no Transformer?"
        raise ValueError(msg)
    assert isinstance(tree, Expr), f"Esperava um Expr, mas recebi {type(tree)}"
    tree.validate_tree()
    tree.desugar_tree()
    return tree


def parse_cst(src: str, expr: bool = False) -> Tree:
    """
    Similar a funcao `parse`, mas retorna a arvore sintatica produzida pelo
    Lark.

    Nao é exatamente a arvore concreta, pois o Lark produz algumas
    simplificacões, mas é próxima o suficiente.

    Args:
        src (str):
            Código fonte a ser analisado.
        expr (bool):
            Se True, analisa o código como se fosse apenas uma expressao.
    """
    start = "expr" if expr else "start"
    return cst_parser.parse(src, start=start)


def lex(src: str) -> Iterator[Token]:
    """
    Retorna um iterador sobre os tokens do código fonte.
    """
    return ast_parser.lex(src)
