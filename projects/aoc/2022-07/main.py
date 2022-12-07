from abc import ABC, abstractmethod
from collections import deque

class Visitor(ABC):
    @abstractmethod
    def visit(self, obj):
        return

class FirstStarVisitor(Visitor):
    def __init__(self, limit):
        self.limit = limit
        self.acc = 0

    def visit(self, obj):
        size = obj.get_size()
        if obj.is_directory() and size <= self.limit:
            self.acc += size
        obj.visited(self)
        return self.acc

class SecondStarVisitor(Visitor):
    def __init__(self, limit, root):
        size = root.get_size() 
        self.closest = size - limit
        self.acc = size

    def visit(self, obj):
        size = obj.get_size()
        if obj.is_directory() and size > self.closest and size < self.acc:
            self.acc = size
        obj.visited(self)
        return self.acc

class Object(ABC):
    def with_parent(self, parent):
        self.parent = parent
        self.level = self.parent.level + 1
        return self

    @abstractmethod
    def get_size(self):
        raise NotImplementedError

    def get_parent(self):
        return self.parent

    @abstractmethod
    def is_directory(self):
        return True

    @abstractmethod
    def visited(self, visitor):
        return

class File(Object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def __str__(self):
        return f"{'  ' * self.level}- {self.name} (file, size={self.size})"

    def is_directory(self):
        return False

    def visited(self, visitor):
        return

class Dir(Object):
    def __init__(self, name):
        self.children = {}
        self.name = name

    def get_size(self):
        # technically speaking, this is inefficient because it recalculates the file size a lot.
        # maybe some kind of caching would work well here, like how filesystems ACTUALLY do it.
        return sum([child.get_size() for child in self.children.values()])

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


class Main:
    def __init__(self, value):
        self.io = (v.split('\n', 1) for v in value.split('$ '))
        next(self.io)
        self.root = Dir('/')
        # for pretty printing purposes: added in as an afterthought
        self.root.level = 0
        self.parse_from_base(self.root)

    def change_dir(self, path, cur):
        if path == '/':
            return self.root
        if path == '..':
            return cur.get_parent()
        if not cur.has_child(path):
            new_child = Dir(path)
            cur.add_child(path, new_child)
        return cur.get_child(path)

    def create_listed_files(self, output, cur):
        for a, b in split_output(output):
            if a == 'dir':
                cur.add_child(b, Dir(b))
            else:
                cur.add_child(b, File(b, a))
            
    def parse_from(self, cur):
        # reserved word kekw
        inn, out = next(self.io)
        if inn == 'ls':
            self.create_listed_files(out, cur)
            return cur
        command, target = inn.split(' ', 1)
        if command == 'cd':
            return self.change_dir(target, cur)

    def parse_from_base(self, cur):
        while True:
            try:
                # mfw $MODERN_LANGUAGE doesn't have tail call optimization
                cur = self.parse_from(cur)
            except StopIteration:
                return

    def firstStar(self):
        visitor = FirstStarVisitor(100000)
        return visitor.visit(self.root)

    def secondStar(self):
        visitor = SecondStarVisitor(70000000 - 30000000, self.root)
        return visitor.visit(self.root)


def split_output(output):
    intify = lambda a: a if a[0] == 'dir' else (int(a[0]), a[1])
    return [intify(a.split(' ', 1)) for a in output.split('\n') if a != '']

def main():
    value = ""
    with open('input.txt', 'r') as f:
        value = f.read()
    obj = Main(value)
    print(obj.root)
    print(f"First Star: {obj.firstStar()}")
    print(f"Second Star: {obj.secondStar()}")


if __name__ == '__main__':
    main()
