"""
Humanization features to make the bot appear more human-like.
"""

import random
import time
from selenium.webdriver.common.action_chains import ActionChains


class Humanizer:
    """Makes bot behavior appear more human-like."""
    
    def __init__(self, driver):
        self.driver = driver
        self.last_move_time = time.time()
    
    def get_thinking_time(self, position_complexity, base_min=3, base_max=12):
        """
        Calculate thinking time based on position complexity.
        
        More complex positions = longer thinking time (like humans).
        
        Args:
            position_complexity: 0-1 score of how complex the position is
            base_min: Minimum base thinking time
            base_max: Maximum base thinking time
            
        Returns:
            float: Thinking time in seconds
        """
        # Humans think longer in complex positions
        complexity_factor = 1 + (position_complexity * 2)
        
        min_time = base_min * complexity_factor
        max_time = base_max * complexity_factor
        
        # Add some randomness
        think_time = random.uniform(min_time, max_time)
        
        # Occasionally have "long thinks" (humans sometimes take extra time)
        if random.random() < 0.15:  # 15% chance
            think_time *= random.uniform(1.5, 2.5)
        
        # Occasionally have "quick moves" in obvious positions
        if position_complexity < 0.2 and random.random() < 0.3:
            think_time *= random.uniform(0.3, 0.6)
        
        return think_time
    
    def calculate_position_complexity(self, board, legal_moves):
        """
        Estimate position complexity (0-1 scale).
        
        Factors:
        - Number of legal moves
        - Pieces in contact
        - Checks/threats
        
        Returns:
            float: 0-1 complexity score
        """
        complexity = 0.0
        
        # More legal moves = more complex
        move_count = len(legal_moves)
        complexity += min(move_count / 40, 1.0) * 0.4
        
        # Count pieces (more pieces = more complex early game)
        piece_count = sum(1 for row in board.grid for piece in row if piece)
        complexity += min(piece_count / 32, 1.0) * 0.2
        
        # Check if position has checks or captures available
        has_tactics = any(board.get_piece(to_pos) for from_pos, to_pos in legal_moves)
        if has_tactics:
            complexity += 0.3
        
        # Random factor
        complexity += random.uniform(0, 0.1)
        
        return min(complexity, 1.0)
    
    def should_make_suboptimal_move(self, position_complexity):
        """
        Decide if we should intentionally not play the best move.
        
        Humans don't always play perfectly. Sometimes make the 2nd or 3rd best move.
        
        Args:
            position_complexity: How complex the position is
            
        Returns:
            bool: True if should play suboptimal move
        """
        # More likely to make "mistakes" in complex positions
        mistake_chance = 0.05 + (position_complexity * 0.10)  # 5-15% chance
        
        return random.random() < mistake_chance
    
    def get_alternative_move_rank(self):
        """
        If making suboptimal move, which rank to choose.
        
        Returns:
            int: 1 (2nd best), 2 (3rd best), rarely 3 (4th best)
        """
        # Weight towards 2nd best (more realistic)
        choices = [1, 1, 1, 2, 2, 3]  # Heavily favor 2nd best
        return random.choice(choices)
    
    def natural_mouse_movement(self, element, hover_first=True):
        """
        Move mouse to element in a more natural way.
        
        Args:
            element: Target element
            hover_first: If True, hover near element before clicking
        """
        actions = ActionChains(self.driver)
        
        if hover_first and random.random() < 0.7:  # 70% of the time hover first
            # Move near the element first (humans don't click instantly)
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)
            
            actions.move_to_element_with_offset(element, offset_x, offset_y)
            actions.pause(random.uniform(0.1, 0.3))
        
        # Move to the actual element
        actions.move_to_element(element)
        actions.pause(random.uniform(0.05, 0.15))
        
        # Click
        actions.click()
        actions.perform()
    
    def pre_move_hesitation(self):
        """
        Add realistic hesitation before making a move.
        
        Humans sometimes hover, move cursor away, come back, etc.
        """
        hesitation_type = random.random()
        
        if hesitation_type < 0.2:  # 20% - quick move
            time.sleep(random.uniform(0.1, 0.3))
        
        elif hesitation_type < 0.6:  # 40% - normal pause
            time.sleep(random.uniform(0.3, 0.8))
        
        else:  # 40% - longer pause (reconsidering)
            time.sleep(random.uniform(0.8, 2.0))
            
            # Sometimes move mouse away and back (like reconsidering)
            if random.random() < 0.3:
                actions = ActionChains(self.driver)
                actions.move_by_offset(random.randint(-100, 100), random.randint(-100, 100))
                actions.perform()
                time.sleep(random.uniform(0.2, 0.5))
    
    def post_move_behavior(self):
        """
        Natural behavior after making a move.
        
        Humans sometimes move cursor away, scroll, etc.
        """
        behavior = random.random()
        
        if behavior < 0.3:  # 30% - move mouse away from board
            actions = ActionChains(self.driver)
            actions.move_by_offset(random.randint(100, 300), random.randint(-100, 100))
            actions.perform()
        
        elif behavior < 0.5:  # 20% - small cursor movement
            actions = ActionChains(self.driver)
            actions.move_by_offset(random.randint(-50, 50), random.randint(-50, 50))
            actions.perform()
        
        # Rest 50% - do nothing (stay on board)
    
    def random_idle_behavior(self):
        """
        Occasionally do random things while waiting for opponent.
        
        Humans don't just sit still - they move mouse, switch tabs, etc.
        """
        if random.random() < 0.3:  # 30% chance
            action_type = random.random()
            
            if action_type < 0.5:  # Move mouse randomly
                actions = ActionChains(self.driver)
                actions.move_by_offset(random.randint(-200, 200), random.randint(-200, 200))
                actions.perform()
            
            elif action_type < 0.7:  # Scroll page slightly
                self.driver.execute_script(f"window.scrollBy(0, {random.randint(-50, 50)})")
            
            # Rest - do nothing
    
    def adaptive_delay_after_opponent(self):
        """
        Delay after opponent moves (humans don't respond instantly).
        
        Returns:
            float: Delay in seconds
        """
        time_since_opponent = time.time() - self.last_move_time
        
        # If opponent moved quickly, we might respond quickly too
        # If opponent took long, we might also take longer
        
        if time_since_opponent < 3:  # Opponent moved fast
            delay = random.uniform(1.5, 4.0)
        elif time_since_opponent < 10:  # Normal pace
            delay = random.uniform(2.0, 5.0)
        else:  # Opponent took a while
            delay = random.uniform(3.0, 8.0)
        
        return delay
    
    def update_last_move_time(self):
        """Update the timestamp of our last move."""
        self.last_move_time = time.time()
