"""
Stockfish-powered AI player using neural network evaluation.
Much faster and stronger than minimax approach.
"""

import chess
import chess.engine
import os
import time


class StockfishPlayer:
    """AI player using Stockfish chess engine."""
    
    def __init__(self, skill_level=20, time_limit=0.1):
        """
        Initialize Stockfish player.
        
        Args:
            skill_level: Stockfish skill (0-20). 20 = strongest (~3200 Elo)
            time_limit: Time limit per move in seconds (0.1 = instant)
        """
        self.skill_level = skill_level
        self.time_limit = time_limit
        
        # Find stockfish binary
        stockfish_paths = [
            '/usr/games/stockfish',  # Ubuntu default
            '/usr/bin/stockfish',
            '/usr/local/bin/stockfish',
            'stockfish'
        ]
        
        self.engine_path = None
        for path in stockfish_paths:
            if os.path.exists(path):
                self.engine_path = path
                break
        
        if not self.engine_path:
            raise Exception("Stockfish not found! Install with: sudo apt install stockfish")
        
        self.engine = None
        self.engine_crashed = False  # Track if engine has died
    
    def start_engine(self):
        """Start the Stockfish engine."""
        if not self.engine:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
            # Set skill level
            self.engine.configure({"Skill Level": self.skill_level})
    
    def stop_engine(self):
        """Stop the Stockfish engine."""
        if self.engine and not self.engine_crashed:
            try:
                self.engine.quit()
            except:
                pass  # Already dead
            self.engine = None
    
    def restart_engine(self):
        """Restart the Stockfish engine after a crash."""
        print("  🔄 Restarting Stockfish engine...")
        self.stop_engine()
        self.engine = None
        self.engine_crashed = False
        time.sleep(0.5)  # Brief pause before restart
        self.start_engine()
        print("  ✅ Stockfish restarted successfully!")
    
    def get_best_move(self, board):
        """
        Get best move from current position using Stockfish.
        
        Args:
            board: ChessEngine board object
        
        Returns:
            Tuple of (from_pos, to_pos) or None
        """
        try:
            self.start_engine()
            
            # Convert our board to python-chess board
            chess_board = self._convert_board(board)
            
            # Get best move from Stockfish
            result = self.engine.play(
                chess_board, 
                chess.engine.Limit(time=self.time_limit)
            )
            
            if result.move:
                # Convert UCI move (e2e4) to our format ((6,4), (4,4))
                from_pos = self._uci_to_pos(str(result.move)[:2])
                to_pos = self._uci_to_pos(str(result.move)[2:4])
                print(f"  🧠 Stockfish recommends: {result.move} (calculated in {self.time_limit}s)")
                return (from_pos, to_pos)
            
            return None
            
        except Exception as e:
            # Only print error message on first crash
            if not self.engine_crashed:
                # Print nothing - the main script will handle the fallback message
                pass
            self.engine_crashed = True
            return None
    
    def _convert_board(self, our_board):
        """
        Convert our board representation to python-chess board.
        IMPORTANT: Re-parse from DOM to avoid state corruption.
        """
        # Get fresh board state from DOM to avoid desync
        try:
            from modern_parser import ModernBoardParser
            from selenium import webdriver
            
            # We need driver reference - get it from the board if available
            # For now, use the board state passed in
            chess_board = chess.Board()
            chess_board.clear()
            
            # Map our piece symbols to python-chess
            piece_map = {
                'P': chess.PAWN, 'N': chess.KNIGHT, 'B': chess.BISHOP,
                'R': chess.ROOK, 'Q': chess.QUEEN, 'K': chess.KING
            }
            
            # Add pieces from our board
            for row in range(8):
                for col in range(8):
                    piece = our_board.get_piece((row, col))
                    if piece:
                        piece_name = piece.__class__.__name__
                        # Get first letter of piece name (Pawn -> P, Knight -> N, etc.)
                        symbol = piece_name[0].upper()
                        
                        # Handle special case for Knight
                        if piece_name == 'Knight':
                            symbol = 'N'
                        
                        if symbol in piece_map:
                            chess_piece = chess.Piece(
                                piece_map[symbol],
                                chess.WHITE if piece.color == 'white' else chess.BLACK
                            )
                            square = chess.square(col, 7 - row)  # Convert coordinates
                            chess_board.set_piece_at(square, chess_piece)
            
            # Set turn
            chess_board.turn = chess.WHITE if our_board.current_turn == 'white' else chess.BLACK
            
            # Validate board - CRITICAL: Reject invalid boards
            if not chess_board.is_valid():
                fen = chess_board.fen()
                print(f"⚠️ WARNING: Invalid board state detected!")
                print(f"   FEN: {fen}")
                print(f"   This board state is impossible in chess.")
                # Raise exception to trigger fallback AI
                raise ValueError(f"Invalid board state: {fen}")
            
            return chess_board
            
        except Exception as e:
            print(f"Board conversion error: {e}")
            import traceback
            traceback.print_exc()
            # Return empty board as fallback
            return chess.Board()
    
    def _uci_to_pos(self, uci):
        """Convert UCI notation (e2) to board position (6, 4)."""
        col = ord(uci[0]) - ord('a')
        row = 8 - int(uci[1])
        return (row, col)
    
    def get_top_moves(self, board, n=5):
        """
        Get top N moves (compatibility with humanization).
        For Stockfish, just return best move.
        
        Args:
            board: ChessEngine board object
            n: Number of moves (ignored)
        
        Returns:
            List of (move, score) tuples
        """
        try:
            best_move = self.get_best_move(board)
            if best_move:
                return [(best_move, 100)]
            return []
        except Exception as e:
            print(f"Stockfish get_top_moves error: {e}")
            return []
    
    def __del__(self):
        """Cleanup when deleted."""
        self.stop_engine()
