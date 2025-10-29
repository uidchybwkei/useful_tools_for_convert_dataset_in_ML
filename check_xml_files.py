import os
import xml.etree.ElementTree as ET

xml_dir = r"CWC_dataset/VOC_xml/Annotions"

print("开始检查所有 XML 文件...")
error_files = []
success_count = 0
total_count = 0

files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
print(f"共找到 {len(files)} 个 XML 文件")

for file in files:
    total_count += 1
    filepath = os.path.join(xml_dir, file)
    try:
        tree = ET.parse(filepath)
        success_count += 1
        if total_count % 100 == 0:
            print(f"已检查 {total_count}/{len(files)} 个文件...")
    except ET.ParseError as e:
        print(f"\n❌ 错误文件: {file}")
        print(f"   错误信息: {e}")
        print(f"   完整路径: {filepath}\n")
        error_files.append(file)
    except Exception as e:
        print(f"\n❌ 其他错误: {file} - {e}\n")
        error_files.append(file)

print(f"\n检查完成！")
print(f"✓ 成功解析: {success_count} 个文件")
print(f"✗ 错误文件: {len(error_files)} 个")

if error_files:
    print("\n错误文件列表:")
    for f in error_files:
        print(f"  - {f}")

