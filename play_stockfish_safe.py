"""
Stockfish bot for Chess.com - SAFE VERSION with fallback AI.

WARNING: This violates Chess.com's Terms of Service.
Use at your own risk with a throwaway account.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

from modern_parser import ModernBoardParser
from chrome_helper import create_chrome_driver
from stockfish_player import StockfishPlayer
from ai_player import AIPlayer


def main():
    """Run the Chess.com bot with Stockfish and fallback AI."""
    print("\n" + "="*70)
    print("  🧠 CHESS.COM BOT - STOCKFISH AI (ULTRA STRONG) 🧠")
    print("="*70)
    print("\nThis bot violates Chess.com's Terms of Service and will likely")
    print("result in an account ban. Use ONLY with a throwaway test account.")
    print("\nSTOCKFISH MODE:")
    print("  - AI: Stockfish 16 (~2400-3200 Elo)")
    print("  - Speed: 0.5 seconds per move")
    print("  - Win rate vs 1200: 99%+")
    print("\n" + "="*70)
    
    confirm = input("\nType 'I UNDERSTAND' to continue: ")
    if confirm != "I UNDERSTAND":
        print("Aborted.")
        return
    
    print("\n" + "="*70)
    print("  STOCKFISH CONFIGURATION")
    print("="*70)
    
    # Get Stockfish skill level
    skill_input = input("Stockfish skill level (0-20) [default: 20]: ").strip()
    skill = int(skill_input) if skill_input else 20
    skill = max(0, min(20, skill))  # Clamp to 0-20
    
    # Estimate Elo
    elo_estimate = 1500 + (skill * 85)
    print(f"Skill: {skill}/20 (Estimated Elo: ~{elo_estimate}+)")
    
    # Get game URL
    print("\nGame URL (optional - press Enter to go to chess.com/play/computer):")
    url = input("URL: ").strip()
    if not url:
        url = "https://www.chess.com/play/computer"
    
    print("\n🧠 Initializing Stockfish bot...")
    print(f"   - Stockfish 16 Neural Network")
    print(f"   - Skill Level: {skill}/20")
    print(f"   - Move time: 0.5 seconds")
    
    # Initialize browser
    print("\nInitializing browser...")
    driver = create_chrome_driver(headless=False)
    print("✓ Browser initialized successfully")
    
    # Initialize Stockfish
    stockfish_ai = StockfishPlayer(skill_level=skill, time_limit=0.5)
    fallback_ai = None
    using_stockfish = True
    
    # Open Chess.com
    driver.get(url)
    
    print("\n" + "="*60)
    print("  CHESS.COM BOT READY")
    print("="*60)
    print("\nPlease:")
    print("  1. Log in to Chess.com if needed")
    print("  2. Navigate to a game (or url already loaded)")
    print("  3. Press ENTER here when game is ready...")
    print("\n" + "="*60)
    
    input()
    
    # Initialize parser
    parser = ModernBoardParser(driver)
    our_color = None
    board = None
    move_count = 0
    
    try:
        print("\n" + "="*60)
        print(f"  STARTING GAME")
        print(f"  Stockfish Skill: {skill}/20")
        print("="*60 + "\n")
        
        # Wait for initial board detection
        print("Detecting board state...")
        while not our_color:
            state = parser.parse_board_state()
            if state and state['pieces']:
                our_color = state['orientation']
                print(f"Playing as: {our_color.upper()}")
                
                # Initialize fallback AI with our color
                fallback_ai = AIPlayer(our_color, depth=3)
                break
            time.sleep(1)
        
        # Main game loop
        while True:
            # Parse current board state
            state = parser.parse_board_state()
            
            if not state or not state['pieces']:
                print("Waiting for game state...")
                time.sleep(2)
                continue
            
            # Check if game is over
            try:
                game_over_selectors = [
                    '[class*="game-over"]',
                    '[class*="game-ended"]',
                ]
                for selector in game_over_selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print("\n" + "="*60)
                        print("  GAME OVER")
                        print("="*60)
                        raise KeyboardInterrupt
            except:
                pass
            
            # Check if it's our turn
            if state['turn'] == our_color:
                move_count += 1
                
                # Convert state to board object
                from chess_engine import ChessBoard
                from pieces import Pawn, Knight, Bishop, Rook, Queen, King
                
                board = ChessBoard()
                board.grid = [[None for _ in range(8)] for _ in range(8)]
                
                piece_map = {'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King}
                
                for symbol, color, row, col in state['pieces']:
                    piece_class = piece_map.get(symbol, Pawn)
                    board.grid[row][col] = piece_class(color, (row, col))
                
                board.current_turn = state['turn']
                
                print(f"\n--- Move {move_count} ---")
                print(f"Our turn ({our_color}). Analyzing position...")
                
                # Get legal moves
                legal_moves = board.get_legal_moves(our_color)
                
                if not legal_moves:
                    print("No legal moves available")
                    break
                
                # Thinking time
                think_time = random.uniform(0.5, 2.0)
                print(f"Thinking for {think_time:.1f} seconds...")
                time.sleep(think_time)
                
                # Get best move from Stockfish or fallback
                best_move = None
                
                if using_stockfish:
                    best_move = stockfish_ai.get_best_move(board)
                    
                    # Check if Stockfish crashed (one-time message)
                    if best_move is None and stockfish_ai.engine_crashed:
                        print("\n" + "!"*70)
                        print("  ⚠️  STOCKFISH CRASHED - SWITCHING TO FALLBACK AI")
                        print(f"  📊 Continuing with Minimax depth 3 (~1900 Elo)")
                        print(f"  ✅ Game will continue to completion")
                        print("!"*70 + "\n")
                        using_stockfish = False
                
                # Use fallback if Stockfish not working
                if best_move is None:
                    best_move = fallback_ai.get_best_move(board)
                
                if not best_move:
                    print("No legal moves available")
                    break
                
                from_pos, to_pos = best_move
                piece = board.get_piece(from_pos)
                
                print(f"Decision: Move {piece.__class__.__name__} from {from_pos} to {to_pos}")
                
                # Execute move
                from_notation = parser._position_to_notation(from_pos[0], from_pos[1], our_color)
                to_notation = parser._position_to_notation(to_pos[0], to_pos[1], our_color)
                
                print(f"  Executing move: {from_notation} -> {to_notation}")
                
                # Find piece and drag it
                piece_element = parser.get_piece_at_square(from_notation)
                
                if not piece_element:
                    print(f"  Error: Could not find piece at {from_notation}")
                    time.sleep(2)
                    continue
                
                # Calculate drag offset
                board_elem = driver.find_element(By.CSS_SELECTOR, 'wc-chess-board, .board')
                board_size = board_elem.size
                square_size = board_size['width'] / 8
                
                from_file = ord(from_notation[0]) - ord('a')
                from_rank = int(from_notation[1]) - 1
                to_file = ord(to_notation[0]) - ord('a')
                to_rank = int(to_notation[1]) - 1
                
                file_diff = (to_file - from_file) * square_size
                rank_diff = (from_rank - to_rank) * square_size
                
                # Drag piece
                print("  Dragging piece...")
                from selenium.webdriver.common.action_chains import ActionChains
                ActionChains(driver).drag_and_drop_by_offset(
                    piece_element,
                    int(file_diff),
                    int(rank_diff)
                ).perform()
                
                print("✓ Move executed successfully")
                time.sleep(0.8)
            
            else:
                # Wait for opponent
                time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n\nBot stopped by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nClosing browser...")
        stockfish_ai.stop_engine()
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    main()
