# AIC26_TayLor
TàyLor team from 25TNT, VNUHCM US at AIC HCMC 2026

## Data Processing
Từ dữ liệu video mà BTC cung cấp cùng với các dữ liệu mẫu, nhóm sẽ xử lý dữ liệu như sau:

- Upload video lên Google Colab, dùng model shot detection TransNetV2 để lấy các scenes từ video, chia keyframes ra và lấy đầu ra dữ liệu là file csv mapkeyframes (n_keyframes, frame_idx, pts_time)

- Tiếp tục, nhóm tải video về VPS, thực hiện xuất audio của tất cả video dưới định dạng file .wav, đồng thời cắt tất cả keyframes của các video từ file csv mapkeyframes thu được ở trên

- Sau khi hoàn thành xuất audio và keyframes, nhóm upload dữ liệu lên Kaggle Dataset, rồi thực hiện extract features (dùng SigLIP2 SO400m Naflex), extract metadata (gồm dữ liệu OCR và image captioning từ Qwen3 VL 2B), object detection (dùng YOLO11x) trên keyframes, và extract transcript (dùng faster-whisper/ model large-v3) trên audio

- Sau khi có siglip features từ pipeline trên, nhóm sử dụng FAISS là công cụ để lưu hết vector lại thành một file .index, và cũng dùng FAISS để phục vụ việc tính cosine similarity cho query 1
