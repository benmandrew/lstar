from itertools import product, combinations
from automata.fa.dfa import DFA


def bin_to_chr(s):
    return chr(int(s, 2))


def chr_to_bin(s, letter_len):
    if s == "":
        return ""
    return f"{ord(s):b}".zfill(letter_len)


def split_string(s, letter_len):
    """Split binary string into alphabet letters and
    convert to unicode so that the DFA can accept them
    """

    return [s[i : i + letter_len] for i in range(0, len(s), letter_len)]

    # return [
    #     bin_to_chr(s[i : i + letter_len]) for i in range(0, len(s), letter_len)
    # ]


class Query:
    def __init__(self, dfa_l, alphabet):
        self.alphabet = alphabet
        self.letter_len = len(next(iter(alphabet)))
        self.dfa_l = dfa_l

    def add(self, dfa):
        self.dfa_l.append(dfa)

    def query(self, s):
        s = split_string(s, self.letter_len)
        return any(dfa.accepts_input(s) for dfa in self.dfa_l)


def row_to_string(row):
    return "".join(map(lambda x: str(int(x)), row))


class Table:
    def __init__(self, q, alphabet):
        self.s = {""}
        self.e = {""}
        self.t = dict()
        self.alphabet = alphabet
        self.letter_len = len(next(iter(alphabet)))
        self.regularise(q)

    def sa(self):
        ret = []
        for s, a in product(self.s, self.alphabet):
            sa = s + a
            if sa not in self.s:
                ret.append(sa)
        return ret

    def add_table_el(self, q, s) -> None:
        if s not in self.t.keys():
            is_in_l = q.query(s)
            self.t.update({s: is_in_l})

    def add_all_els(self, q) -> None:
        with_a = product(self.s, self.alphabet, self.e)
        for s, a, e in with_a:
            self.add_table_el(q, s + a + e)
        without_a = product(self.s, self.e)
        for s, e in without_a:
            self.add_table_el(q, s + e)

    def add_prefix(self, pre) -> None:
        if (pre not in self.s) and pre != "":
            self.s.add(pre)
            self.add_prefix(pre[: -self.letter_len])

    def add_suffix(self, suf) -> None:
        if (suf not in self.e) and suf != "":
            self.e.add(suf)
            self.add_prefix(suf[self.letter_len :])

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
        ss = combinations(self.s, 2)
        x = product(ss, self.alphabet, self.e)
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
        split_cex = split_string(cex, self.letter_len)
        for c in split_cex:
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
    def from_cexs(q, cexs, alphabet):
        ret = Table(q, alphabet)
        for c in cexs:
            ret.add_cex(q, c)
        return ret

    def update_query(self, q):
        for k, v in self.t.items():
            if not v:
                self.t[k] = q.query(k)
        self.regularise(q)

    def print(self):
        def eps(s):
            return "." if s == "" else s

        sa = sorted(self.sa())
        c_width = len(max(sa, key=len))
        print("x---------------")
        print((" " * c_width) + "|", end="")
        for e in sorted(self.e):
            print(f"{eps(e): >7}", end="")
        print("\n----------------")
        for pre in sorted(self.s):
            print(f"{eps(pre): <{c_width}}|", end="")
            for suf in self.e:
                print(f"{int(self.t.get(pre + suf)): >7}", end="")
            print()
        print("----------------")
        for pre in sa:
            print(f"{eps(pre): <{c_width}}|", end="")
            for suf in self.e:
                print(f"{int(self.t.get(pre + suf)): >7}", end="")
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
            path=f"out/{name}.svg", args=f'-Glabel="{title}" '
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
