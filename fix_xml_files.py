import os
import re

xml_dir = r"PDT_dataset/LL/VOC_xml/Annotations"
backup_dir = r"PDT_dataset/LL/VOC_xml/Annotations_backup"

# 创建备份目录
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
    print(f"已创建备份目录: {backup_dir}")

fixed_count = 0
error_count = 0
total_count = 0

print(f"开始修复 XML 文件...\n")

for file in os.listdir(xml_dir):
    if not file.endswith('.xml'):
        continue
    
    total_count += 1
    filepath = os.path.join(xml_dir, file)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有多余的 </annotation> 标签
        # 使用正则表达式匹配结尾的多个 </annotation>
        pattern = r'(</annotation>)(</annotation>)+\s*$'
        
        if re.search(pattern, content):
            # 备份原文件
            backup_path = os.path.join(backup_dir, file)
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 修复：将多个 </annotation> 替换为单个
            fixed_content = re.sub(pattern, r'\1', content)
            
            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            # 统计替换了多少个
            original_count = content.count('</annotation>')
            fixed_count_in_file = fixed_content.count('</annotation>')
            removed = original_count - fixed_count_in_file
            
            print(f"✓ 修复: {file} (移除了 {removed} 个多余的 </annotation> 标签)")
            fixed_count += 1
        
        if total_count % 500 == 0:
            print(f"进度: 已检查 {total_count} 个文件...")
            
    except Exception as e:
        print(f"✗ 处理失败: {file} - {e}")
        error_count += 1

print(f"\n{'='*60}")
print(f"修复完成！")
print(f"{'='*60}")
print(f"总计检查: {total_count} 个文件")
print(f"✓ 成功修复: {fixed_count} 个文件")
print(f"✗ 处理失败: {error_count} 个文件")
print(f"\n备份文件保存在: {backup_dir}")

