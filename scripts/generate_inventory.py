"""Print the canonical inventory without modifying source content."""
import sys
from hub import main

if __name__ == '__main__':
    sys.argv.append('inventory')
    main()
