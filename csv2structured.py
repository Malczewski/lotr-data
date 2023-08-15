import csv
import sys
import os
from enrichments import get_characters, get_locations, get_artifacts

def process_enrichments(rows):
	for row in rows:
		text = row["TEXT"]
		row["CHARACTERS"] = ','.join(get_characters(text))
		row["LOCATIONS"] = ','.join(get_locations(text))
		row["ARTIFACTS"] = ','.join(get_artifacts(text))

def process_csv(input_filename, output_filename):
	result_list = []

	with open(input_filename, 'r', encoding='utf-8') as csvfile:
		csvreader = csv.DictReader(csvfile)
		
		current_data = {
			"SOURCE": os.path.splitext(os.path.basename(input_file))[0],
			"TITLE": None,
			"BOOK": None,
			"PART": None,
			"AUTHOR": None,
			"CHAPTER_NAME": None,
			"CHAPTER_NUMBER": None,
			"SPEAKER": None,
			"TEXT_TYPE": None,
		}

		for row in csvreader:
			type = row['Type']
			value = row['Text']

			if type in current_data:
				current_data[type] = value
			elif "TEXT" in type:
				if current_data["SPEAKER"] != None and type != 'TEXT_SPEECH':
					current_data["SPEAKER"] = None
				last_row = result_list[-1] if len(result_list) > 0 else None
				if last_row != None \
						and (last_row["TEXT_TYPE"] == type == 'TEXT_POEM' \
						or last_row["TEXT_TYPE"] == type == 'TEXT_LETTER'):
					last_row["TEXT"] += ' ' + value
				elif last_row != None and last_row["TEXT_TYPE"] == type == 'TEXT_SPEECH'\
						and current_data["SPEAKER"] == last_row["SPEAKER"]:
					last_row["TEXT"] += ' ' + value
				else:
					current_data["TEXT"] = value
					current_data["TEXT_TYPE"] = type
					result_list.append(dict(current_data))

	process_enrichments(result_list)

	with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
		fieldnames = result_list[0].keys()
		csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		csvwriter.writeheader()
		for item in result_list:
			csvwriter.writerow(item)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python script.py input_file.csv")
		sys.exit(1)
	
	input_file = sys.argv[1]
	output_file = 'output/' + os.path.splitext(os.path.basename(input_file))[0] + '.csv'
	process_csv(input_file, output_file)
