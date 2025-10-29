import os

# 要操作的目录
folder = '/Users/elijah/Desktop/PlantDoc-Object-Detection-Dataset-master/TRAIN'

cnt = 0
for filename in os.listdir(folder):
    if filename.lower().endswith('.xml'):
        file_path = os.path.join(folder, filename)
        try:
            os.remove(file_path)
            cnt += 1
            print(f'已删除: {file_path}')
        except Exception as e:
            print(f'删除失败: {file_path}，原因: {e}')
print(f'共删除 {cnt} 个xml文件。')
