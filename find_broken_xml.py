import os
import xml.etree.ElementTree as ET

# VOC XML 文件夹路径
xml_dir = r"PDT_dataset/LL/VOC_xml/Annotations"

print(f"开始检查 {xml_dir} 下的所有 XML 文件...\n")

error_files = []
success_count = 0
total_count = 0

# 获取所有xml文件
xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
total_files = len(xml_files)
print(f"共找到 {total_files} 个 XML 文件\n")

# 遍历所有xml文件
for file in xml_files:
    total_count += 1
    filepath = os.path.join(xml_dir, file)
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # 尝试读取基本信息
        filename = root.find('filename')
        size = root.find('size')
        
        if filename is None:
            print(f"⚠️  文件 {file} 缺少 <filename> 标签")
            error_files.append((file, "缺少filename标签"))
            continue
            
        if size is None:
            print(f"⚠️  文件 {file} 缺少 <size> 标签")
            error_files.append((file, "缺少size标签"))
            continue
        
        width = size.find('width')
        height = size.find('height')
        
        if width is None or height is None:
            print(f"⚠️  文件 {file} 缺少 width 或 height 标签")
            error_files.append((file, "缺少宽高标签"))
            continue
        
        success_count += 1
        
        # 每处理100个文件显示进度
        if total_count % 500 == 0:
            print(f"进度: {total_count}/{total_files} ({success_count} 成功, {len(error_files)} 错误)")
            
    except ET.ParseError as e:
        print(f"\n❌ XML解析错误!")
        print(f"   文件名: {file}")
        print(f"   错误信息: {e}")
        print(f"   完整路径: {filepath}")
        print()
        error_files.append((file, str(e)))
        
    except Exception as e:
        print(f"\n❌ 其他错误!")
        print(f"   文件名: {file}")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {e}")
        print()
        error_files.append((file, str(e)))

print("\n" + "="*60)
print("检查完成！")
print("="*60)
print(f"✓ 成功解析: {success_count} 个文件")
print(f"✗ 错误文件: {len(error_files)} 个")
print(f"总计: {total_count} 个文件")

if error_files:
    print("\n错误文件详细列表:")
    print("-"*60)
    for idx, (file, error) in enumerate(error_files, 1):
        print(f"{idx}. {file}")
        print(f"   错误: {error}")
        print()
else:
    print("\n🎉 所有文件都正常！")

