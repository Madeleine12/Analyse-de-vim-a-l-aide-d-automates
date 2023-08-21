# Analyse-de-vim-a-l-aide-d-automates
## Apprentissage automatique du fonctionnement de vim
Dans le fichier `aalpy_learning_neovim.py`, l'apprentissage de vim est effectué à partir de la librairie d'apprentisage actif AALpy.

La méthode `run_leaning_for_vim` permet de lancer l'apprentissage.\
Arguments : 
- learning_algorithm : 'KV' ou 'L_star'
- input_al : alphabet utilisé pour l'apprentissage, par défaut on utilise ['i', 'w', '<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']
- WPS : walk per states valeur par défaut 150
- WL : walk len valeur par défaut 10
Retours :
-Automate obtenu au terme de l'apprentissage (il est également enregistré dans le dosier dans lequel se trouve le fichier python sous format dot)

## Méthodes utiles pour le parcouts d'automates 
Dans le fichier `useful_methods.py`, j'ai codé des méthodes afin de faciliter le parcours des automates et d'éviter de devoir faire ces recherches manuellement.

La méthode `path_between_two_states` permet de trouver le chemin entre deux états d'un automate.\
Arguments : 
- automaton_path : chemin d'accès et le nom d'un automate en format dot 
- beginning : le nom du premier état, début du chemin (str)
- end : le nom du second état, fin du chemin (str)
Retours :
- Une liste de charatères le l'alphabet entré lors de l'apprentissage correspondant au un chemin allant du premier au second état

La méthode `result_of_path` permet de trouver l'état d'arrivée apres une séquence de charactères dans l'automate.\
Arguments : 
- automaton_path : chemin d'accès et le nom d'un automate en format dot
- path : liste correspondant à la séquence de charactères à effectuer
- input_al : alphabet utilisé lors de l'apprentissage, par défaut cet alphabet est ['i', 'w','<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']
Retours :
- le nom de l'état d'arrivée 


## Exploitation des automates pour étudier le fonctionnement de vim
Dans le fichier `vim_automata_analysis.py`, j'ai codé des méthodes qui permettent de former des conclusions à propos du comportement de vim.

La méthode `find_different_sequence_for_similar_states` permet de comparer deux états le l'automate.\
Arguments :
- list_of_similar_states : liste d'états similaires que l'on souhaite comparer deux à deux
- automaton_path : chemin d'accès et le nom d'un automate en format dot
- learned_automata : automate renvoyé par la méthode `run_leaning_for_vim`
Affichage pour chaque paire d'états :
- une liste d'entrées qui différencie les deux états
- une liste de caractères de l'alphabet entré lors de l'apprentissage permettant de mettre vim dans chacun des états

La méthode `def compare_learned_automata_for_vim` permet de comparer deux automates entre eux afin par exemple de déterminer lequel des deux modélise le mieux le comportement de vim.\
Arguments : 
- learned_automata_1 : premier automate renvoyé par la méthode `run_leaning_for_vim`
- automaton_path_1 : chemin d'accès et le nom du premier automate en format dot
- learned_automata_2 : second automate renvoyé par la méthode `run_leaning_for_vim`
- automaton_path_2 : chemin d'accès et le nom du second automate en format dot
- max_seq_returned : nombre maximal de séquences renvoyées, la valeur par defaut est 10
Affichage pour chaque séquence de contre exemple :
- la séquence de contre exemple
- le nom de l'état d'arrivée avec le premier automate
- le nom de l'état d'arrivée avec le second automate


