#!/usr/bin/env python3
"""
Quick test script for Chess.com bot.
Tests browser launch and board detection.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from modern_parser import ModernBoardParser
import time

def test_bot():
    """Test browser and parser."""
    
    print("="*60)
    print("CHESS.COM BOT - QUICK TEST")
    print("="*60)
    
    driver = None
    try:
        # Setup browser
        print("\n1. Initializing browser...")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=options)
        print("   ✓ Browser started")
        
        # Open Chess.com
        print("\n2. Opening Chess.com...")
        driver.get('https://www.chess.com/play/computer')
        print("   ✓ Page loaded")
        
        # Wait for user to start game
        print("\n" + "="*60)
        print("Please start a game in the browser")
        print("="*60)
        input("\nPress ENTER when the game board is visible...")
        
        # Test parser
        print("\n3. Testing board parser...")
        parser = ModernBoardParser(driver)
        
        for attempt in range(3):
            print(f"\n   Attempt {attempt + 1}...")
            state = parser.parse_board_state()
            
            if state and state.get('pieces'):
                print(f"   ✓ SUCCESS! Found {len(state['pieces'])} pieces")
                print(f"   Orientation: {state.get('orientation', 'unknown')}")
                print("\n   Pieces found:")
                for symbol, color, row, col in state['pieces'][:10]:
                    print(f"     {color} {symbol} at ({row}, {col})")
                if len(state['pieces']) > 10:
                    print(f"     ... and {len(state['pieces']) - 10} more")
                
                print("\n" + "="*60)
                print("✓ TEST PASSED - Bot should work!")
                print("="*60)
                break
            else:
                print("   ✗ No pieces found, retrying...")
                time.sleep(2)
        else:
            print("\n" + "="*60)
            print("✗ TEST FAILED - Could not parse board")
            print("="*60)
            print("\nThe board structure may have changed.")
            print("Try running: python3 inspect_dom.py")
        
        print("\nPress ENTER to close browser...")
        input()
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed.")

if __name__ == '__main__':
    test_bot()
