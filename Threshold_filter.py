import json
import matplotlib.pyplot as plt
import numpy as np

input_file = 'instances_default.json'
output_file = 'threshold_filtered.json'
threshold = 1.8

with open(input_file) as f:
    data = json.load(f)

for category in data['categories']:
    if category['name'] == 'Flower':
        flower_id = category['id']

all_area = {}
for annotation in data['annotations']:
    if annotation['category_id'] == flower_id:
        if annotation['image_id'] not in all_area:
            all_area[annotation['image_id']] = []

        all_area[annotation['image_id']].append(annotation['area'])


min_area = {}
for image_id in all_area:
    min_area[image_id] = min(all_area[image_id])


filtered_annotations = []
count = {}
for annotation in data['annotations']:
    if annotation['category_id'] == flower_id:
        if annotation['area'] <  min_area[annotation['image_id']] * threshold:
            count[annotation['image_id']] = count.get(annotation['image_id'], 0) + 1
            filtered_annotations.append(annotation)

data['annotations'] = filtered_annotations

print(len(filtered_annotations))

with open(output_file, 'w') as f:
    json.dump(data, f)