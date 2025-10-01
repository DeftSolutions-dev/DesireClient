import os
import hashlib
import json

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def collect_hashes(root_dir, target_folders):
    hashes = {}
    
    for item in os.listdir(root_dir):
        file_path = os.path.join(root_dir, item)
        if os.path.isfile(file_path):
            try:
                hashes[file_path] = compute_md5(file_path)
            except Exception as e:
                hashes[file_path] = f"Error: {str(e)}"
    
    for target_folder in target_folders:
        folder_path = os.path.join(root_dir, target_folder)
        if os.path.exists(folder_path):
            for subdir, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(subdir, file)
                    try:
                        hashes[file_path] = compute_md5(file_path)
                    except Exception as e:
                        hashes[file_path] = f"Error: {str(e)}"
    
    return hashes

target_folders = ['RustClient_Data', 'workshop', 'bundles', 'cfg']
all_hashes = collect_hashes('.', target_folders)

with open('files_hashes.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_hashes, json_file, ensure_ascii=False, indent=4)

print("JSON-файл 'files_hashes.json' создан с путями и MD5-хэшами для локальных файлов и папок RustClient_Data и workshop.")