#!/usr/bin/env python3
"""
Chromium compatibility helper - creates browser with working options.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


def create_chrome_driver(headless=False):
    """
    Create Chrome driver with working options.
    Uses regular Chrome (not snap Chromium).
    
    Args:
        headless: Whether to run in headless mode
    
    Returns:
        WebDriver instance
    """
    options = webdriver.ChromeOptions()
    
    # Essential flags that work
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    if headless:
        options.add_argument('--headless=new')
    
    # Anti-detection
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Install ChromeDriver (will auto-match Chrome version)
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Hide automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


if __name__ == '__main__':
    # Test the driver
    print("Testing Chrome driver...")
    driver = create_chrome_driver(headless=False)
    print("✓ Driver created successfully!")
    driver.get('https://www.chess.com')
    print("✓ Loaded chess.com")
    input("Press ENTER to close...")
    driver.quit()
    print("✓ Test complete!")
