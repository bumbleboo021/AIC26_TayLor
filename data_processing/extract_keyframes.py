import os
import glob
import cv2
import pandas as pd
from decord import VideoReader, cpu
from concurrent.futures import ProcessPoolExecutor, as_completed
from config import BASE_DIR

VIDEO_DIR = os.path.join(BASE_DIR, 'video')
CSV_DIR = os.path.join(BASE_DIR, 'csv_keyframes')

def extract_keyframes_parallel(video_path, frame_column='frame_idx'):

    video_name = os.path.basename(video_path)
    video_id = os.path.splitext(video_name)[0]
    lxx_prefix = video_id.split("_")[0]
    csv_path = os.path.join(CSV_DIR, f"{video_id}.csv")
    output_dir = os.path.join(BASE_DIR, f"Keyframes_{lxx_prefix}", video_id)
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(csv_path)
        frame_indices = sorted(list(set(df[frame_column].astype(int).tolist())))
    except Exception as e:
        print(f"[Lỗi] Không thể đọc CSV của {video_id}: {e}")
        return video_id, False

    try:
        vr = VideoReader(video_path, ctx=cpu(0))
        total_frames = len(vr)
    except Exception as e:
        print(f"[Lỗi] Không thể mở video {video_id} bằng decord: {e}")
        return video_id, False

    valid_indices = [idx for idx in frame_indices if 0 <= idx < total_frames]
    
    if not valid_indices:
        print(f"[Cảnh báo] Không có frame hợp lệ để trích xuất cho {video_id}.")
        return video_id, True

    try:
        n_keyframe = 1
        chunk_size = 100
        
        for i in range(0, len(valid_indices), chunk_size):
            batch_indices = valid_indices[i : i + chunk_size]
            frames = vr.get_batch(batch_indices).asnumpy()
            
            for frame in frames:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                image_filename = f"{n_keyframe:04d}.jpg"
                image_path = os.path.join(output_dir, image_filename)
                
                cv2.imwrite(image_path, frame_bgr)
                n_keyframe += 1
                
    except Exception as e:
        print(f"[Lỗi] Trích xuất frame của {video_id} thất bại: {e}")
        return video_id, False

    return video_id, True


if __name__ == '__main__':
    video_paths = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))
    print(f"Tìm thấy {len(video_paths)} video cần xử lý. Bắt đầu trích xuất...")

    max_workers = os.cpu_count()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(extract_keyframes_parallel, path): path for path in video_paths}

        for future in as_completed(futures):
            vid_id, success = future.result()
            if success:
                print(f"Done: {vid_id}")
            else:
                print(f"Failed, skip: {vid_id}")
                
    print("Done")