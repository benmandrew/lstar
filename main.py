import parser.mona as mona
from table import Table, DfaQuery

# dfa = mona.ltl_to_dfa("F(a & F(b & F(c)))")
dfa = mona.ltl_to_dfa("F(a)")

t = Table(DfaQuery([dfa]), dfa.input_symbols)

print(dfa.transitions)
print(dfa.final_states)

print(dfa.accepts_input("11"))

t.draw("tmp", "main")
