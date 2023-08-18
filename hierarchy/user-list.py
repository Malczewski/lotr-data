import csv
import random
import sys
from unidecode import unidecode

random.seed(42)

def generate_email(first_name, last_name, index, domain_name):
	email = f"{first_name.replace(' ', '.').lower()}.{last_name.replace(' ', '.').lower()}_{index}@{domain_name}"
	return unidecode(email)

def main(num_rows, output_path, domain_name):
	# Read last names from the file
	with open('last_names.txt', 'r', encoding='utf-8') as f:
		last_names = list(set([line.strip() for line in f]))

	# Read character data from the CSV file
	with open('characters.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		characters = list(reader)

	# Create a new CSV file for output
	with open(output_path, 'w', newline='', encoding='utf-8') as f:
		fieldnames = ['first name', 'last name', 'email', 'gender', 'race']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()

		main_characters = []
		for index in range(num_rows):
			random_character = random.choice(characters)
			name_parts = random_character['name'].split()

			if len(name_parts) == 1:
				first_name = name_parts[0]
				last_name = ''
			else:
				first_name = name_parts[0]
				last_name = ' '.join(name_parts[1:])
				if first_name + ' ' + last_name in main_characters:
					last_name = ''
				else:
					main_characters.append(first_name + ' ' + last_name)

			if last_name == '':
				last_name = random.choice(last_names)

			email = generate_email(first_name, last_name, index + 1, domain_name)

			writer.writerow({
				'first name': first_name,
				'last name': last_name,
				'email': email,
				'gender': random_character['gender'],
				'race': random_character['race']
			})

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Usage: python script.py <num_rows> <output_file> [<domain_name>]")
	else:
		num_rows = int(sys.argv[1])
		output_file = sys.argv[2]
		domain_name = 'cxstudio.app' if len(sys.argv) < 4 else sys.argv[3]
		main(num_rows, output_file, domain_name)