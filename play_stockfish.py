"""
Stockfish-powered Chess.com bot - Uses ML engine for instant moves!

WARNING: This violates Chess.com's Terms of Service.
Use at your own risk with a throwaway account.
"""

from chess_com_bot import ChessComBot
from stockfish_player import StockfishPlayer
import sys


def main():
    """Run the Chess.com bot with Stockfish engine."""
    
    print("\n" + "="*70)
    print("  🧠 CHESS.COM BOT - STOCKFISH AI 🧠")
    print("="*70)
    print("""
This bot violates Chess.com's Terms of Service and will likely
result in an account ban. Use ONLY with a throwaway test account.

STOCKFISH MODE: 
  - AI: Stockfish 16 Neural Network (~3200 Elo!)
  - Thinking: INSTANT (0.1 second calculation)
  - Total move time: 0.5-2 seconds
  - Always plays BEST move (no humanization mistakes)
""")
    print("="*70)
    
    response = input("\nType 'I UNDERSTAND' to continue: ")
    
    if response.strip().upper() != "I UNDERSTAND":
        print("Exiting...")
        return
    
    # Stockfish configuration
    print("\n" + "="*70)
    print("  STOCKFISH CONFIGURATION")
    print("="*70)
    
    try:
        skill = input("Stockfish skill level (0-20) [default: 15]: ").strip()
        skill_level = int(skill) if skill else 15
        skill_level = max(0, min(20, skill_level))
    except:
        skill_level = 15
    
    # Display Elo estimate
    elo_map = {
        0: "~800", 5: "~1400", 10: "~1900", 
        15: "~2400", 20: "~3200+"
    }
    closest_elo = elo_map.get(skill_level, "~2000+")
    print(f"Skill: {skill_level}/20 (Estimated Elo: {closest_elo})")
    
    # FAST humanization times
    min_think = 0.5  # Minimal delay
    max_think = 2    # Max 2 seconds total
    
    # Game URL
    print("\nGame URL (optional - press Enter to go to chess.com/play/computer):")
    game_url = input("URL: ").strip() or None
    
    # Initialize bot with Stockfish
    bot = None
    stockfish_ai = None
    
    try:
        print("\n🧠 Initializing Stockfish bot...")
        print(f"   - Stockfish 16 Neural Network")
        print(f"   - Skill Level: {skill_level}/20")
        print(f"   - Move time: {min_think}-{max_think} seconds\n")
        
        # Create Stockfish player
        stockfish_ai = StockfishPlayer(skill_level=skill_level, time_limit=0.1)
        
        # Create bot with Stockfish (humanize movement but no mistakes)
        bot = ChessComBot(
            ai_depth=2,  # Depth is ignored, Stockfish handles it
            min_think_time=min_think,
            max_think_time=max_think,
            humanize=False  # Disable to prevent suboptimal moves - Stockfish always plays best
        )
        
        # Replace the minimax AI with Stockfish
        bot.ai = stockfish_ai
        
        print("\n" + "="*70)
        print("  LAUNCHING BROWSER...")
        print("="*70)
        
        bot.open_chess_com(game_url)
        
        # Start playing
        bot.play_game()
    
    except KeyboardInterrupt:
        print("\n\nBot stopped by user")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if stockfish_ai:
            stockfish_ai.stop_engine()
        if bot:
            print("\nClosing browser...")
            bot.close()
        print("Done.")


if __name__ == '__main__':
    main()
