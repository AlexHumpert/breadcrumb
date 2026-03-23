#!/bin/bash
# setup.sh — One-time setup for the tweet generator
# Run this once from your terminal: bash setup.sh

set -e

# Resolve the directory this script lives in (works regardless of where you call it from)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/generate_tweets.py"
PYTHON_PATH=$(which python3)

echo "🚀 Setting up Tweet Generator..."
echo "   Project folder: $SCRIPT_DIR"

# 1. Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install anthropic pypdf --user --quiet
echo "   ✅ Dependencies installed."

# 2. Set your Anthropic API key
echo ""
echo "🔑 You need an Anthropic API key."
echo "   Get one at: https://console.anthropic.com"
echo ""
read -p "   Paste your ANTHROPIC_API_KEY here: " API_KEY

if [ -z "$API_KEY" ]; then
  echo "❌ No API key provided. Exiting."
  exit 1
fi

# Add to .zshrc (or .bash_profile if using bash)
SHELL_CONFIG="$HOME/.zshrc"
if [ ! -f "$SHELL_CONFIG" ]; then
  SHELL_CONFIG="$HOME/.bash_profile"
fi

if ! grep -q "ANTHROPIC_API_KEY" "$SHELL_CONFIG"; then
  echo "" >> "$SHELL_CONFIG"
  echo "# Anthropic API Key (for tweet generator)" >> "$SHELL_CONFIG"
  echo "export ANTHROPIC_API_KEY=\"$API_KEY\"" >> "$SHELL_CONFIG"
  echo "   ✅ API key saved to $SHELL_CONFIG"
else
  echo "   ℹ️  ANTHROPIC_API_KEY already in $SHELL_CONFIG — skipping."
fi

export ANTHROPIC_API_KEY="$API_KEY"

# 3. Create intake/ folder if it doesn't exist
echo ""
INTAKE_DIR="$SCRIPT_DIR/intake"
if [ ! -d "$INTAKE_DIR" ]; then
  mkdir -p "$INTAKE_DIR"
  echo "📁 Created intake/ folder at: $INTAKE_DIR"
else
  echo "📁 intake/ folder already exists."
fi

# 4. Schedule the cron job (runs daily at 8:00 AM)
CRON_JOB="0 8 * * * ANTHROPIC_API_KEY=$API_KEY $PYTHON_PATH $SCRIPT_PATH >> /tmp/tweet_generator.log 2>&1"

echo ""
echo "⏰ Setting up daily cron job at 8:00 AM..."
( crontab -l 2>/dev/null | grep -v "generate_tweets.py" ; echo "$CRON_JOB" ) | crontab -
echo "   ✅ Cron job scheduled."

# 5. Test run
echo ""
echo "🧪 Running a test now..."
$PYTHON_PATH "$SCRIPT_PATH"

echo ""
echo "✅ Setup complete!"
echo ""
echo "How to use:"
echo "  1. Drop articles (.txt, .md, .html, or .pdf) into:"
echo "     $INTAKE_DIR"
echo "  2. The script runs automatically every day at 8:00 AM"
echo "  3. Tweet drafts are saved (one file per article) to:"
echo "     $SCRIPT_DIR/tweets/"
echo "  4. To run manually anytime:"
echo "     python3 $SCRIPT_PATH"
