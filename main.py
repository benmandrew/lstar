import parser.mona as mona
import dfa_table as dt


def generate_cex(dfa_tgt, t):
    dfa_gen = t.to_dfa()
    dfa = dfa_tgt.difference(dfa_gen)
    cutoff = 50
    cex = None
    for i in range(cutoff):
        try:
            cex = dfa.random_word(i)
            break
        except ValueError:
            pass
    return cex


dfa_tgt = mona.ltl_to_dfa("F(a) & F(b) & F(c)")

q = dt.Query([dfa_tgt], dfa_tgt.input_symbols)
t = dt.Table(q, dfa_tgt.input_symbols)

cex = ""
while cex is not None:
    cex = generate_cex(dfa_tgt, t)
    if cex is None:
        break
    print("Counterexample:", cex)
    t.add_cex(q, cex)

mona.draw_dfa(t.to_dfa(), "tmp")
