"""
Game interface for playing chess against the AI.
"""

from chess_engine import ChessBoard
from ai_player import AIPlayer


class ChessGame:
    """Manages a chess game between human and AI."""
    
    def __init__(self, human_color='white', ai_depth=4):
        """
        Initialize a chess game.
        
        Args:
            human_color: 'white' or 'black'
            ai_depth: AI search depth
        """
        self.board = ChessBoard()
        self.human_color = human_color
        self.ai_color = 'black' if human_color == 'white' else 'white'
        self.ai = AIPlayer(self.ai_color, depth=ai_depth)
    
    def play(self):
        """Start the game loop."""
        print("\n" + "="*50)
        print("    CHESS AI - PREPARE TO BE CHALLENGED!")
        print("="*50)
        print(f"\nYou are playing as {self.human_color.upper()}")
        print(f"AI difficulty: Depth {self.ai.depth} (looking {self.ai.depth} moves ahead)")
        print("\nMove format: Enter moves like 'e2 e4' or 'e2e4'")
        print("Type 'quit' to exit, 'help' for help\n")
        
        while not self.board.is_game_over():
            self.board.display()
            
            if self.board.current_turn == self.human_color:
                self._human_turn()
            else:
                self._ai_turn()
            
            # Check for check
            if self.board.is_in_check(self.board.current_turn):
                print(f"\n{'='*50}")
                print(f"  {self.board.current_turn.upper()} IS IN CHECK!")
                print(f"{'='*50}\n")
        
        # Game over
        self.board.display()
        result = self.board.get_game_result()
        print("\n" + "="*50)
        print(f"  GAME OVER: {result}")
        print("="*50 + "\n")
    
    def _human_turn(self):
        """Handle human player's turn."""
        while True:
            try:
                move_str = input(f"{self.human_color.capitalize()}'s turn. Enter move: ").strip().lower()
                
                if move_str == 'quit':
                    print("Thanks for playing!")
                    exit(0)
                
                if move_str == 'help':
                    self._show_help()
                    continue
                
                if move_str == 'moves':
                    self._show_legal_moves()
                    continue
                
                from_pos, to_pos = self._parse_move(move_str)
                
                if self.board.move_piece(from_pos, to_pos):
                    break
                else:
                    print("Illegal move! Try again.")
            
            except (ValueError, IndexError) as e:
                print(f"Invalid input format. Use format like 'e2 e4' or 'e2e4'")
    
    def _ai_turn(self):
        """Handle AI player's turn."""
        print(f"\n{self.ai_color.capitalize()} (AI) is thinking...")
        
        move = self.ai.get_best_move(self.board)
        
        if move:
            from_pos, to_pos = move
            from_notation = self._pos_to_notation(from_pos)
            to_notation = self._pos_to_notation(to_pos)
            
            piece = self.board.get_piece(from_pos)
            piece_name = piece.__class__.__name__
            
            self.board.move_piece(from_pos, to_pos, validate=False)
            
            print(f"\nAI moves: {piece_name} from {from_notation} to {to_notation}")
        else:
            print("AI has no legal moves!")
    
    def _parse_move(self, move_str):
        """
        Parse move string to positions.
        
        Args:
            move_str: string like 'e2 e4' or 'e2e4'
            
        Returns:
            tuple: (from_pos, to_pos)
        """
        # Remove spaces
        move_str = move_str.replace(' ', '')
        
        if len(move_str) != 4:
            raise ValueError("Invalid move format")
        
        from_notation = move_str[:2]
        to_notation = move_str[2:4]
        
        from_pos = self._notation_to_pos(from_notation)
        to_pos = self._notation_to_pos(to_notation)
        
        return from_pos, to_pos
    
    def _notation_to_pos(self, notation):
        """Convert algebraic notation (e.g., 'e2') to position (6, 4)."""
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return (row, col)
    
    def _pos_to_notation(self, pos):
        """Convert position (6, 4) to algebraic notation (e.g., 'e2')."""
        row, col = pos
        return f"{chr(col + ord('a'))}{8 - row}"
    
    def _show_help(self):
        """Show help information."""
        print("\n" + "="*50)
        print("HELP")
        print("="*50)
        print("Commands:")
        print("  - Enter moves in format: 'e2 e4' or 'e2e4'")
        print("  - 'moves' - Show all legal moves")
        print("  - 'help' - Show this help")
        print("  - 'quit' - Exit the game")
        print("\nPiece abbreviations:")
        print("  WP/BP = Pawn, WN/BN = Knight, WB/BB = Bishop")
        print("  WR/BR = Rook, WQ/BQ = Queen, WK/BK = King")
        print("="*50 + "\n")
    
    def _show_legal_moves(self):
        """Show all legal moves for current player."""
        legal_moves = self.board.get_legal_moves(self.board.current_turn)
        
        if not legal_moves:
            print("No legal moves available!")
            return
        
        print(f"\nLegal moves for {self.board.current_turn}:")
        move_strings = []
        for from_pos, to_pos in legal_moves:
            from_notation = self._pos_to_notation(from_pos)
            to_notation = self._pos_to_notation(to_pos)
            piece = self.board.get_piece(from_pos)
            move_strings.append(f"{from_notation}{to_notation} ({piece.symbol})")
        
        # Display in columns
        for i in range(0, len(move_strings), 4):
            print("  " + "  ".join(move_strings[i:i+4]))
        print()
