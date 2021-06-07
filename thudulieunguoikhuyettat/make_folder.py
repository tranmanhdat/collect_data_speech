import os
import shutil
import sys

root = sys.argv[1]
folders = os.listdir(root)
for folder in folders:
    files = os.listdir(os.path.join(root, folder))
    for file in files:
        folder_name = file.split(".")[0]
        path_folder = os.path.join(os.path.join(root,folder), folder_name)
        os.makedirs(os.path.join(os.path.join(root,folder), folder_name))
        shutil.move(os.path.join(os.path.join(root,folder), file), os.path.join(os.path.join(os.path.join(root,folder), folder_name),file))