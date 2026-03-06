#!/bin/bash
# Install Google Chrome (not snap Chromium) for better Selenium compatibility

echo "=================================================="
echo "Installing Google Chrome for Chess.com Bot"
echo "=================================================="

# Download Chrome
echo "Downloading Google Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb

# Install Chrome
echo "Installing Chrome (requires sudo password)..."
sudo dpkg -i /tmp/chrome.deb || sudo apt-get install -f -y

# Verify installation
if command -v google-chrome &> /dev/null; then
    echo "✓ Google Chrome installed successfully!"
    google-chrome --version
else
    echo "✗ Installation failed"
    exit 1
fi

# Clean up
rm /tmp/chrome.deb

echo ""
echo "=================================================="
echo "✓ Setup complete!"
echo "=================================================="
echo ""
echo "Now run the bot:"
echo "  /usr/bin/python3 play_online.py"
echo ""
