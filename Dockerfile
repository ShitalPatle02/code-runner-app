# Step 1: Build the React frontend
FROM node:18 AS frontend-builder
WORKDIR /app
COPY frontend/ ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Step 2: Python + FastAPI backend
FROM python:3.10
WORKDIR /app

# Copy backend code
COPY backend/ ./backend

# Copy frontend build from previous step
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
