# Installation & Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Chrome/Chromium browser (for Chess.com bot only)

## Option 1: Local Chess Game (No Extra Dependencies)

### Basic Setup
```bash
cd "Chess agent"
python3 test_chess.py
```

Play against the AI locally with no additional installation needed.

## Option 2: Chess.com Bot Integration

### Step 1: Install Dependencies
```bash
pip3 install -r requirements.txt
```

This installs:
- `selenium`: For browser automation
- `webdriver-manager`: For managing Chrome WebDriver

### Step 2: Verify Chrome/Chromium
The bot requires Chrome or Chromium. Check installation:
```bash
which google-chrome
# or
which chromium
```

If not installed, install it:
```bash
# Ubuntu/Debian
sudo apt install chromium

# Or Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### Step 3: Clear WebDriver Cache (if needed)
```bash
rm -rf ~/.wdm
```

### Step 4: Run the Bot
```bash
python3 play_online.py
```

## Configuration

### AI Difficulty Levels

**Play Fast** (1-2 moves ahead):
```bash
python3 play_fast.py
```

**Standard** (4 moves ahead):
```bash
python3 play_online.py
```

**Maximum Strength** (6+ moves ahead):
```bash
python3 play_maximum_strength.py
```

**Stockfish Integration** (External engine):
```bash
pip3 install stockfish
python3 play_stockfish.py
```

### Customization

Edit `play_online.py` to adjust:
- `ai_depth`: Search depth (4 = 4 moves ahead)
- `min_time`: Minimum thinking time in seconds
- `max_time`: Maximum thinking time in seconds
- Humanization parameters in `humanizer.py`

## Module Overview

- **game.py**: Chess game logic and rules
- **ai_player.py**: AI with minimax algorithm
- **evaluator.py**: Position evaluation
- **humanizer.py**: Advanced humanization features
- **board_parser.py**: Parse Chess.com board
- **chess_com_bot.py**: Main bot controller
- **chrome_helper.py**: Browser automation

## Troubleshooting

### "DevToolsActivePort" Error
```bash
rm -rf ~/.wdm
pkill -f chrome
python3 play_online.py
```

### Board Not Detected
Run the test first:
```bash
python3 test_bot.py
```

This will verify the bot can detect the board correctly.

### Chrome/Chromium Not Found
Make sure Chrome is installed and the path is correct in `chrome_helper.py`.

## Legal Notice

⚠️ **Using this bot on Chess.com violates their Terms of Service and may result in account bans.**

This project is for **educational purposes only**. Use Lichess instead:
- Lichess has an official [Bot API](https://lichess.org/api#tag/Bot)
- It's legal and encouraged
- Free and open-source friendly

