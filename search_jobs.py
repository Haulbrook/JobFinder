"""
Windows-friendly wrapper for multi-platform job search
Handles Unicode encoding issues on Windows console
"""

import sys
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

    # Set console to UTF-8
    os.system('chcp 65001 > nul')

# Now import and run the main script
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from multi_platform_search import main

if __name__ == '__main__':
    main()
