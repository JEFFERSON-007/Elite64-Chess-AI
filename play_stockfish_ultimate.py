"""
ULTIMATE STOCKFISH BOT - Maximum Strength, Multi-Game Mode

This bot plays at near-GM level (~2600+ Elo) and can play multiple games
in a row without restarting the browser.

WARNING: This violates Chess.com's Terms of Service.
Use at your own risk with a throwaway account.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

from modern_parser import ModernBoardParser
from chrome_helper import create_chrome_driver
from stockfish_player import StockfishPlayer
from ai_player import AIPlayer


def detect_game_result(driver):
    """
    Detect if game is over and return result.
    Returns: ('win', 'loss', 'draw', None)
    """
    try:
        # Check for game over modal or indicators
        selectors = [
            '[class*="game-over"]',
            '[class*="game-ended"]',
            '.modal-game-over-content',
            '[data-cy="game-over-modal"]'
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Try to extract result text
                    text = elements[0].text.lower()
                    if 'won' in text or 'victory' in text or 'checkmate' in text and 'you' in text:
                        return 'win'
                    elif 'lost' in text or 'defeat' in text:
                        return 'loss'
                    elif 'draw' in text or 'stalemate' in text:
                        return 'draw'
                    else:
                        return 'ended'  # Game over but unclear result
            except:
                continue
        
        return None
    except:
        return None


def click_new_game(driver):
    """
    Click the 'New Game' or 'Play Again' button.
    Returns True if successful, False otherwise.
    """
    try:
        # Try different selectors for new game button
        selectors = [
            'button[data-cy="new-game-button"]',
            'button:contains("New Game")',
            'button:contains("Play Again")',
            'a[href*="/play/computer"]',
            '.ui_v5-button-component:contains("New")',
        ]
        
        # Also try clicking rematch/new game in modal
        for selector in selectors:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                for button in buttons:
                    if button.is_displayed():
                        button.click()
                        print("  ✓ Clicked new game button")
                        time.sleep(2)
                        return True
            except:
                continue
        
        # If no button found, try navigating to computer page
        print("  → No new game button found, refreshing page...")
        driver.get("https://www.chess.com/play/computer")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"  ⚠ Error clicking new game: {e}")
        return False


def main():
    """Run the ultimate Chess.com bot."""
    print("\n" + "="*70)
    print("  ♟️  ULTIMATE STOCKFISH BOT - MAXIMUM STRENGTH ♟️")
    print("="*70)
    print("\nThis bot violates Chess.com's Terms of Service and will likely")
    print("result in an account ban. Use ONLY with a throwaway test account.")
    print("\nULTIMATE MODE:")
    print("  - AI: Stockfish 16 NNUE (~2600+ Elo)")
    print("  - Thinking: 1-2 seconds per move (deeper analysis)")
    print("  - Multi-game: Plays continuously until stopped")
    print("  - Win rate vs 1200: 99.9%")
    print("\n" + "="*70)
    
    confirm = input("\nType 'I UNDERSTAND' to continue: ")
    if confirm != "I UNDERSTAND":
        print("Aborted.")
        return
    
    print("\n" + "="*70)
    print("  CONFIGURATION")
    print("="*70)
    
    # Get Stockfish skill level
    skill_input = input("Stockfish skill level (0-20) [default: 20]: ").strip()
    skill = int(skill_input) if skill_input else 20
    skill = max(0, min(20, skill))
    
    # Get thinking time
    time_input = input("Thinking time per move (0.1-5.0s) [default: 1.5]: ").strip()
    think_time = float(time_input) if time_input else 1.5
    think_time = max(0.1, min(5.0, think_time))
    
    # Estimate Elo
    elo_estimate = 1500 + (skill * 85) + int(think_time * 100)
    print(f"\n✓ Skill: {skill}/20")
    print(f"✓ Think time: {think_time}s")
    print(f"✓ Estimated Elo: ~{elo_estimate}+")
    
    # Get game URL
    print("\nGame URL [press Enter for chess.com/play/computer]:")
    url = input("URL: ").strip()
    if not url:
        url = "https://www.chess.com/play/computer"
    
    print("\n♟️  Initializing Ultimate Bot...")
    print(f"   - Stockfish 16 Neural Network")
    print(f"   - Skill Level: {skill}/20")
    print(f"   - Deep analysis: {think_time}s per move")
    print(f"   - Multi-game mode enabled")
    
    # Initialize browser
    print("\nInitializing browser...")
    driver = create_chrome_driver(headless=False)
    print("✓ Browser initialized successfully")
    
    # Initialize Stockfish
    stockfish_ai = StockfishPlayer(skill_level=skill, time_limit=think_time)
    fallback_ai = None
    
    # Open Chess.com
    driver.get(url)
    
    print("\n" + "="*60)
    print("  CHESS.COM BOT READY")
    print("="*60)
    print("\nPlease:")
    print("  1. Log in to Chess.com if needed")
    print("  2. Start a game against computer")
    print("  3. Press ENTER here when ready...")
    print("\n" + "="*60)
    
    input()
    
    # Game counter
    games_played = 0
    wins = 0
    losses = 0
    draws = 0
    
    try:
        while True:
            games_played += 1
            using_stockfish = True
            
            print("\n" + "="*70)
            print(f"  GAME {games_played}")
            print(f"  Record: {wins}W - {losses}L - {draws}D")
            print("="*70 + "\n")
            
            # Initialize parser
            parser = ModernBoardParser(driver)
            our_color = None
            move_count = 0
            
            # Wait for initial board detection
            print("Detecting board state...")
            for attempt in range(10):
                state = parser.parse_board_state()
                if state and state['pieces']:
                    our_color = state['orientation']
                    print(f"✓ Playing as: {our_color.upper()}")
                    
                    # Initialize fallback AI if not already
                    if fallback_ai is None:
                        fallback_ai = AIPlayer(our_color, depth=4)  # Deeper fallback
                    break
                time.sleep(1)
            
            if not our_color:
                print("⚠ Could not detect board. Skipping game...")
                continue
            
            # Main game loop
            game_result = None
            last_parse_time = 0
            
            while not game_result:
                # Check if game is over
                game_result = detect_game_result(driver)
                if game_result:
                    break
                
                # Parse current board state (throttle to reduce spam)
                current_time = time.time()
                if current_time - last_parse_time < 2:
                    time.sleep(0.5)
                    continue
                
                last_parse_time = current_time
                state = parser.parse_board_state()
                
                if not state or not state['pieces']:
                    time.sleep(2)
                    continue
                
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
                    
                    # Display board state
                    print("\n" + "-"*30)
                    print(f" Current Board State (Turn: {board.current_turn.upper()})")
                    print("-"*30)
                    board.display()
                    
                    print(f"\n--- Move {move_count} ---")
                    
                    # Get legal moves
                    legal_moves = board.get_legal_moves(our_color)
                    
                    if not legal_moves:
                        print("No legal moves available - game over")
                        game_result = 'ended'
                        break
                    
                    # Thinking delay (humanized)
                    delay = random.uniform(0.3, 1.2)
                    print(f"Analyzing... ({delay:.1f}s)")
                    time.sleep(delay)
                    
                    # Get best move from Stockfish or fallback
                    best_move = None
                    
                    if using_stockfish:
                        best_move = stockfish_ai.get_best_move(board)
                        
                        # Check if Stockfish crashed - RESTART IT!
                        if best_move is None and stockfish_ai.engine_crashed:
                            print("\n" + "!"*70)
                            print("  ⚠️  STOCKFISH CRASHED - RESTARTING ENGINE")
                            print("!"*70)
                            
                            # Restart Stockfish engine
                            stockfish_ai.restart_engine()
                            
                            # Try again with restarted engine
                            best_move = stockfish_ai.get_best_move(board)
                            
                            if best_move:
                                print("  ✅ Stockfish recovered! Continuing with full strength...")
                            else:
                                # If restart failed, use fallback
                                print("  ⚠️  Restart failed - using fallback AI")
                                using_stockfish = False
                    
                    # Use fallback only if Stockfish completely failed
                    if best_move is None:
                        best_move = fallback_ai.get_best_move(board)
                    
                    if not best_move:
                        print("No valid moves - game over")
                        game_result = 'ended'
                        break
                    
                    from_pos, to_pos = best_move
                    piece = board.get_piece(from_pos)
                    
                    print(f"→ {piece.__class__.__name__}: {from_pos} → {to_pos}")
                    
                    # Execute move
                    from_notation = parser._position_to_notation(from_pos[0], from_pos[1], our_color)
                    to_notation = parser._position_to_notation(to_pos[0], to_pos[1], our_color)
                    
                    # Find piece and drag it
                    piece_element = parser.get_piece_at_square(from_notation)
                    
                    if not piece_element:
                        print(f"  ⚠ Could not find piece at {from_notation}")
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
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(driver).drag_and_drop_by_offset(
                        piece_element,
                        int(file_diff),
                        int(rank_diff)
                    ).perform()
                    
                    # Handle pawn promotion
                    is_pawn = piece.__class__.__name__ == 'Pawn'
                    is_promotion_rank = (our_color == 'white' and to_pos[0] == 0) or \
                                       (our_color == 'black' and to_pos[0] == 7)
                    
                    if is_pawn and is_promotion_rank:
                        print("   👑 PAWN PROMOTION! Selecting Queen...")
                        time.sleep(0.5)  # Wait for promotion dialog
                        
                        # Try to click Queen promotion button
                        try:
                            # Chess.com shows promotion options, click Queen (usually the first/default)
                            queen_selectors = [
                                '.promotion-piece.wq',  # White queen
                                '.promotion-piece.bq',  # Black queen
                                '[class*="promotion"][class*="queen"]',
                                '.promotion-piece:first-child',  # Default is usually Queen
                            ]
                            
                            for selector in queen_selectors:
                                try:
                                    queen_btn = driver.find_element(By.CSS_SELECTOR, selector)
                                    if queen_btn.is_displayed():
                                        queen_btn.click()
                                        print("   ✓ Promoted to QUEEN!")
                                        break
                                except:
                                    continue
                        except Exception as e:
                            print(f"   ⚠️ Promotion click failed (may auto-promote): {e}")
                    
                    time.sleep(0.5)
                
                else:
                    # Wait for opponent
                    if move_count == 0:
                        print(f"  Waiting for {('white' if our_color == 'black' else 'black').upper()} to move first...")
                    time.sleep(2)
            
            # Game ended - show result
            print("\n" + "="*70)
            print("  GAME OVER")
            print("="*70)
            
            # Try to detect actual result
            time.sleep(2)
            final_result = detect_game_result(driver)
            
            if final_result == 'win':
                print("  🏆 VICTORY!")
                wins += 1
            elif final_result == 'loss':
                print("  ❌ Defeat")
                losses += 1
            elif final_result == 'draw':
                print("  🤝 Draw")
                draws += 1
            else:
                print("  ⚪ Result unknown")
            
            print(f"\n  Total Record: {wins}W - {losses}L - {draws}D")
            print("="*70)
            
            # Ask to play again
            print("\n" + "="*60)
            response = input("Play another game? (y/n) [default: y]: ").strip().lower()
            print("="*60)
            
            if response == 'n' or response == 'no':
                print("\n✓ Stopping bot...")
                break
            
            # Click new game button
            print("\nStarting new game...")
            if not click_new_game(driver):
                print("⚠ Could not start new game. Please start manually and press Enter...")
                input()
            
            time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Bot stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "="*70)
        print(f"  FINAL STATISTICS")
        print(f"  Games Played: {games_played}")
        print(f"  Record: {wins}W - {losses}L - {draws}D")
        if games_played > 0:
            win_rate = (wins / games_played) * 100
            print(f"  Win Rate: {win_rate:.1f}%")
        print("="*70)
        
        print("\nClosing browser...")
        stockfish_ai.stop_engine()
        driver.quit()
        print("Done. Thanks for using Ultimate Stockfish Bot! 👑")


if __name__ == "__main__":
    main()
