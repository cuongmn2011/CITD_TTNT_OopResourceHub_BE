# Hướng dẫn Deploy lên Google Cloud Run

## Bước 1: Chuẩn bị Google Cloud Account

1. Truy cập: https://console.cloud.google.com/
2. Đăng nhập/Đăng ký (cần credit card để verify, nhưng sẽ không charge trong free tier)
3. Nhận $300 credit free trial (300 ngày) khi đăng ký mới

## Bước 2: Tạo Project

1. Vào Console: https://console.cloud.google.com/
2. Click dropdown project ở góc trên → **New Project**
3. Đặt tên project: `oop-resource-hub` → **Create**
4. Chọn project vừa tạo

## Bước 3: Enable APIs

Chạy các lệnh sau hoặc enable qua Console:

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API (optional, cho auto deploy)
gcloud services enable cloudbuild.googleapis.com
```

Hoặc enable qua UI:
- Vào: https://console.cloud.google.com/apis/library
- Tìm và enable: **Cloud Run API**, **Container Registry API**, **Cloud Build API**

## Bước 4: Cài đặt Google Cloud CLI

### Windows:
1. Download: https://cloud.google.com/sdk/docs/install
2. Chạy installer
3. Sau khi cài xong, mở PowerShell mới

### Khởi tạo gcloud CLI:
```powershell
# Login
gcloud auth login

# Set project
gcloud config set project oop-resource-hub

# Verify
gcloud config list
```

## Bước 5: Deploy lên Cloud Run

### Cách 1: Deploy trực tiếp (Đơn giản nhất)

```powershell
# Deploy (Cloud Run sẽ tự build Docker image)
gcloud run deploy oop-resource-hub `
  --source . `
  --region us-central1 `
  --platform managed `
  --allow-unauthenticated `
  --set-env-vars "ENVIRONMENT=production,DATABASE_URL=your_database_url_here"
```

**Lưu ý:** Thay `your_database_url_here` bằng PostgreSQL URL thật

### Cách 2: Build và Deploy riêng (Kiểm soát tốt hơn)

```powershell
# Set project ID
$PROJECT_ID = "oop-resource-hub"

# Build Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/oop-resource-hub

# Deploy
gcloud run deploy oop-resource-hub `
  --image gcr.io/$PROJECT_ID/oop-resource-hub `
  --region us-central1 `
  --platform managed `
  --allow-unauthenticated `
  --set-env-vars "ENVIRONMENT=production,DATABASE_URL=your_database_url_here"
```

## Bước 6: Setup Database

### Option A: Sử dụng Neon (Free PostgreSQL)

1. Vào: https://neon.tech/
2. Tạo database free
3. Copy connection string
4. Update environment variable trên Cloud Run:

```powershell
gcloud run services update oop-resource-hub `
  --region us-central1 `
  --set-env-vars "DATABASE_URL=postgresql://user:pass@host/db"
```

### Option B: Cloud SQL (Có phí nhưng tốt hơn)

```powershell
# Tạo Cloud SQL instance (có phí ~$7-10/tháng)
gcloud sql instances create oop-resource-db `
  --database-version=POSTGRES_14 `
  --tier=db-f1-micro `
  --region=us-central1
```

## Bước 7: Kiểm tra Deployment

Sau khi deploy xong, sẽ có URL dạng:
```
https://oop-resource-hub-xxxx-uc.a.run.app
```

Kiểm tra:
- API docs: https://your-url/docs
- Health check: https://your-url/

## Bước 8: Setup Auto Deploy từ GitHub (Optional)

1. Vào Cloud Console → Cloud Build → Triggers
2. Click **Create Trigger**
3. Chọn GitHub repository
4. Configure:
   - Branch: `main` hoặc `feat/related_topics`
   - Build configuration: Cloud Build configuration file
   - File location: `/cloudbuild.yaml`
5. **Create**

Giờ mỗi khi push code lên GitHub, sẽ tự động deploy!

## Quản lý Cost

### Xem usage:
```powershell
gcloud run services describe oop-resource-hub --region us-central1
```

### Set spending limit:
1. Vào: https://console.cloud.google.com/billing
2. Budgets & alerts → Create Budget
3. Set limit (VD: $5/tháng) → Create alert

### Stop service (khi không dùng):
```powershell
gcloud run services delete oop-resource-hub --region us-central1
```

## Troubleshooting

### Lỗi "Permission denied":
```powershell
gcloud auth application-default login
```

### Xem logs:
```powershell
gcloud run logs read --service oop-resource-hub --region us-central1
```

### Test local với Docker:
```powershell
# Build
docker build -t oop-resource-hub .

# Run
docker run -p 8080:8080 -e DATABASE_URL="your_db_url" oop-resource-hub
```

Truy cập: http://localhost:8080/docs

## Free Tier Limits

- **2 triệu requests/tháng**
- **180,000 vCPU-seconds**
- **360,000 GiB-seconds memory**
- **1 GB network egress/tháng**

Đủ cho project học tập/demo!
