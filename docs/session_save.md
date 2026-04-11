# 🌅 Tomorrow's Quick Start

Welcome back! Here is exactly where we left off.

### 1. Environment Setup
Make sure your `.env` file in the root directory looks like this:
```env
HF_TOKEN=your_huggingface_token_here
PSQL_USER=aura_user
PSQL_PASSWORD=aura_password
PSQL_DB=aura_db
```

### 2. Launch Commands
Run these in separate terminal tabs:

**Tab 1: Backend & Infrastructure**
```bash
docker-compose up --build
```

**Tab 2: Frontend UI**
```bash
cd aura-ui
npm run dev
```

### 3. Key URLs
- **Aura API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend UI**: [http://localhost:5173](http://localhost:5173)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3000](http://localhost:3000) (Admin / Admin)

---
*Note: The first `docker-compose up` will download the Qwen2.5 model. It might take 5-10 minutes depending on your internet speed.*
