"""
Fast mode Chess.com bot - Optimized for speed.

WARNING: This violates Chess.com's Terms of Service.
Use at your own risk with a throwaway account.
"""

from chess_com_bot import ChessComBot
import sys


def main():
    """Run the Chess.com bot in FAST mode."""
    
    print("\n" + "="*70)
    print("  ⚡ CHESS.COM BOT - FAST MODE ⚡")
    print("="*70)
    print("""
This bot violates Chess.com's Terms of Service and will likely
result in an account ban. Use ONLY with a throwaway test account.

FAST MODE: 
  - AI Depth: 2 (instant moves, ~1600 Elo)
  - Thinking time: 1-3 seconds
  - Quick piece dragging
""")
    print("="*70)
    
    response = input("\nType 'I UNDERSTAND' to continue: ")
    
    if response.strip().upper() != "I UNDERSTAND":
        print("Exiting...")
        return
    
    # Fast configuration
    ai_depth = 2  # Much faster (500 positions instead of 3724)
    min_think = 1  # Minimum 1 second
    max_think = 3  # Maximum 3 seconds
    
    # Game URL (optional)
    print("\nGame URL (optional - press Enter to go to chess.com/play/computer):")
    game_url = input("URL: ").strip() or None
    
    # Initialize and run bot
    bot = None
    try:
        print("\n⚡ Initializing FAST bot...")
        print(f"   - AI Depth: {ai_depth} (quick calculation)")
        print(f"   - Thinking time: {min_think}-{max_think} seconds")
        print("   - Quick piece movement\n")
        
        bot = ChessComBot(
            ai_depth=ai_depth, 
            min_think_time=min_think, 
            max_think_time=max_think,
            humanize=True  # Still use natural movement, but faster
        )
        
        print("\n" + "="*70)
        print("  LAUNCHING BROWSER...")
        print("="*70)
        
        bot.open_chess_com(game_url)
        
        # Start playing
        bot.play_game()
    
    except KeyboardInterrupt:
        print("\n\nBot stopped")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if bot:
            print("\nClosing browser...")
            bot.close()
        print("Done.")


if __name__ == '__main__':
    main()
