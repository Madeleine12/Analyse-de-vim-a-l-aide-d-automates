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
-
Retours : 


result_of_path


## `vim_automata_analysis.py`
