import json
from collections import defaultdict

def count_images_per_category(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 获取类别id到名字映射
    data_cats = {cat['id']:cat['name'] for cat in data['categories']}

    # 每个类别统计唯一image_id集合
    cat_imgset = defaultdict(set)
    for ann in data['annotations']:
        cat_imgset[ann['category_id']].add(ann['image_id'])

    # 打印统计结果
    print(f'== {json_path} ==')
    for catid, catname in data_cats.items():
        print(f"类别: {catname:30} | 图像数: {len(cat_imgset[catid])}")
    print()

if __name__ == '__main__':
    count_images_per_category('train.json')
    count_images_per_category('test.json')
