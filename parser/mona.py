from lark import Lark, Transformer, Discard
from automata.fa.dfa import DFA

from ltlf2dfa.parser.ltlf import LTLfParser
import pydot

from copy import deepcopy

class TreeTransformer(Transformer):
    INT = int
    WORD = str
    true = lambda self, _: True
    false = lambda self, _: False
    unknown = lambda self, _: None
    info = lambda self, _: Discard
    NL = lambda self, _: Discard
    edge_var_list = list

    def edge(self, e):
        return {
            "s":e[0],
            "t":e[1],
            "e":e[2],
        }

def bool_list_to_str(l):
    return "".join([ "1" if b else "0" for b in l ])

"""
Generate all concrete transitions from an abstract transition of the form:
    01X0X
Where 0 is a negated literal, 1 is positive,
and X is either negative or positive, i.e. both satisfy the edge.
"""
def concrete_transitions(t):
    def f(i, t, acc):
        if i >= len(t):
            return acc
        if t[i] is None:
            other = deepcopy(acc)
            for j in range(len(acc)):
                acc[j].append(True)
                other[j].append(False)
            return f(i + 1, t, acc + other)
        elif t[i]:
            for j in range(len(acc)):
                acc[j].append(True)
            return f(i + 1, t, acc)
        else:
            for j in range(len(acc)):
                acc[j].append(False)
            return f(i + 1, t, acc)
    res = f(0, t, [[]])
    return [ bool_list_to_str(l) for l in res ]

def get_transitions(t_l):
    res = dict()
    for t in t_l:
        for label in concrete_transitions(t["t"]):
            if t["s"] not in res:
                res[t["s"]] = { label: t["e"] }
            else:
                res[t["s"]][label] = t["e"]
    return res

ltlf_parser = LTLfParser()
with open("parser/mona.lark", "r") as f:
    mona_parser = Lark(f.read(), parser="lalr")

# def remove_initial_transition(transitions):
#     print(transitions)
#     return list(filter(lambda x: x["s"] != 0, transitions))

def mona_to_dfa(mona, name):
    s = mona.split("A counter-example of least length")[0]
    out = mona_parser.parse(s)
    out = TreeTransformer().transform(out).children

    free_vars = out[0].children
    initial = out[1].children[0]
    accepting = out[2].children
    rejecting = out[3].children
    transitions = out[4].children

    input_symbols = concrete_transitions([None] * len(free_vars))
    my_dfa = DFA(
        states=set(accepting + rejecting),
        input_symbols=set(input_symbols),
        transitions=get_transitions(transitions),
        initial_state=initial,
        final_states=set(accepting),
    )
    my_dfa.show_diagram().draw(path=name + ".svg")

def ltl_to_mona(formula):
    f = ltlf_parser(formula)
    return f.to_dfa(mona_dfa_out=True)

def ltl_to_dfa(formula, name):
    mona_to_dfa(ltl_to_mona(formula), name)

def draw_ltl(formula, name):
    f = ltlf_parser(formula)
    dfa = f.to_dfa()
    (graph,) = pydot.graph_from_dot_data(dfa)
    graph.write_svg("out/" + name + ".svg")


ltl_to_dfa("F(a & F(b & F(c)))", "desired")
ltl_to_dfa("F(a) & F(b) & F(c)", "intermediate")
ltl_to_dfa("F(a) | F(b) | F(c)", "critical")
