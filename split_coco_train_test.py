import json
import random
from collections import defaultdict

# 输入和输出文件
input_json = 'total.json'
train_json = 'train.json'
test_json = 'test.json'

# 加载数据
def load_coco(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

coco = load_coco(input_json)

# 统计每张图片、每类包含的图片
dict_imgid_to_catids = defaultdict(set)
dict_catid_to_imgids = defaultdict(set)
for ann in coco['annotations']:
    imgid = ann['image_id']
    catid = ann['category_id']
    dict_imgid_to_catids[imgid].add(catid)
    dict_catid_to_imgids[catid].add(imgid)

all_imgids = list(dict_imgid_to_catids.keys())
random.shuffle(all_imgids)

# 按类别统计每类总图片数量，计算应属于test的目标数量
target_test_num = {}
for cat in coco['categories']:
    cid = cat['id']
    total = len(dict_catid_to_imgids[cid])
    n_test = max(1, int(total * 0.15))  # 至少留1张
    target_test_num[cid] = n_test

# 贪心全局分配，每遍历一张图片，优先分给test（前提是它包含的所有类别都未超目标）
imgid_in_test = set()
imgid_in_train = set()
cat_test_count = defaultdict(int)
cat_train_count = defaultdict(int)

for imgid in all_imgids:
    cats = dict_imgid_to_catids[imgid]
    can_test = all(cat_test_count[cid] < target_test_num[cid] for cid in cats)
    if can_test:
        imgid_in_test.add(imgid)
        for cid in cats:
            cat_test_count[cid] += 1
    else:
        imgid_in_train.add(imgid)
        for cid in cats:
            cat_train_count[cid] += 1

# 构造images/annotations
imgid_to_img = {img['id']: img for img in coco['images']}
train_images = [imgid_to_img[iid] for iid in imgid_in_train]
test_images = [imgid_to_img[iid] for iid in imgid_in_test]

train_imgid_set = set(img['id'] for img in train_images)
test_imgid_set = set(img['id'] for img in test_images)
train_annotations = [ann for ann in coco['annotations'] if ann['image_id'] in train_imgid_set]
test_annotations = [ann for ann in coco['annotations'] if ann['image_id'] in test_imgid_set]

# 写回文件（包含完整结构）
def save_coco(coco, imglist, annlist, outjson):
    outdict = {
        'info': coco['info'],
        'licenses': coco['licenses'],
        'categories': coco['categories'],
        'images': imglist,
        'annotations': annlist
    }
    with open(outjson, 'w', encoding='utf-8') as f:
        json.dump(outdict, f, ensure_ascii=False, indent=2)

save_coco(coco, train_images, train_annotations, train_json)
save_coco(coco, test_images, test_annotations, test_json)

# 打印每类分布汇总
def print_stat():
    def get_class_name(cid):
        for cat in coco['categories']:
            if cat['id']==cid:
                return cat['name']
        return str(cid)
    stat = lambda cid, imset: len([iid for iid in dict_catid_to_imgids[cid] if iid in imset])
    print('== train.json ==')
    for cat in coco['categories']:
        cname = cat['name']
        cid = cat['id']
        n = stat(cid, imgid_in_train)
        print(f'类别: {cname}  | 图像数: {n}')
    print('\n== test.json ==')
    for cat in coco['categories']:
        cname = cat['name']
        cid = cat['id']
        n = stat(cid, imgid_in_test)
        print(f'类别: {cname}  | 图像数: {n}')

print_stat()
print(f"划分完成！训练集{len(train_images)}张，测试集{len(test_images)}张。")
