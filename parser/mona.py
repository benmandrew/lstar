from lark import Lark, Transformer, Discard

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

with open("parser/mona.lark", "r") as f:
    parser = Lark(f.read(), parser="lalr")

with open("parser/ex.mona", "r") as f:
    s = f.read().split("A counter-example of least length")[0]

out = parser.parse(s)
out = TreeTransformer().transform(out).children

for o in out:
    print(o.children)

free = out[0].children
initial = out[1].children[0]
accepting = out[2].children
rejecting = out[3].children
transitions = out[4].children

# def get_edges =