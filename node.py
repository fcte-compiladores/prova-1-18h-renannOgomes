"""
ATENcaO: EVITE MODIFICAR ESTE ARQUIVO!

Define estrutura de dados basicas para as arvores sintaticas.
"""

from abc import ABC
from dataclasses import dataclass, field
from functools import singledispatch
from types import BuiltinFunctionType, FunctionType, MethodDescriptorType, MethodType
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Optional,
    TypeVar,
    cast,
)

N = TypeVar("N", bound="Node", contravariant=True)


class Node(ABC):
    """
    Classe base para todos os nós da arvore sintatica.

    O módulo `abc` é usado para criar uma classe abstrata. Isso significa que
    nao podemos instanciar essa classe diretamente. Em vez disso, devemos
    criar subclasses que implementem os métodos abstratos definidos aqui.
    """

    def eval(self, ctx):
        name = type(self).__name__
        raise NotImplementedError(f"Método eval nao implementado para {name}!")

    def pretty(self, indent: int = 2) -> str:
        """
        Método para imprimir a arvore sintatica de forma legivel.

        O parâmetro `indent` é usado para controlar a indentacao da impressao.
        """
        parts = []
        for indent_level, line in self._pretty_lines():
            parts.append(indent * indent_level * " ")
            parts.append(line)
            parts.append("\n")
        return "".join(parts)

    def is_leaf(self) -> bool:
        """
        Método que verifica se o nó é uma folha na arvore sintatica.

        Um nó é considerado uma folha se nao tem filhos do tipo `Node`.
        """
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, (Node, list, tuple, dict)):
                return False
        return True

    def _pretty_lines(self, indent_level: int = 0, end="") -> Iterator[tuple[int, str]]:
        """
        Método auxiliar para imprimir a arvore sintatica de forma legivel.

        O parâmetro `indent_level` é usado para controlar a indentacao da impressao.
        """
        # Um pouquinho de Python avancado aqui.
        # O método `_pretty_lines` é um gerador. Cada yield retorna uma dupla com
        # o nivel de indentacao da linha e o conteudo a ser impresso
        #
        # No caso simples, imprimimos a classe usando str(self). Fazemos isso se
        # a classe nao tiver nenhum filho do tipo Node.
        if can_print_as_leaf(self):
            yield indent_level, str(self)
            return

        # No caso mais complexo, comecamos com a linha de abertura, imprimindo
        # o nome da classe e um parêntese de abertura
        yield indent_level, str(self.__class__.__name__) + "("

        # O attributo "__annotations__" é um dicionario que contém os nomes dos
        # atributos declarados e seus tipos correspondentes. Vamos pegar os tipos
        # na ordem de declaracao e imprimir o nome e valores correspondentes
        for attr in self.__annotations__:
            # attr é o nome do atributo. Obtemos o valor do atributo usando a
            # funcao `getattr` do Python
            value = getattr(self, attr)

            # Se o valor for um objeto do tipo `Node`, chamamos o método `pretty_lines`
            # recursivamente. Caso contrario, usamos a implementacao genérica
            # do método `pretty`
            if isinstance(value, Node):
                yield from self._pretty_lines_node(attr + "=", value, indent_level)
            elif isinstance(value, (list, tuple)):
                yield from self._pretty_lines_list(attr, value, indent_level)
            else:
                yield indent_level + 1, f"{attr}={pretty(value)}"
                continue

        # Terminamos fechando o parênteses que foi aberto na primeira linha
        yield indent_level, ")" + end

    def _pretty_lines_node(
        self,
        prefix: str,
        value: "Node",
        indent_level: int = 0,
    ) -> Iterator[tuple[int, str]]:
        """
        Método auxiliar para imprimir nós de forma legivel.
        """
        lines = iter(value._pretty_lines(indent_level + 1))
        (_, first_line) = next(lines)

        # Tratamos a primeira linha de forma diferente, pois ela é prefixada
        # com o nome do atributo.
        yield indent_level + 1, prefix + first_line

        # O comando "yield from" gera todos os valores remanescentes do
        # iterador `lines`.
        yield from lines

    def _pretty_lines_list(
        self,
        attr: str,
        value: list[Any] | tuple[Any],
        indent_level: int = 0,
    ) -> Iterator[tuple[int, str]]:
        """
        Método auxiliar para imprimir listas de forma legivel.
        """
        if all(not isinstance(item, Node) for item in value):
            yield indent_level + 1, f"{attr}={list(value)}"
            return

        yield indent_level + 1, f"{attr}=["

        for item in value:
            if isinstance(item, Node):
                yield from item._pretty_lines(indent_level + 2, end=",")
            else:
                yield indent_level + 2, pretty(item) + ","
        yield indent_level + 1, "]"

    def visit(self, visitors: dict[type["Node"], Callable[[N], Any]]) -> None:
        """
        Recebe um dicionario de tipos associados a funcões.

        Executa a funcao correspondente ao tipo para cada nó na arvore sintatica.
        """

        # Primeiro visitamos os filhos do nó atual.
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, Node):
                value.visit(visitors)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, Node):
                        item.visit(visitors)
                    else:
                        visit_once(item, visitors)
            else:
                visit_once(value, visitors)

        # Agora visitamos self
        visit_once(self, visitors)

    def children(self) -> Iterable["Node"]:
        """
        Retorna todos os filhos do nó atual.

        O método `children` retorna um iterador que percorre todos os filhos
        do nó atual. Isso é util para percorrer a arvore sintatica de forma
        recursiva.
        """
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, Node):
                yield value
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, Node):
                        yield item

    def descendants(self) -> Iterable[Any]:
        """
        Retorna todos os descendentes do nó atual.

        O método `descendants` retorna um iterador que percorre todos os
        descendentes do nó atual. Isso é util para percorrer a arvore sintatica
        de forma recursiva.
        """
        yield self
        for child in self.children():
            yield from child.descendants()

    def cursor(self, cursor: Optional["Cursor[N]"] = None) -> "Cursor[N]":
        """
        Retorna um cursor para o nó atual.

        O método `cursor` retorna um cursor para o nó atual. Isso é util
        para navegar na arvore sintatica de forma recursiva.
        """
        if cursor is None:
            return Cursor(self)  # type: ignore

        if cursor.node is self:
            return cursor

        # Busca em largura
        pending = [cursor]
        while pending:
            cursor = pending.pop()
            if cursor.node is self:
                return cursor
            pending.extend(cursor.children())
        raise ValueError("O cursor nao aponta para o nó atual")

    def replace_child(self, old: "Node", new: "Node") -> None:
        """
        Substitui um filho do nó atual.

        O método `replace_child` substitui um filho do nó atual por um novo
        nó. Isso é util para modificar a arvore sintatica de forma recursiva.
        """
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, Node):
                if value is old:
                    setattr(self, name, new)
                    return
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(value):
                    if item is old:
                        if isinstance(value, tuple):
                            msg = f"Em {type(self).__name__}.{name}: esperava uma lista de filhos, mas encontrei uma tupla"
                            raise TypeError(msg)
                        value[i] = new
                        return

    def desugar_self(self):
        """
        Método que transforma o nó atual em uma versao sem auxilios sintaticos.

        A implementacao padrao nao faz nada, mas subclasses podem
        sobrescrever esse método para realizar transformacões especificas.
        """

    def desugar_tree(self):
        """
        Remove acucar sintatico do nó atual e todos os filhos.
        """
        pending = [self.cursor()]

        while pending:
            cursor = pending.pop()
            cursor.node.desugar_self()
            pending.extend(cursor.children())

    def validate_self(self, cursor: "Cursor[Node]"):
        """
        Realiza a analise semântica do nó atual.

        Recebe um cursor focado no objecto com relacao à raiz do módulo. Isso
        pode util para fazer consultas sobre os nós pais, irmaos, etc.

        Caso o nó nao seja valido, deve lancar uma excecao do tipo SemanticError.
        """

    def validate_tree(self):
        """
        Valida o nó atual e todos os filhos.
        """
        for cursor in self.cursor().descendants():
            cursor.node.validate_self(cursor)


@dataclass
class Cursor(Generic[N]):
    """
    Classe que representa um cursor para navegar na arvore sintatica.
    """

    node: N
    parent_cursor: Optional["Cursor[Node]"] = field(default=None, repr=False)

    def parent(self) -> "Cursor[Node]":
        """
        Retorna o nó pai do cursor.

        O método `parent` retorna o nó pai do cursor. Isso é util para
        navegar na arvore sintatica de forma recursiva.
        """
        if self.parent_cursor is None:
            raise ValueError("O cursor nao tem pai")
        return self.parent_cursor

    def root(self) -> "Cursor[Node]":
        """
        Retorna o nó raiz do cursor.

        O método `root` retorna o nó raiz do cursor. Isso é util para
        navegar na arvore sintatica de forma recursiva.
        """
        if not self.parent_cursor:
            return cast("Cursor[Node]", self)
        return self.parent_cursor.root()

    def is_root(self) -> bool:
        """
        Verifica se o cursor é o nó raiz.

        O método `is_root` verifica se o cursor é o nó raiz. Isso é util
        para verificar se o cursor esta no topo da arvore sintatica.
        """
        return self.parent_cursor is None
        # ou seja, se o cursor nao tem pai

    def parents(self) -> Iterable["Cursor[Node]"]:
        """
        Retorna todos os pais do nó atual.

        O método `parents` retorna um iterador que percorre todos os
        pais do nó atual. Isso é util para navegar na arvore sintatica
        de forma recursiva.
        """
        parent = self.parent_cursor
        while parent:
            yield parent
            parent = parent.parent_cursor

    def siblings(self) -> Iterable["Cursor[Node]"]:
        """
        Retorna os irmaos do nó atual.

        O método `siblings` retorna um iterador que percorre todos os
        irmaos do nó atual. Isso é util para navegar na arvore sintatica
        de forma recursiva.
        """
        if not self.parent_cursor:
            return
        for sibling in self.parent_cursor.node.children():
            if sibling is not self.node:
                yield Cursor(sibling, self.parent_cursor)

    def children(self) -> Iterable["Cursor[Node]"]:
        """
        Retorna os filhos do nó atual.

        O método `children` retorna um iterador que percorre todos os
        filhos do nó atual. Isso é util para navegar na arvore sintatica
        de forma recursiva.
        """
        self = cast("Cursor[Node]", self)
        for child in self.node.children():
            yield Cursor(child, self)

    def descendants(
        self, skip: Callable[["Cursor"], bool] | None = None, skip_self: bool = False
    ) -> Iterable["Cursor[Node]"]:
        """
        Retorna todos os descendentes do nó atual.

        O método `descendants` retorna um iterador que percorre todos os
        descendentes do nó atual. Isso é util para navegar na arvore sintatica
        de forma recursiva.
        """
        if skip is None or not skip(self):
            if not skip_self:
                yield cast("Cursor[Node]", self)
            for child in self.children():
                yield from child.descendants(skip)

    def is_scoped_to(self, scope: type[Node]) -> bool:
        """
        Verifica se o nó atual esta definido dentro de um escopo especifico.

        O método `is_scoped` verifica se o nó atual esta dentro de um
        escopo especifico. Isso é util para verificar se o nó atual
        esta dentro de uma classe ou funcao.
        """
        for parent in self.parents():
            if isinstance(parent.node, scope):
                return True
        return False


@singledispatch
def pretty(obj: Any) -> str:
    """
    Funcao que imprime attributos da arvore sintatica de forma legivel.

    Aqui usamos o `singledispatch` para criar uma funcao genérica que pode
    ser chamada com diferentes implementacões dependendo do tipo do primeiro
    argumento.

    A implementacao genérica simplesmente pergunta se o objeto tem um método
    pretty e executa ele. Caso contrario, converte o objeto para string usando
    o método `repr` do Python.
    """
    if hasattr(obj, "pretty"):
        data = obj.pretty()
        if not isinstance(data, str):
            raise ValueError("O método pretty deve retornar uma string")
        return data

    return repr(obj)


# Implementacao de `pretty` para argumentos do tipo Funcao
# Como se pode ver, existem varios tipos que representam funcões de
# diferentes maneiras no Python.
@pretty.register(FunctionType)
@pretty.register(BuiltinFunctionType)
@pretty.register(MethodDescriptorType)
@pretty.register(MethodType)
def _(obj) -> str:
    """
    Implementacao do método `pretty` para objetos do tipo `Node`.

    Aqui chamamos o método `pretty` da classe base `Node`.
    """
    return obj.__name__


def visit_once(obj: Node, visitors: dict[type[Node], Callable[[N], Any]]) -> None:
    """
    Visita um nó e executa a primeira funcao consistente com o tipo do objecto.
    """
    for subtype in type(obj).mro():
        try:
            visitor = visitors[subtype]
            visitor(obj)  # type: ignore
            break
        except KeyError:
            continue


def can_print_as_leaf(node: Node) -> bool:
    """
    Verifica se o nó pode ser impresso como uma folha.

    Um nó pode ser impresso como uma folha se nao tem filhos do tipo `Node`.
    """
    while node:
        args = []
        for attr in node.__annotations__:
            obj = getattr(node, attr)
            if isinstance(obj, (list, tuple)) and obj:
                return False
            elif isinstance(obj, Node):
                args.append(obj)

        match args:
            case []:
                return True
            case [arg]:
                node = arg
            case _:
                return False

    return True
