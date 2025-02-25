import itertools
import re as regex
from automata.fa.dfa import DFA


class Query:
    def __init__(self, re_l):
        self.re_l = re_l

    def add(self, re):
        self.re_l.append(re)

    def query(self, s):
        return any(
            True if regex.fullmatch(re, s) else False for re in self.re_l
        )


def row_to_string(row):
    return "".join(map(lambda x: str(int(x)), row))


class Table:
    def __init__(self, q, alphabet):
        self.s = {""}
        self.e = {""}
        self.t = dict()
        self.alphabet = alphabet
        self.regularise(q)

    def sa(self):
        ret = []
        for s, a in itertools.product(self.s, self.alphabet):
            sa = s + a
            if sa not in self.s:
                ret.append(sa)
        return ret

    def add_table_el(self, q, s) -> None:
        if s not in self.t.keys():
            is_in_l = q.query(s)
            self.t.update({s: is_in_l})

    def add_all_els(self, q) -> None:
        with_a = itertools.product(self.s, self.alphabet, self.e)
        for s, a, e in with_a:
            self.add_table_el(q, s + a + e)
        without_a = itertools.product(self.s, self.e)
        for s, e in without_a:
            self.add_table_el(q, s + e)

    def add_prefix(self, pre) -> None:
        if (pre not in self.s) and pre != "":
            self.s.add(pre)
            self.add_prefix(pre[:-1])

    def add_suffix(self, suf) -> None:
        if (suf not in self.e) and suf != "":
            self.e.add(suf)
            self.add_prefix(suf[1:])

    def row(self, pre: str) -> list[bool]:
        e = sorted(self.e)
        return [self.t.get(pre + suf) for suf in e]

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

    def make_closed(self, q):
        changed = False
        non_closed = self.get_non_closed()
        if non_closed != []:
            changed = True
            for pre in non_closed:
                self.add_prefix(pre)
            self.add_all_els(q)
        return changed

    def get_inconsistent(self):
        ss = itertools.combinations(self.s, 2)
        x = itertools.product(ss, self.alphabet, self.e)
        ret = []
        for (pre_1, pre_2), a, e in x:
            if self.row(pre_1) == self.row(pre_2) and self.t.get(
                pre_1 + a + e
            ) != self.t.get(pre_2 + a + e):
                ret.append(a + e)
        return ret

    def make_consistent(self, q):
        changed = False
        inconsistent = self.get_inconsistent()
        if inconsistent != []:
            changed = True
            for suf in inconsistent:
                self.add_suffix(suf)
            self.add_all_els(q)
        return changed

    def regularise(self, q):
        self.add_all_els(q)
        changed = True
        while changed:
            changed = self.make_closed(q) or self.make_consistent(q)

    def add_cex(self, q, cex):
        for c in cex:
            assert c in self.alphabet
        self.add_prefix(cex)
        self.regularise(q)

    def get_terminals(self):
        ret = []
        for s in self.s:
            if self.t.get(s):
                ret.append(s)
        return ret

    @staticmethod
    def from_cexs(q, cexs, alphabet, debug=False):
        ret = Table(q, alphabet)
        for i, cex in enumerate(cexs):
            if debug:
                print("ITER {d}".format(d=i))
                ret.print()
            ret.add_cex(q, cex)
        if debug:
            print("FINAL")
            ret.print()
        return ret

    def update_query(self, q):
        for k, v in self.t.items():
            if not v:
                self.t[k] = q.query(k)
        self.regularise(q)

    def print(self):
        def eps(s):
            return "." if s == "" else s

        print("x---------------")
        print("       |", end="")
        for e in sorted(self.e):
            print("{s: >7}".format(s=eps(e)), end="")
        print("\n----------------")
        for pre in sorted(self.s):
            print("{s: <7}|".format(s=eps(pre)), end="")
            for suf in self.e:
                print("{d: >7}".format(d=int(self.t.get(pre + suf))), end="")
            print()
        print("----------------")
        for pre in sorted(self.sa()):
            print("{s: <7}|".format(s=eps(pre)), end="")
            for suf in self.e:
                print("{d: >7}".format(d=int(self.t.get(pre + suf))), end="")
            print()
        print("x---------------")

    def get_transitions(self):
        ret = dict()
        for s in self.s:
            rs = row_to_string(self.row(s))
            for a in self.alphabet:
                rsa = row_to_string(self.row(s + a))
                if rs in ret:
                    ret[rs][a] = rsa
                else:
                    ret[rs] = {a: rsa}
        return ret

    def draw(self, name: str, title: str):
        self.to_dfa().show_diagram().draw(
            path="out/{}.svg".format(name), args='-Glabel="{}" '.format(title)
        )

    def to_dfa(self):
        states = set(map(lambda x: row_to_string(self.row(x)), self.s))
        initial = row_to_string(self.row(""))
        finals = set(
            map(lambda x: row_to_string(self.row(x)), self.get_terminals())
        )
        transitions = self.get_transitions()
        return DFA(
            states=states,
            input_symbols=set(self.alphabet),
            transitions=transitions,
            initial_state=initial,
            final_states=finals,
        )
