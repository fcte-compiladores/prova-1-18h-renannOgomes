#​ Edite ​as ​classes​ ​nesse​ ​arquivo. ​Boa​ ​prova!
from abc import ABC
from dataclasses import dataclass
from typing import Callable

from . import runtime
from .ctx import Ctx

# Declaramos nossa classe base num módulo separado para esconder um pouco de
# Python relativamente avancado de quem nao se interessar pelo assunto.
#
# A classe Node implementa um método `pretty` que imprime as arvores de forma
# legivel. Também possui funcionalidades para navegar na arvore usando cursores
# e métodos de visitacao.
from .node import Node

#
# TIPOS BaSICOS
#

# Tipos de valores que podem aparecer durante a execucao do programa
Value = bool | str | float | None


class Expr(Node, ABC):
    """
    Classe base para expressões.

    Expressões sao nós que podem ser avaliados para produzir um valor.
    Também podem ser atribuidos a variaveis, passados como argumentos para
    funcões, etc.
    """


class Stmt(Node, ABC):
    """
    Classe base para comandos.

    Comandos sao associdos a construtos sintaticos que alteram o fluxo de
    execucao do código ou declaram elementos como classes, funcões, etc.
    """


@dataclass
class Program(Node):
    """
    Representa um programa.

    Um programa é uma lista de comandos.
    """

    stmts: list[Stmt]

    def eval(self, ctx: Ctx):
        for stmt in self.stmts:
            stmt.eval(ctx)


#
# EXPRESSÕES
#
@dataclass
class BinOp(Expr):
    """
    Uma operacao infixa com dois operandos.

    Ex.: x + y, 2 * x, 3.14 > 3 and 3.14 < 4
    """

    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]

    def eval(self, ctx: Ctx):
        left_value = self.left.eval(ctx)
        right_value = self.right.eval(ctx)
        return self.op(left_value, right_value)


@dataclass
class Var(Expr):
    """
    Uma variavel no código

    Ex.: x, y, z
    """

    name: str

    def eval(self, ctx: Ctx):
        try:
            return ctx[self.name]
        except KeyError:
            raise NameError(f"variavel {self.name} nao existe!")


@dataclass
class Literal(Expr):
    """
    Representa valores literais no código, ex.: strings, booleanos,
    numeros, etc.

    Ex.: "Hello, world!", 42, 3.14, true, nil
    """

    value: Value

    def eval(self, ctx: Ctx):
        return self.value


@dataclass
class UnaryOp(Expr):
    """
    Uma operacao prefixa com um operando.

    Ex.: -x, !x
    """

    op: Callable[[Value], Value]
    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        return self.op(value)


@dataclass
class Call(Expr):
    """
    Uma chamada de funcao.

    Ex.: fat(42)
    """

    name: str
    params: list[Expr]

    def eval(self, ctx: Ctx):
        func = ctx[self.name]
        params = []
        for param in self.params:
            params.append(param.eval(ctx))

        if callable(func):
            return func(*params)
        raise TypeError(f"{self.name} nao é uma funcao!")


@dataclass
class Assign(Expr):
    """
    Atribuicao de variavel.

    Ex.: x = 42
    """

    name: str
    value: Expr

    def eval(self, ctx: Ctx):
        value = self.value.eval(ctx)
        ctx[self.name] = value
        return value


#
# COMANDOS E DECLARAcÕES
#
@dataclass
class Print(Stmt):
    """
    Representa uma instrucao de impressao.

    Ex.: print "Hello, world!";
    """

    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        runtime.print(value, end="\n")


@dataclass
class VarDef(Stmt):
    """
    Representa uma declaracao de variavel.

    Ex.: var x = 42;
    """

    name: str
    value: Expr | None

    def eval(self, ctx: Ctx):
        value = None if self.value is None else self.value.eval(ctx)
        ctx[self.name] = value


@dataclass
class Block(Node):
    """
    Representa bloco de comandos.

    Ex.: { var x = 42; print x;  }
    """

    stmts: list[Stmt]

    def eval(self, ctx: Ctx):
        for stmt in self.stmts:
            stmt.eval(ctx)


@dataclass
class While(Stmt):
    """
    Representa um laço de repetição.

    Ex.: while (x > 0) { ... }
    """

    cond: Expr
    body: Stmt

    def eval(self, ctx: Ctx):
       while True:
            cond_val = self.cond.eval(ctx)
            if cond_val is False or cond_val is None:
                break
            self.body.eval(ctx)
            
@dataclass
class List(Expr):
    elems: list[Expr]

    def eval(self, ctx: Ctx):
        value = []
        for elem in self.elems:
            value.append(elem.eval(ctx))
        return value
