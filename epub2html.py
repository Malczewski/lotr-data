import os
from ebooklib import epub

def convert_epub_to_html(epub_path, output_folder):
	book = epub.read_epub(epub_path)
	text = ""
	
	for item in book.get_items():
		if isinstance(item, epub.EpubHtml):
			content = item.get_content()
			text += content.decode("utf-8")  # Decode the content from bytes to str

	
	# Generate a new HTML filename
	html_filename = os.path.splitext(os.path.basename(epub_path))[0] + '.html'
	output_path = os.path.join(output_folder, html_filename)
	with open(output_path, "w", encoding="utf-8") as f:
		f.write(text)


def convert_all_epubs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.epub'):
            epub_path = os.path.join(input_folder, filename)
            convert_epub_to_html(epub_path, output_folder)
            print(f"Converted {filename} to HTML")

if __name__ == "__main__":
    input_folder = "books"
    output_folder = "books-html"
    convert_all_epubs_in_folder(input_folder, output_folder)
