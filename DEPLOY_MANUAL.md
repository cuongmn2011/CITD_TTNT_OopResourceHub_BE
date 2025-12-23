# Hướng dẫn Deploy thủ công lên Google Cloud

## Yêu cầu
- Google Cloud SDK đã được cài đặt
- Docker Desktop đang chạy (nếu muốn build local)
- Tài khoản Google Cloud có quyền deploy

## Bước 1: Đăng nhập Google Cloud

```bash
gcloud auth login
```

## Bước 2: Thiết lập Project

```bash
# Xem danh sách projects
gcloud projects list

# Chọn project
gcloud config set project YOUR_PROJECT_ID
```

## Bước 3: Enable các API cần thiết

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Bước 4: Deploy lên Cloud Run

### Cách 1: Sử dụng script deploy (Đơn giản nhất - Khuyến nghị)

File deploy script đã được tạo sẵn với cấu hình database và biến môi trường.

**Trên Windows PowerShell:**
```powershell
.\deploy.ps1
```

**Trên Linux/Mac:**
```bash
bash deploy.sh
```

> **Lưu ý:** File `deploy.ps1` và `deploy.sh` không được commit lên git vì chứa thông tin database nhạy cảm.

### Cách 2: Deploy trực tiếp từ source code (Manual)

```bash
gcloud run deploy oopresourcehub-api \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars ENVIRONMENT=production,DATABASE_URL="your_database_connection_string"
```

### Cách 3: Build Docker image và deploy

#### Bước 4.1: Build và push Docker image

```bash
# Tạo Artifact Registry repository (chỉ cần làm 1 lần)
gcloud artifacts repositories create oopresourcehub-repo \
  --repository-format=docker \
  --location=asia-southeast1 \
  --description="OOP Resource Hub API"

# Configure Docker với Artifact Registry
gcloud auth configure-docker asia-southeast1-docker.pkg.dev

# Build và tag image
docker build -t asia-southeast1-docker.pkg.dev/YOUR_PROJECT_ID/oopresourcehub-repo/api:latest .

# Push image lên Artifact Registry
docker push asia-southeast1-docker.pkg.dev/YOUR_PROJECT_ID/oopresourcehub-repo/api:latest
```

#### Bước 4.2: Deploy image lên Cloud Run

```bash
gcloud run deploy oopresourcehub-api \
  --image asia-southeast1-docker.pkg.dev/YOUR_PROJECT_ID/oopresourcehub-repo/api:latest \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars ENVIRONMENT=production,DATABASE_URL="your_database_connection_string"
```

## Bước 5: Cấu hình biến môi trường

### Nếu đã deploy bằng deploy.sh
Biến môi trường đã được cấu hình tự động. Nếu cần thay đổi:

```bash
gcloud run services update oopresourcehub-api \
  --region asia-southeast1 \
  --update-env-vars DATABASE_URL=your_database_url,OTHER_VAR=value
```

## Bước 6: Xem URL của service

```bash
gcloud run services describe oopresourcehub-api \
  --region asia-southeast1 \
  --format='value(status.url)'
```

## Các lệnh hữu ích

### Xem logs
```bash
gcloud run services logs read oopresourcehub-api \
  --region asia-southeast1 \
  --limit=50
```

### Xem danh sách services
```bash
gcloud run services list
```

### Xóa service
```bash
gcloud run services delete oopresourcehub-api \
  --region asia-southeast1
```

### Update service với cấu hình mới
```bash
gcloud run services update oopresourcehub-api \
  --region asia-southeast1 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 0 \
  --timeout 300
```

## Lưu ý

1. **deploy.ps1/deploy.sh**: File script này chứa database connection string và không được commit lên git. Nếu làm việc nhóm, mỗi người cần tạo file riêng với thông tin database của mình.
2. **Region**: Đang sử dụng `asia-southeast1` (Singapore), có thể đổi sang region khác nếu cần
3. **Port**: Ứng dụng FastAPI chạy trên port 8000
4. **Authentication**: Đang để `--allow-unauthenticated` để public, xóa flag này nếu muốn yêu cầu xác thực
5. **Database**: Connection string được cấu hình trong file deploy script hoặc qua `--set-env-vars`
6. **Cost**: Cloud Run tính phí theo usage, cân nhắc thiết lập min/max instances phù hợp

## Troubleshooting

### Lỗi port
Đảm bảo Dockerfile expose port 8000 và Cloud Run cũng được cấu hình port 8000

### Lỗi permissions
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/run.admin"
```

### Kiểm tra service health
```bash
curl https://YOUR_SERVICE_URL/docs
```
