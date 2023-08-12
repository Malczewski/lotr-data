import unicodedata

with open('data/characters.txt', 'r') as file:
	__characters_fullnames = [line.rstrip("\n") for line in file.readlines()]

__characters_names = []
for name in __characters_fullnames:
	words = name.strip().split() 
	for word in words:
		if not word[0].islower():
			__characters_names.append(word)

__characters_names = set(__characters_names)
__characters_names = list(__characters_names)
__characters_names = [item for item in __characters_names if item not in ['I', 'II', 'III', 'IV', 'V', 'VI', 'Great', 'Eagle']]

def is_substring_in_string(substring, text):
	# Normalize both the substring and text to NFD form
	normalized_substring = unicodedata.normalize('NFD', substring)
	normalized_text = unicodedata.normalize('NFD', text)

	return normalized_substring in normalized_text

def characters_enrichment(row):
	text = row["text"]
	result = []

	# Check for full name matches
	for full_name in __characters_fullnames:
		if is_substring_in_string(full_name, text):
			result.append(full_name)

	# Check for partial name matches
	for name in __characters_names:
		if any(name == word for word in text.split()):
			# Check if the name is not part of any full name
			if not any(name in full_name for full_name in result):
				result.append(name)
	row["characters"] = ",".join(list(set(result)))


with open('data/locations.txt', 'r') as file:
	__locations = [line.rstrip("\n") for line in file.readlines()]

def location_enrichment(row):
	text = row["text"]
	result = []

	for location in __locations:
		if is_substring_in_string(location, text):
			result.append(location)

	row["locations"] = ",".join(list(set(result)))

with open('data/artifacts.txt', 'r') as file:
	__artifacts = [line.rstrip("\n") for line in file.readlines()]

def artifact_enrichment(row):
	text = row["text"]
	result = []

	for location in __artifacts:
		if is_substring_in_string(location, text):
			result.append(location)

	row["artifacts"] = ",".join(list(set(result)))
