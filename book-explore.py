import csv
import sys
import random
from collections import defaultdict

def explore_csv(csv_filename):
	class_texts = defaultdict(list)

	with open(csv_filename, 'r', encoding='utf-8') as csvfile:
		csv_reader = csv.DictReader(csvfile)
		
		for row in csv_reader:
			text = row['Text'][:50]  # Truncate text to 50 characters
			class_name = row['Class']
			if text:  # Skip empty text
				class_texts[class_name].append(text)
	
	print("Exploring Random 5 Elements from Each Class:")
	for class_name, texts in class_texts.items():
		print(f"- {class_name}")
		if texts:
			random_texts = random.sample(texts, min(5, len(texts)))
			for text in random_texts:
				print(f"  - {text}")
		else:
			print("  - No texts available")
		print()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python script_name.py csv_filename")
	else:
		csv_filename = sys.argv[1]
		explore_csv(csv_filename)
