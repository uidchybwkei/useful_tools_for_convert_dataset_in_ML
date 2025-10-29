import os
import json
import xml.etree.ElementTree as ET

# VOC XML 文件夹路径
xml_dir = r"PDT_dataset/LL/VOC_xml/Annotations"
output_json = "total.json"

# 类别相关结构
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

images = []
annotations = []
img_filename_to_id = {}
current_img_id = 0
annotation_id = 0

# 遍历 xml_dir 下所有 xml 文件
for file in os.listdir(xml_dir):
    if not file.endswith('.xml'):
        continue
    filepath = os.path.join(xml_dir, file)
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    if filename not in img_filename_to_id:
        img_filename_to_id[filename] = current_img_id
        images.append({
            "id": current_img_id,
            "file_name": filename,
            "width": width,
            "height": height,
        })
        current_img_id += 1
    image_id = img_filename_to_id[filename]

    # 遍历每个 object
    for obj in root.findall('object'):
        class_name = obj.find('name').text.strip()
        category_id = get_category_id(class_name)
        bndbox = obj.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        bbox = [xmin, ymin, xmax-xmin, ymax-ymin]
        area = bbox[2] * bbox[3]
        annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": bbox,
            "area": area,
            "iscrowd": 0,
            "segmentation": []
        }
        annotations.append(annotation)
        annotation_id += 1

# 构造COCO格式
coco_data = {
    "info": {
        "year": "2025",
        "version": "1.0",
        "description": "Converted from VOC XML dataset",
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
    json.dump(coco_data, fo, ensure_ascii=False, indent=2)

print(f"已完成！已生成 {output_json}")

print("\n'classes': (", end='')
for idx, cat in enumerate(categories):
    if idx != 0:
        print(", ", end='')
    print(f"'{cat['name']}'", end='')
print(")\n")

print(categories)
