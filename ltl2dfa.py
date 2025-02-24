from ltlf2dfa.parser.ltlf import LTLfParser
import pydot

import ltlf2dfa.pl

parser = LTLfParser()

def draw_formula(f, name):
    formula = parser(f)
    # print(type(formula))
    # print(formula)
    dfa = formula.to_dfa(mona_dfa_out=True)
    print(type(dfa))
    print(dfa)
    # (graph,) = pydot.graph_from_dot_data(dfa)
    # graph.write_svg("out/" + name + ".svg")

def main():
    # draw_formula("F(a & F(b & F(c)))", "desired")
    # draw_formula("F(a) & F(b) & F(c)", "intermediate")
    draw_formula("F(a) | F(b) | F(c)", "critical")

if __name__ == "__main__":
    main()
