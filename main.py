"""
Main entry point for Chess AI.
"""

from game import ChessGame


def main():
    """Start a chess game."""
    print("\n" + "="*50)
    print("       WELCOME TO CHESS AI")
    print("="*50)
    print("\nThis AI uses minimax with alpha-beta pruning")
    print("to predict moves and make intelligent decisions.")
    print("\n" + "="*50 + "\n")
    
    # Get player preferences
    while True:
        color_choice = input("Choose your color (w/b) [default: white]: ").strip().lower()
        if color_choice in ['', 'w', 'white']:
            human_color = 'white'
            break
        elif color_choice in ['b', 'black']:
            human_color = 'black'
            break
        else:
            print("Invalid choice. Enter 'w' or 'b'")
    
    while True:
        try:
            depth_input = input("Choose AI difficulty (1-6) [default: 4]: ").strip()
            if depth_input == '':
                ai_depth = 4
                break
            ai_depth = int(depth_input)
            if 1 <= ai_depth <= 6:
                break
            else:
                print("Please enter a number between 1 and 6")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 6")
    
    # Create and start game
    game = ChessGame(human_color=human_color, ai_depth=ai_depth)
    game.play()


if __name__ == '__main__':
    main()
