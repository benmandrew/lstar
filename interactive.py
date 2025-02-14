import re as regex
from table import Table

def main():
    # re = regex.compile(r"(ab){3,}")
    # t = Table(re)
    re1 = regex.compile(r"((ab){2,})")
    t = Table.from_cexs([ re1 ], [ "abab" ])
    re2 = regex.compile(r"(b(ab)*aa)")
    t.update_re([ re2 ])
    # t.add_cex([ re1, re2 ], "baaaaa")
    title = "((ab){2,}) then (b(ab)*aa)"
    cex = ""
    while cex != "FIN":
        t.print()
        t.to_dfa().show_diagram().draw(path="tmp.svg", args="-Glabel=\"{}\" ".format(title))
        cex = input()
        t.add_cex([ re1, re2 ], cex)
    

if __name__ == "__main__":
    main()
