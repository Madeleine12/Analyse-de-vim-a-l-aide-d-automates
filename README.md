# Analyse-de-vim-a-l-aide-d-automates
## Apprentissage automatique du fonctionnement de vim
Dans le fichier `aalpy_learning_neovim.py`, l'apprentissage de vim est effectué à partir de la librairie d'apprentisage actif AALpy.
La méthode `run_leaning_for_vim` permet de lancer l'apprentissage.
### Arguments : 
- learning_algorithm : 'KV' ou 'L_star'
- input_al : alphabet utilisé pour l'apprentissage, par défaut on utilise ['i', 'w', '<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']
- WPS : walk per states valeur par défaut 150
- WL : walk len valeur par défaut 10
## `useful_methods.py`
## `vim_automata_analysis.py`
