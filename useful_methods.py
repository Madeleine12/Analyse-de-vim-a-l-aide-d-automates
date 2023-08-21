import pydot


def path_between_two_states(automaton_path, beginning, end):
    graph = pydot.graph_from_dot_file(automaton_path)[0]
    # fonctionne pas forcement si beginnig différent de s0
    if beginning == end:
        return []
    for edge in graph.get_edges():
        if edge.get_destination() == end:
            return path_between_two_states(automaton_path, beginning, edge.get_source()) + [edge.get_label()]


def result_of_path(automaton_path, path, input_al = ['i', 'w','<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']):
    graph = pydot.graph_from_dot_file(automaton_path)[0]
    source = 's0'
    for character in path :
        i = int(source[1:]) * len(input_al)
        stop = False
        while not stop :
            edge = graph.get_edges()[i]
            if edge.get_label() == '\"'+character+'\"' and edge.get_source() == source:
                source = edge.get_destination()
                stop = True
            i += 1    
    return source

