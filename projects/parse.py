from abc import ABC, abstractmethod
from dataclasses import dataclass

"""[[(%[[{g_x_y^s}%]|   ):x,sep: ]\n:y]
[ y :y,sep: )]
\n\n
[move {a_x^n} from {b_x^n} to {c_x^n}\n:x]"""

@dataclass
class Context:
    cur_vars: Dict

class BaseNode(ABC):
    @abstractmethod
    def __init__(self, context):
        self.context = context

    def create(self, template):
        if fits_template
        
    """Does the current class even fit the template? eg. iteratingnode will match a '['.
    It does not try to parse the entire template or syntax checks. Just checks the beginning essentials."""
    @abstractmethod
    def fits_template(self, template):
        pass

    """Syntax checks all of the valid possibilities"""
    @abstractmethod
    def fits_counts(self, test):
        return []

    def getVarsFor(self, restStr):
        partOfStr = restStr[0:self.fitsUpTo(restStr)]
        return self.getMatchingDict(partOfStr)

    @abstractmethod
    def getMatchingDict(self, string):
        pass


class IteratingNode(BaseNode):
    pass




def parse(input, template):
    pass
