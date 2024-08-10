import os
import pandas as pd

'''将Q3_compare所得数据合并到一个文件'''
def merge_excels(output_dir, final_output):
    writer = pd.ExcelWriter(final_output)
    for file in os.listdir(output_dir):
        if file.startswith('diff_') and file.endswith('.xlsx'):
            file_path = os.path.join(output_dir, file)
            df = pd.read_excel(file_path, sheet_name=None)
            for sheet_name, data in df.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
    writer._save()

# Merge all individual Excel files into one
merge_excels(r'G:\protein_in_G\temp', r'G:\protein_in_G\result\nodes_diff.xlsx')