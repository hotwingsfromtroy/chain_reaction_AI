import tkinter


WINNER = 1


OPT_RED = '#d10404'
OPT_GREEN = '#00911f'



DRAW_STATE = '#002559'

COMPUTER_CELL = OPT_RED
HUMAN_CELL= OPT_GREEN



root_final_screen = tkinter.Tk()
root_final_screen.title("ChainReaction")

if WINNER == 1:
    txt = 'You Won!'
    col = HUMAN_CELL
elif WINNER == -1:
    txt = 'You Lost!'
    col = COMPUTER_CELL
else:
    txt = 'Draw!'
    col = DRAW_STATE


tkinter.Label(root_final_screen, text=txt, bg = col , fg = 'white', height=5, width = 15, font=("Courier", 30)).pack()

root_final_screen.resizable(0,0)
root_final_screen.mainloop()

