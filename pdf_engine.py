# A small engine to build the exact pdf we might need.
# Should support adding paragraphs and pictures
# It is based on building a markdown and converting it into a pdf using pandoc
# Please install pandoc using tool-installer script (for macOS or for Windows)
# on linux, please use your own tools to install (apt install pandoc on Debian)

import subprocess
import io
import os

# Call pandoc which should be installed on the system to generate a PDF
def pandoc_call(test_markdown_path: str, output_file: str, delete_markdown: bool):
    command = "pandoc {} -o {}".format(test_markdown_path, output_file)
    print(command)
    stout = subprocess.run(["pandoc", test_markdown_path, "-o", output_file])
    print(stout)
    if (delete_markdown):
        os.remove(test_markdown_path)

# Creates a file object which allows to build a markdown
def pdf_start_markdown(filename) -> io.TextIOWrapper:
    return open(filename, "w+")

def pdf_close_markdown(markdown_file: io.TextIOWrapper):
    markdown_file.close()

def pdf_append_large_header(markdown_file: io.TextIOWrapper, header_contents: str):
    markdown_file.write("# {}\n".format(header_contents))

def pdf_append_small_header(markdown_file: io.TextIOWrapper, header_contents: str):
    markdown_file.write("## {}\n".format(header_contents))

def pdf_append_paragraph(markdown_file: io.TextIOWrapper, paragraph_contents: str):
    markdown_file.write("{}\n\n".format(paragraph_contents))

def pdf_append_image(markdown_file: io.TextIOWrapper, image_path:str, alt_text = "image", title = "image", width_percent = 100, height_percent = 100):
    markdown_file.write("![{}]({} \"{}\")".format(title, image_path, alt_text, str(width_percent), str(height_percent)) + "{" + "width={}\% height={}%".format(width_percent, height_percent) + "}\n")

