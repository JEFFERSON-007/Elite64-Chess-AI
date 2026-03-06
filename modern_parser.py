"""
Modern Chess.com board parser with multiple detection strategies.
"""

from selenium.webdriver.common.by import By
import time


class ModernBoardParser:
    """
    Updated parser for current Chess.com DOM structure.
    Tries multiple strategies to find pieces.
    """
    
    def __init__(self, driver):
        self.driver = driver
        
    def parse_board_state(self):
        """
        Parse board using multiple strategies.
        
        Returns:
            dict with 'pieces', 'orientation', 'turn' or None
        """
        print("Attempting to parse Chess.com board...")
        
        # Try multiple parsing strategies
        strategies = [
            self._parse_new_chessboard,
            self._parse_legacy_board,
            self._parse_by_coordinates
        ]
        
        for i, strategy in enumerate(strategies, 1):
            try:
                print(f"  Strategy {i}: {strategy.__name__}")
                result = strategy()
                if result and result.get('pieces'):
                    print(f"  ✓ Success! Found {len(result['pieces'])} pieces")
                    return result
            except Exception as e:
                print(f"  ✗ Failed: {e}")
        
        print("  All strategies failed")
        return None
    
    def _parse_new_chessboard(self):
        """Parse using actual Chess.com structure (wc-chess-board)."""
        pieces = []
        
        # Chess.com uses wc-chess-board tag OR .board class
        try:
            board = self.driver.find_element(By.CSS_SELECTOR, 'wc-chess-board, .board')
        except:
            board = self.driver.find_element(By.TAG_NAME, 'body')
        
        orientation = 'black' if 'flipped' in board.get_attribute('class') else 'white'
        
        # Find all piece elements (they have class="piece XX square-YY")
        piece_elements = self.driver.find_elements(By.CSS_SELECTOR, '.piece')
        
        for elem in piece_elements:
            classes = elem.get_attribute('class') or ''
            class_list = classes.split()
            
            # Extract piece code (e.g., "br", "wn", "bp")
            piece_code = None
            square_code = None
            
            for cls in class_list:
                # Piece type: 2 chars, first is color (w/b), second is piece (p/n/b/r/q/k)
                if len(cls) == 2 and cls[0] in 'wb' and cls[1] in 'pnbrqk':
                    piece_code = cls
                # Square position: square-XY where X=file(1-8), Y=rank(1-8)
                elif cls.startswith('square-') and len(cls) == 9:
                    square_code = cls.replace('square-', '')
            
            if not piece_code or not square_code or len(square_code) != 2:
                continue
            
            # Convert Chess.com format to our format
            color = 'white' if piece_code[0] == 'w' else 'black'
            symbol = piece_code[1].upper()
            
            # Convert square-XY notation to row,col
            row, col = self._numeric_square_to_pos(square_code, orientation)
            
            if row is not None and col is not None:
                pieces.append((symbol, color, row, col))
        
        return {
            'pieces': pieces,
            'orientation': orientation,
            'turn': self._detect_turn()
        }
    
    def _parse_legacy_board(self):
        """Parse using older Chess.com structure."""
        pieces = []
        
       # Find board with legacy selectors
        board_elem = self.driver.find_element(By.CSS_SELECTOR, '.board, #board-board, [id*="board"]')
        orientation = self._get_orientation(board_elem)
        
        # Look for pieces
        piece_map = {
            'wp': ('P', 'white'), 'wn': ('N', 'white'), 'wb': ('B', 'white'),
            'wr': ('R', 'white'), 'wq': ('Q', 'white'), 'wk': ('K', 'white'),
            'bp': ('P', 'black'), 'bn': ('N', 'black'), 'bb': ('B', 'black'),
            'br': ('R', 'black'), 'bq': ('Q', 'black'), 'bk': ('K', 'black'),
        }
        
        for piece_code, (symbol, color) in piece_map.items():
            elements = board_elem.find_elements(By.CSS_SELECTOR, f'.{piece_code}')
            
            for elem in elements:
                # Try to find position
                parent = elem.find_element(By.XPATH, '..')
                classes = parent.get_attribute('class') or ''
                
                square = None
                for cls in classes.split():
                    if cls.startswith('square-'):
                        square = cls.replace('square-', '')
                        break
                
                if square:
                    row, col = self._notation_to_pos(square, orientation)
                    if row is not None:
                        pieces.append((symbol, color, row, col))
        
        return {
            'pieces': pieces,
            'orientation': orientation,
            'turn': self._detect_turn()
        }
    
    def _parse_by_coordinates(self):
        """Parse by looking at actual board coordinates."""
        pieces = []
        
        # Find all elements with piece classes
        all_pieces = self.driver.find_elements(By.CSS_SELECTOR, '[class*="piece"]')
        
        board = self.driver.find_element(By.CSS_SELECTOR, 'chess-board, .board')
        orientation = self._get_orientation(board)
        
        for elem in all_pieces:
            classes = elem.get_attribute('class') or ''
            style = elem.get_attribute('style') or ''
            
            # Try to extract piece info from any class that looks like piece code
            piece_info = None
            for cls in classes.split():
                if len(cls) == 2 and cls[0] in 'wb' and cls[1] in 'pnbrqk':
                    color = 'white' if cls[0] == 'w' else 'black'
                    symbol = cls[1].upper()
                    piece_info = (symbol, color)
                    break
            
            if not piece_info:
                continue
            
            # Try to get position from transform or other attributes
            # This is a fallback if square classes don't work
            square = self._extract_square_from_element(elem)
            
            if square:
                row, col = self._notation_to_pos(square, orientation)
                if row is not None:
                    pieces.append((*piece_info, row, col))
        
        return {
            'pieces': pieces,
            'orientation': orientation,
            'turn': self._detect_turn()
        }
    
    def _extract_square_from_element(self, elem):
        """Try multiple ways to extract square notation from element."""
        # Method 1: data attribute
        square = elem.get_attribute('data-square')
        if square:
            return square
        
        # Method 2: class name
        classes = elem.get_attribute('class') or ''
        for cls in classes.split():
            if cls.startswith('square-') and len(cls) == 9:  # "square-e2"
                return cls.replace('square-', '')
        
        # Method 3: parent class
        try:
            parent = elem.find_element(By.XPATH, '..')
            classes = parent.get_attribute('class') or ''
            for cls in classes.split():
                if cls.startswith('square-'):
                    return cls.replace('square-', '')
        except:
            pass
        
        return None
    
    def _numeric_square_to_pos(self, square_code, orientation):
        """
        Convert Chess.com square notation to position.
        Chess.com uses square-XY where X=file(1-8), Y=rank(1-8).
        For example: square-58 = file 5, rank 8 = square e8
        """
        try:
            if not square_code or len(square_code) != 2:
                return (None, None)
            
            file_num = int(square_code[0])  # 1-8
            rank_num = int(square_code[1])  # 1-8
            
            if not (1 <= file_num <= 8 and 1 <= rank_num <= 8):
                return (None, None)
            
            # Convert to 0-indexed
            col = file_num - 1  # file 1 = col 0 (a), file 8 = col 7 (h)
            row = 8 - rank_num  # rank 8 = row 0, rank 1 = row 7
            
            if orientation == 'black':
                row = 7 - row
                col = 7 - col
            
            return (row, col)
        except (ValueError, IndexError):
            return (None, None)
    
    def _notation_to_pos(self, notation, orientation):
        """Convert notation like 'e2' to (row, col)."""
        try:
            if not notation or len(notation) != 2:
                return (None, None)
            
            col = ord(notation[0]) - ord('a')
            row = 8 - int(notation[1])
            
            if not (0 <= row <= 7 and 0 <= col <= 7):
                return (None, None)
            
            if orientation == 'black':
                row = 7 - row
                col = 7 - col
            
            return (row, col)
        except:
            return (None, None)
    
    def _position_to_notation(self, row, col, orientation):
        """
        Convert board position to Chess.com notation.
        Returns notation like 'e2' for standard chess notation.
        """
        try:
            # Undo orientation flip
            if orientation == 'black':
                row = 7 - row
                col = 7 - col
            
            # Convert to standard notation
            file_letter = chr(ord('a') + col)
            rank_number = 8 - row
            
            return f"{file_letter}{rank_number}"
        except:
            return None
    
    def get_orientation(self):
        """Get current board orientation."""
        try:
            board = self.driver.find_element(By.CSS_SELECTOR, 'wc-chess-board, .board')
            return 'black' if 'flipped' in board.get_attribute('class') else 'white'
        except:
            return 'white'
    
    def _get_orientation(self, board_elem):
        """Determine board orientation."""
        try:
            classes = board_elem.get_attribute('class') or ''
            if 'flipped' in classes.lower():
                return 'black'
        except:
            pass
        return 'white'
    
    def _detect_turn(self):
        """Detect whose turn it is."""
        # This is approximate - will be overridden by game state sync
        return 'white'
    
    def get_square_element(self, notation):
        """
        Get DOM element for a square using Chess.com's actual format.
        Chess.com uses numeric squares like square-45 (file 4, rank 5 = d5).
        """
        try:
            # Convert standard notation (e2) to Chess.com's numeric format (square-52)
            if not notation or len(notation) != 2:
                return None
            
            file_letter = notation[0]  # e.g., 'e'
            rank_number = int(notation[1])  # e.g., 2
            
            # Convert to Chess.com's format: file number (1-8), rank number (1-8)
            file_num = ord(file_letter) - ord('a') + 1  # a=1, b=2, ..., h=8
            rank_num = rank_number  # same as input
            
            # Try multiple selector formats
            selectors = [
                f'.square-{file_num}{rank_num}',  # .square-52
                f'[class*="square-{file_num}{rank_num}"]',  # contains square-52
                f'div.square-{file_num}{rank_num}',  # div.square-52
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        return elements[0]
                except:
                    continue
            
            # Fallback: Find all squares and match by position
            all_squares = self.driver.find_elements(By.CSS_SELECTOR, '[class*="square-"]')
            for square in all_squares:
                classes = square.get_attribute('class') or ''
                if f'square-{file_num}{rank_num}' in classes:
                    return square
            
            return None
            
        except Exception as e:
            print(f"Error finding square {notation}: {e}")
            return None
    
    def get_piece_at_square(self, notation):
        """
        Get the piece element at a given square.
        Pieces have classes like "piece wp square-52" for white pawn on e2.
        
        Args:
            notation: Standard notation like 'e2'
        
        Returns:
            WebElement of the piece, or None if not found
        """
        try:
            if not notation or len(notation) != 2:
                return None
            
            # Convert notation to Chess.com's numeric format
            file_letter = notation[0]
            rank_number = int(notation[1])
            file_num = ord(file_letter) - ord('a') + 1  # a=1...h=8
            rank_num = rank_number  # 1-8
            
            # Find piece with this square class
            selector = f'.piece.square-{file_num}{rank_num}'
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            if elements:
                return elements[0]
            
            # Fallback: look for any piece with square-XY in its classes
            all_pieces = self.driver.find_elements(By.CSS_SELECTOR, '.piece')
            for piece in all_pieces:
                classes = piece.get_attribute('class') or ''
                if f'square-{file_num}{rank_num}' in classes:
                    return piece
            
            return None
            
        except Exception as e:
            print(f"Error finding piece at {notation}: {e}")
            return None

