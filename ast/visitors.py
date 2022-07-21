from abc import ABC, abstractmethod
import nodes
from nodes import Visitor


class EvaluateVisitor(Visitor):
    def visit(self, node: nodes.Node):
        super().visit(node)

    def visitNumber(self):
        print("this is the right one")
        pass


EvaluateVisitor().visit(nodes.Number(3))
