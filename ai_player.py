"""
AI player using minimax with alpha-beta pruning.
"""

from evaluator import Evaluator
import random


class AIPlayer:
    """Chess AI using minimax algorithm with alpha-beta pruning."""
    
    def __init__(self, color, depth=4):
        """
        Initialize AI player.
        
        Args:
            color: 'white' or 'black'
            depth: search depth (number of plies to look ahead)
        """
        self.color = color
        self.depth = depth
        self.evaluator = Evaluator()
        self.nodes_searched = 0
    
    def get_best_move(self, board):
        """
        Get the best move for the current position.
        
        Args:
            board: ChessBoard instance
            
        Returns:
            tuple: ((from_row, from_col), (to_row, to_col)) or None
        """
        self.nodes_searched = 0
        legal_moves = board.get_legal_moves(self.color)
        
        if not legal_moves:
            return None
        
        # Order moves: captures first, then others
        ordered_moves = self._order_moves(board, legal_moves)
        
        best_move = None
        best_score = float('-inf') if self.color == 'white' else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in ordered_moves:
            from_pos, to_pos = move
            
            # Make move on a copy
            temp_board = board.clone()
            temp_board.move_piece(from_pos, to_pos, validate=False)
            
            # Evaluate with minimax
            score = self._minimax(temp_board, self.depth - 1, alpha, beta, 
                                 self.color == 'black')
            
            # Update best move
            if self.color == 'white':
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
        
        print(f"AI searched {self.nodes_searched} positions. Best score: {best_score}")
        return best_move
    
    def get_top_moves(self, board, n=5):
        """
        Get the top N moves for the current position (for humanization).
        
        Args:
            board: ChessBoard instance
            n: Number of top moves to return
            
        Returns:
            list: [(move, score), ...] sorted by score
        """
        self.nodes_searched = 0
        legal_moves = board.get_legal_moves(self.color)
        
        if not legal_moves:
            return []
        
        # Order moves
        ordered_moves = self._order_moves(board, legal_moves)
        
        move_scores = []
        alpha = float('-inf')
        beta = float('inf')
        
        for move in ordered_moves:
            from_pos, to_pos = move
            
            # Make move on a copy
            temp_board = board.clone()
            temp_board.move_piece(from_pos, to_pos, validate=False)
            
            # Evaluate with minimax
            score = self._minimax(temp_board, self.depth - 1, alpha, beta, 
                                 self.color == 'black')
            
            move_scores.append((move, score))
        
        # Sort by score (best first)
        if self.color == 'white':
            move_scores.sort(key=lambda x: x[1], reverse=True)
        else:
            move_scores.sort(key=lambda x: x[1])
        
        print(f"AI searched {self.nodes_searched} positions")
        return move_scores[:n]

    
    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: ChessBoard instance
            depth: remaining depth to search
            alpha: alpha value for pruning
            beta: beta value for pruning
            maximizing: True if maximizing player, False if minimizing
            
        Returns:
            int: evaluation score
        """
        self.nodes_searched += 1
        
        # Base case: depth 0 or game over
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)
        
        color = 'white' if maximizing else 'black'
        legal_moves = board.get_legal_moves(color)
        
        if not legal_moves:
            # No legal moves = checkmate or stalemate
            return self.evaluator.evaluate(board)
        
        # Order moves for better pruning
        ordered_moves = self._order_moves(board, legal_moves)
        
        if maximizing:
            max_eval = float('-inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                temp_board = board.clone()
                temp_board.move_piece(from_pos, to_pos, validate=False)
                
                eval_score = self._minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                temp_board = board.clone()
                temp_board.move_piece(from_pos, to_pos, validate=False)
                
                eval_score = self._minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def _order_moves(self, board, moves):
        """
        Order moves to improve alpha-beta pruning efficiency.
        Prioritizes: captures > checks > other moves
        
        Args:
            board: ChessBoard instance
            moves: list of moves
            
        Returns:
            list: ordered moves
        """
        def move_priority(move):
            from_pos, to_pos = move
            score = 0
            
            # Prioritize captures
            target = board.get_piece(to_pos)
            if target:
                # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
                attacker = board.get_piece(from_pos)
                score += target.value * 10 - attacker.value
            
            # Prioritize center control
            center_bonus = {(3, 3): 20, (3, 4): 20, (4, 3): 20, (4, 4): 20,
                           (2, 2): 10, (2, 5): 10, (5, 2): 10, (5, 5): 10}
            score += center_bonus.get(to_pos, 0)
            
            return score
        
        # Sort moves by priority (highest first)
        sorted_moves = sorted(moves, key=move_priority, reverse=True)
        return sorted_moves
