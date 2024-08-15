import time
from engine import *
import sys
import os

def main():
    if len(sys.argv) != 2:
        print(sys.argv)
        sys.exit("Usage: python3 solver.py name.txt")
    f = sys.argv[1]
    if not f.endswith('.txt'):
        sys.exit("Please input valid file")
    path = os.path.join('SAT', f)
    cls = load_dimacs(path)
    # Choose an engine

    # Evaluate the performance
    
if __name__ == "__main__":
    main()