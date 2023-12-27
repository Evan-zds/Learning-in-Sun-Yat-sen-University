import os
import shutil

source_path = r'E:\Data\光合有效辐射吸收比FAPAR0.05D'
destination_path = r'I:\DATA\植被\光和有效辐射吸收比FAPAR0.05D'
for year_folder in os.listdir(source_path):
    year_folder_path = os.path.join(source_path, year_folder)
    year_files_list = []
    for file in os.listdir(year_folder_path):
        if file.startswith('FAPAR'):
            year_files_list.append(os.path.join(year_folder_path, file))

    destination_year_folder = os.path.join(destination_path, year_folder)

    if not os.path.exists(destination_year_folder):
        os.makedirs(destination_year_folder)

    for file in year_files_list:
        file_name = os.path.basename(file)
        destination_file = os.path.join(destination_year_folder, file_name)
        shutil.copy(file, destination_file)

print('done!')
