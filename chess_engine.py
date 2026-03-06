"""
Chess board representation and game logic.
"""

from pieces import Pawn, Knight, Bishop, Rook, Queen, King
import copy


class ChessBoard:
    """Represents a chess board and game state."""
    
    def __init__(self):
        """Initialize a chess board with pieces in starting position."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'
        self.en_passant_target = None
        self.move_history = []
        self.captured_pieces = []
        self._setup_board()
    
    def _setup_board(self):
        """Set up pieces in their starting positions."""
        # Pawns
        for col in range(8):
            self.grid[1][col] = Pawn('black', (1, col))
            self.grid[6][col] = Pawn('white', (6, col))
        
        # Rooks
        self.grid[0][0] = Rook('black', (0, 0))
        self.grid[0][7] = Rook('black', (0, 7))
        self.grid[7][0] = Rook('white', (7, 0))
        self.grid[7][7] = Rook('white', (7, 7))
        
        # Knights
        self.grid[0][1] = Knight('black', (0, 1))
        self.grid[0][6] = Knight('black', (0, 6))
        self.grid[7][1] = Knight('white', (7, 1))
        self.grid[7][6] = Knight('white', (7, 6))
        
        # Bishops
        self.grid[0][2] = Bishop('black', (0, 2))
        self.grid[0][5] = Bishop('black', (0, 5))
        self.grid[7][2] = Bishop('white', (7, 2))
        self.grid[7][5] = Bishop('white', (7, 5))
        
        # Queens
        self.grid[0][3] = Queen('black', (0, 3))
        self.grid[7][3] = Queen('white', (7, 3))
        
        # Kings
        self.grid[0][4] = King('black', (0, 4))
        self.grid[7][4] = King('white', (7, 4))
    
    def get_piece(self, position):
        """Get piece at the given position."""
        row, col = position
        return self.grid[row][col]
    
    def move_piece(self, from_pos, to_pos, validate=True):
        """
        Move a piece from one position to another.
        
        Args:
            from_pos: tuple (row, col) of source
            to_pos: tuple (row, col) of destination
            validate: if True, check if move is legal
            
        Returns:
            bool: True if move was successful
        """
        if validate and not self.is_legal_move(from_pos, to_pos):
            return False
        
        piece = self.get_piece(from_pos)
        target = self.get_piece(to_pos)
        
        # Handle en passant capture
        en_passant_capture = False
        if isinstance(piece, Pawn) and to_pos == self.en_passant_target:
            en_passant_capture = True
            direction = 1 if piece.color == 'white' else -1
            captured_pawn_pos = (to_pos[0] + direction, to_pos[1])
            captured_pawn = self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]]
            if captured_pawn:
                self.captured_pieces.append(captured_pawn)
                self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = None
        
        # Handle castling
        if isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) == 2:
            # Move the rook
            if to_pos[1] > from_pos[1]:  # Kingside
                rook = self.grid[from_pos[0]][7]
                self.grid[from_pos[0]][7] = None
                self.grid[from_pos[0]][5] = rook
                rook.position = (from_pos[0], 5)
                rook.has_moved = True
            else:  # Queenside
                rook = self.grid[from_pos[0]][0]
                self.grid[from_pos[0]][0] = None
                self.grid[from_pos[0]][3] = rook
                rook.position = (from_pos[0], 3)
                rook.has_moved = True
        
        # Capture piece if present
        if target and not en_passant_capture:
            self.captured_pieces.append(target)
        
        # Update en passant target
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(to_pos[0] - from_pos[0]) == 2:
            direction = -1 if piece.color == 'white' else 1
            self.en_passant_target = (from_pos[0] + direction, from_pos[1])
        
        # Move the piece
        self.grid[to_pos[0]][to_pos[1]] = piece
        self.grid[from_pos[0]][from_pos[1]] = None
        piece.position = to_pos
        piece.has_moved = True
        
        # Handle pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_pos[0] == 0) or (piece.color == 'black' and to_pos[0] == 7):
                # Auto-promote to Queen for now
                self.grid[to_pos[0]][to_pos[1]] = Queen(piece.color, to_pos)
        
        # Record move
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': piece.symbol,
            'captured': target.symbol if target else None
        })
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        return True
    
    def is_legal_move(self, from_pos, to_pos):
        """Check if a move is legal."""
        piece = self.get_piece(from_pos)
        
        if piece is None:
            return False
        
        if piece.color != self.current_turn:
            return False
        
        # Check if destination is in possible moves
        possible_moves = piece.get_possible_moves(self)
        if to_pos not in possible_moves:
            return False
        
        # Simulate move and check if it leaves king in check
        if self._leaves_king_in_check(from_pos, to_pos):
            return False
        
        return True
    
    def get_legal_moves(self, color):
        """Get all legal moves for a color."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    for to_pos in piece.get_possible_moves(self):
                        if not self._leaves_king_in_check((row, col), to_pos):
                            moves.append(((row, col), to_pos))
        return moves
    
    def _leaves_king_in_check(self, from_pos, to_pos):
        """Check if move would leave own king in check."""
        # Create a temporary board state
        temp_board = copy.deepcopy(self)
        temp_board.move_piece(from_pos, to_pos, validate=False)
        
        # Get the color of the piece that moved
        piece_color = self.get_piece(from_pos).color
        
        return temp_board.is_in_check(piece_color)
    
    def is_in_check(self, color):
        """Check if the king of the given color is in check."""
        # Find the king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        return self.is_square_attacked(king_pos, color)
    
    def is_square_attacked(self, position, defender_color):
        """Check if a square is attacked by the opponent."""
        attacker_color = 'black' if defender_color == 'white' else 'white'
        
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == attacker_color:
                    # Get possible moves (skip castling checks to avoid infinite recursion)
                    if isinstance(piece, King):
                        possible_moves = piece.get_possible_moves(self, skip_castling=True)
                    else:
                        possible_moves = piece.get_possible_moves(self)
                    if position in possible_moves:
                        return True
        
        return False
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate."""
        if not self.is_in_check(color):
            return False
        
        # Check if there are any legal moves
        return len(self.get_legal_moves(color)) == 0
    
    def is_stalemate(self, color):
        """Check if the given color is in stalemate."""
        if self.is_in_check(color):
            return False
        
        return len(self.get_legal_moves(color)) == 0
    
    def is_game_over(self):
        """Check if the game is over."""
        return (self.is_checkmate('white') or self.is_checkmate('black') or 
                self.is_stalemate('white') or self.is_stalemate('black'))
    
    def get_game_result(self):
        """Get the result of the game."""
        if self.is_checkmate('white'):
            return 'Black wins by checkmate'
        elif self.is_checkmate('black'):
            return 'White wins by checkmate'
        elif self.is_stalemate('white') or self.is_stalemate('black'):
            return 'Draw by stalemate'
        else:
            return 'Game in progress'
    
    def display(self):
        """Display the board in ASCII."""
        print('\n  a b c d e f g h')
        print('  ----------------')
        for row in range(8):
            print(f'{8-row}|', end='')
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    print(f'{piece}', end=' ')
                else:
                    print('. ', end='')
            print(f'|{8-row}')
        print('  ----------------')
        print('  a b c d e f g h\n')
    
    def clone(self):
        """Create a deep copy of the board."""
        return copy.deepcopy(self)
