from abc import ABC, abstractmethod
import functools


class Node(ABC):
    def accept(self, visitor):
        visitor.visit(self)

    pass


class Number(Node):
    def __init__(self, value: float):
        if not (type(value) is int or type(value) is float):
            raise TypeError(
                f"Number should be type float, not {value} with type {type(value)}."
            )
        self.v = value


class Variable(Node):
    def __init__(self, name):
        if type(value) is not str:
            raise TypeError(
                f"Number should be type float, not {value} with type {type(value)}."
            )
        self.v = name


class BinaryOperator(Node):
    @abstractmethod
    def __init__(self, children: tuple[Node, Node]):
        if len(children) != 2:
            raise TypeError(
                f"BinaryOperator expects children to contain exactly two Nodes."
            )
        self.c = children


class CommutativeBinaryOperator(Node):
    @abstractmethod
    def __init__(self, children: tuple[Node, ...]):
        if len(children) < 2:
            raise TypeError(
                f"CommutativeBinaryOperator expects children to contain at least two Nodes."
            )
        elif len(children) == 2:
            self.c = children
        self.c = (self.children[0], type(self)(self.children[1:]))


class Equation(BinaryOperator):
    pass


class Add(CommutativeBinaryOperator):
    def __init__(self, children: tuple[Node, ...]):
        super().__init__(children)


class Multiply(CommutativeBinaryOperator):
    def __init__(self, children: tuple[Node, ...]):
        super().__init__(children)


class Subtract(BinaryOperator):
    def __init__(self, children: tuple[Node, Node]):
        super().__init__(children)


class Divide(BinaryOperator):
    def __init__(self, children: tuple[Node, Node]):
        super().__init__(children)


class Visitor(ABC):
    @abstractmethod
    def visit(self, node: Node):
        if not hasattr(self, dispatch):
            self.dispatch = {
                Number: self.vNumber,
            }
        pass

    @abstractmethod
    def vNumber(self):
        pass
