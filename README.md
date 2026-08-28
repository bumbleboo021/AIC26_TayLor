# AIC26_TayLor
TàyLor team from 25TNT, VNUHCM US at AIC HCMC 2026

## First at all
AI Challenge HCMC là một cuộc thi đã được tổ chức nhiều lần tại Ho Chi Minh City. Đề bài của cuộc thi là xây dựng giải pháp để hỗ trợ phân tích và truy xuất thông tin trong một dữ liệu lớn multimedia (gồm hình ảnh, âm thanh, văn bản). Dữ liệu cung cấp và thi chính thức là video, bên cạnh đó, BTC cũng cung cấp một số dữ liệu mẫu để nhóm có thể tham khảo và xem xét nâng cấp dựa trên đó. Khi trích xuất và xử lý dữ liệu thành công, nhóm sẽ phải thực hiện các truy vấn của BTC để chấm điểm, và các loại truy vấn gồm có:

- Textual KIS (Textual Known Item Search): Tìm kiếm frames diễn ra sự kiện với mô tả văn bản

- Q&A (Visual Question Answering và có thể kết hợp với cả những thông tin từ audio): Tìm kiếm frames diễn ra sự kiện với mô tả ngữ cảnh và trả lời câu hỏi

- TRAKE (Temporal Retrieval and Alignment of Key Events): Truy vấn là sự kiện gồm có nhiều giai đoạn nhỏ, yêu cầu tìm kiếm các frames gần nhau, khớp với truy vấn và trả về frames ứng với từng giai đoạn nhỏ

## Data Processing
Từ dữ liệu video mà BTC cung cấp cùng với các dữ liệu mẫu, nhóm sẽ xử lý dữ liệu như sau:

- Upload video lên Google Colab, dùng model shot detection TransNetV2 để lấy các scenes từ video, chia keyframes ra và lấy đầu ra dữ liệu là file csv mapkeyframes (n_keyframes, frame_idx, pts_time)

- Tiếp tục, nhóm tải video về VPS, thực hiện xuất audio của tất cả video dưới định dạng file .wav, đồng thời cắt tất cả keyframes của các video từ file csv mapkeyframes thu được ở trên

- Sau khi hoàn thành xuất audio và keyframes, nhóm upload dữ liệu lên Kaggle Dataset, rồi thực hiện extract features (dùng SigLIP2 SO400m Naflex), extract metadata (gồm dữ liệu OCR và image captioning từ Qwen3 VL 2B), object detection (dùng YOLO11x) trên keyframes, và extract transcript (dùng faster-whisper/ model large-v3) trên audio

- Sau khi có siglip features từ pipeline trên, nhóm sử dụng FAISS là công cụ để lưu hết vector lại thành một file .index, và cũng dùng FAISS để phục vụ việc tính cosine similarity cho query 1
