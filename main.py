import parser.mona as mona
from dfa_table import Table, Query

ltl = "F(a) & F(b)"
dfa = mona.ltl_to_dfa(ltl)
# dfa = mona.ltl_to_dfa("F(a & b)")

# mona.draw_ltl(ltl, "ltl")
mona.draw_dfa(dfa, "bruh")

q = Query([dfa], dfa.input_symbols)
t = Table(q, dfa.input_symbols)

# t.draw("tmp", "main")

cex = ""
while cex != "FIN":
    t.print()
    t.draw("tmp", "main")
    cex = input()
    t.add_cex(q, cex)
