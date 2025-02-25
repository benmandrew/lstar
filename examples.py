import re as regex
import re_table as rt
import parser.mona as mona
import dfa_table as dt


class Re:
    alphabet = ["a", "b"]

    @staticmethod
    def ab_plus():
        re_s = r"(ab)+"
        re = regex.compile(re_s)
        return (
            rt.Table.from_cexs(rt.Query([re]), ["ab", "abbab"], Re.alphabet),
            re_s,
        )

    @staticmethod
    def ab_star():
        re_s = r"(ab)*"
        re = regex.compile(re_s)
        return rt.Table.from_cexs(rt.Query([re]), [], Re.alphabet), re_s

    @staticmethod
    def b_ab_plus():
        re_s = r"b(ab)+"
        re = regex.compile(re_s)
        return (
            rt.Table.from_cexs(rt.Query([re]), ["bab", "bbbab"], Re.alphabet),
            re_s,
        )

    @staticmethod
    def ab_plus_2():
        re_s = r"(ab){2,}"
        re = regex.compile(re_s)
        return rt.Table.from_cexs(rt.Query([re]), ["abab"], Re.alphabet), re_s

    @staticmethod
    def ab_plus_3():
        re_s = r"(ab){3,}"
        re = regex.compile(re_s)
        return rt.Table.from_cexs(rt.Query([re]), ["ababab"], Re.alphabet), re_s

    @staticmethod
    def ab_plus_3_union_b_ab_star():
        re1_s = r"((ab){3,})"
        re1 = regex.compile(re1_s)
        re2_s = r"(b(ab)*)"
        re2 = regex.compile(re2_s)
        re_s = re1_s + "|" + re2_s
        return (
            rt.Table.from_cexs(
                rt.Query([re1, re2]), ["ab", "ababab", "bbbabab"], Re.alphabet
            ),
            re_s,
        )

    @staticmethod
    def ab_plus_3_then_b_ab_star():
        re1_s = r"((ab){3,})"
        re1 = regex.compile(re1_s)
        t = rt.Table.from_cexs(rt.Query([re1]), ["ababab"], Re.alphabet)
        re2_s = r"b(ab)*"
        re2 = regex.compile(re2_s)
        re_s = re1_s + " then " + re2_s
        t.update_query(rt.Query([re1, re2]))
        return t, re_s

    @staticmethod
    def tables():
        return [
            (Re.ab_plus, "ab_plus"),
            (Re.ab_star, "ab_star"),
            (Re.b_ab_plus, "b_ab_plus"),
            (Re.ab_plus_2, "ab_plus_2"),
            (Re.ab_plus_3_union_b_ab_star, "ab_plus_3_union_b_ab_star"),
            (Re.ab_plus_3_then_b_ab_star, "ab_plus_3_then_b_ab_star"),
        ]


class Dfa:

    @staticmethod
    def make_example(ltl_s, cexs):
        dfa = mona.ltl_to_dfa(ltl_s)
        q = dt.Query([dfa], dfa.input_symbols)
        t = dt.Table.from_cexs(q, cexs, dfa.input_symbols)
        return t, ltl_s

    @staticmethod
    def fafbfc_chain():
        return Dfa.make_example("F(a & F(b & F(c)))", ["100" "010" "001"])

    @staticmethod
    def fafbfc_or():
        return Dfa.make_example("F(a) | F(b) | F(c)", [])

    @staticmethod
    def tables():
        return [
            (Dfa.fafbfc_chain, "fafbfc_chain"),
            (Dfa.fafbfc_or, "fafbfc_or"),
        ]


def main():
    for t, name in Re.tables():
        t, title = t()
        t.draw(name, title)

    for t, name in Dfa.tables():
        t, title = t()
        t.draw(name, title)


if __name__ == "__main__":
    main()
