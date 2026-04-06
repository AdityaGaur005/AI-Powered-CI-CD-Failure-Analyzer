# 1. Base image (Python environment)
FROM python:3.10-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy project files into container
COPY . .

# 4. Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt || true

# 5. Default command (batch mode)
CMD ["python", "app/main.py", "logs/sample.log"]
