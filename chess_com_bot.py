"""
Chess.com bot using browser automation.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random

from modern_parser import ModernBoardParser
from chess_engine import ChessBoard
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from ai_player import AIPlayer
from humanizer import Humanizer


class ChessComBot:
    """Automates playing chess on Chess.com."""
    
    def __init__(self, ai_depth=4, min_think_time=3, max_think_time=12, humanize=True):
        """
        Initialize Chess.com bot.
        
        Args:
            ai_depth: AI search depth
            min_think_time: Minimum seconds to wait before moving
            max_think_time: Maximum seconds to wait before moving
            humanize: Enable advanced humanization features
        """
        self.ai_depth = ai_depth
        self.min_think_time = min_think_time
        self.max_think_time = max_think_time
        self.humanize = humanize
        
        # Initialize browser using compatibility helper
        print("Initializing browser...")
        from chrome_helper import create_chrome_driver
        
        try:
            self.driver = create_chrome_driver(headless=False)
            print("✓ Browser initialized successfully")
        except Exception as e:
            print(f"✗ Error starting browser: {e}")
            raise
        
        self.parser = ModernBoardParser(self.driver)
        self.humanizer = Humanizer(self.driver) if humanize else None
        self.board = None
        self.ai = None
        self.our_color = None
    
    def open_chess_com(self, url=None):
        """
        Open Chess.com.
        
        Args:
            url: Optional specific game URL
        """
        if url:
            self.driver.get(url)
        else:
            self.driver.get('https://www.chess.com/play/online')
        
        print("\n" + "="*60)
        print("  CHESS.COM BOT READY")
        print("="*60)
        print("\nPlease:")
        print("  1. Log in to Chess.com if needed")
        print("  2. Navigate to a game (or url already loaded)")
        print("  3. Press ENTER here when game is ready...")
        print("\n" + "="*60)
        
        input()
    
    def detect_game_state(self):
        """Detect the current game state from the webpage."""
        try:
            board_state = self.parser.parse_board_state()
            
            if not board_state or not board_state['pieces']:
                return None
            
            # Determine our color
            self.our_color = board_state['orientation']
            
            # Create internal board representation
            self.board = ChessBoard()
            self.board.grid = [[None for _ in range(8)] for _ in range(8)]
            
            # Place pieces
            for symbol, color, row, col in board_state['pieces']:
                piece_class = self._get_piece_class(symbol)
                self.board.grid[row][col] = piece_class(color, (row, col))
            
            self.board.current_turn = board_state['turn']
            
            # Initialize AI if not already done
            if self.ai is None:
                self.ai = AIPlayer(self.our_color, depth=self.ai_depth)
            
            return board_state
        
        except Exception as e:
            print(f"Error detecting game state: {e}")
            return None
    
    def _get_piece_class(self, symbol):
        """Get piece class from symbol."""
        piece_map = {
            'P': Pawn,
            'N': Knight,
            'B': Bishop,
            'R': Rook,
            'Q': Queen,
            'K': King
        }
        return piece_map.get(symbol, Pawn)
    
    def is_our_turn(self):
        """Check if it's our turn."""
        if not self.board:
            return False
        return self.board.current_turn == self.our_color
    
    def make_move(self, from_pos, to_pos):
        """
        Make a move on Chess.com by dragging the piece.
        
        Args:
            from_pos: (row, col) tuple
            to_pos: (row, col) tuple
        """
        try:
            # Convert positions to Chess.com notation
            orientation = self.our_color
            from_notation = self.parser._position_to_notation(from_pos[0], from_pos[1], orientation)
            to_notation = self.parser._position_to_notation(to_pos[0], to_pos[1], orientation)
            
            print(f"  Executing move: {from_notation} -> {to_notation}")
            
            # Find the PIECE to move (pieces have class like "piece wp square-52")
            piece_element = self.parser.get_piece_at_square(from_notation)
            
            if not piece_element:
                print(f"  Error: Could not find piece at {from_notation}")
                return False
            
            # Get the board element to calculate destination coordinates
            board = self.driver.find_element(By.CSS_SELECTOR, 'wc-chess-board, .board')
            
            # Calculate destination coordinates on the board
            # from_notation is like "e2", we need to get board coordinates for "e3"
            from_file = ord(from_notation[0]) - ord('a')  # 0-7
            from_rank = int(from_notation[1]) - 1  # 0-7
            to_file = ord(to_notation[0]) - ord('a')
            to_rank = int(to_notation[1]) - 1
            
            # Get board size and calculate square size
            board_size = board.size
            square_size = board_size['width'] / 8
            
            # Calculate offset from piece to destination (in pixels)
            file_diff = (to_file - from_file) * square_size
            rank_diff = (from_rank - to_rank) * square_size  # Note: rank increases upward in chess
            
            if self.humanize and self.humanizer:
                # Quick humanized movement (no laggy multi-step animation)
                print("  Moving piece...")
                
                # Small pre-move pause
                time.sleep(random.uniform(0.1, 0.2))
                
                # Single smooth drag (no multi-step animation)
                action = ActionChains(self.driver)
                action.move_to_element(piece_element)
                action.pause(0.05)
                action.click_and_hold()
                action.pause(0.1)
                action.move_by_offset(int(file_diff), int(rank_diff))
                action.pause(0.05)
                action.release()
                action.perform()
                
                self.humanizer.update_last_move_time()
            else:
                # Simple instant drag
                print("  Dragging piece...")
                ActionChains(self.driver).drag_and_drop_by_offset(
                    piece_element, 
                    int(file_diff), 
                    int(rank_diff)
                ).perform()
            
            # Wait for move to register on Chess.com
            time.sleep(0.8)
            
            # DO NOT update internal board - we'll re-parse from DOM for accuracy
            # Internal tracking causes desync issues
            
            return True
        
        except Exception as e:
            print(f"  Error making move: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def play_game(self):
        """Main game loop with humanization."""
        print("\n" + "="*60)
        print(f"  STARTING GAME")
        print(f"  AI Depth: {self.ai_depth}")
        print(f"  Humanization: {'ENABLED' if self.humanize else 'DISABLED'}")
        print("="*60 + "\n")
        
        move_count = 0
        wait_cycles = 0
        
        # Wait for initial board detection
        print("Detecting board state...")
        while not self.our_color:
            state = self.detect_game_state()
            if state and self.our_color:
                print(f"Playing as: {self.our_color.upper()}")
                break
            time.sleep(1)
        
        while True:
            try:
                # Detect current state
                state = self.detect_game_state()
                
                if not state:
                    print("Waiting for game state...")
                    time.sleep(2)
                    continue
                
                # Check if game is over  
                if self._is_game_over():
                    print("\n" + "="*60)
                    print("  GAME OVER")
                    print("="*60)
                    break
                
                # ALWAYS re-parse board from DOM for accurate state
                state = self.detect_game_state()
                
                if not state:
                    print("Unable to parse board state")
                    time.sleep(2)
                    continue
                
                # Check whose turn it is
                if self.board.current_turn == self.our_color:
                    move_count += 1
                    wait_cycles = 0
                    
                    print(f"\n--- Move {move_count} ---")
                    print(f"Our turn ({self.our_color}). Analyzing position...")
                    
                    # Get legal moves
                    legal_moves = self.board.get_legal_moves(self.our_color)
                    
                    if not legal_moves:
                        print("No legal moves available")
                        break
                    
                    # Calculate position complexity
                    complexity = 0.5  # Default
                    if self.humanize and self.humanizer:
                        complexity = self.humanizer.calculate_position_complexity(
                            self.board, legal_moves
                        )
                        print(f"Position complexity: {complexity:.2f}")
                    
                    # Determine thinking time based on complexity
                    if self.humanize and self.humanizer:
                        # Add initial delay after opponent's move
                        initial_delay = self.humanizer.adaptive_delay_after_opponent()
                        print(f"Pausing {initial_delay:.1f}s before analysis...")
                        time.sleep(initial_delay)
                        
                        think_time = self.humanizer.get_thinking_time(
                            complexity, 
                            self.min_think_time, 
                            self.max_think_time
                        )
                        print(f"Thinking for {think_time:.1f} seconds...")
                    else:
                        think_time = random.uniform(self.min_think_time, self.max_think_time)
                        print(f"Thinking for {think_time:.1f} seconds...")
                    
                    time.sleep(think_time)
                    
                    # Decide whether to make suboptimal move (appear human)
                    make_mistake = False
                    if self.humanize and self.humanizer:
                        make_mistake = self.humanizer.should_make_suboptimal_move(complexity)
                    
                    # Get best move(s)
                    if make_mistake:
                        print("🎲 Being 'human' - considering alternative moves...")
                        top_moves = self.ai.get_top_moves(self.board, n=5)
                        
                        if len(top_moves) > 1:
                            # Pick 2nd, 3rd, or 4th best sometimes
                            rank = self.humanizer.get_alternative_move_rank()
                            if rank < len(top_moves):
                                best_move, score = top_moves[rank]
                                print(f"  Selected {rank+1}{'st' if rank==0 else 'nd' if rank==1 else 'rd' if rank==2 else 'th'} best move")
                            else:
                                best_move, score = top_moves[0]
                        else:
                            best_move = top_moves[0][0] if top_moves else None
                    else:
                        best_move = self.ai.get_best_move(self.board)
                    
                    if best_move:
                        from_pos, to_pos = best_move
                        piece = self.board.get_piece(from_pos)
                        
                        print(f"Decision: Move {piece.__class__.__name__} from {from_pos} to {to_pos}")
                        
                        # Execute move with humanization
                        if self.make_move(from_pos, to_pos):
                            print("✓ Move executed successfully")
                        else:
                            print("✗ Failed to execute move")
                            time.sleep(2)
                    else:
                        print("No legal moves available")
                        break
                
                else:
                    # Wait for opponent
                    wait_cycles += 1
                    
                    if wait_cycles % 3 == 0:  # Print less frequently
                        print(f"Waiting for opponent... ({self.board.current_turn}'s turn)")
                    
                    # Do random idle behaviors while waiting (appear human)
                    if self.humanize and self.humanizer and random.random() < 0.2:
                        self.humanizer.random_idle_behavior()
                    
                    time.sleep(3)
            
            except KeyboardInterrupt:
                print("\n\nBot stopped by user")
                break
            
            except Exception as e:
                print(f"Error in game loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(2)
    
    def _is_game_over(self):
        """Check if the game is over."""
        try:
            # Look for game over indicators on Chess.com
            game_over_selectors = [
                '[class*="game-over"]',
                '[class*="game-ended"]',
                'text=Checkmate',
                'text=Draw',
                'text=Stalemate'
            ]
            
            for selector in game_over_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return True
            
            return False
        
        except:
            return False
    
    def close(self):
        """Clean up and close browser."""
        if self.driver:
            self.driver.quit()
