import sys
import csv
import os
from unidecode import unidecode

class Node:
	def __init__(self, realm, gender, race, name, fullname=None):
		self.realm = realm
		self.gender = gender
		self.race = race
		self.name = name
		self.fullname = fullname
		
class Character:
	def __init__(self, gender, race, name, fullname, email):
		self.gender = gender
		self.race = race
		self.name = name
		self.fullname = fullname
		self.email = email

def gather_unique_values(data: list, include_fullname: bool):
	unique_values = {
		'Gender': set(),
		'Race': set(),
		'Name': set(),
	}

	if include_fullname:
		unique_values['Fullname'] = set()

	for char in data:
		unique_values['Gender'].add(char.gender)
		unique_values['Race'].add(char.race)
		unique_values['Name'].add(char.name)
		
		if include_fullname and char.fullname:
			unique_values['Fullname'].add(char.fullname)
	
	return unique_values

def add_char_to_dict(dict: dict, key: tuple, char: Character):
	if key in dict:
		dict[key].append(char)
	else:
		dict[key] = [char]

def get_existing_data_map(selected_data: list, include_fullname: bool):
	data_dict = {}

	for char in selected_data:
		if (include_fullname):
			add_char_to_dict(data_dict, (char.gender, char.race, char.name, char.fullname), char)
		add_char_to_dict(data_dict, (char.gender, char.race, char.name), char)
		add_char_to_dict(data_dict, (char.gender, char.race), char)
		add_char_to_dict(data_dict, (char.gender,), char)

	return data_dict

def generate_hierarchy(unique_values, selected_data, include_fullname):
	data_dict = get_existing_data_map(selected_data, include_fullname)
	hierarchy = []

	realm = 'Middle Earth'
	hierarchy.append(Node(realm, None, None, None))

	for gender in sorted(unique_values['Gender']):
		fullkey = (gender,)
		if fullkey not in data_dict:
			continue
		hierarchy.append(Node(realm, gender, None, None))

		for race in sorted(unique_values['Race']):
			fullkey = (gender, race)
			if fullkey not in data_dict:
				continue
			hierarchy.append(Node(realm, gender, race, None))

			for name in sorted(unique_values['Name']):
				fullkey = (gender, race, name)
				if fullkey not in data_dict:
					continue
				hierarchy.append(Node(realm, gender, race, name))

				if include_fullname:
					for fullname in sorted(unique_values['Fullname']):
						fullkey = (gender, race, name, fullname)
						if fullkey not in data_dict:
							continue
						hierarchy.append(Node(realm, gender, race, name, fullname))
	
	return hierarchy

def main(input_file, count, output_file, mode, include_fullname):
	data = []

	with open(input_file, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			first_name = row['first name']
			last_name = row['last name']
			full_name = f"{first_name} {last_name}"
			data.append(Character(row['gender'], row['race'], first_name, full_name, row['email']))

	selected_data = data[:count]

	unique_values = gather_unique_values(selected_data, include_fullname)
	hierarchy = generate_hierarchy(unique_values, selected_data, include_fullname)
	data_map = get_existing_data_map(selected_data, include_fullname)

	with open(output_file, 'w', newline='', encoding='utf-8') as f:
		used_fields = ['Realm', 'Gender', 'Race', 'Name']
		if include_fullname:
			used_fields.append('Fullname')
		if mode == "structure":
			fieldnames = used_fields
		elif mode == "filters" or mode == "users":
			fieldnames = ['key', 'value']

		writer = csv.DictWriter(f, fieldnames=fieldnames)

		if mode == "structure":
			writer.writeheader()
			for node in hierarchy:
				row = {
					'Realm': node.realm,
					'Gender': node.gender,
					'Race': node.race,
					'Name': node.name
				}

				if include_fullname:
					row['Fullname'] = node.fullname

				writer.writerow(row)
		elif mode == "filters" or mode == 'users':
			path_value = ' --> '.join(used_fields)
			if mode == 'filters':
				writer.writerow({'key': 'Organization Hierarchy (DO NOT EDIT)','value': '<CP/WORKSPACE>'})
				writer.writerow({'key': path_value,'value': '<PROJECT_NAME>'})
			else:
				writer.writerow({'key': path_value, 'value': 'Studio Email Address'})

			for node in hierarchy:
				values = [value for value in (node.gender, node.race, node.name, node.fullname if include_fullname else None) if value is not None]
				path = ' --> '.join([node.realm] + values)
				key = tuple(values)

				chars = data_map[key] if len(values) > 2 else None
				if mode == "filters":
					if chars:
						unique_words = set()
						for character in chars:
							unique_words.update(character.fullname.split())
						filter = ", ".join(sorted([unidecode(value) for value in unique_words]))
					else:
						filter = 'ALL'

					row = {
						'key': path,
						'value': filter
					}
				else:
					if chars:
						emails = [char.email for char in chars]
					else:
						emails = []
					row = {
						'key': path,
						'value': ','.join(sorted(emails))
					}
				writer.writerow(row)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print("Usage: python script.py <input_file> <count> [--all | <output_file> <mode>] [--fullname]")
		print("Mode options: structure, filters, users")
	else:
		input_file = sys.argv[1]
		count = int(sys.argv[2])

		include_fullname = False
		if sys.argv[-1] == "--fullname":
			include_fullname = True

		if sys.argv[3] == '--all':
			filebase = os.path.splitext(input_file)[0]
			main(input_file, count, f"{filebase}_{count}_structure.csv", 'structure', include_fullname)
			main(input_file, count, f"{filebase}_{count}_filters.csv", 'filters', include_fullname)
			main(input_file, count, f"{filebase}_{count}_users.csv", 'users', include_fullname)
		else:
			output_file = sys.argv[3]
			mode = sys.argv[4]
			if mode not in ["structure", "filters", "users"]:
				print("Invalid mode. Mode options: structure, filters, users")
				sys.exit(1)

			main(input_file, count, output_file, mode, include_fullname)