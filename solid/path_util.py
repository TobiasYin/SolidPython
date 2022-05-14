import os, sys
def add_import_path(p):
    sys.path.extend([p] + [os.path.join(root, name) for root, dirs, _ in os.walk(p) for name in dirs])

