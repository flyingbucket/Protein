import pandas as pd
import multiprocessing as mp
import os

'''计算相邻两年节点度的变化'''

path_to_Q3DC=r'G:\protein_in_G\result\Q3DC.xlsx'
temp_path=r'G:\protein_in_G\temp'
merge_path=r'G:\protein_in_G\result'

sheet_dict=pd.read_excel(path_to_Q3DC,sheet_name=None,header=0)
names=[]
sheets=[]
i=2012
for sheet_name in sheet_dict.keys():
    i+=1
    name='year'+str(i)
    globals()[name]=sheet_dict[sheet_name]
    sheets.append(globals()[name])
    names.append(name)
print(len(sheets))
print(names)
def process_sheets(j, sheets, names):
    former = sheets[j]
    latter = sheets[j + 1]

    former.set_index('Node', inplace=True)
    latter.set_index('Node', inplace=True)

    merged = pd.merge(former, latter, left_index=True, right_index=True,
                      how='outer', suffixes=('_former', '_latter'))
    merged.fillna(0, inplace=True)
    merged.columns = ['old_d', 'new_d']
    merged['diff'] = merged['new_d'] - merged['old_d']

    m_name = names[j] + '-' + names[j + 1]
    
    merged.to_excel(temp_path, sheet_name=m_name, index=True)

def merge_excels(output_dir, final_output):
    writer = pd.ExcelWriter(final_output)
    for file in os.listdir(output_dir):
        if file.startswith('diff_') and file.endswith('.xlsx'):
            file_path = os.path.join(output_dir, file)
            df = pd.read_excel(file_path, sheet_name=None)
            for sheet_name, data in df.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
    writer._save()

if __name__ == '__main__':
    mp.freeze_support()
    # Assuming sheets and names are already defined
    num_processes = mp.cpu_count()  # Use the number of available CPU cores
    pool = mp.Pool(processes=num_processes)

    # Create a list of arguments for each process
    args = [(j, sheets, names) for j in range(11)]

    # Use pool.starmap to apply the function to each set of arguments
    pool.starmap(process_sheets, args)

    pool.close()
    pool.join()

    # Merge all individual Excel files into one
    merge_excels(temp_path, merge_path)