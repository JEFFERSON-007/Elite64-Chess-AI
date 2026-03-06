"""
Chess piece classes with movement logic.
"""

class Piece:
    """Base class for all chess pieces."""
    
    def __init__(self, color, position):
        """
        Initialize a chess piece.
        
        Args:
            color: 'white' or 'black'
            position: tuple (row, col) on the board
        """
        self.color = color
        self.position = position
        self.has_moved = False
    
    def __repr__(self):
        return f"{self.color[0].upper()}{self.symbol}"
    
    def get_possible_moves(self, board):
        """
        Get all possible moves for this piece (may include illegal moves that leave king in check).
        
        Args:
            board: ChessBoard instance
            
        Returns:
            list of tuples: [(row, col), ...]
        """
        raise NotImplementedError("Subclasses must implement get_possible_moves")
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8


class Pawn(Piece):
    """Pawn piece."""
    symbol = 'P'
    value = 100
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1  # White moves up, black down
        
        # Forward move
        new_row = row + direction
        if self.is_valid_position(new_row, col) and board.grid[new_row][col] is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row2 = row + 2 * direction
                # Bounds check before accessing grid
                if self.is_valid_position(new_row2, col) and board.grid[new_row2][col] is None:
                    moves.append((new_row2, col))
        
        # Capture diagonally
        for dcol in [-1, 1]:
            new_row = row + direction
            new_col = col + dcol
            if self.is_valid_position(new_row, new_col):
                target = board.grid[new_row][new_col]
                if target and target.color != self.color:
                    moves.append((new_row, new_col))
                
                # En passant
                if (new_row, new_col) == board.en_passant_target:
                    moves.append((new_row, new_col))
        
        return moves


class Knight(Piece):
    """Knight piece."""
    symbol = 'N'
    value = 320
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All possible L-shaped moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for drow, dcol in knight_moves:
            new_row, new_col = row + drow, col + dcol
            if self.is_valid_position(new_row, new_col):
                target = board.grid[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves


class Bishop(Piece):
    """Bishop piece."""
    symbol = 'B'
    value = 330
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # Diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row = row + i * drow
                new_col = col + i * dcol
                
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.grid[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Rook(Piece):
    """Rook piece."""
    symbol = 'R'
    value = 500
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row = row + i * drow
                new_col = col + i * dcol
                
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.grid[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Queen(Piece):
    """Queen piece."""
    symbol = 'Q'
    value = 900
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All 8 directions (combination of rook and bishop)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row = row + i * drow
                new_col = col + i * dcol
                
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.grid[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class King(Piece):
    """King piece."""
    symbol = 'K'
    value = 20000
    
    def get_possible_moves(self, board, skip_castling=False):
        moves = []
        row, col = self.position
        
        # One square in any direction
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if self.is_valid_position(new_row, new_col):
                target = board.grid[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        # Castling - skip during attack detection to avoid infinite recursion
        if not skip_castling and not self.has_moved and not board.is_in_check(self.color):
            # Kingside castling
            if self._can_castle_kingside(board):
                moves.append((row, col + 2))
            # Queenside castling
            if self._can_castle_queenside(board):
                moves.append((row, col - 2))
        
        return moves
    
    def _can_castle_kingside(self, board):
        """Check if kingside castling is possible."""
        row, col = self.position
        rook = board.grid[row][7]
        
        if rook is None or rook.symbol != 'R' or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        if board.grid[row][5] is not None or board.grid[row][6] is not None:
            return False
        
        # Check if king passes through or ends up in check
        for check_col in [col + 1, col + 2]:
            if board.is_square_attacked((row, check_col), self.color):
                return False
        
        return True
    
    def _can_castle_queenside(self, board):
        """Check if queenside castling is possible."""
        row, col = self.position
        rook = board.grid[row][0]
        
        if rook is None or rook.symbol != 'R' or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        if board.grid[row][1] is not None or board.grid[row][2] is not None or board.grid[row][3] is not None:
            return False
        
        # Check if king passes through or ends up in check
        for check_col in [col - 1, col - 2]:
            if board.is_square_attacked((row, check_col), self.color):
                return False
        
        return True
