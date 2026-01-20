# main.py

'''Main site generator script'''

from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    print(">>> main.py starting")
    copy_static("static", "public")
    print(">>> copy_static completed")
    generate_pages_recursive("content", "template.html", "public")
    print(">>> generate_page completed")
    print(">>> main.py finished")

main()
