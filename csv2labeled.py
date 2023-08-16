import csv
import re
import sys
import unicodedata
import os

def clean_text(text):
	cleaned_text = re.sub(r'\s+', ' ', text)
	cleaned_text = ''.join(c for c in cleaned_text if not unicodedata.category(c).startswith('C'))
	return cleaned_text.strip()

def apply_condition(condition, text, prev_type = '', next_type = ''):
	prev_type = '' if prev_type == None else prev_type
	next_type = '' if next_type == None else next_type
	if condition == 'BEFORE_SPEECH':
		return 'SPEECH' in next_type
	elif condition == 'AFTER_TEXT':
		return ('TEXT' in prev_type and not 'TEXT_EXTRA' in next_type)
	elif condition == 'AFTER_TEXT_EXTRA':
		return ('TEXT_EXTRA' in prev_type)
	elif condition == 'BEFORE_CN':
		return next_type == 'CHAPTER_NUMBER'
	elif condition == 'NO_NUMBER':
		return not re.match('^\d*$', text)
	raise
	
def read_mapping_from_file(mapping_csv):
	mappings = []
	with open('class-mappings/' + mapping_csv, 'r', encoding='utf-8') as mapfile:
		map_reader = csv.DictReader(mapfile)
		for row in map_reader:
			class_pattern = row['Class']
			class_type = row['Type']
			class_condition = row['Condition']
			mapping = (class_pattern, class_type, class_condition)
			mappings.append(mapping)
	return mappings

def get_simple_mapping(mappings, class_name):
	for class_pattern, class_type, class_condition in mappings:
		if re.match('^' + class_pattern + '$', class_name):
			return class_type

def process_csv(input_csv, custom_mapping_csv, output_csv):
	class_to_mappings = read_mapping_from_file(custom_mapping_csv)
	hardcoded_mappings = read_mapping_from_file('common.csv')
	class_to_mappings.extend(hardcoded_mappings)
	
	non_matched_classes = []
	filtered_data = []
	with open(input_csv, 'r', encoding='utf-8') as csvfile:
		csv_reader = csv.DictReader(csvfile)
		
		row = next(csv_reader)
		while True:
			class_name = row['Class']
	
			next_row = None
			try:
				next_row = next(csv_reader)
			except StopIteration:
				next_row = None
				pass

			mapped_row = None
			text = clean_text(row['Text'])
			for class_pattern, class_type, class_condition in class_to_mappings:
				if re.match('^' + class_pattern + '$', class_name):
					if next_row != None:
						next_type = get_simple_mapping(class_to_mappings, next_row['Class'])
					prev_type = None
					if len(filtered_data) > 0:
						prev_type = filtered_data[-1]["Type"]
					if not class_condition or apply_condition(class_condition, text, prev_type, next_type):
						mapped_row = {'Type': class_type, 'Text': text}
						break  # Only one mapping needs to match
			if mapped_row != None:
				filtered_data.append(mapped_row)
			else:
				filtered_data.append({'Type': f"UNKNOWN({class_name})", 'Text': text[:50]})
				non_matched_classes.append(class_name)
	
			if (next_row != None):
				row = next_row
			else: 
				break

	with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
		csv_writer = csv.DictWriter(csvfile, fieldnames=['Type', 'Text'])
		csv_writer.writeheader()
		csv_writer.writerows(filtered_data)

	non_matched_classes = set(non_matched_classes)
	print("Non-Covered Class Names:")
	for class_name in non_matched_classes:
		print(f"- {class_name}")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python script_name.py input_csv custom_mapping_csv output_csv")
	else:
		input_csv = sys.argv[1]
		custom_mapping_csv = sys.argv[2]
		output_csv = 'books-filtered/' + os.path.splitext(os.path.basename(input_csv))[0] + '.csv'
		process_csv(input_csv, custom_mapping_csv, output_csv)
		print(f"Filtered data written to {output_csv}")
