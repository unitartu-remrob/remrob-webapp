import json
import csv
import os
import re

test_name = 'rviz_load_test'
# set to True if the file prefix is {num}m_ (for network speed tests)
m_prefix = False

log_dir = f'data/{test_name}'
csv_file = f'output/{test_name}.csv'

def sort_key(filename):
    match = re.search(r'^(\d+)(m)?', filename)
    if match:
        numeric_part = int(match.group(1))
    else:
        numeric_part = float('inf')
    return numeric_part

json_files = sorted(
    [f for f in os.listdir(log_dir) if f.endswith('.json')],
    key=sort_key
)
headers = ['index']


data = []
for file in json_files:
    file_path = os.path.join(log_dir, file)
    with open(file_path, 'r') as f:
        content = json.load(f)
        match = re.search(r'^(\d+)(m)?', file)
        if match:
            if m_prefix and match.group(2):
                index_value = match.group(0)
            else:
                index_value = match.group(1)
        else:
            index_value = "Unknown"
        content['index'] = index_value
        data.append(content)

if data:
    keys = ['index'] + [key for key in data[0].keys() if key != 'index']
else:
    keys = ['index']

with open(csv_file, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=keys)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f'Data written to {csv_file}.')
