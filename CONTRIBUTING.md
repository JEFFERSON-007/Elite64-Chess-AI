# Contributing to Elite64 Chess AI

Thank you for interest in contributing! Here's how you can help.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow

## How to Contribute

### Bug Reports
1. Check [Issues](https://github.com/JEFFERSON-007/Elite64-Chess-AI/issues) for duplicates
2. Include:
   - Python version (`python3 --version`)
   - Error message and stack trace
   - Steps to reproduce
   - System information (OS, Chrome version if using bot)

### Feature Requests
1. Describe the feature clearly
2. Explain use case and benefits
3. Provide examples if applicable

### Code Contributions

#### Setup Development Environment
```bash
git clone https://github.com/JEFFERSON-007/Elite64-Chess-AI.git
cd Elite64-Chess-AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Making Changes
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make focused, atomic commits
3. Test thoroughly
4. Push to your fork
5. Submit a pull request

#### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep lines under 100 characters

#### Testing
- Test locally before submitting PR
- For Chess.com changes: test with `test_bot.py`
- For AI changes: test with `test_chess.py`
- Update existing tests if behavior changes

## Areas to Contribute

### High Priority
- [ ] Performance optimization (faster evaluation, better pruning)
- [ ] Opening book integration (better opening play)
- [ ] Endgame tables (perfect endgame knowledge)
- [ ] Better move ordering heuristics
- [ ] Transposition table implementation

### Medium Priority
- [ ] Enhanced board visualization
- [ ] Game replay/analysis
- [ ] PGN import/export
- [ ] Chess.com integration improvements
- [ ] Better error handling

### Low Priority
- [ ] Documentation improvements
- [ ] Code refactoring
- [ ] UI enhancements
- [ ] Additional test cases

## Legal Note

⚠️ Keep legal/ethical considerations in mind:
- Chess.com bot features should include clear warnings
- Document Terms of Service violations
- Suggest legal alternatives (Lichess)

## Questions?

Feel free to open an issue to discuss before starting work on large features.

Thank you for contributing!
