from vigoux_neovim import run_leaning_for_vim
from aalpy.utils.ModelChecking import compare_automata
from random import seed
from parcours_automate import path_between_two_states, result_of_path2
seed(100)  # all experiments will be reproducible


def find_different_sequence_for_similar_states(list_of_similar_states, automaton_path, learned_automata):
    bis = list_of_similar_states.copy()
    for name1 in list_of_similar_states:
        bis.remove(name1)
        for name2 in bis:
            print('Comparing results for ' + name1 + ' and ' + name2)
            state1 = learned_automata.get_state_by_id(name1)
            state2 = learned_automata.get_state_by_id(name2)
            dist_seq = learned_automata.find_distinguishing_seq(state1, state2)
            print(dist_seq)
    for name in list_of_similar_states :
        print('chemin vers ' + name + ' : ' + str(path_between_two_states(automaton_path, 's0', name)))
    return

def compare_learned_automata_for_vim(learned_automata_1, automaton_path_1, learned_automata_2, automaton_path_2, max_seq_returned = 10):
    print('Comparing results')
    cexes = compare_automata( learned_automata_1, learned_automata_2, num_cex=max_seq_returned)
    print(cexes)
    for path in cexes:
        print(path)
        print('results with automata 1' + ': ' + result_of_path2(automaton_path_1, path))
        print('results with automata 2' + ': ' + result_of_path2(automaton_path_2, path))
    return



learned_automata_KV = run_leaning_for_vim(learning_algotithm='KV')
file_path_KV = 'nvim_KV_300_10.dot'

learned_automata_L_star = run_leaning_for_vim(learning_algotithm='L_star', WPS=100, WL=15)
file_path_L_star = 'nvim_L_star_100_15.dot'

# compare s25 and s99 because they have same label in the automata : Replace waiting for input (blocking)
find_different_sequence_for_similar_states(['s25', 's99'], file_path_KV, learned_automata_KV)

# compare learning automatas obtained with KV and L star
compare_learned_automata_for_vim(learned_automata_KV, file_path_KV, learned_automata_L_star, file_path_L_star)
