# Chess.com Bot - Quick Start Guide

## ⚠️ WARNING
This bot violates Chess.com's Terms of Service. Use ONLY with throwaway accounts.

## Quick Setup

### 1. Kill Any Running Instances
```bash
pkill -f play_online.py
```

### 2. Test the Bot (Recommended First Step)
```bash
cd "/home/jeff/Documents/projects/Chess agent"
/usr/bin/python3 test_bot.py
```

This will:
- Open browser automatically
- Tell you when to start a game
- Test if it can detect the board
- Show you if everything works

### 3. Run the Full Bot
```bash
/usr/bin/python3 play_online.py
```

Then follow the prompts:
1. Type `I UNDERSTAND`
2. Press Enter for AI depth (uses 4)
3. Press Enter for min time (uses 3 sec)
4. Press Enter for max time (uses 12 sec)
5. Enter URL or press Enter for computer game

### 4. When Browser Opens
1. Start or join a game on Chess.com
2. Go back to terminal
3. Press Enter
4. **Keep the browser window open!**
5. Watch the terminal - it will show each move

## Troubleshooting

### "DevToolsActivePort" Error
- Chromium/Chrome version issue
- Run: `rm -rf ~/.wdm` to clear driver cache
- Try again

### "list assignment index out of range"
- Board parser can't find pieces
- Run `test_bot.py` to diagnose
- Chess.com may have changed their DOM structure

### Bot Not Moving
- Make sure browser window stays open
- Check terminal for error messages
- Ensure it's your turn in the game
- Try refreshing the page and restarting

### Browser Won't Start
- Make sure Chromium is installed: `snap list | grep chromium`
- If not: `sudo snap install chromium`

## Files

- `play_online.py` - Main bot entry point
- `test_bot.py` - Quick test script (use this first!)
- `chess_com_bot.py` - Core bot logic
- `modern_parser.py` - Board parser with 3 strategies
- `humanizer.py` - Makes moves look human
- `inspect_dom.py` - Debug tool to see Chess.com structure

## Support

If nothing works, the bot may need updates for Chess.com's latest structure.
Consider using Lichess Bot API instead (legal and supported).
