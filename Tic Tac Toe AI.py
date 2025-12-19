import random
# Board display
def print_board(board):
    print()
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])
    print()

# Empty positions
def get_empty_positions(board):
    return [i for i in range(9) if board[i] == " "]

win_conditions = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]

def check_winner(board, player):
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False


def is_draw(board):
    return " " not in board


def player_move(board):
    while True:
        try:
            move = int(input("Enter position (0-8): "))
            if move in range(9) and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 0 and 8.")


# EASY AI (Random)
def ai_move_easy(board):
    move = random.choice(get_empty_positions(board))
    board[move] = "O"

# MINIMAX (Hard AI)
def minimax(board, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for move in get_empty_positions(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in get_empty_positions(board):
            board[move] = "X"
            score = minimax(board, True)
            board[move] = " "
            best_score = min(best_score, score)
        return best_score


def ai_move_hard(board):
    best_score = -float("inf")
    best_move = None

    for move in get_empty_positions(board):
        board[move] = "O"
        score = minimax(board, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move

    board[best_move] = "O"

# MEDIUM AI (Mix)
def ai_move_medium(board):
    if random.random() < 0.5:
        ai_move_easy(board)
    else:
        ai_move_hard(board)

def game_loop(board, ai_move):
    while True:
        print_board(board)

        # Human turn
        player_move(board)
        if check_winner(board, "X"):
            print_board(board)
            print("You win!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # AI turn
        ai_move(board)
        if check_winner(board, "O"):
            print_board(board)
            print("AI wins!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

def main():
    board = [" "] * 9

    print("Welcome to Tic Tac Toe!")
    print("Board positions:")
    print("0 | 1 | 2")
    print("3 | 4 | 5")
    print("6 | 7 | 8")

    difficulty = input("Choose difficulty (easy / medium / hard): ").lower()

    if difficulty == "easy":
        ai_move = ai_move_easy
    elif difficulty == "medium":
        ai_move = ai_move_medium
    else:
        ai_move = ai_move_hard

    game_loop(board, ai_move)


if __name__ == "__main__":
    main()
