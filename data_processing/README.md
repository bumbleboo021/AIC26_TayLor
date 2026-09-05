# Pipeline:

- Dùng Google Colab, chạy notebook extract_csv_keyframes.ipynb (wget một phần video trước khi chạy, k nên tải nhiều quá để tránh bị đang chạy thì crash time out do hết quota T4)

- ZIP folder csv_keyframes rồi tải về (chạy dần dần nhiều lượt cho hết mớ video)

Ở trên VPS:

- Vào AIC26_TayLor, tạo thư mục AIC26_TayLor/dataset (hoặc chạy mkdir ./AIC26_TayLor/dataset)

- Tải mớ video về */AIC26_TayLor/dataset/video, gảii nén

- Tải qua choco: Python 3.10, git, ffpmeg

- Vào thư mục AIC26/data_processing, mở trực tiếp file audio_keyframes.bat lên, chờ nó chạy

- (Note: Chỉ up folder lên Kaggle dataset khi đã gói lại thành file .tar/zip)
- Trên VPS, đăng nhập Kaggle dataset, upload folder Keyframes_Lxx theo từng đợt nếu SSD VPS không lưu đủ hết được

Upload folder audio khi đã chạy hết video  (Up xong hết mớ này là không cần VPS nữa)

- Nên chia dữ liệu btc làm thành 2/3 Kaggle Dataset để tránh bị time out khi chạy (max time của Kaggle chỉ là 12h)

- Upload các file .ipynb còn lại lên kaggle, dẫn input là Kaggle Dataset mới nãy tạo vào

- Chạy lần lượt các file metadata_extract/features_extract/object_detect/transcript_extract, lưu mớ folder metadata, siglip_features, object_detection, transcripts thành một folder lớn ở máy rồi tiếp tục up lên Kaggle Dataset

Up xong mới chạy file mapkeyframes_transcript (để map kết quả transcript với n_keyframes)

Done (tự thêm siglip_features vào FAISS rồi lưu lại thành định dạng file .index)

* Note: Đã có file sample sẵn để đọc file dữ liệu lưu trên Kaggle Dataset

Source: Special thanks tới một số nhóm AIC24, AIC25 và thầy Huỳnh Lâm Hải Đăng đã tư vấn cho pipeline data processing này
