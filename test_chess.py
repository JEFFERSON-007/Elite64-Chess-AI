"""
Unit tests for chess engine and AI.
"""

from chess_engine import ChessBoard
from ai_player import AIPlayer
from pieces import Pawn, Knight, Bishop, Rook, Queen, King


def test_board_setup():
    """Test that board is set up correctly."""
    board = ChessBoard()
    
    # Check pawns
    for col in range(8):
        assert isinstance(board.grid[1][col], Pawn)
        assert board.grid[1][col].color == 'black'
        assert isinstance(board.grid[6][col], Pawn)
        assert board.grid[6][col].color == 'white'
    
    # Check white pieces
    assert isinstance(board.grid[7][0], Rook)
    assert isinstance(board.grid[7][1], Knight)
    assert isinstance(board.grid[7][2], Bishop)
    assert isinstance(board.grid[7][3], Queen)
    assert isinstance(board.grid[7][4], King)
    
    print("✓ Board setup test passed")


def test_pawn_moves():
    """Test pawn movement."""
    board = ChessBoard()
    
    # Pawn can move 1 or 2 squares from starting position
    moves = board.get_legal_moves('white')
    
    # White should have 20 legal moves at start (16 pawn moves + 4 knight moves)
    assert len(moves) == 20, f"Expected 20 starting moves, got {len(moves)}"
    
    # Move pawn
    assert board.move_piece((6, 4), (4, 4))  # e2 to e4
    
    # Black's turn now
    assert board.current_turn == 'black'
    
    print("✓ Pawn movement test passed")


def test_knight_moves():
    """Test knight movement."""
    board = ChessBoard()
    
    # Move knight
    assert board.move_piece((7, 1), (5, 2))  # Nb1 to c3
    
    # Knight should be at new position
    piece = board.get_piece((5, 2))
    assert isinstance(piece, Knight)
    assert piece.color == 'white'
    
    print("✓ Knight movement test passed")


def test_illegal_moves():
    """Test that illegal moves are rejected."""
    board = ChessBoard()
    
    # Try to move opponent's piece
    assert not board.move_piece((1, 0), (2, 0))  # Black pawn on white's turn
    
    # Try to move piece to invalid square
    assert not board.move_piece((6, 0), (3, 0))  # Pawn can't move 3 squares
    
    print("✓ Illegal move rejection test passed")


def test_check_detection():
    """Test check detection."""
    board = ChessBoard()
    
    # Set up a position where black king is in check
    board.grid = [[None for _ in range(8)] for _ in range(8)]
    board.grid[0][4] = King('black', (0, 4))
    board.grid[7][4] = King('white', (7, 4))
    board.grid[1][4] = Rook('white', (1, 4))  # Rook checking king
    
    assert board.is_in_check('black')
    assert not board.is_in_check('white')
    
    print("✓ Check detection test passed")


def test_ai_returns_valid_move():
    """Test that AI returns a valid move."""
    board = ChessBoard()
    ai = AIPlayer('white', depth=2)
    
    move = ai.get_best_move(board)
    
    assert move is not None
    from_pos, to_pos = move
    
    # Verify move is legal
    legal_moves = board.get_legal_moves('white')
    assert move in legal_moves
    
    print("✓ AI valid move test passed")


def test_ai_captures_free_piece():
    """Test that AI captures an undefended piece."""
    board = ChessBoard()
    
    # Set up position where black has a free queen that can be captured
    board.grid = [[None for _ in range(8)] for _ in range(8)]
    board.grid[0][4] = King('black', (0, 4))
    board.grid[7][4] = King('white', (7, 4))
    board.grid[4][3] = Queen('black', (4, 3))  # Free queen 
    board.grid[5][4] = Pawn('white', (5, 4))  # White pawn can capture diagonally
    board.grid[5][4].has_moved = True  # Mark as moved to be in capturing position
    
    board.current_turn = 'white'
    
    ai = AIPlayer('white', depth=3)
    move = ai.get_best_move(board)
    
    # AI should capture the queen
    from_pos, to_pos = move
    assert to_pos == (4, 3), f"AI should capture the free queen at (4,3), but moved to {to_pos}"
    
    print("✓ AI capture test passed")



def test_checkmate():
    """Test checkmate detection."""
    board = ChessBoard()
    
    # Set up a proper checkmate position (back rank mate)
    # King on back rank with pawns blocking escape
    board.grid = [[None for _ in range(8)] for _ in range(8)]
    board.grid[0][6] = King('black', (0, 6))
    board.grid[1][5] = Pawn('black', (1, 5))  # Pawn blocks diagonal escape
    board.grid[1][6] = Pawn('black', (1, 6))  # Pawn blocks forward escape
    board.grid[1][7] = Pawn('black', (1, 7))  # Pawn blocks diagonal escape
    board.grid[7][4] = King('white', (7, 4))
    board.grid[0][0] = Rook('white', (0, 0))  # Rook delivers checkmate on back rank
    
    board.current_turn = 'black'
    
    # Verify it's check first
    is_check = board.is_in_check('black')
    is_mate = board.is_checkmate('black')
    
    assert is_check, "King should be in check"
    assert is_mate, f"Should detect checkmate (check: {is_check}, mate: {is_mate})"
    
    print("✓ Checkmate detection test passed")




def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running Chess Engine Tests")
    print("="*50 + "\n")
    
    try:
        test_board_setup()
        test_pawn_moves()
        test_knight_moves()
        test_illegal_moves()
        test_check_detection()
        test_ai_returns_valid_move()
        test_ai_captures_free_piece()
        test_checkmate()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED! ✓")
        print("="*50 + "\n")
        return True
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    run_all_tests()
