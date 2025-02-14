def read_user_input(my_automaton):
    try:
        while True:
            if my_automaton.accepts_input(input("Please enter your input: ")):
                print("Accepted")
            else:
                print("Rejected")
    except KeyboardInterrupt:
        print("")

from automata.fa.dfa import DFA

# DFA which matches all binary strings ending in an odd number of '1's
my_dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)

import re as regex
from table import Table

# re = regex.compile(r"(ab)+")
# ab_plus = Table.from_cexs(re, [ "ab", "aaab" ]).to_dfa()

re = regex.compile(r"b(ab)+")
b_ab_plus = Table.from_cexs(re, [ "bab", "ab", "bab" ]).to_dfa()

re = regex.compile(r"(ab)*")
ab_star = Table.from_cexs(re, []).to_dfa()

dfa = ab_star.difference(b_ab_plus)

dfa.show_diagram().draw(path="bruh.svg")

# read_user_input(dfa)
