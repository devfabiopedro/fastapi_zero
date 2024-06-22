import os
import webbrowser

file_path = os.path.abspath("./htmlcov/index.html")

webbrowser.open(f"file://{file_path}")
