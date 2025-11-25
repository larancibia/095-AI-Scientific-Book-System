#!/usr/bin/env python3
"""
Pre-Flight Check - Validate system before book generation
Run this before generating any book to catch issues early.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def check_system():
    """Run all pre-flight checks."""

    print("="*70)
    print("PRE-FLIGHT CHECK - AI Scientific Book System v2.0")
    print("="*70)

    checks_passed = 0
    checks_failed = 0
    warnings = []

    # Check 1: Python version
    print("\n[1/10] Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        checks_passed += 1
    else:
        print(f"  ✗ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
        checks_failed += 1

    # Check 2: Claude CLI
    print("\n[2/10] Checking Claude CLI...")
    if shutil.which('claude'):
        try:
            result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=5)
            print(f"  ✓ Claude CLI installed")
            checks_passed += 1
        except:
            print("  ⚠ Claude CLI found but not responding")
            warnings.append("Claude CLI may not be configured")
            checks_passed += 1
    else:
        print("  ✗ Claude CLI not found")
        print("     Install: npm install -g @anthropic-ai/claude-cli")
        checks_failed += 1

    # Check 3: Gemini CLI
    print("\n[3/10] Checking Gemini CLI...")
    if shutil.which('gemini'):
        print(f"  ✓ Gemini CLI installed (gemini-2.0-flash)")
        checks_passed += 1
    else:
        print("  ✗ Gemini CLI not found")
        checks_failed += 1

    # Check 4: Required Python packages
    print("\n[4/10] Checking Python dependencies...")
    required_packages = {
        'chromadb': 'chromadb',
        'sentence_transformers': 'sentence-transformers',
        'reportlab': 'reportlab',
        'arxiv': 'arxiv',
        'yaml': 'pyyaml'
    }

    missing = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (missing)")
            missing.append(package_name)

    if not missing:
        checks_passed += 1
    else:
        checks_failed += 1
        print(f"\n  Install with: pip install {' '.join(missing)}")

    # Check 5: LaTeX/pandoc
    print("\n[5/10] Checking PDF generation tools...")
    pdf_tools = []

    if shutil.which('pandoc'):
        pdf_tools.append('pandoc')
        print("  ✓ pandoc")
    else:
        print("  ✗ pandoc (recommended)")

    if shutil.which('xelatex'):
        pdf_tools.append('xelatex')
        print("  ✓ xelatex (BEST for UTF-8)")
    elif shutil.which('pdflatex'):
        pdf_tools.append('pdflatex')
        print("  ⚠ pdflatex (may have UTF-8 issues, use xelatex)")
        warnings.append("Install xelatex for better UTF-8 support")

    if pdf_tools:
        checks_passed += 1
    else:
        print("  ✗ No LaTeX engine found")
        print("     Install: sudo apt install texlive-xetex pandoc")
        checks_failed += 1

    # Check 6: Working directory
    print("\n[6/10] Checking working directory...")
    cwd = Path.cwd()
    print(f"  Current: {cwd}")
    checks_passed += 1

    # Check 7: Embeddings model cache
    print("\n[7/10] Checking embeddings model cache...")
    cache_dir = Path.home() / '.cache' / 'chroma' / 'onnx_models' / 'all-MiniLM-L6-v2'
    if cache_dir.exists():
        print("  ✓ Embeddings model cached (fast startup)")
        checks_passed += 1
    else:
        print("  ⚠ Model not cached (first run will download 79MB, ~10 seconds)")
        warnings.append("First embeddings run will download 79MB model")
        checks_passed += 1

    # Check 8: Write permissions
    print("\n[8/10] Checking write permissions...")
    test_file = Path("test_write_permission.tmp")
    try:
        test_file.write_text("test", encoding='utf-8')
        test_file.unlink()
        print("  ✓ Can write to current directory")
        checks_passed += 1
    except Exception as e:
        print(f"  ✗ Cannot write to current directory: {e}")
        checks_failed += 1

    # Check 9: Disk space
    print("\n[9/10] Checking disk space...")
    stat = shutil.disk_usage('.')
    free_gb = stat.free / (1024**3)
    if free_gb > 2:
        print(f"  ✓ {free_gb:.1f} GB free (plenty)")
        checks_passed += 1
    elif free_gb > 0.5:
        print(f"  ⚠ {free_gb:.1f} GB free (should be ok)")
        warnings.append(f"Low disk space: {free_gb:.1f}GB")
        checks_passed += 1
    else:
        print(f"  ✗ Only {free_gb:.1f} GB free (too low!)")
        checks_failed += 1

    # Check 10: Git configured
    print("\n[10/10] Checking Git...")
    if shutil.which('git'):
        try:
            result = subprocess.run(['git', 'config', 'user.name'],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"  ✓ Git configured ({result.stdout.strip()})")
                checks_passed += 1
            else:
                print("  ⚠ Git installed but not configured")
                warnings.append("Run: git config --global user.name 'Your Name'")
                checks_passed += 1
        except:
            print("  ✓ Git installed")
            checks_passed += 1
    else:
        print("  ✗ Git not found")
        checks_failed += 1

    # Summary
    print("\n" + "="*70)
    print(f"PRE-FLIGHT CHECK COMPLETE")
    print("="*70)
    print(f"✅ Passed: {checks_passed}/10")
    print(f"❌ Failed: {checks_failed}/10")
    if warnings:
        print(f"⚠️  Warnings: {len(warnings)}")
        for w in warnings:
            print(f"   - {w}")

    print()

    if checks_failed == 0:
        print("✅ ALL SYSTEMS GO - Ready to generate books!")
        print("   Run: python create_scientific_book.py init --title 'Your Book' ...")
        return True
    elif checks_failed <= 2:
        print("⚠️ CAUTION - Some issues detected but can proceed with care")
        return True
    else:
        print("❌ ABORT - Too many issues, fix before proceeding")
        print("\n   Fix these issues first:")
        if not shutil.which('claude'):
            print("   - Install Claude CLI")
        if missing:
            print(f"   - pip install {' '.join(missing)}")
        return False

if __name__ == "__main__":
    success = check_system()
    sys.exit(0 if success else 1)
