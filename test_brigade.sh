#!/bin/bash
# BRIGADE Testing Script

echo "🎖️ BRIGADE Testing Guide"
echo "========================"

echo ""
echo "1. Test Analysis (no approval needed):"
echo "   ./brigade analyze test_code.py"

echo ""
echo "2. Test Auto-fix with Approval:"
echo "   ./brigade auto-fix test_code.py --create-pr"
echo "   (This will show approval prompt)"

echo ""
echo "3. Test Dry Run (no approval needed):"
echo "   ./brigade auto-fix test_code.py --dry-run"

echo ""
echo "4. Test Approval Management:"
echo "   ./brigade approve --list"

echo ""
echo "5. Test Deploy Command:"
echo "   ./brigade deploy test_code.py --mode analysis"

echo ""
echo "📋 Test File Created: test_code.py"
echo "   - Contains security issues (eval)"
echo "   - Contains resource leaks (unclosed files)"
echo "   - Contains style issues (!= None)"
echo "   - Contains potential bugs (division by zero)"

echo ""
echo "🚀 Start testing with:"
echo "   ./brigade analyze test_code.py"
