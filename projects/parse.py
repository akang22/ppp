from abc import ABC, abstractmethod

from dataclasses import dataclass

"""[[(%[[{g_x_y^s}%]|   ):x,sep: ]\n:y]
[ y :y,sep: )]
\n\n
[move {a_x^n} from {b_x^n} to {c_x^n}\n:x]"""

@dataclass
class Context:
    cur_vars: 

class BaseMatch(ABC):
    def with_parent(self, parent):
        self.parent = parent
        return self

    def with_context(self, context):
        self.context = context
        return self

    @abstractmethod
    def fits_counts(self, test):
        return []

    def get_vars_for(self, rest_str):
        partOfStr = rest_str[0:self.fitsUpTo(restStr)]
        return self.getMatchingDict(partOfStr)

    @abstractmethod
    def getMatchingDict(self, string):
        pass

def node_factory(rest_template):
    # try one.



class ConcatMatch(BaseMatch):
    def __init__(self, name):
        self.children = {}
        self.name = name

    def add_child(self, name, child):
        if name not in self.children:
            self.children[name] = child.with_parent(self)
            return True
        return False

    def has_child(self, child_name):
        return child_name in self.children

    def get_child(self, child_name):
        if self.has_child(child_name):
            return self.children[child_name]
        return None

    def __str__(self):
        return f"{'  ' * self.level}- {self.name} (dir)\n" + \
    '\n'.join([str(child) for child in self.children.values()]) 

    def is_directory(self):
        return True

    def visited(self, visitor):
        for obj in self.children.values():
            visitor.visit(obj)




class IteratingNode(BaseNode):
    pass


class Parser:
    def __init__(self, template):
        self.template = template

def parse(input, template):
    pass
