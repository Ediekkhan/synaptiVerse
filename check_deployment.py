#!/usr/bin/env python3
"""
Quick diagnostic script to test if deployment will work
Run this locally to verify all imports work
"""

import sys
import os

print("=" * 60)
print("SynaptiVerse Deployment Diagnostic")
print("=" * 60)
print()

# Test 1: Python version
print("✓ Python version:", sys.version)
assert sys.version_info >= (3, 8), "Python 3.8+ required"
print()

# Test 2: Required packages
print("Checking required packages...")
required_packages = [
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('pydantic', 'Pydantic'),
]

all_ok = True
for package, name in required_packages:
    try:
        __import__(package)
        print(f"  ✓ {name} installed")
    except ImportError:
        print(f"  ✗ {name} NOT installed")
        all_ok = False

print()

# Test 3: File structure
print("Checking file structure...")
required_files = [
    'src/agents/web_ui.py',
    'src/metta/metta_interface.py',
    'src/metta/knowledge_graphs/medical_facts.metta',
    'requirements.txt',
    'Procfile',
]

for filepath in required_files:
    if os.path.exists(filepath):
        print(f"  ✓ {filepath}")
    else:
        print(f"  ✗ {filepath} MISSING")
        all_ok = False

print()

# Test 4: Import web_ui
print("Testing imports...")
try:
    sys.path.insert(0, 'src')
    from agents import web_ui
    print("  ✓ web_ui imports successfully")
except Exception as e:
    print(f"  ✗ web_ui import failed: {e}")
    all_ok = False

print()

# Test 5: MeTTa interface
try:
    from metta.metta_interface import query_metta
    print("  ✓ query_metta imports successfully")
    
    # Try a query
    result = query_metta("fever headache")
    if result.get("status") == "success":
        print("  ✓ query_metta executes successfully")
        print(f"    Found {len(result.get('possible_conditions', []))} conditions")
    else:
        print("  ⚠ query_metta returned non-success status")
except Exception as e:
    print(f"  ✗ query_metta failed: {e}")
    all_ok = False

print()
print("=" * 60)
if all_ok:
    print("✓ ALL CHECKS PASSED - Ready for deployment!")
else:
    print("✗ SOME CHECKS FAILED - Fix issues before deploying")
print("=" * 60)

sys.exit(0 if all_ok else 1)
