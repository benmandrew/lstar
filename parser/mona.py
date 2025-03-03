from copy import deepcopy

from lark import Lark, Transformer, Discard
from automata.fa.dfa import DFA

from ltlf2dfa.parser.ltlf import LTLfParser
import pydot


class TreeTransformer(Transformer):
    INT = int
    WORD = str
    true = lambda self, _: True  # noqa: E731
    false = lambda self, _: False  # noqa: E731
    unknown = lambda self, _: None  # noqa: E731
    info = lambda self, _: Discard  # noqa: E731
    NL = lambda self, _: Discard  # noqa: E731
    edge_var_list = list

    def edge(self, e):
        return {
            "s": e[0],
            "t": e[1],
            "e": e[2],
        }


def bool_list_to_str(bl):
    return "".join(["1" if b else "0" for b in bl])


def concrete_transitions(t):
    """Generate all concrete transitions from an abstract transition of the form:
        01X0X
    Where 0 is a negated literal, 1 is positive,
    and X is either negative or positive, i.e. both satisfy the edge.
    """

    def f(i, t, acc):
        if i >= len(t):
            return acc
        if t[i] is None:
            other = deepcopy(acc)
            for el_acc, el_other in zip(acc, other):
                el_acc.append(True)
                el_other.append(False)
            return f(i + 1, t, acc + other)
        elif t[i]:
            for el in acc:
                el.append(True)
            return f(i + 1, t, acc)
        else:
            for el in acc:
                el.append(False)
            return f(i + 1, t, acc)

    res = f(0, t, [[]])
    return [bool_list_to_str(bl) for bl in res]


def get_transitions(t_l):
    res = dict()
    for t in t_l:
        for label in concrete_transitions(t["t"]):
            if t["s"] not in res:
                res[t["s"]] = {label: t["e"]}
            else:
                res[t["s"]][label] = t["e"]
    return res


ltlf_parser = LTLfParser()
with open("parser/mona.lark", "r") as f:
    mona_parser = Lark(f.read(), parser="lalr")


def remove_initial_transition(transitions):
    transitions = list(filter(lambda x: x["s"] != 0, transitions))
    for t in transitions:
        t["s"] -= 1
        t["e"] -= 1
    return transitions


def reorder_transition_letters(
    transitions, edge_letters: list[str], true_letters: list[str]
):
    """Expand an abstract `edge` to a wider set of `true_letters`, and reorder to the true order"""

    def f(edge: str):
        new_edge = []
        for true_l in true_letters:
            try:
                i = edge_letters.index(true_l)
                new_edge.append(edge[i])
            except ValueError:
                new_edge.append(None)
        return new_edge

    for t in transitions:
        t["t"] = f(t["t"])
    return transitions


def decrement_states(accepting: list[int]):
    accepting = list(filter(lambda x: x != 0, accepting))
    return [x - 1 for x in accepting]


def mona_to_free_vars(mona: str) -> list[str]:
    s = mona.split("A counter-example of least length")[0]
    out = mona_parser.parse(s)
    out = TreeTransformer().transform(out).children
    return set(out[0].children)


def mona_to_dfa(mona: str, all_free_vars=None):
    s = mona.split("A counter-example of least length")[0]
    out = mona_parser.parse(s)
    out = TreeTransformer().transform(out).children
    free_vars = out[0].children
    # The MONA output has an unnecessary initial node, labelled '0'
    # This assumes that the real next node is labelled '1', which is then decremented
    initial = out[1].children[0]
    accepting = decrement_states(out[2].children)
    rejecting = decrement_states(out[3].children)
    transitions = remove_initial_transition(out[4].children)
    if all_free_vars is not None:
        assert all([x in all_free_vars for x in free_vars])
        input_symbols = concrete_transitions([None] * len(all_free_vars))
        transitions = reorder_transition_letters(
            transitions, free_vars, all_free_vars
        )
    else:
        input_symbols = concrete_transitions([None] * len(free_vars))
    return DFA(
        states=set(accepting + rejecting),
        input_symbols=set(input_symbols),
        transitions=get_transitions(transitions),
        initial_state=initial,
        final_states=set(accepting),
    )


def ltl_to_mona(formula: str):
    parser = ltlf_parser(formula)
    return parser.to_dfa(mona_dfa_out=True)


def ltl_to_dfa(formula: str, all_free_vars=None):
    return mona_to_dfa(ltl_to_mona(formula), all_free_vars)


def draw_ltl(formula: str, name: str):
    parser = ltlf_parser(formula)
    dfa = parser.to_dfa()
    (graph,) = pydot.graph_from_dot_data(dfa)
    graph.write_svg(f"out/{name}.svg")


def draw_dfa(dfa: DFA, name: str):
    dfa.show_diagram().draw(path=f"out/{name}.svg")
