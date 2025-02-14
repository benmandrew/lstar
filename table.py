import itertools
import re as regex
from automata.fa.dfa import DFA

alphabet = [ "a", "b" ]

def row_to_string(row):
    return "".join(map(lambda x: str(int(x)), row))

class Table:
    
    def __init__(self, re):
        self.s: set[str] = { "" }
        self.e: set[str] = { "" }
        self.t: dict[str, bool] = dict()
        self.regularise(re)

    def sa(self):
        ret = []
        for s, a in itertools.product(self.s, alphabet):
            sa = s + a
            if sa not in self.s:
                ret.append(sa)
        return ret

    def add_table_el(self, re, s) -> None:
        if s not in self.t.keys():
            is_in_l = True if any(regex.fullmatch(re, s) for re in re) else False
            self.t.update({ s : is_in_l })

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

    def row(self, pre: str) -> list[bool]:
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
        changed = False
        non_closed = self.get_non_closed()
        if non_closed != []:
            changed = True
            for pre in non_closed:
                self.add_prefix(pre)
            self.add_all_els(re)
        return changed

    def get_inconsistent(self):
        ss = itertools.combinations(self.s, 2)
        x = itertools.product(ss, alphabet, self.e)
        ret = []
        for ((pre_1, pre_2), a, e) in x:
            if (self.row(pre_1) == self.row(pre_2) and
                self.t.get(pre_1 + a + e) != self.t.get(pre_2 + a + e)):
                ret.append(a + e)
        return ret

    def make_consistent(self, re):
        changed = False
        inconsistent = self.get_inconsistent()
        if inconsistent != []:
            changed = True
            for suf in inconsistent:
                self.add_suffix(suf)
            self.add_all_els(re)
        return changed

    def regularise(self, re):
        self.add_all_els(re)
        changed = True
        while changed:
            changed = self.make_closed(re) or self.make_consistent(re)

    def add_cex(self, re, cex):
        self.add_prefix(cex)
        self.regularise(re)

    def get_terminals(self):
        ret = []
        for s in self.s:
            if self.t.get(s):
                ret.append(s)
        return ret

    @staticmethod
    def from_cexs(re, cexs, debug=False):
        ret = Table(re)
        for i, cex in enumerate(cexs):
            if debug:
                print("ITER {d}".format(d=i))
                ret.print()
            ret.add_cex(re, cex)
        if debug:
            print("FINAL")
            ret.print()
        return ret

    def update_re(self, re):
        for k, v in self.t.items():
            if not v:
                self.t[k] = True if any(regex.fullmatch(re, k) for re in re) else False
        self.regularise(re)

    def print(self):
        eps = lambda x: "." if x == "" else x
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
            for a in alphabet:
                rsa = row_to_string(self.row(s + a))
                if rs in ret:
                    ret[rs][a] = rsa
                else:
                    ret[rs] = { a : rsa }
        return ret

    def to_dfa(self):
        states = set(map(lambda x: row_to_string(self.row(x)), self.s))
        initial = row_to_string(self.row(""))
        finals = set(map(lambda x: row_to_string(self.row(x)), self.get_terminals()))
        transitions = self.get_transitions()
        return DFA(
            states=states,
            input_symbols=set(alphabet),
            transitions=transitions,
            initial_state=initial,
            final_states=finals
        )
