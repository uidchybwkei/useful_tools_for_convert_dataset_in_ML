import json

remove_names = {'Potato leaf', 'Tomato two spotted spider mites leaf'}
input_json = 'train_labels_coco.json'
output_json = 'train_.json'

with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. 查找需要删除的类别ID
target_cat_ids = {cat['id'] for cat in data['categories'] if cat['name'] in remove_names}

# 2. 移除categories中这些类别
data['categories'] = [cat for cat in data['categories'] if cat['id'] not in target_cat_ids]

# 3. 移除相关annotation，同时记录涉及images
target_img_ids = set()
filtered_annotations = []
for ann in data['annotations']:
    if ann['category_id'] in target_cat_ids:
        target_img_ids.add(ann['image_id'])
    else:
        filtered_annotations.append(ann)
data['annotations'] = filtered_annotations

# 4. 移除纯属被删类别的images（只保留还有其它annotation的images）
ann_img_ids = {ann['image_id'] for ann in data['annotations']}
data['images'] = [img for img in data['images'] if img['id'] in ann_img_ids]

# 5. 导出到新文件
data['info']['description'] += ' (去除指定类别)'
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已生成: {output_json}')
