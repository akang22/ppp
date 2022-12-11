from collections import deque
from functools import reduce
from abc import ABC, abstractmethod
from operator import mul

# not my best code. Included because the analogy to message passing/distributed systems was obvious.

class Emitter:
    def __init__(self, intercept_fn):
        self.intercept_fn = intercept_fn
        self.listeners = {}

    def add_listener(self, listener):
        key = listener.listen_key()
        if key not in self.listeners:
            self.listeners[key] = []
        self.listeners[key].append(listener)

    def emit(self, src, passer, value):
        value = self.intercept_fn(value)
        dest = passer(value)
        for listener in self.listeners[dest]:
            listener.recv(value)

class Listener(ABC):
    @abstractmethod
    def recv(self, item):
        pass

    @abstractmethod
    def listen_key(self):
        pass

    @abstractmethod
    def recv(self, item):
        pass

class Monkey(Listener):
    def __init__(self, name, operation, items, passer, emitter, call_fns={}):
        self.name = name
        self.op = operation
        self.items = deque(items)
        self.passer = passer
        self.emitter = emitter
        self.call_fns = call_fns
        emitter.add_listener(self)

    def listen_key(self):
        return self.name
    
    def recv(self, item):
        self.items.append(item)

    def iter(self):
        for fn in self.call_fns.values():
            fn(self)
        while self.items:
            item = self.items.popleft()
            self.emitter.emit(src=self.name, passer=self.passer, value=self.op(item))
    
    def call_fn(self, fn_name):
        return self.call_fns[fn_name](None)

class Main:
    def __init__(self, value):
        values = value.split('\n\n')
        self.monkeys = []
        # I don't know if this is good practice, doing some experimentation.
        # goal is to make it easy to extend (arbitrary function that is called each round, and closure as accumulator)
        def items_passed():
            acc = 0
            def inner(monkey):
                nonlocal acc
                if not monkey:
                    return acc
                acc += len(monkey.items)
            return inner

        min_mod = 1
        
        for m in values:
            lines = m.split('\n')
            mod = int(lines[3].split(' ')[-1])
            if min_mod % mod != 0: # assume it's prime
                min_mod *= mod

        self.emitter = Emitter(intercept_fn=lambda x: x % min_mod)
        
        for m in values:
            lines = m.split('\n')
            name = lines[0].split(' ')[1].split(':')[0]
            items = [int(l) for l in lines[1].split(': ')[1].split(', ')]
            # i love writing secure code
            def op(old, lines=lines):
                return eval(lines[2].split('new = ')[1])
            mod = int(lines[3].split(' ')[-1])
            def cond(x, lines=lines, mod=mod):
                # i love how closures are mutable
                return lines[4].split(' ')[-1] if (x % mod == 0) else lines[5].split(' ')[-1] 
            self.monkeys.append(Monkey(name, op, items, cond, self.emitter, { 'ip': items_passed(), }))

        for i in range(20):
            for m in self.monkeys:
                m.iter()

        l = sorted([m.call_fn('ip') for m in self.monkeys])
        print(l)
        self.fs = l[-1] * l[-2]

        for i in range(10000 - 20):
            for m in self.monkeys:
                m.iter()

        l = sorted([m.call_fn('ip') for m in self.monkeys])
        self.ss = l[-1] * l[-2]

    def first_star(self):
        # note: this is wrong because it doesn't get divided by 3
        return self.fs

    def second_star(self):
        return self.ss


def main():
    with open('input.txt', 'r') as f:
        value = f.read()
    obj = Main(value)
    print(f"First Star: {obj.first_star()}")
    print(f"Second Star: {obj.second_star()}")

if __name__ == '__main__':
    main()

