#!/bin/bash
# Quick Start Script for MoneyPrinter Automation

echo "🤖 MoneyPrinter Automation Setup"
echo "================================="
echo ""

# Check if automation_config.yaml exists
if [ -f "automation_config.yaml" ]; then
    echo "✓ Configuration file exists: automation_config.yaml"
else
    echo "⚠️  No automation_config.yaml found"
    echo "   Copying from example file..."
    cp automation_config.example.yaml automation_config.yaml
    echo "✓ Created automation_config.yaml"
    echo ""
    echo "📝 Please edit automation_config.yaml to configure your automation settings"
    echo "   Key settings to review:"
    echo "   - video_topics: Add your video topics"
    echo "   - automate_youtube_upload: Enable when you've set up OAuth"
    echo "   - generation_interval_hours: How often to generate videos"
    echo ""
fi

# Check if PyYAML is installed
echo ""
echo "Checking dependencies..."
python -c "import yaml" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ PyYAML is installed"
else
    echo "⚠️  PyYAML is not installed"
    echo "   Installing PyYAML..."
    pip install PyYAML==6.0.1
    if [ $? -eq 0 ]; then
        echo "✓ PyYAML installed successfully"
    else
        echo "❌ Failed to install PyYAML"
        echo "   Please run: pip install PyYAML==6.0.1"
        exit 1
    fi
fi

# Check if backend is running
echo ""
echo "Checking backend connection..."
curl -s http://localhost:8080/api/cancel > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Backend is running"
else
    echo "⚠️  Backend is not running"
    echo ""
    echo "   The MoneyPrinter backend must be running for automation to work."
    echo "   Start it with:"
    echo "   cd Backend && python main.py"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
fi

echo ""
echo "================================="
echo "Setup complete! 🎉"
echo ""
echo "Usage:"
echo "  python automation.py              # Run once"
echo "  python automation.py --daemon     # Run continuously"
echo ""
echo "For more information, see AUTOMATION.md"
echo ""
