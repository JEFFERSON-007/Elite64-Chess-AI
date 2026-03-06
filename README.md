# Elite64 Chess AI

A competitive chess-playing AI that uses the minimax algorithm with alpha-beta pruning to predict moves ahead and make intelligent decisions. Includes advanced humanization for realistic play and optional Chess.com integration.

**Key Features**: Minimax AI (4+ moves ahead), Advanced humanization, Chess.com bot integration, Stockfish support

## ⚠️ IMPORTANT WARNING - Chess.com Bot

The Chess.com integration (`play_online.py`) **violates Chess.com's Terms of Service**:
- Using bots on Chess.com **may result in account bans**
- This is provided for **educational purposes only**
- **Use ONLY with throwaway/test accounts**
- You accept all responsibility for consequences

**The bot includes advanced humanization to reduce detection risk**, but no guarantees.

**Recommended Alternative**: Use [Lichess Bot API](https://lichess.org/api#tag/Bot) for legal bot play.

## Features

- **Smart AI**: Uses minimax algorithm with alpha-beta pruning to look 4 moves ahead (configurable)
- **Complete Chess Rules**: Supports all standard chess moves including castling, en passant, and pawn promotion
- **Position Evaluation**: Evaluates positions based on material, piece placement, and mobility
- **Interactive Interface**: Command-line interface with clear board visualization
- **Intelligent Move Ordering**: Optimizes search by examining promising moves first

## Installation

### Dependencies

For local play (no external dependencies needed):
```bash
# No installation needed - uses Python standard library
cd "Chess agent"
```

For Chess.com bot integration:
```bash
# Install pip first if needed
sudo apt install python3-pip

# Install bot dependencies
pip3 install -r requirements.txt
```

Alternatively, install dependencies manually:
```bash
pip3 install selenium webdriver-manager
```

## Usage - Local Play

Run the chess game locally:

```bash
python3 main.py
```

You'll be prompted to:
1. Choose your color (white or black)
2. Select AI difficulty (1-6, where higher = stronger but slower)

### Making Moves

Enter moves in algebraic notation:
- Format: `e2 e4` or `e2e4`
- Example: Move pawn from e2 to e4

### Commands

- `moves` - Show all legal moves for your pieces
- `help` - Display help information
- `quit` - Exit the game

---

## Usage - Chess.com Bot

> [!CAUTION]
> This violates Chess.com ToS. Use at your own risk with throwaway accounts only.

Run the Chess.com bot:

```bash
python3 play_online.py
```

You'll be prompted to:
1. Confirm you understand the risks (type `I UNDERSTAND`)
2. Set AI difficulty (1-6)
3. Set thinking time range (to appear more human)
4. Optionally provide a game URL

The bot will:
- Open a Chrome browser
- Wait for you to log in and navigate to a game
- Automatically detect the board and play moves
- Add random delays to appear more human-like

### Bot Features

**Advanced Humanization (Anti-Detection)**:
- **Natural Mouse Movements**: Curved paths, hovering, hesitation
- **Adaptive Thinking Time**: Longer in complex positions (3-20+ seconds)
- **Occasional "Mistakes"**: Plays 2nd/3rd best move 5-15% of the time
- **Position Complexity Analysis**: Thinks longer when there are more tactics
- **Pre-move Hesitation**: Random delays before clicking (0.1-2 seconds)
- **Post-move Behavior**: Cursor movements after moves
- **Idle Behaviors**: Mouse movements while waiting for opponent
- **Adaptive Response Time**: Doesn't respond instantly to opponent moves
- **No Perfect Play**: Intentionally plays like a strong human, not an engine

**Technical Features**:
- **Board Detection**: Automatically reads Chess.com board state
- **AI Integration**: Uses the same minimax engine
- **Anti-Detection Browser**: Disables automation flags
- **Move Execution**: Clicks squares with human-like timing

---

## How It Works

### Minimax Algorithm

The AI explores the game tree using minimax with alpha-beta pruning:
- Looks ahead multiple moves (default: 4 plies)
- Evaluates positions using material and positional factors
- Prunes branches that won't affect the final decision
- Orders moves to maximize pruning efficiency

### Position Evaluation

Positions are scored based on:
- **Material**: Piece values (Pawn=100, Knight=320, Bishop=330, Rook=500, Queen=900)
- **Position**: Piece-square tables favor center control and development
- **Mobility**: Bonus for having more legal moves
- **King Safety**: Evaluated differently in middle game vs endgame

### Search Optimization

- **Alpha-Beta Pruning**: Eliminates ~50-90% of positions from search
- **Move Ordering**: Examines captures and center moves first
- **MVV-LVA**: Most Valuable Victim - Least Valuable Attacker heuristic

## Project Structure

```
Chess agent/
├── main.py              # Entry point for local play
├── game.py              # Game interface and user interaction
├── chess_engine.py      # Board representation and move validation
├── pieces.py            # Piece classes with movement logic
├── ai_player.py         # AI with minimax algorithm
├── evaluator.py         # Position evaluation
├── test_chess.py        # Unit tests
├── play_online.py       # Chess.com bot entry point (⚠️ ToS violation)
├── chess_com_bot.py     # Chess.com browser automation
├── board_parser.py      # Parse Chess.com board state
├── requirements.txt     # Python dependencies for bot
└── README.md            # This file
```

## Difficulty Levels

- **Level 1-2**: Beginner (good for learning)
- **Level 3-4**: Intermediate (competitive play)
- **Level 5-6**: Advanced (strong tactical play, slower computation)

## Future Enhancements

- Opening book for stronger opening play
- Transposition tables to avoid re-evaluating positions
- Iterative deepening for time management
- UCI protocol support for chess GUIs
- Web-based graphical interface
- Machine learning integration

## Example Game

```
  a b c d e f g h
  ----------------
8|BR BN BB BQ BK BB BN BR |8
7|BP BP BP BP BP BP BP BP |7
6|.  .  .  .  .  .  .  .  |6
5|.  .  .  .  .  .  .  .  |5
4|.  .  .  .  .  .  .  .  |4
3|.  .  .  .  .  .  .  .  |3
2|WP WP WP WP WP WP WP WP |2
1|WR WN WB WQ WK WB WN WR |1
  ----------------
  a b c d e f g h

White's turn. Enter move: e2 e4
```

## License

This project is open source and available for educational purposes.

## Author

Built with minimax, alpha-beta pruning, and a passion for chess! 🎯♟️
