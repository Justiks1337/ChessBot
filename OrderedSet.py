"""OrderedSet class from - https://code.activestate.com/recipes/576694/"""


from collections.abc import MutableSet


class OrderedSet(MutableSet):

    def __init__(self):
        self.map = {}

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key in self.map:
            raise KeyError("The element is already in the set!")

        self.map[key] = key

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')

        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
