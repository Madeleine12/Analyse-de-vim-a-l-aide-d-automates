#"""
#A script to resize and decorate nvim-moore dot file (save again in dot)
#"""

import pygraphviz
import re
import sys

if __name__ == '__main__':
    prog = re.compile(
        r".*\|(Normal|Insert|Visual|Visual|Replace|Command-line editting|Select|Virtual Replace)$")

    G = pygraphviz.AGraph(filename=sys.argv[1] + ".dot")
    G.node_attr.update(color='black', width=5, fontname='sans-serif',
                       height=2.5, fontsize=30, fillcolor='#ffcc00')
    G.edge_attr.update(fontname='sans-serif', fontsize=25,
                       arrowsize=1.6, penwidth=2)
    for e in G:
        if prog.match(e.attr["label"]) is not None:
            e.attr["width"] = 50
            e.attr["height"] = 30
            e.attr["fontsize"] = 70
        e.attr["style"] = 'rounded,filled'

    G.draw(sys.argv[1] + ".xdot", format="xdot", prog="dot")
