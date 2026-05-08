import json
import sys
import glob

def read_notebooks(pattern):
    for f in sorted(glob.glob(pattern)):
        print(f"=== {f} ===")
        try:
            with open(f, 'r') as file:
                nb = json.load(file)
                for cell in nb.get('cells', []):
                    if cell.get('cell_type') == 'markdown':
                        print(''.join(cell.get('source', [])))
        except Exception as e:
            print(f"Error reading {f}: {e}")
        print("\n\n")

if __name__ == "__main__":
    read_notebooks("*.ipynb")
