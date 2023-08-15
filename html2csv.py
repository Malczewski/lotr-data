import os
import csv
from bs4 import BeautifulSoup

def extract_and_mark_text(html_content):
	html_content = html_content.replace('<br/>', ' ')
	soup = BeautifulSoup(html_content, 'html.parser')
	extracted_text = []

	for element in soup.find_all(class_=True):
		text = element.get_text(strip=False)
		class_name = " ".join(element["class"])
		extracted_text.append((text, class_name))
	
	return extracted_text

def convert_to_csv(data, csv_filename):
	with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(['Text', 'Class'])

		for text, class_name in data:
			if class_name != 'body' and class_name != 'img':
				csv_writer.writerow([text, class_name])

def process_html_files(input_folder, output_folder):
	for filename in os.listdir(input_folder):
		if filename.endswith('.html'):
			html_path = os.path.join(input_folder, filename)
			
			with open(html_path, 'r', encoding='utf-8') as html_file:
				html_content = html_file.read()

			extracted_data = extract_and_mark_text(html_content)
			
			csv_filename = os.path.splitext(filename)[0] + '.csv'
			output_csv = os.path.join(output_folder, csv_filename)
			
			convert_to_csv(extracted_data, output_csv)
			print(f"Converted and saved data to {output_csv}")

if __name__ == "__main__":
	input_folder = "books-html"
	output_folder = "books-csv"
	
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	
	process_html_files(input_folder, output_folder)
