import itertools

alphabet = [ "a", "b" ]

class Table:
    
    def __init__(self):
        self.s: set[str] = set()
        self.e: set[str] = set()
        self.t: dict[str, bool] = dict()

    def sa(self):
        itertools.product(self.s, alphabet)

    def add_table_el(self, re, s) -> None:
        if s not in self.t.keys():
            is_in_l = True
            self.t.update(s, is_in_l)

    def add_all_els(self, re) -> None:
        with_a = itertools.product(self.s, alphabet, self.e)
        for (s, a, e) in with_a:
            self.add_table_el(re, s + a + e)
        without_a = itertools.product(self.s, self.e)
        for (s, e) in without_a:
            self.add_table_el(re, s + e)

    def add_prefix(self, pre) -> None:
        if (pre not in self.s) and pre != "":
            self.s.add(pre)
            self.add_prefix(pre[:-1])

    def add_suffix(self, suf) -> None:
        if (suf not in self.e) and suf != "":
            self.e.add(suf)
            self.add_prefix(suf[1:])

    def row(self, pre) -> list[bool]:
        e = sorted(self.e)
        return [ self.t.get(pre + suf) for suf in e ]

    def get_non_closed(self):
        ret = []
        for sa in self.sa():
            row_a = self.row(sa)
            exists = False
            for s in self.s:
                if self.row(s) == row_a:
                    exists = True
                    break
            if not exists:
                ret.append(sa)
        return ret

    def make_closed(self, re):
        non_closed = self.get_non_closed()
        if non_closed != []:
            for pre in non_closed:
                self.add_prefix(pre)
            self.add_all_els(re)

    def get_inconsistent(self):
        ss = itertools.combinations(self.s, 2)
        x = itertools.product(ss, alphabet, self.e)
        ret = []
        for ((pre_1, pre_2), a, e) in x:
            if (self.row(pre_1) == self.row(pre_2) and
                self.t.get(pre_1 + a + e) != self.t.get(pre_2 + a + e)):
                ret.append(a + e)
        return ret
