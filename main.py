import parser.mona as mona

from dfa_table import Table, Query
from automata.fa.dfa import DFA


def generate_random_cex(dfa_tgt, t):
    dfa_gen: DFA = t.to_dfa()
    dfa: DFA = dfa_tgt.difference(dfa_gen)
    cutoff = 50
    cex = None
    for i in range(cutoff):
        try:
            cex = dfa.random_word(i)
            break
        except ValueError:
            pass
    return cex


def dfa_to_table(dfa: DFA, query: Query) -> Table:
    t = Table(query, dfa.input_symbols)
    cex = ""
    while cex is not None:
        cex = generate_random_cex(dfa, t)
        if cex is None:
            break
        t.add_cex(query, cex)
    return t


def ltl_to_table(ltl: str) -> Table:
    dfa = mona.ltl_to_dfa(ltl)
    query = Query([dfa], dfa.input_symbols)
    return dfa_to_table(dfa, query)


def weaken_to_target(target: DFA, origin: DFA, t: Table):
    query_both: Query = Query([target, origin], origin.input_symbols)
    t.update_query(query_both)
    j = 0
    modified = True
    while modified:
        j += 1
        modified = False
        dfa_gen: DFA = t.to_dfa()
        dfa_diff: DFA = target.difference(dfa_gen)
        if dfa_diff.isempty():
            break
        i = 0
        found_cex = False
        while not found_cex:
            i += 1
            for cex in dfa_diff.words_of_length(i):
                t.add_cex(query_both, cex)
                found_cex = True
                modified = True
                break
    return t


def ltl_to_dfa_shared_alphabet(ltls):
    monas = [mona.ltl_to_mona(ltl) for ltl in ltls]
    free_vars = [mona.mona_to_free_vars(m) for m in monas]
    return sorted(list(set().union(*free_vars)))


ltl_formulae = ["F(b & F(c))", "F(a) & F(b) & F(c)"]

alphabet = ltl_to_dfa_shared_alphabet(ltl_formulae)

dfa = mona.ltl_to_dfa(ltl_formulae[0], alphabet)

mona.draw_dfa(dfa, "expanded")

dfa = mona.ltl_to_dfa(ltl_formulae[0])

mona.draw_dfa(dfa, "original")


# desired: DFA = mona.ltl_to_dfa("F(a & F(b & F(c)))")
# query = Query([desired], desired.input_symbols)
# t: Table = dfa_to_table(desired, query)

# assumption: DFA = mona.ltl_to_dfa("F(a) & F(b) & F(c)")

# t_weak = weaken_to_target(assumption, desired, t)

# t_weak.draw("weakened", "Weakened")
