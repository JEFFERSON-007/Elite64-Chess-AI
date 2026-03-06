"""
Parse Chess.com board state from the webpage.
"""


class BoardParser:
    """Parses Chess.com board state from DOM elements."""
    
    # Chess.com piece class names to our notation
    PIECE_MAP = {
        'wp': ('P', 'white'),  # White Pawn
        'wn': ('N', 'white'),  # White Knight
        'wb': ('B', 'white'),  # White Bishop
        'wr': ('R', 'white'),  # White Rook
        'wq': ('Q', 'white'),  # White Queen
        'wk': ('K', 'white'),  # White King
        'bp': ('P', 'black'),  # Black Pawn
        'bn': ('N', 'black'),  # Black Knight
        'bb': ('B', 'black'),  # Black Bishop
        'br': ('R', 'black'),  # Black Rook
        'bq': ('Q', 'black'),  # Black Queen
        'bk': ('K', 'black'),  # Black King
    }
    
    def __init__(self, driver):
        """
        Initialize board parser.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
    
    def get_board_orientation(self):
        """
        Determine if board is flipped (playing as black).
        
        Returns:
            str: 'white' if playing as white, 'black' if playing as black
        """
        try:
            # Check if board is flipped - Chess.com adds 'flipped' class when playing black
            board = self.driver.find_element('css selector', 'chess-board, .board')
            classes = board.get_attribute('class') or ''
            
            if 'flipped' in classes.lower():
                return 'black'
            return 'white'
        except:
            # Default to white if can't determine
            return 'white'
    
    def parse_board_state(self):
        """
        Parse the current board state from Chess.com.
        
        Returns:
            dict: {
                'pieces': [(piece_symbol, color, row, col), ...],
                'orientation': 'white' or 'black',
                'turn': 'white' or 'black'
            }
        """
        pieces = []
        orientation = self.get_board_orientation()
        
        # Chess.com uses different selectors - try multiple approaches
        try:
            # Method 1: Try new Chess.com board structure
            piece_elements = self.driver.find_elements('css selector', '[class*="piece"]')
            
            for element in piece_elements:
                piece_info = self._parse_piece_element(element, orientation)
                if piece_info:
                    symbol, color, row, col = piece_info
                    # Validate position
                    if row is not None and col is not None and 0 <= row <= 7 and 0 <= col <= 7:
                        pieces.append(piece_info)
            
            # If no pieces found, try alternate method
            if not pieces:
                pieces = self._parse_board_alternate(orientation)
        
        except Exception as e:
            print(f"Error parsing board: {e}")
            return None
        
        # Determine whose turn it is
        turn = self._get_current_turn()
        
        return {
            'pieces': pieces,
            'orientation': orientation,
            'turn': turn
        }
    
    def _parse_piece_element(self, element, orientation):
        """Parse a single piece element."""
        try:
            # Get piece class
            classes = element.get_attribute('class') or ''
            
            # Extract piece type from class
            piece_type = None
            for piece_class in classes.split():
                if piece_class.lower() in self.PIECE_MAP:
                    piece_type = piece_class.lower()
                    break
            
            if not piece_type:
                return None
            
            # Get position from data attributes or class
            square = element.get_attribute('data-square') or self._extract_square_from_class(classes)
            
            if not square:
                return None
            
            # Convert Chess.com square notation (e.g., 'e2') to row, col
            row, col = self._notation_to_position(square, orientation)
            
            symbol, color = self.PIECE_MAP[piece_type]
            
            return (symbol, color, row, col)
        
        except Exception as e:
            return None
    
    def _parse_board_alternate(self, orientation):
        """Alternate method to parse board using SVG or other elements."""
        pieces = []
        
        try:
            # Try to find pieces by their specific class patterns
            for piece_code, (symbol, color) in self.PIECE_MAP.items():
                elements = self.driver.find_elements('css selector', f'.{piece_code}')
                
                for element in elements:
                    # Try to extract position
                    classes = element.get_attribute('class') or ''
                    square = self._extract_square_from_class(classes)
                    
                    if square:
                        row, col = self._notation_to_position(square, orientation)
                        if row is not None and col is not None:
                            pieces.append((symbol, color, row, col))
        
        except Exception as e:
            print(f"Alternate parsing failed: {e}")
        
        return pieces
    
    def _extract_square_from_class(self, classes):
        """Extract square notation from class string (e.g., 'square-e2')."""
        for cls in classes.split():
            if 'square-' in cls:
                return cls.split('square-')[1]
        return None
    
    def _notation_to_position(self, notation, orientation):
        """
        Convert Chess.com notation to board position.
        
        Args:
            notation: String like 'e2', 'a8', etc.
            orientation: 'white' or 'black' board orientation
            
        Returns:
            tuple: (row, col) in 0-7 range or (None, None) if invalid
        """
        try:
            if not notation or len(notation) < 2:
                return (None, None)
                
            col = ord(notation[0]) - ord('a')
            row = 8 - int(notation[1])
            
            # Validate bounds before flipping
            if not (0 <= row <= 7 and 0 <= col <= 7):
                return (None, None)
            
            # If playing as black, board is flipped
            if orientation == 'black':
                row = 7 - row
                col = 7 - col
            
            # Validate again after flipping
            if not (0 <= row <= 7 and 0 <= col <= 7):
                return (None, None)
                
            return (row, col)
        except (ValueError, IndexError, TypeError):
            return (None, None)
    
    def _position_to_notation(self, row, col, orientation):
        """
        Convert board position to Chess.com notation.
        
        Args:
            row: 0-7
            col: 0-7
            orientation: 'white' or 'black'
            
        Returns:
            str: Notation like 'e2'
        """
        # If playing as black, flip coordinates
        if orientation == 'black':
            row = 7 - row
            col = 7 - col
        
        file = chr(col + ord('a'))
        rank = str(8 - row)
        
        return f"{file}{rank}"
    
    def _get_current_turn(self):
        """Determine whose turn it is."""
        try:
            # Look for indicators that it's your turn
            # Chess.com shows different indicators depending on game state
            
            # Check for "Your turn" text or similar indicators
            turn_indicators = self.driver.find_elements('css selector', 
                '[class*="turn"], [class*="player-turn"]')
            
            # If we can't determine, check if there's a highlighted player
            # This is a fallback - may need adjustment based on Chess.com's actual DOM
            
            # For now, default to white (will be overridden when we sync with game state)
            return 'white'
        
        except:
            return 'white'
    
    def get_square_element(self, notation):
        """
        Get the DOM element for a square.
        
        Args:
            notation: Square notation like 'e2'
            
        Returns:
            WebElement or None
        """
        try:
            # Try different selectors
            selectors = [
                f'[data-square="{notation}"]',
                f'.square-{notation}',
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements('css selector', selector)
                if elements:
                    return elements[0]
            
            return None
        
        except:
            return None
