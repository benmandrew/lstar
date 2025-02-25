import re as regex
from re_table import Table, Query

alphabet = ["a", "b"]


def ab_plus():
    re_s = r"(ab)+"
    re = regex.compile(re_s)
    return Table.from_cexs(Query([re]), ["ab", "abbab"], alphabet), re_s


def ab_star():
    re_s = r"(ab)*"
    re = regex.compile(re_s)
    return Table.from_cexs(Query([re]), [], alphabet), re_s


def b_ab_plus():
    re_s = r"b(ab)+"
    re = regex.compile(re_s)
    return Table.from_cexs(Query([re]), ["bab", "bbbab"], alphabet), re_s


def ab_plus_2():
    re_s = r"(ab){2,}"
    re = regex.compile(re_s)
    return Table.from_cexs(Query([re]), ["abab"], alphabet), re_s


def ab_plus_3():
    re_s = r"(ab){3,}"
    re = regex.compile(re_s)
    return Table.from_cexs(Query([re]), ["ababab"], alphabet), re_s


def ab_plus_3_union_b_ab_star():
    re1_s = r"((ab){3,})"
    re1 = regex.compile(re1_s)
    re2_s = r"(b(ab)*)"
    re2 = regex.compile(re2_s)
    re_s = re1_s + "|" + re2_s
    return (
        Table.from_cexs(
            Query([re1, re2]), ["ab", "ababab", "bbbabab"], alphabet
        ),
        re_s,
    )


def ab_plus_3_then_b_ab_star():
    re1_s = r"((ab){3,})"
    re = regex.compile(re1_s)
    t = Table.from_cexs(Query([re]), ["ababab"], alphabet)
    re2_s = r"b(ab)*"
    re = regex.compile(re2_s)
    re_s = re1_s + " then " + re2_s
    t.update_query(Query([re]))
    return t, re_s


def main():
    tables = [
        (ab_plus, "ab_plus"),
        (ab_star, "ab_star"),
        (b_ab_plus, "b_ab_plus"),
        (ab_plus_2, "ab_plus_2"),
        (ab_plus_3_union_b_ab_star, "ab_plus_3_union_b_ab_star"),
        (ab_plus_3_then_b_ab_star, "ab_plus_3_then_b_ab_star"),
    ]
    for t, name in tables:
        t, title = t()
        t.draw(name, title)


if __name__ == "__main__":
    main()
