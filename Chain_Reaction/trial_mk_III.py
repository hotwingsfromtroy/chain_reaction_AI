import tkinter
# import tkFont
import time

import copy
import random

ROW_SIZE = 0
COL_SIZE = 0

DEPTH = 1
LEVEL = 0

OPT_RED = '#d10404'
OPT_GREEN = '#00911f'

MINIMAX_VANILLA = 1
MINIMAX_ALPHABETA = 2





SELECTED_ALGO = 0





UNOCCUPIED_CELL = '#485969'
COMPUTER_CELL = ''
HUMAN_CELL= ''


CURR_PLAYER = 1


class Board:
    def __init__(self, dimensions):
        self.row = dimensions[0]
        self.col = dimensions[1]
        self.board = [[0 for j in range(self.col)] for i in range(self.row)]
        
        self.crit = [[4 for j in range(self.col)] for i in range(self.row)]
        
        for i in range(self.col):
            self.crit[0][i] = 3
            self.crit[self.row-1][i] = 3

        for i in range(self.row):
            self.crit[i][0] = 3
            self.crit[i][self.col-1] = 3

        self.crit[0][0] = self.crit[0][self.col-1] = self.crit[self.row-1][0] = self.crit[self.row-1][self.col-1] = 2

        # self.crit_corner = 2
        # self.crit_edge = 3
        # self.crit_middle = 4

    def neighbours(self, dimensions):
        r = dimensions[0]
        c = dimensions[1]
        neigh = [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]
        act_neigh = []
        for i in neigh:
            if i[0] != -1 and i[0] != self.row and i[1] != -1 and i[1] != self.col:
                act_neigh.append(i)
        return act_neigh

    def print_board(self):
        for i in range(self.row):
            for j in range(self.col):
                print(self.board[i][j], end = ' ')
            print('')

def sig(val):
    if not(val):
        return 0
    return int(val/abs(val))


def update_board(board):
    print('START UPDATE BOARD')
    global button_list
    for i in range(board.row):
        for j in range(board.col):
            button_list[i][j].config(bg = UNOCCUPIED_CELL)
            button_list[i][j].config(text=button_text(abs(board.board[i][j])))
            if sig(board.board[i][j]) == -1:
                button_list[i][j].config(bg = COMPUTER_CELL)
            elif sig(board.board[i][j]) == 1:
                button_list[i][j].config(bg = HUMAN_CELL)
    print('END UPDATE BOARD')



def commit_move(board, pos, player):
    print('START COMMIT MOVE')
    # global CURR_PLAYER
    r = pos[0]; c=pos[1]
    if sig(board.board[r][c]) == 0 or sig(board.board[r][c]) == player:
        print('GONNA COMMIT')
        
        # board.board[r][c] += 1
       
        board.board[r][c] = player*( abs(board.board[r][c]) + 1)
        t = time.time()
        while True:
            # update_board(board)
            # time.sleep(0.2)
            mod_list = []
            for i in range(board.row):
                for j in range(board.col):
                    if abs(board.board[i][j]) >= board.crit[i][j]:
                        mod_list.append((i, j))

            if time.time() - t >= 3:
			#Can't afford to spend more time, strange loop here!
			#print board, pos
			#raw_input()
                return 0
			    # break
            if not mod_list:
                break
            else:
                for i in mod_list:
                    board.board[i[0]][i[1]] = player*( abs(board.board[i[0]][i[1]]) - board.crit[i[0]][i[1]])
                    for j in board.neighbours(i):
                        board.board[j[0]][j[1]] = player*( abs(board.board[j[0]][j[1]]) + 1)
            # time.sleep(0.5)

        # CURR_PLAYER *= -1
    else:
        print('END COMMIT MOVE')
        return -1

    # update_board(board)

    # board.print_board()
    
    print('END COMMIT MOVE')
    return 1

# def get_values(row, col, opt):
def get_values():

    global ROW_SIZE
    global COL_SIZE
    global COMPUTER_CELL
    global HUMAN_CELL
    global SELECTED_ALGO
    global MINIMAX_VANILLA
    global MINIMAX_ALPHABETA
    global LEVEL

    ROW_SIZE = row_var.get()
    COL_SIZE = col_var.get()

    opt = opt_var.get()

    if opt == 1:
        HUMAN_CELL = OPT_RED
        COMPUTER_CELL = OPT_GREEN
    elif opt == 2:
        HUMAN_CELL = OPT_GREEN
        COMPUTER_CELL = OPT_RED


    algo_opt = algo_opt_var.get()

    if algo_opt == 1:
        SELECTED_ALGO = MINIMAX_VANILLA
    elif algo_opt == 2:
        SELECTED_ALGO = MINIMAX_ALPHABETA

    LEVEL = level_var.get()

    root_start_menu.destroy()







def button_text(num_val):
    if not(num_val):
        return ' '
    return str(num_val)









def chains(board, player):
    board = copy.deepcopy(board)
    lengths = []
	# for pos in [(x,y) for x in range(board.m) for y in range(board.n)]:
    for i in range(board.row):
        for j in range(board.col):
            if abs(board.board[i][j]) == (board.crit[i][j] - 1) and sig(board.board[i][j]) == player:
                l = 0
                visiting_stack = []
                visiting_stack.append((i, j))
                while visiting_stack:
                    pos = visiting_stack.pop()
                    board.board[pos[0]][pos[1]] = 0
                    l += 1
                    for k in board.neighbours(pos):
                        if abs(board.board[k[0]][k[1]]) == (board.crit[k[0]][k[1]] - 1) and sig(board.board[k[0]][k[1]]) == player:
                            visiting_stack.append(k)
                lengths.append(l)
    return lengths


def score(board, player):
    print('START SCORE')

    sc = 0
    player_orbs, enemy_orbs = 0, 0
	# for pos in [(x,y) for x in range(board.m) for y in range(board.n)]:
    for i in range(board.row):
        for j in range(board.col):
            if sig(board.board[i][j]) == player:
                player_orbs += abs(board.board[i][j])
                flag_not_vulnerable = True
                for k in board.neighbours((i, j)):
                    if sig(board.board[k[0]][k[1]]) == -player and (abs(board.board[k[0]][k[1]]) == board.crit[k[0]][k[1]] - 1):
                        sc -= 5-board.crit[i][j]
                        flag_not_vulnerable = False
                if flag_not_vulnerable:
                    #The edge Heuristic
                    if board.crit[i][j] == 3:
                        sc += 2
                    #The corner Heuristic
                    elif board.crit[i][j] == 2:
                        sc += 3
                    #The unstability Heuristic
                    if abs(board.board[i][j]) == board.crit[i][j] - 1:
                        sc += 2
                    #The vulnerablity Heuristic
            else:
                enemy_orbs += abs(board.board[i][j])
	#The number of Orbs Heuristic
    sc += player_orbs
	#You win when the enemy has no orbs
    if enemy_orbs == 0 and player_orbs > 1:
        print('END SCORE')

        return 10000
	#You loose when you have no orbs
    elif player_orbs == 0 and enemy_orbs > 1:
        print('END SCORE')
        
        return -10000
	#The chain Heuristic
    sc += sum([2*i for i in chains(board,player) if i > 1])
    print('END SCORE')
    
    return sc







# def minimax(board, pos, depth, player, isMax, level):
#     print('START MINIMAX')

#     board = copy.deepcopy(board)
#     # alpha = copy.deepcopy(alpha)
#     # beta = copy.deepcopy(beta)

#     code = commit_move(board, pos, player)
#     if depth == 0 or code == 0:
#         print('END MINIMAX')
        
#         return score(board, player)

#     child_pos = []
#     for i in range(board.row):
#         for j in range(board.col):
#             if sig(board.board[i][j]) != -player:
#                 child_pos.append((i, j))
#     child_pos = list(set(child_pos))



#     rand_val = random.randint(1, 100)




#     if isMax:
#         bestVal = float('-inf')

#         if rand_val > level*10:
#             i = random.choice(child_pos)
#             value = minimax(board, i, depth-1, -player, False, level)
#             bestVal = max(bestVal, value)
#         else:
#             for i in child_pos:
#                 value = minimax(board, i, depth-1, -player, False, level)
#                 bestVal = max(bestVal, value)
#                 alpha = max(alpha, bestVal)

#         print('END MINIMAX')
        
#         return bestVal

#     else:
#         bestVal = float('inf')

#         if rand_val > level*10:
#             i = random.choice(child_pos)
#             bestVal = minimax(board, i, depth-1, -player, True, level)
#             # bestVal = int(max(bestVal, value))
#         else:
#             for i in child_pos:
#                 value = minimax_alphabeta(board, i, depth-1, -player, True, alpha, beta, level)
#                 bestVal = min(bestVal, value)
#                 beta = min(beta, bestVal)

#                 if beta <= alpha:
#                     break
#         print('END MINIMAX')
        
#         return bestVal



























def minimax_alphabeta(board, pos, depth, player, isMax, alpha, beta, level):
    print('START MINIMAX')

    board = copy.deepcopy(board)
    alpha = copy.deepcopy(alpha)
    beta = copy.deepcopy(beta)

    code = commit_move(board, pos, player)
    if depth == 0 or code == 0:
        print('END MINIMAX')
        
        return score(board, player)

    child_pos = []
    for i in range(board.row):
        for j in range(board.col):
            if sig(board.board[i][j]) != -player:
                child_pos.append((i, j))
    child_pos = list(set(child_pos))



    rand_val = random.randint(1, 100)




    if isMax:
        bestVal = float('-inf')

        if rand_val > level*10:
            i = random.choice(child_pos)
            value = minimax_alphabeta(board, i, depth-1, -player, False, alpha, beta, level)
            bestVal = max(bestVal, value)
        else:
            for i in child_pos:
                value = minimax_alphabeta(board, i, depth-1, -player, False, alpha, beta, level)
                bestVal = max(bestVal, value)
                alpha = max(alpha, bestVal)

                # if beta <= alpha or alpha == 10000 or alpha == -10000 or beta == 10000 or beta == -10000:
                if beta <= alpha:

                    break
        print('END MINIMAX')
        
        return bestVal

    else:
        bestVal = float('inf')

        if rand_val > level*10:
            i = random.choice(child_pos)
            bestVal = minimax_alphabeta(board, i, depth-1, -player, True, alpha, beta, level)
            # bestVal = int(max(bestVal, value))
        else:
            for i in child_pos:
                value = minimax_alphabeta(board, i, depth-1, -player, True, alpha, beta, level)
                bestVal = min(bestVal, value)
                beta = min(beta, bestVal)

                # if beta <= alpha or alpha == 10000 or alpha == -10000 or beta == 10000 or beta == -10000:
                if beta <= alpha:
                    break
        print('END MINIMAX')
        
        return bestVal



















root_start_menu = tkinter.Tk()
root_start_menu.title("Tk dropdown example")

# Add a grid
mainframe = tkinter.Frame(root_start_menu)
mainframe.grid(column=0,row=0, sticky=(tkinter.N,tkinter.W,tkinter.E,tkinter.S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 40, padx = 40)

# Create a Tkinter variable
row_var = tkinter.IntVar(root_start_menu)
col_var = tkinter.IntVar(root_start_menu)

# Dictionary with options
dim_choices = {4, 5, 6, 7}
row_var.set(5) # set the default option
col_var.set(5) # set the default option



row_dim_opt = tkinter.OptionMenu(mainframe, row_var, *dim_choices)

col_dim_opt = tkinter.OptionMenu(mainframe, col_var, *dim_choices)


tkinter.Label(mainframe, text="Select board dimensions").grid(row = 0, column = 1)
row_dim_opt.grid(row = 2, column =1)
col_dim_opt.grid(row = 2, column =2)


tkinter.Label(mainframe, text="Select color").grid(row = 3, column = 1)


opt_var = tkinter.IntVar(root_start_menu)
opt_var.set(1)
option1 = tkinter.Radiobutton(mainframe, text="Red", variable=opt_var, value=1)
option1.grid(row = 4, column = 1)

option2 = tkinter.Radiobutton(mainframe, text="Green", variable=opt_var, value=2)
option2.grid(row = 4, column = 2)




tkinter.Label(mainframe, text="Select Algorithm").grid(row = 5, column = 1)


algo_opt_var = tkinter.IntVar(root_start_menu)
algo_opt_var.set(2)
algo_option1 = tkinter.Radiobutton(mainframe, text="Minimax Vanilla", variable=algo_opt_var, value=1)
algo_option1.grid(row = 6, column = 1)

algo_option2 = tkinter.Radiobutton(mainframe, text="Minimax with Alpha-Beta pruning", variable=algo_opt_var, value=2)
algo_option2.grid(row = 6, column = 2)





depth_var = tkinter.IntVar(root_start_menu)
# Dictionary with options
depth_choices = {1, 2, 3}
depth_var.set(1) # set the default option

depth_opt = tkinter.OptionMenu(mainframe, depth_var, *depth_choices)

tkinter.Label(mainframe, text="Select depth").grid(row = 7, column = 1)
depth_opt.grid(row = 8, column =1)



level_var = tkinter.IntVar(root_start_menu)
# Dictionary with options
level_choices = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
level_var.set(5) # set the default option

level_opt = tkinter.OptionMenu(mainframe, level_var, *level_choices)

tkinter.Label(mainframe, text="Select Level").grid(row = 9, column = 1)
level_opt.grid(row = 10, column =1)



button = tkinter.Button(mainframe, text='Play', command= get_values)

button.grid(row = 3, column = 3)

# var.set('Playyyyyy')

root_start_menu.resizable(0, 0)
root_start_menu.mainloop()




board = Board([ROW_SIZE, COL_SIZE])




root_game = tkinter.Tk()
root_game.title("ChainReaction")

button_list = []


def make_move(board, button):
    print('START MAKE MOVE')
    global CURR_PLAYER
    global LEVEL
    gi=button.grid_info()
    r=gi['row']
    c=gi['column']

    if CURR_PLAYER == 1:
        code = commit_move(board, (r, c), CURR_PLAYER)
        if code == 1:
            update_board(board)

            if score(board, CURR_PLAYER) == 10000:
                print('PLAYER WINS')
                CURR_PLAYER *= -1
                print('END MAKE MOVE')

                return

            CURR_PLAYER *= -1
            # board.print_board()
            # print('\n\n')
            
            



            pos_and_val = dict()
            row_list = list(set(list(range(board.row))))
            col_list = list(set(list(range(board.col))))

            # for i in range(board.row):
            for i in row_list:
                for j in col_list:

                # for j in range(board.col):
                    if sig(board.board[i][j]) != -CURR_PLAYER:
                        pos_and_val[(i, j)] = float('inf')
            
            depth = 2*DEPTH -1
            bestPos = (-1, -1)
            bestVal = float('inf')


            if SELECTED_ALGO == MINIMAX_VANILLA:
                pass
            
            elif SELECTED_ALGO == MINIMAX_ALPHABETA:

                for i in pos_and_val:
                    pos_and_val[i] = minimax_alphabeta(board, i, depth, CURR_PLAYER, False, float('-inf'), float('inf'), LEVEL)
                    if pos_and_val[i] < bestVal:
                        bestVal = int(pos_and_val[i])
                        bestPos = i

                    if bestVal == -10000:
                        print('COMPUTER WINS')

                        break



            
            print(bestPos, bestVal)
            print('\n\n')
            print(pos_and_val)
            print('\n\n')

            code = commit_move(board, bestPos, CURR_PLAYER)
            if code == 1:
                update_board(board)

                CURR_PLAYER *= -1
                # board.print_board()
                # print('\n\n') 
            if bestVal == -10000:
                    # CURR_PLAYER *= -1
                    CURR_PLAYER = -1

                    print('COMPUTER WINS')  

        elif code == 0:
            update_board(board)
            CURR_PLAYER = -1

            sc_player = score(board, 1)
            sc_computer = score(board, -1)
            if sc_player > sc_computer:
                print('PLAYER WINS') 
            elif sc_player < sc_computer:
                print('COMPUTER WINS')
            else:
                print('DRAW') 
    print('END MAKE MOVE')











for i in range(board.row):
    button_list.append([])
    for j in range(board.col):
        obj = tkinter.Button(root_game, relief= tkinter.FLAT, text= button_text(board.board[i][j]), height = 2, width = 4  )
        
        obj.configure(command=lambda button=obj: make_move(board, button))
        # button_list[i][j]['font'] = myFont
        # button_list[i][j].config(bg = UNOCCUPIED_CELL)
        obj.config(bg = UNOCCUPIED_CELL, fg = 'white')
        
        # button_list[i][j].grid(row = i, column = j, padx = 2, pady = 2)
        obj.grid(row = i, column = j, padx = 2, pady = 2)

        button_list[i].append(obj)




root_game.resizable(0, 0) # keeing window un-resizeable

root_game.mainloop()
















# username_input_frame.pack(fill = tkinter.X)######################################################













