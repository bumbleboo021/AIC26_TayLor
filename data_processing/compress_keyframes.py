import os
import glob
import json
import webdataset as wds
from config import BASE_DIR

KEYFRAMES_DIRS = glob.glob(os.path.join(BASE_DIR, "Keyframes_*"))

def pack_keyframes_to_wds(keyframes_dir, output_wds_dir, dict_dir, max_size=1e9, max_count=10000):
 
    os.makedirs(output_wds_dir, exist_ok=True)
    os.makedirs(dict_dir, exist_ok=True)
    folder_name = os.path.basename(keyframes_dir)
    lxx_prefix = folder_name.split("_")[1]


    index_map = {lxx_prefix: {}}
    shard_pattern = os.path.join(output_wds_dir, f"{lxx_prefix}_keyframes-%02d.tar")
    shard_pattern = os.path.relpath(shard_pattern, os.getcwd()).replace('\\', '/')
    image_files = sorted([f for f in os.listdir(keyframes_dir) if f.endswith('.jpg')])
    
    if not image_files:
        print(f"[Cảnh báo] Không có ảnh nào trong {keyframes_dir}")
        return

    with wds.ShardWriter(shard_pattern, maxsize=max_size, maxcount=max_count) as sink:
        for img_filename in image_files:
            img_path = os.path.join(keyframes_dir, img_filename)
            base_name = os.path.splitext(img_filename)[0]

            try:
                parts = base_name.split('_')
                if len(parts) == 3:
                    file_lxx, vxx_prefix, n_keyframe_str = parts
                    n_keyframe = int(n_keyframe_str)
                else:
                    print(f"[Bỏ qua] Sai format tên file (cần Lxx_Vxx_N.jpg): {img_filename}")
                    continue
            except ValueError:
                print(f"[Bỏ qua] Không thể đọc số keyframe từ: {img_filename}")
                continue

            if vxx_prefix not in index_map[lxx_prefix]:
                index_map[lxx_prefix][vxx_prefix] = {}

            sample_key = base_name       
            index_map[lxx_prefix][vxx_prefix][str(n_keyframe)] = {
                "tar_key": sample_key,
                "original_file": img_filename
            }
            
            with open(img_path, "rb") as stream:
                image_bytes = stream.read()
                
            sample = {
                "__key__": sample_key,
                "jpg": image_bytes,
                "json": json.dumps({
                    "L_id": file_lxx, 
                    "V_id": vxx_prefix,
                    "n_keyframes": n_keyframe
                }).encode('utf-8')
            }
            
            sink.write(sample)

    index_file_path = os.path.join(dict_dir, f"{lxx_prefix}.json")
    with open(index_file_path, "w", encoding='utf-8') as f:
        json.dump(index_map, f, indent=4)

    print(f"[Thành công] Đã pack {lxx_prefix} và lưu bản đồ index tại: {index_file_path}")


if __name__ == '__main__':
    if not KEYFRAMES_DIRS:
        print(f"Không tìm thấy thư mục Keyframes_* nào trong {BASE_DIR}")
        
    for keyframes_dir in KEYFRAMES_DIRS:
        folder_name = os.path.basename(keyframes_dir)
  
        OUTPUT_DIR = os.path.join(BASE_DIR, f"WDS_Tar")
        DICT_DIR = os.path.join(BASE_DIR, f"WDS_Dict")
        
        print(f"\nĐang xử lý thư mục: {keyframes_dir}...")
        pack_keyframes_to_wds(keyframes_dir, OUTPUT_DIR, DICT_DIR)