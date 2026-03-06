# Project Architecture

## System Overview

Elite64 Chess AI is a modular chess engine with Chess.com integration. The system is divided into core chess logic and bot automation layers.

```
┌─────────────────────────────────────────┐
│     Chess.com Bot Layer                 │
│  (play_online.py, chess_com_bot.py)     │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│     Browser Automation Layer            │
│  (chrome_helper.py, board_parser.py)    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│     Core Chess Engine                   │
│  (game.py, ai_player.py, evaluator.py)  │
└─────────────────────────────────────────┘
```

## Core Modules

### 1. **game.py** - Chess Rules Engine
- Implements complete chess rules
- Supports all legal moves (castling, en passant, promotion)
- Move validation and board state management
- Move generation (pseudo-legal and legal moves)

### 2. **pieces.py** - Piece Definitions
- Piece class hierarchy
- Piece movement rules
- Piece value constants

### 3. **ai_player.py** - AI Decision Making
- Minimax algorithm with alpha-beta pruning
- Configurable search depth
- Move ranking and selection
- Performance optimizations (move ordering, transposition tables)

### 4. **evaluator.py** - Position Evaluation
Evaluates board positions using:
- **Material Score**: Piece values (Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9)
- **Position Score**: Piece placement quality
- **Mobility Score**: Number of available moves
- **Tactical Patterns**: Captures, checks, threats

Score calculation:
```
Position Value = Material + Position Bonus + Mobility Factor
```

### 5. **humanizer.py** - Humanization Features
Applies advanced techniques to avoid detection:
- **Adaptive Thinking Time**: Variable delays based on position complexity
- **Occasional Blunders**: Plays 2nd-4th best moves sometimes
- **Natural Mouse Movement**: Curved paths, realistic pauses
- **Behavioral Patterns**: Idle animations, post-move behavior

See [HUMANIZATION.md](HUMANIZATION.md) for detailed features.

## Bot Integration Modules

### 6. **board_parser.py** - Chess.com Board Recognition
- Parses Chess.com DOM structure
- Extracts board state from page
- Identifies pieces and positions
- Handles board orientation detection

### 7. **chrome_helper.py** - Browser Automation
- WebDriver management
- Element clicking and interaction
- Screenshot capture
- Page waiting and synchronization

### 8. **chess_com_bot.py** - Bot Controller
- Orchestrates board parsing and AI
- Handles game loop
- Converts AI moves to board actions
- Integrates humanization

## Stockfish Integration

### 9. **stockfish_player.py** - External Engine Wrapper
- Uses Stockfish chess engine
- Provides strongest play option
- Fallback when builtin AI is too slow

## Gameplay Modes

### Local Play
- `test_chess.py`: Interactive human vs AI
- `play_fast.py`: Fast 1-2 move lookahead
- `play_maximum_strength.py`: Deep 6+ move analysis

### Online Play
- `play_online.py`: Standard Chess.com bot
- `play_stockfish_ultimate.py`: Stockfish-powered bot
- `play_stockfish_safe.py`: Rate-limited Stockfish

## Data Flow - Online Game Example

```
1. Chrome opens Chess.com
   │
2. board_parser.py reads DOM → 2D board array
   │
3. game.py converts to Game object
   │
4. ai_player.py runs minimax search
   │
5. evaluator.py scores positions
   │
6. humanizer.py adds delays & variations
   │
7. chess_com_bot.py converts move to clicks
   │
8. chrome_helper.py performs drag/click actions
   │
9. Return to step 2 (repeat for opponent's move)
```

## Algorithm Details

### Minimax with Alpha-Beta Pruning

**Pseudocode:**
```
minimax(position, depth, alpha, beta, is_maximizing):
    if depth == 0 or game_over:
        return evaluate(position)
    
    if is_maximizing:
        max_eval = -infinity
        for each move:
            eval = minimax(position+move, depth-1, alpha, beta, false)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break  # Prune
        return max_eval
    else:
        min_eval = +infinity
        for each move:
            eval = minimax(position+move, depth-1, alpha, beta, true)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break  # Prune
        return min_eval
```

**Complexity:**
- Depth 1: ~35 positions
- Depth 2: ~1,225 positions
- Depth 3: ~42,875 positions
- Depth 4: ~1.5M positions (typical)
- Depth 6: ~1.8B positions (slow)

**Optimizations:**
- Move ordering (checks, captures first)
- Killer move heuristic
- Position caching

## Performance Characteristics

| Depth | Time | Quality |
|-------|------|---------|
| 2 | <0.5s | Weak |
| 3 | 0.5-2s | Intermediate |
| 4 | 2-8s | Strong |
| 6 | 15-30s | Very Strong |
| Stockfish | Variable | Expert |

## Dependencies

```
Python 3.7+
├── selenium (for browser automation)
├── webdriver-manager (for Chrome driver)
└── stockfish (optional, for external engine)
```

No dependencies needed for local play.

## Extension Points

To customize or extend:

1. **Custom Evaluator**: Modify `evaluator.py` scoring function
2. **Different Algorithm**: Replace minimax in `ai_player.py`
3. **New Humanization**: Add features to `humanizer.py`
4. **Alternative Browser**: Modify `chrome_helper.py`
5. **Different Platform**: Create new parser like `board_parser.py`

