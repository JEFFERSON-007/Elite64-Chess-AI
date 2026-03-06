"""
Inspect Chess.com DOM structure to understand how to parse it.
Run this first to see what the actual structure looks like.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def inspect_chess_com():
    """Open Chess.com and print DOM structure."""
    
    print("Initializing browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("\nOpening Chess.com...")
        driver.get('https://www.chess.com/play/computer')
        
        print("\n" + "="*60)
        print("BROWSER OPENED - Please start a game")
        print("="*60)
        input("\nPress ENTER when the game board is visible...")
        
        print("\n" + "="*60)
        print("INSPECTING DOM STRUCTURE")
        print("="*60)
        
        # Find board element
        print("\n1. Looking for board container...")
        board_selectors = ['chess-board', '.board', '[class*="board"]']
        for selector in board_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"   ✓ Found {len(elements)} elements with selector: {selector}")
                    board = elements[0]
                    print(f"   Classes: {board.get_attribute('class')}")
                    print(f"   Tag: {board.tag_name}")
            except:
                pass
        
        # Find all piece elements
        print("\n2. Looking for piece elements...")
        piece_selectors = [
            '[class*="piece"]',
            '[class*="chess"]',
            '.piece',
            'chess-board [class*="square"]'
        ]
        
        for selector in piece_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\n   Selector: {selector}")
                    print(f"   Found {len(elements)} elements")
                    
                    # Show first few elements
                    for i, elem in enumerate(elements[:5]):
                        classes = elem.get_attribute('class')
                        tag = elem.tag_name
                        data_square = elem.get_attribute('data-square')
                        style = elem.get_attribute('style')
                        
                        print(f"\n   Element {i+1}:")
                        print(f"     Tag: {tag}")
                        print(f"     Classes: {classes}")
                        if data_square:
                            print(f"     data-square: {data_square}")
                        if style and len(style) < 200:
                            print(f"     Style: {style[:100]}...")
            except Exception as e:
                print(f"   Error with {selector}: {e}")
        
        # Get page source sample
        print("\n3. Page source sample (first 2000 chars)...")
        source = driver.page_source[:2000]
        print(source)
        
        print("\n" + "="*60)
        print("INSPECTION COMPLETE")
        print("="*60)
        print("\nPress ENTER to close browser...")
        input()
        
    finally:
        driver.quit()

if __name__ == '__main__':
    inspect_chess_com()
