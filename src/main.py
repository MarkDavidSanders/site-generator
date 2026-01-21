# main.py

'''Main site generator script'''

import sys

from copy_static import copy_static
from generate_page import generate_pages_recursive

if len(sys.argv) > 1:
    print(">>> Basepath argument provided:", sys.argv[1])
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    print(">>> main.py starting")
    copy_static("static", "docs")
    print(">>> copy_static completed")
    generate_pages_recursive(basepath, "content", "template.html", "docs")
    print(">>> generate_page completed")
    print(">>> main.py finished")

main()
