#!/bin/bash
# Run E2E test scenarios for SynaptiVerse

echo "🚀 SynaptiVerse E2E Test Runner"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Run tests
echo ""
echo "Running E2E test scenarios..."
echo ""

python3 tests/e2e_scenarios.py

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed (exit code: $TEST_EXIT_CODE)"
    exit $TEST_EXIT_CODE
fi
