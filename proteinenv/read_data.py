import os
import pandas as pd


'''将数据转化为csv格式并生成对应的图'''

input_folder = r'D:\mypython\math_modeling\protein\data\file'
output_folder = r'D:\mypython\math_modeling\protein\data\csv'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, filename)
    
    try:
        output_file_path = os.path.join(output_folder, filename + '.csv')
        
        # 读取数据并转换为csv格式
        data = pd.read_csv(input_file_path, sep=';', header=0)
        data.to_csv(output_file_path, index=False)
        print(f"{filename} 已成功转换为CSV格式。")
    except Exception as e:
        print(f"转换 {filename} 时出错: {e}")

print("所有文件已处理。")