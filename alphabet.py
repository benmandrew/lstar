from copy import deepcopy


class Alphabet:

    def __init__(self, exposed, hidden=[]):
        self.exposed = list(map(str.upper, exposed))
        self.hidden = list(map(str.upper, hidden))

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        i = self.current
        self.current += 1
        len_exposed = len(self.exposed)
        if i < len_exposed:
            return self.exposed[i - 1]
        if i - len_exposed < len(self.hidden):
            return self.hidden[i - len_exposed - 1]
        raise StopIteration

    def __len__(self):
        return len(self.exposed) + len(self.hidden)

    def __contains__(self, key):
        return key in self.exposed or key in self.hidden

    def all_concrete_transitions(self) -> list[list[bool]]:
        return self.concrete_transitions([None] * len(self))

    def concrete_transitions(self, t: list[bool | None]) -> list[list[bool]]:
        """Generate all concrete transitions from an abstract transition of the form:
            01X0X
        Where 0 is a negated literal, 1 is positive,
        and X is either negative or positive, i.e. both satisfy the edge.
        """

        def f(i, t, acc):
            if i >= len(t):
                return acc
            if t[i] is None:
                other = deepcopy(acc)
                for el_acc, el_other in zip(acc, other):
                    el_acc.append(True)
                    el_other.append(False)
                return f(i + 1, t, acc + other)
            elif t[i]:
                for el in acc:
                    el.append(True)
                return f(i + 1, t, acc)
            else:
                for el in acc:
                    el.append(False)
                return f(i + 1, t, acc)

        return f(0, t, [[]])
        # return [bool_list_to_str(bl) for bl in res]

    def generalise_edge(self, edge: list[bool]):
        """Generalise an edge to a collection of edges with the same valuations
        for exposed variables, but all valuations for hidden variables.

        Assumes the edge is in the order defined by `exposed` + `hidden`.
        """
        len_exposed = len(self.exposed)
        for i, _ in enumerate(self.hidden):
            edge[i + len_exposed] = None
        return edge
