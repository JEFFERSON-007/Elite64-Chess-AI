#!/usr/bin/env python3
"""
Quick debug script to find out what square elements actually look like on Chess.com.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from chrome_helper import create_chrome_driver
import time

driver = create_chrome_driver()

try:
    print("Opening Chess.com...")
    driver.get('https://www.chess.com/play/computer')
    
    print("\nWait for game to load, then press Enter...")
    input()
    
    print("\nSearching for square elements...")
    
    # Try to find squares (not pieces)
    print("\n1. Looking for all elements with 'square' in class:")
    all_with_square = driver.find_elements(By.CSS_SELECTOR, '[class*="square"]')
    print(f"   Found {len(all_with_square)} elements")
    
    # Look at first few
    for i, elem in enumerate(all_with_square[:10]):
        classes = elem.get_attribute('class')
        tag = elem.tag_name
        print(f"   {i+1}. {tag}.{classes}")
    
    # Try finding specific square
    print("\n2. Trying to find square for e2 (should be square-52):")
    selectors_to_try = [
        '.square-52',
        '[class*="square-52"]',
        'div.square-52',
        '[data-square="52"]',
        '[data-square="e2"]',
    ]
    
    for selector in selectors_to_try:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)  
            print(f"   {selector}: {len(elements)} found")
            if elements:
                print(f"      Classes: {elements[0].get_attribute('class')}")
        except Exception as e:
            print(f"   {selector}: Error - {e}")
    
    # Look at the board structure
    print("\n3. Board structure:")
    board = driver.find_element(By.CSS_SELECTOR, 'wc-chess-board, .board')
    print(f"   Board tag: {board.tag_name}")
    print(f"   Board classes: {board.get_attribute('class')}")
    
    # Look for children
    children = board.find_elements(By.CSS_SELECTOR, '*')
    print(f"   Direct children: {len(children)}")
    for i, child in enumerate(children[:5]):
        print(f"   {i+1}. {child.tag_name}.{child.get_attribute('class')}")
    
    print("\nDone! Press Enter to close...")
    input()
    
finally:
    driver.quit()
