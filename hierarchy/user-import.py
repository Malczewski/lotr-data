import csv
import sys
import math

def main(input_file, count, output_file_prefix, limit):
	with open(input_file, 'r', newline='', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		data = list(reader)

	num_files = math.ceil(count / limit)

	for file_idx in range(num_files):
		start_idx = file_idx * limit
		end_idx = min((file_idx + 1) * limit, count)

		output_data = []
		for idx in range(start_idx, end_idx):
			row = data[idx]
			first_name = row['first name']
			last_name = row['last name']
			email = row['email']
			race = row['race']

			output_row = {
				'First Name': first_name,
				'Last Name': last_name,
				'Email Address': email,
				'Password': '1234567890Aa!',
				'License Type': 'Report Consumer',
				#'Groups': '',
				'Race': race
			}
			output_data.append(output_row)

		output_filename = f"{output_file_prefix}_{file_idx + 1}.csv"
		with open(output_filename, 'w', newline='', encoding='utf-8') as f:
			fieldnames = ['First Name', 'Last Name', 'Email Address', 'Password', 'License Type', 'Race']
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(output_data)

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Usage: python script.py <input_file> <count> <output_file_prefix> <limit>")
	else:
		input_file = sys.argv[1]
		count = int(sys.argv[2])
		output_file_prefix = sys.argv[3]
		limit = int(sys.argv[4])

		main(input_file, count, output_file_prefix, limit)
