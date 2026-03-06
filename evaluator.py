"""
Position evaluation for chess AI.
"""

from pieces import Pawn, Knight, Bishop, Rook, Queen, King


# Piece-square tables for positional bonuses
# These favor center control and piece development
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_MIDDLE_GAME_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

KING_END_GAME_TABLE = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]


class Evaluator:
    """Evaluates chess positions."""
    
    def __init__(self):
        self.piece_tables = {
            'P': PAWN_TABLE,
            'N': KNIGHT_TABLE,
            'B': BISHOP_TABLE,
            'R': ROOK_TABLE,
            'Q': QUEEN_TABLE,
            'K': KING_MIDDLE_GAME_TABLE
        }
    
    def evaluate(self, board):
        """
        Evaluate the current board position.
        
        Args:
            board: ChessBoard instance
            
        Returns:
            int: evaluation score (positive favors white, negative favors black)
        """
        if board.is_checkmate('white'):
            return -100000
        if board.is_checkmate('black'):
            return 100000
        if board.is_stalemate('white') or board.is_stalemate('black'):
            return 0
        
        score = 0
        
        # Count material and apply piece-square tables
        for row in range(8):
            for col in range(8):
                piece = board.grid[row][col]
                if piece:
                    piece_value = self._evaluate_piece(piece, row, col, board)
                    if piece.color == 'white':
                        score += piece_value
                    else:
                        score -= piece_value
        
        # Mobility bonus
        white_moves = len(board.get_legal_moves('white'))
        black_moves = len(board.get_legal_moves('black'))
        score += (white_moves - black_moves) * 5
        
        return score
    
    def _evaluate_piece(self, piece, row, col, board):
        """Evaluate a single piece including positional bonus."""
        value = piece.value
        
        # Apply piece-square table
        if piece.symbol in self.piece_tables:
            table = self.piece_tables[piece.symbol]
            
            # Use endgame king table if in endgame
            if piece.symbol == 'K' and self._is_endgame(board):
                table = KING_END_GAME_TABLE
            
            # Flip table for black pieces
            if piece.color == 'white':
                value += table[row][col]
            else:
                value += table[7 - row][col]
        
        return value
    
    def _is_endgame(self, board):
        """Check if we're in the endgame (few pieces left)."""
        piece_count = 0
        for row in range(8):
            for col in range(8):
                piece = board.grid[row][col]
                if piece and not isinstance(piece, (King, Pawn)):
                    piece_count += 1
        
        return piece_count <= 6
