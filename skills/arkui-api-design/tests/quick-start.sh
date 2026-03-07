#!/bin/bash

# Quick Start Script for ArkUI API Design Skill Evaluation
# This script helps you get started with testing the skill

set -e

echo "=================================="
echo "ArkUI API Design Skill Test Suite"
echo "=================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi

echo "✅ npm version: $(npm --version)"
echo ""

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "=================================="
echo "Choose an option:"
echo "=================================="
echo "1. Read Manual Evaluation Guide"
echo "2. View Test Cases"
echo "3. Run Automated Tests (when implemented)"
echo "4. View Sample Report"
echo "5. Clean Old Results"
echo ""
read -p "Enter option (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Opening Manual Evaluation Guide..."
        cat MANUAL_EVALUATION.md | less
        ;;
    2)
        echo ""
        echo "Test Cases Summary:"
        echo "==================="
        if command -v jq &> /dev/null; then
            cat test-cases.json | jq '.categories | to_entries[] | "\n\(.key): \(.value.name)\n  Tests: \(.value.test_cases | length)\n  Description: \(.value.description)"'
        else
            echo "Note: Install 'jq' for formatted output"
            cat test-cases.json | grep -E '"(id|name|description)"' | head -40
        fi
        ;;
    3)
        echo ""
        echo "🚀 Running automated tests..."
        npm test
        ;;
    4)
        echo ""
        echo "Sample Evaluation Report:"
        echo "========================="
        cat results/sample-report.json | grep -E '(category_name|score|passed|failed|overall_score|summary)' | head -30
        echo ""
        echo "Full report available at: results/sample-report.json"
        ;;
    5)
        echo ""
        echo "🧹 Cleaning old results..."
        rm -rf results/*.json results/*.txt
        echo "✅ Cleaned old results"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "For more information, see README.md"
echo "=================================="
