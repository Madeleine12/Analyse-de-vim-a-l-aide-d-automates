import neovim
from aalpy.base import SUL
from aalpy.oracles import StatePrefixEqOracle
from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.utils import save_automaton_to_file
from aalpy.utils.ModelChecking import compare_automata
from random import seed
seed(100)  # all experiments will be reproducible


class NvimSUL(SUL):
    """
    System under learning for Moore machine
    """

    def __init__(self):
        super().__init__()
        self.n = None
        self.reset()
        self.max_counter = 5

    def reset(self):
        if self.n is not None:
            self.n.close()

        self.n = neovim.attach(
                #"child", argv=['./nvim', '--clean', '-i NONE', '--embed', '--headless'])
                "child", argv=['/home/madeleine.mathieu/local/nvim/bin/nvim', '-u', 'NONE', '-i', 'NONE', '-n', '--embed', '--headless', 'filename']) # -n : no swap file
        self.n.lua.vim.api.nvim_set_keymap('n', '<C-O>', '', {}) # Else not a state machine (result depends on jump list)
        self.n.lua.vim.api.nvim_set_keymap('n', '<C-I>', '', {}) # Else not a state machine (result depends on jump list)
        # The next two are preventing a too large state machine since the state remembers the state of the last visual selection. Disabling the mapping still gives you a state machine but too large for now. It basically halved the number of states
        self.n.lua.vim.api.nvim_set_keymap('n', 'gv', '', {}) # Else not the state machine we would like to see (result of last visual selection :help gv depends on the history in keys entered)
        self.n.lua.vim.api.nvim_set_keymap('x', 'gv', '', {}) # Else not the state machine we would like to see (result of last visual selection :help gv depends on the history in keys entered), NOTE: Visual but not select
        self.n.lua.vim.api.nvim_set_keymap('i', '/', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'w', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'term', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', '<CR>', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', ':', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'v', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'g', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'h', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', 'r', '', {}) # Else not a state machine
        self.n.lua.vim.api.nvim_set_keymap('i', '$', '', {}) # Else not a state machine
        # Fixed 
        # The following 'language-mapping' does work unless 'iminsert' is set to 0 (tested and it works with 1). They are not needed since the fix for (https://github.com/vim/vim/issues/12045) has been upstreamed
        #self.n.lua.vim.api.nvim_set_keymap('l', '<C-g>', '', {}) # gr<C-g> is the same as gR (https://github.com/vim/vim/issues/12045) so we disable it. Also see https://neovim.io/doc/user/insert.html#i_CTRL-G_j
        #self.n.lua.vim.api.nvim_set_keymap('l', '<C-o>', '', {}) # (Fixed in vim waiting to be upstreamed in neovim) gr<C-o> is the same as gR (https://github.com/vim/vim/issues/12045) so we disable it
        self.n.lua.vim.api.nvim_set_keymap('o', '/$', '', {}) # Else not a state machine (why?? it is a move that depends on the buffer content and can be extended. `/$` is not the same as `/$w` )
        self.n.lua.vim.api.nvim_set_keymap('c', 'i', '', {}) # Else can run :i (remains a state machine but with lots of garbage) 
        self.n.lua.vim.api.nvim_set_keymap('c', 'c', '', {}) # ibid (can run :c)
        self.n.lua.vim.api.nvim_set_keymap('c', 'w', '', {}) # Else (can run :w) not a state machine because return value depends whether a file exists or not
        self.n.lua.vim.api.nvim_set_keymap('c', 'v', '', {}) # Else (can run :vglobal) 
        self.n.lua.vim.api.nvim_set_keymap('c', 'g', '', {}) # Else (can run :gr that is grep)
        self.n.lua.vim.api.nvim_set_keymap('c', 'r', '', {}) # Else (can run :gr that is grep)
        self.n.lua.vim.api.nvim_set_keymap('c', 'h', '', {}) # Else (can run :gr that is grep)
        self.n.lua.vim.api.nvim_set_keymap('c', ':', '', {}) # Else (can run :gr that is grep)
        self.n.lua.vim.api.nvim_set_keymap('c', '<C-o>', '', {}) # Else (can run : which returns, "E492: Not an editor command")
        self.n.lua.vim.api.nvim_set_keymap('c', 'gh', '', {}) # Else (can run :gh which returns, "E492: Not an editor command")
        self.n.lua.vim.api.nvim_set_keymap('c', '<C-v>', '', {}) # Else we can still insert `w`, `i`, or `c`
        self.n.lua.vim.api.nvim_set_keymap('l', '/$', '', {}) # to make my life easier (language mapping)
        # TODO: consider adding `te` if it works out
        # input_al = ['i', 'w', '<C-c>', '<C-g>', '<C-v>', 'c', ':', 'v', 'gh', '<C-o>', 'gr', '<Esc>', '<CR>']
        #self.n.lua.vim.api.nvim_set_option('cmdheight', 2) # That should work as well
        self.n.api.set_option('cmdheight', 2)    # Not entirely sure why (because of more-prompts IIRC)
        # Not needed since the fix for (https://github.com/vim/vim/issues/12045) has been upstreamed
        #self.n.api.set_option('iminsert' , 1) # Added for language-mapping to take effect
        self.n.api.set_option('timeout' , False) # Added by Vigoux
        self.n.api.set_option('ttimeout', False) # Added by Vigoux
        self.n.api.set_option('writeany', True)  # To avoid 'file already exists' message
        self.n.api.set_option('shortmess', 'filnxtToOsWAIcqFSI') # Not seen any effect yet
        self.n.api.set_option('showcmd', False)
        self.n.api.set_option('showmode', False) # https://github.com/neovim/neovim/issues/19352#issuecomment-1183200652


    def cast_mode(mode):
        cast_mode = {
                'n': 'Normal',
                'no': 'Operator-pending',
                'nov': 'Operator-pending charwise',
                'noV': 'Operator-pending linewise',
                'no\x16': 'Operator-pending blockwise',
                'niI': 'Insert Normal (insert)',
                'niR': 'Replace Normal (replace)',
                'niV': 'Virtual Replace Normal',
                'nt': 'Normal in terminal-emulator',
                'v': 'Visual',
                'vs': 'Select Visual',
                'V': 'Visual Line',
                'Vs': 'Select Visual Line',
                '\x16': 'Visual Block',
                '\x16s': 'Select Visual Block',
                's': 'Select',
                'S': 'Select Line',
                '\x13': 'Select Block',
                'i': 'Insert',
                'ic': 'Insert Command-line completion',
                'ix': 'Insert Ctrl-X Mode',
                'R': 'Replace',
                'Rc': 'Replace Command-line completion',
                'Rx': 'Replace Ctrl-X Mode',
                'Rv': 'Virtual Replace',
                'Rvc': 'Virtual Replace mode completion',
                'c': 'Command-line editing',
                'cv': 'Ex mode',
                'r': 'Hit-enter prompt',
                'rm': 'The more prompt',
                't': 'Terminal mode',
                'er': 'MAX_MODEL_DEPTH'
                }
        return cast_mode[mode["mode"]] + (' waiting for input (blocking)' if mode["blocking"] else '')


    def pre(self):
        self.counter = 0
        assert self.mode()["mode"] == "n"
        # DEBUG print
        #print("<<<")

    def mode(self):
        return self.n.api.get_mode()

    def feed(self, keys):
        return self.n.input(keys)

    def post(self):
        mode = self.mode()

        if mode["blocking"]:
            self.feed("<Ignore>")

        if mode["mode"] == "t":
            self.feed("<C-\\><C-N>")
        elif mode["mode"] == "nt":
            print("Resetting session (from nt):", mode)
            self.reset()
        else:
            self.feed("<ESC>")

        #self.n.lua.vim.api.nvim_command('') # untested but should work as well
        self.n.api.command("%bwipeout!") # delete all buffers (one is expected but who knows)
        self.n.api.command("file filename") # restore the buffer name or else we restart with an unnamed buffer
        #self.n.lua.vim.api.nvim_set_var('@/', '') # untested but should work as well
        self.n.api.command("let @/=''") # set the search register to '' or else `:v` has different effect

        if self.mode()["mode"] != "n":
            self.reset()

    def step(self, letter):        
        if self.counter >= self.max_counter:
            xxx = {'mode': 'er', 'blocking': False}
        else:
            if letter is not None:
                self.counter += 1
                self.feed(letter)
            # DEBUG print
            #print(letter, end=" !", flush=True)

            xxx = self.n.api.get_mode()
            # DEBUG print
            #print(' ', end='!', flush=True)
        next_mode = NvimSUL.cast_mode(xxx)
        # DEBUG print
        print('@', next_mode, flush=True)
        return next_mode


sul = NvimSUL()

input_al = ['i', 'w']#, #, #'<C-\\><C-N>', 'term<CR>', '/$', 
            #'<C-c>', '<C-g>', '<C-v>']#, 'c', ':', 'v', 'g', 'h', '<C-o>', 'r', '<Esc>', '<CR>']
# NOTE: Merging 'g' and 'r' into 'gr' changes the learning time drastically. (> 200 seconds)
# DEBUG alphabet
#input_al = [':', 'i', 'c', '<C-o>', '<CR>']

# state_origin_eq_oracle = StatePrefixEqOracle(
#     input_al, sul, walks_per_state=250, walk_len=40)
# #Aalpy author recommends KV over Lstar: https://github.com/DES-Lab/AALpy/issues/43#issuecomment-1441909285 
# print('Lstar')
# learned_moore_Lstar = run_Lstar(input_al, sul, state_origin_eq_oracle, cex_processing='rs',
#                          closing_strategy='single', automaton_type='moore', cache_and_non_det_check=True, print_level=2)

# save_automaton_to_file(learned_moore_Lstar, path='nvim-Lstar-100walks-15len', file_type='dot')

# I am performing these two assigments to start with a clean "state" (or else I hit a bug)
sul = NvimSUL()
state_origin_eq_oracle = StatePrefixEqOracle(
    input_al, sul, walks_per_state=250, walk_len=10)
print('KV')
learned_moore_KV = run_KV(input_al, sul, state_origin_eq_oracle, cex_processing='rs',
                          automaton_type='moore', cache_and_non_det_check=True, print_level=3)

save_automaton_to_file(learned_moore_KV, path='nvim-KV-250-40len', file_type='dot')

# print('Comparing results for s98 and s0')
# s98 = learned_moore_Lstar.get_state_by_id('s98')
# s0 = learned_moore_Lstar.get_state_by_id('s0')
# dist_seq = learned_moore_Lstar.find_distinguishing_seq(s0, s98)
# print(dist_seq)

# print('Comparing results')
# cexes = compare_automata( learned_moore_Lstar, learned_moore_KV, num_cex=10)
# print(cexes)
