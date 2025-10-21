#!/bin/bash
# CodeViewX API Key Setup Script
# This script helps you set up the ANTHROPIC_API_KEY environment variable

echo "🚀 CodeViewX API Key Setup"
echo "=========================="
echo ""

# Check if API key is already set
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "✅ ANTHROPIC_API_KEY is already set"
    echo "   Current value: ${ANTHROPIC_API_KEY:0:12}..."
    echo ""
    echo "Do you want to update it? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "✅ Setup complete. You can now run codeviewx!"
        exit 0
    fi
fi

echo "📝 Please enter your Anthropic API key:"
echo "   (Get your key from: https://console.anthropic.com)"
echo ""
read -s -p "API Key: " api_key
echo ""

# Validate API key format
if [[ ! "$api_key" =~ ^sk-ant-api ]]; then
    echo "⚠️  Warning: API key should start with 'sk-ant-api'"
    echo "   Are you sure this is correct? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled. Please get a valid API key from https://console.anthropic.com"
        exit 1
    fi
fi

if [ ${#api_key} -lt 20 ]; then
    echo "❌ Error: API key appears to be too short"
    echo "   Please check that you copied the full API key"
    exit 1
fi

echo ""
echo "🔧 Setting up your API key..."
echo ""

# Detect shell and update appropriate config file
SHELL_NAME=$(basename "$SHELL")

case "$SHELL_NAME" in
    bash)
        CONFIG_FILE="$HOME/.bashrc"
        ;;
    zsh)
        CONFIG_FILE="$HOME/.zshrc"
        ;;
    fish)
        CONFIG_FILE="$HOME/.config/fish/config.fish"
        FISH_FORMAT="set -gx ANTHROPIC_API_KEY '$api_key'"
        ;;
    *)
        echo "⚠️  Unsupported shell: $SHELL_NAME"
        echo "   Please manually add this line to your shell configuration:"
        echo "   export ANTHROPIC_API_KEY='$api_key'"
        exit 1
        ;;
esac

if [[ "$SHELL_NAME" == "fish" ]]; then
    if grep -q "ANTHROPIC_API_KEY" "$CONFIG_FILE" 2>/dev/null; then
        # Update existing line
        sed -i.bak "s|^set -gx ANTHROPIC_API_KEY.*|$FISH_FORMAT|" "$CONFIG_FILE"
    else
        # Add new line
        echo "$FISH_FORMAT" >> "$CONFIG_FILE"
    fi
else
    if grep -q "ANTHROPIC_API_KEY" "$CONFIG_FILE" 2>/dev/null; then
        # Update existing line
        sed -i.bak "s|^export ANTHROPIC_API_KEY.*|export ANTHROPIC_API_KEY='$api_key'|" "$CONFIG_FILE"
    else
        # Add new line
        echo "export ANTHROPIC_API_KEY='$api_key'" >> "$CONFIG_FILE"
    fi
fi

# Set for current session
export ANTHROPIC_API_KEY="$api_key"

echo "✅ API key configured successfully!"
echo ""
echo "📁 Configuration updated: $CONFIG_FILE"
echo "🔄 To apply changes, restart your terminal or run:"
if [[ "$SHELL_NAME" == "fish" ]]; then
    echo "   source $CONFIG_FILE"
else
    echo "   source $CONFIG_FILE"
fi
echo ""
echo "🎉 You can now run CodeViewX:"
echo "   codeviewx"
echo "   codeviewx -w /path/to/your/project"