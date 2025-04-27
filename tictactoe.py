import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]

    def print_board(self):
        print()
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False

    def undo_move(self, position):
        self.board[position] = ' '

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],  
            [0,3,6], [1,4,7], [2,5,8],  
            [0,4,8], [2,4,6]            
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board

    # MiniMAx Algorithm
    def minimax(self, is_maximizing):
        if self.check_winner('X'):
            return 1
        if self.check_winner('O'):
            return -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                self.make_move(move, 'X')
                score = self.minimax(False)
                self.undo_move(move)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.make_move(move, 'O')
                score = self.minimax(True)
                self.undo_move(move)
                best_score = min(score, best_score)
            return best_score

    def get_ai_move_minimax(self):
        best_score = -float('inf')
        best_move = None
        for move in self.available_moves():
            self.make_move(move, 'X')
            score = self.minimax(False)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    # Alpha-Beta Pruning 
    def minimax_alpha_beta(self, is_maximizing, alpha, beta):
        if self.check_winner('X'):
            return 1
        if self.check_winner('O'):
            return -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                self.make_move(move, 'X')
                score = self.minimax_alpha_beta(False, alpha, beta)
                self.undo_move(move)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.make_move(move, 'O')
                score = self.minimax_alpha_beta(True, alpha, beta)
                self.undo_move(move)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def get_ai_move_alpha_beta(self):
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        for move in self.available_moves():
            self.make_move(move, 'X')
            score = self.minimax_alpha_beta(False, alpha, beta)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

# Play Game   
def play_game(ai_type='minimax'):
    human_score = 0
    ai_score = 0
    draw_score = 0

    while True:
        game = TicTacToe()
        human = 'O'
        ai = 'X'
        current_player = human

        while True:
            game.print_board()
            if current_player == human:
                move = int(input("Enter your move (0-8): "))
                if not game.make_move(move, human):
                    print("Invalid move! Try again.")
                    continue
            else:
                print(f"AI ({ai_type}) is thinking...")
                start = time.time()
                if ai_type == 'minimax':
                    move = game.get_ai_move_minimax()
                else:
                    move = game.get_ai_move_alpha_beta()
                end = time.time()
                game.make_move(move, ai)
                print(f"AI chose move {move} in {round(end - start, 4)} seconds.")

            if game.check_winner(current_player):
                game.print_board()
                if current_player == human:
                    print("You win! 🎉")
                    human_score += 1
                else:
                    print("AI wins! 🤖")
                    ai_score += 1
                break

            if game.is_draw():
                game.print_board()
                print("It's a draw! 🤝")
                draw_score += 1
                break

            current_player = human if current_player == ai else ai

        # Game Over
        print("\nScoreboard:")
        print(f"You: {human_score} | AI: {ai_score} | Draws: {draw_score}")

        choice = input("\nDo you want to play again? (y/n): ").lower()
        if choice != 'y':
            print("\nNice game! Challenge yourself again soon!")
            print("Final Score:")
            print(f"You: {human_score} | AI: {ai_score} | Draws: {draw_score}")
            break
    print("\nPress Enter to go to the main menu...")
    input() 
    main_menu() 

# Comparison        
def compare_performance():
    game = TicTacToe()

    print("\nTesting Minimax...")
    start = time.time()
    game.get_ai_move_minimax()
    end = time.time()
    print(f"Minimax Time: {round(end - start, 5)} seconds")

    game = TicTacToe()
    print("\nTesting Alpha-Beta Pruning...")
    start = time.time()
    game.get_ai_move_alpha_beta()
    end = time.time()
    print(f"Alpha-Beta Time: {round(end - start, 5)} seconds\n")

# Main Menu
def main_menu():
    print("\nWelcome to Tic-Tac-Toe AI!")
    print("1. Play against Minimax AI")
    print("2. Play against Alpha-Beta Pruning AI")
    print("3. Compare AI performance")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        play_game('minimax')
    elif choice == '2':
        play_game('alphabeta')
    elif choice == '3':
        compare_performance()
        main_menu()
    elif choice == '4':
        print("Thanks for Playing!")
    else:
        print("Invalid choice! Try again.")
        main_menu()
        
if __name__ == "__main__":
    main_menu()

