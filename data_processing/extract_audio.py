import os
import glob
import subprocess
import json
import cv2
import pandas as pd
import webdataset as wds
from decord import VideoReader, cpu
from config import BASE_DIR

VIDEO_DIR = os.path.join(BASE_DIR, 'video')
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
os.makedirs(AUDIO_DIR, exist_ok = True)

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