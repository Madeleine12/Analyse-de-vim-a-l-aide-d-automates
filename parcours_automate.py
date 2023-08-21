import pydot

# auto = pydot.graph_from_dot_file('test.dot')
# auto = auto[0]


def path_between_two_states(graph_file, beginning, end):
    graph = pydot.graph_from_dot_file(graph_file)[0]
    # fonctionne pas forcement si beginnig est pas s0
    if beginning == end:
        return []
    for edge in graph.get_edges():
        if edge.get_destination() == end:
            #print(edge.get_source())
            #print(edge.get_label())
            return path_between_two_states(graph_file, beginning, edge.get_source()) + [edge.get_label()]


# def result_of_path(automaton_file, path):
#     automaton = pydot.graph_from_dot_file(automaton_file)[0]
#     source = 's0'
#     for character in path :
#         i = 0  
#         stop = False
#         while not stop :
#             edge = automaton.get_edges()[i]
#             if edge.get_label() == '\"'+character+'\"' and edge.get_source() == source:
#                 source = edge.get_destination()
#                 stop = True
#             i += 1    
#     return source


def result_of_path2(automaton_file, path, input_al = ['i', 'w','<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']):
    graph = pydot.graph_from_dot_file(automaton_file)[0]
    source = 's0'
    for character in path :
        i = int(source[1:]) * len(input_al)
        stop = False
        while not stop :
            edge = graph.get_edges()[i]
            if edge.get_label() == '\"'+character+'\"' and edge.get_source() == source:
                source = edge.get_destination()
                # print(source)
                stop = True
            i += 1    
    return source

