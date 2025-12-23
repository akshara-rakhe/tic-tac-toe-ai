import tkinter as tk
from tkinter import messagebox
import random

# WINDOW SETUP 
root = tk.Tk()
root.title("Tic Tac Toe AI")

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

x = (screen_w // 2) - (WINDOW_WIDTH // 2)
y = (screen_h // 2) - (WINDOW_HEIGHT // 2)

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main = tk.Frame(root)
main.grid(row=0, column=0)

main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)

# VARIABLES 
board = [""] * 9
buttons = []
current_player = "X"

wins = 0
losses = 0
draws = 0

difficulty = tk.StringVar(value="Hard")

# GAME LOGIC 
def check_winner(player):
    win_positions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(all(board[i] == player for i in pos) for pos in win_positions)

def is_draw():
    return "" not in board

def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(False)
                board[i] = ""
                best = max(best, score)
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(True)
                board[i] = ""
                best = min(best, score)
        return best

def ai_move():
    if difficulty.get() == "Easy":
        move = random.choice([i for i in range(9) if board[i] == ""])
    elif difficulty.get() == "Medium":
        if random.random() < 0.5:
            move = random.choice([i for i in range(9) if board[i] == ""])
        else:
            move = best_move()
    else:
        move = best_move()

    board[move] = "O"
    buttons[move].config(text="O", state="disabled")

def best_move():
    best_score = -100
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def update_scoreboard():
    win_label.config(text=f"Wins: {wins}")
    loss_label.config(text=f"Losses: {losses}")
    draw_label.config(text=f"Draws: {draws}")

def end_game(message):
    messagebox.showinfo("Game Over", message)
    reset_board()

def click(index):
    global wins, losses, draws
    if board[index] == "":
        board[index] = "X"
        buttons[index].config(text="X", state="disabled")

        if check_winner("X"):
            wins += 1
            update_scoreboard()
            end_game("You Win!")
            return

        if is_draw():
            draws += 1
            update_scoreboard()
            end_game("Draw!")
            return

        ai_move()

        if check_winner("O"):
            losses += 1
            update_scoreboard()
            end_game("AI Wins!")
            return

        if is_draw():
            draws += 1
            update_scoreboard()
            end_game("Draw!")

def reset_board():
    for i in range(9):
        board[i] = ""
        buttons[i].config(text="", state="normal")

# BOARD
left = tk.Frame(main)
left.grid(row=0, column=0, padx=50)

board_frame = tk.Frame(left)
board_frame.pack()

for i in range(9):
    btn = tk.Button(
        board_frame,
        text="",
        font=("Arial", 20),
        width=5,
        height=2,
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

restart_btn = tk.Button(left, text="Restart", command=reset_board)
restart_btn.pack(pady=10)

# SCOREBOARD
right = tk.Frame(main)
right.grid(row=0, column=1, padx=50)

tk.Label(right, text="Difficulty", font=("Arial", 12, "bold")).pack(pady=5)
tk.OptionMenu(right, difficulty, "Easy", "Medium", "Hard").pack()

tk.Label(right, text="Scoreboard", font=("Arial", 14, "bold")).pack(pady=15)

win_label = tk.Label(right, text="Wins: 0", font=("Arial", 12))
loss_label = tk.Label(right, text="Losses: 0", font=("Arial", 12))
draw_label = tk.Label(right, text="Draws: 0", font=("Arial", 12))

win_label.pack()
loss_label.pack()
draw_label.pack()

root.mainloop()
