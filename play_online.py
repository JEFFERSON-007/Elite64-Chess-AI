"""
Play chess on Chess.com using the AI bot.

WARNING: This violates Chess.com's Terms of Service.
Use at your own risk with a throwaway account.
"""

from chess_com_bot import ChessComBot
import sys


def main():
    """Run the Chess.com bot."""
    
    print("\n" + "="*70)
    print("  ⚠️  CHESS.COM BOT - WARNING ⚠️")
    print("="*70)
    print("""
This bot violates Chess.com's Terms of Service and will likely
result in an account ban. Use ONLY with a throwaway test account.

By continuing, you accept full responsibility for any consequences.
""")
    print("="*70)
    
    response = input("\nType 'I UNDERSTAND' to continue: ")
    
    if response.strip().upper() != "I UNDERSTAND":
        print("Exiting...")
        return
    
    # Configuration
    print("\n" + "="*70)
    print("  BOT CONFIGURATION")
    print("="*70)
    
    try:
        depth = input("AI Depth (1-6) [default: 4]: ").strip()
        ai_depth = int(depth) if depth else 4
        ai_depth = max(1, min(6, ai_depth))
    except:
        ai_depth = 4
    
    try:
        min_time = input("Min thinking time in seconds [default: 3]: ").strip()
        min_think = float(min_time) if min_time else 3
    except:
        min_think = 3
    
    try:
        max_time = input("Max thinking time in seconds [default: 12]: ").strip()
        max_think = float(max_time) if max_time else 12
    except:
        max_think = 12
    
    # Game URL (optional)
    print("\nGame URL (optional - press Enter to go to chess.com/play/online):")
    game_url = input("URL: ").strip() or None
    
    # Initialize and run bot
    bot = None
    try:
        print("\n🤖 Initializing humanized bot...")
        print("   - Natural mouse movements")
        print("   - Adaptive thinking times")
        print("   - Occasional suboptimal moves (appears human)")
        print("   - Realistic behavioral patterns\n")
        
        bot = ChessComBot(
            ai_depth=ai_depth, 
            min_think_time=min_think, 
            max_think_time=max_think,
            humanize=True  # Always use humanization
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
