import csv
import json
from collections import defaultdict

# 类别字典，需根据实际情况补充和修改！
category_name_to_id = {}
categories = []
current_cat_id = 0

def get_category_id(class_name):
    global current_cat_id
    if class_name not in category_name_to_id:
        category_name_to_id[class_name] = current_cat_id
        categories.append({
            "id": current_cat_id,
            "name": class_name,
            "supercategory": "leaf"
        })
        current_cat_id += 1
    return category_name_to_id[class_name]

csv_file = "train_labels.csv"
output_json = "train_labels_coco.json"

images = []
annotations = []
img_filename_to_id = {}
current_img_id = 0
annotation_id = 0

with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row['filename']
        width = int(row['width'])
        height = int(row['height'])
        class_name = row['class']
        bbox = [
            int(row['xmin']),
            int(row['ymin']),
            int(row['xmax']) - int(row['xmin']),
            int(row['ymax']) - int(row['ymin']),
        ]
        
        if filename not in img_filename_to_id:
            # 新图片，分配一个ID
            img_filename_to_id[filename] = current_img_id
            images.append({
                "id": current_img_id,
                "file_name": filename,
                "width": width,
                "height": height,
                # 按需可加更多字段（如date_captured等）
            })
            current_img_id += 1
        
        category_id = get_category_id(class_name)
        annotations.append({
            "id": annotation_id,
            "image_id": img_filename_to_id[filename],
            "category_id": category_id,
            "bbox": bbox,
            "area": bbox[2] * bbox[3],
            "iscrowd": 0,
            "segmentation": []
        })
        annotation_id += 1

# 构造COCO格式
data = {
    "info": {
        "year": "2025",
        "version": "1.0",
        "description": "Converted from train_labels.csv",
        "contributor": "",
        "date_created": "",
    },
    "licenses": [
        {
            "id": 1,
            "url": "",
            "name": ""
        }
    ],
    "categories": categories,
    "images": images,
    "annotations": annotations
}

with open(output_json, 'w', encoding='utf-8') as fo:
    json.dump(data, fo, ensure_ascii=False, indent=2)

print(f"Done! 已生成 {output_json}")

# 输出所有类别名称，以 tuple/元组字符串形式输出
print("\n'classes': (", end='')
for idx, cat in enumerate(categories):
    if idx != 0:
        print(", ", end='')
    print(f"'{cat['name']}'", end='')
print(")\n")

print(categories)

