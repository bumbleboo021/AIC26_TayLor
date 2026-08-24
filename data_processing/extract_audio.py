import os
import glob
import subprocess
import json
import cv2
import pandas as pd
import webdataset as wds
from decord import VideoReader, cpu

VIDEO_DIR = "/content/video" ## Cần chỉnh sửa
CSV_DIR = "/content/mapkeyframes" ## Cần chỉnh sửa
AUDIO_DIR = ""
os.makedirs(AUDIO_DIR, exist = True)

video_paths = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))
video_paths.sort()

for video_path in video_paths:
    video_filename = os.path.basename(video_path)
    video_id, _ = os.path.splitext(video_filename)
    audio_path = os.path.join(AUDIO_DIR, f"{video_id}.wav")

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
        "-y"
    ]

    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
    print(f"[{video_id}] Đã xuất âm thanh thành công vào: {audio_path}")

def pack_keyframes_to_wds(input_base_dir, output_wds_dir, dict_dir, max_size=1e9, max_count=10000):
    """
    Nén các thư mục Keyframes thành các file WebDataset (.tar/.wds).
    Tạo file index.json để tra cứu nhanh.

    :param max_size: Kích thước tối đa của mỗi shard (mặc định ~1GB).
    :param max_count: Số lượng ảnh tối đa trong 1 shard (mặc định 10k ảnh).
    """
    os.makedirs(output_wds_dir, exist_ok=True)

    # Dictionary để lưu cấu trúc index json
    # Format: index_map["Lxx"]["Vxx"]["n_keyframes"] = "key_trong_wds"
    index_map = {}
    lxx_folders = [f for f in os.listdir(input_base_dir) if os.path.isdir(os.path.join(input_base_dir, f))]

    for lxx_folder in lxx_folders:
        folder_path = os.path.join(input_base_dir, lxx_folder)
        lxx_prefix = lxx_folder.split(" ")[1]

        index_map[lxx_prefix] = {}

        shard_pattern = os.path.join(output_wds_dir, f"{lxx_prefix}_keyframes-%02d.tar")
        with wds.ShardWriter(shard_pattern, maxsize=max_size, maxcount=max_count) as sink:
            image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])

            for img_filename in image_files:
                img_path = os.path.join(folder_path, img_filename)
                base_name = os.path.splitext(img_filename)[0]
                vxx_prefix, n_keyframe_str = base_name.split('_')
                n_keyframe = int(n_keyframe_str)

                if vxx_prefix not in index_map[lxx_prefix]:
                    index_map[lxx_prefix][vxx_prefix] = {}

                sample_key = f"{lxx_prefix}_{base_name}"
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
                        "L_id": lxx_prefix,
                        "V_id": vxx_prefix,
                        "n_keyframes": n_keyframe
                    }).encode('utf-8')
                }

                sink.write(sample)

    index_file_path = os.path.join(dict_dir, f"{lxx_prefix}_keyframes.json")
    with open(index_file_path, "w", encoding='utf-8') as f:
        json.dump(index_map, f, indent=4)

    print(f"\nHoàn tất! Đã lưu bản đồ index tại: {index_file_path}")
INPUT_DIR = "Extracted_Keyframes"  # Thư mục gốc chứa các folder 'Keyframes Lxx'
OUTPUT_DIR = "WebDataset_Output"   # Thư mục sẽ chứa các file .tar và file index.json

pack_keyframes_to_wds(INPUT_DIR, OUTPUT_DIR)